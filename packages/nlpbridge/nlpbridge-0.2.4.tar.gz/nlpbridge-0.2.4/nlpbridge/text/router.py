import logging
import random
from typing import List, Literal, Optional, TypeVar, TypedDict, Callable, Tuple, Any, Dict

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.base import RunnableLike, Runnable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph

from nlpbridge import ChatAgent
from nlpbridge.persistent.mysql import CRUDNode, CRUDEdge, CRUDTemplate, CRUDRouter
from nlpbridge.persistent.mysql import MySqlDBClient
from nlpbridge.persistent.mysql_dataschema import Node as NodeModel
from nlpbridge.text.tools import tool_list

memory = MemorySaver()

Input = TypeVar("Input", contravariant=True)
Output = TypeVar("Output", covariant=True)
logger = logging.getLogger(__name__)


class BaseNode:
    id: int
    name: str
    description: str
    goal: str  # node goal
    chat_limit: int
    system_template_ids: List[int]
    user_template_ids: List[int]
    tool_names: List[str]


class Template:
    id: int
    name: str
    type: Literal["user", "sys"] = "user"
    content: str


class Edge:
    id: int
    start_id: int
    end_id: int
    goal: str
    weight: float


def get_sys_template_pair(system_templates) -> Tuple[str, str]:
    start_sys_template = system_templates[0] if len(system_templates) > 0 else None
    end_sys_template = system_templates[1] if len(system_templates) > 1 else None
    return start_sys_template, end_sys_template


class Node(Callable[[dict], TypedDict]):
    def __init__(self, id, name, description, goal, chat_limit, system_template_ids, user_template_ids,
                 system_templates,
                 user_templates, tool_names,
                 in_edges,
                 out_edges,
                 llm,
                 chat_id, **kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.goal = goal
        self.chat_limit = chat_limit
        self.system_templates_ids = system_template_ids
        self.user_templates_ids = user_template_ids
        self.tool_names = tool_names
        self.system_templates = system_templates
        self.user_templates = user_templates
        self.user_template_index = len(user_templates)  # 当前使用user_template的index
        self.in_edges = in_edges
        self.out_edges = out_edges
        self.llm = llm
        self.chat_id = chat_id

    system_templates: List[Template]
    user_templates: List[Template]
    chain: Optional[RunnableLike]
    in_edges: List[Edge]
    out_edges: List[Edge]

    def rand_prompt(self):
        # start_sys_template + user_prompt + end_sys_template
        start_sys_template, end_sys_template = get_sys_template_pair(self.system_templates)
        start_sys_prompt = start_sys_template.content if start_sys_template else ""
        end_sys_prompt = end_sys_template.content if end_sys_template else ""

        user_template = None
        if self.user_templates:
            if self.user_template_index < 0:
                # chat_limit - len(user_templates), 随机选择一个user_template
                user_template = random.choice(self.user_templates)
            else:
                user_template = self.user_templates[self.user_template_index]

        user_prompt = user_template.content if user_template else ""
        return ChatPromptTemplate.from_messages(
            [
                ("system", start_sys_prompt + user_prompt + end_sys_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "User qeustion: {input}"),
            ]
        )

    def _set_stop_signal(self, state: dict):
        state["stop"] = True

    def _init_agent(self):
        prompt = self.rand_prompt()
        self.agent = ChatAgent(None, self.chat_id, self.llm, self.tool_names, prompt, True)

    def __call__(self, state: dict) -> Output:
        self.user_template_index -= 1
        self._init_agent()
        self.chat_limit -= 1
        # question = input("[Question]: ")
        question = "你好呀，你是谁？"
        response = self.agent.run(question)
        print(f"[current agent generate]: {response}")
        print(f"[node state]:\n{state}")
        return {"context": {"input": question, "response": response.content}}

    @classmethod
    def init_with_params(cls, id, name, description, goal, chat_limit, system_template_ids, user_template_ids,
                         system_templates,
                         user_templates, tool_names,
                         in_edges,
                         out_edges,
                         llm,
                         chat_id, **kwargs):
        return cls(id, name, description, goal, chat_limit, system_template_ids, user_template_ids,
                   system_templates,
                   user_templates, tool_names,
                   in_edges,
                   out_edges,
                   llm,
                   chat_id, **kwargs)


class DefaultNode(Callable[[dict], TypedDict]):
    def __init__(self):
        self.id = -1
        self.chat_limit = 0
        self.name = "default"

    async def __call__(self, state: dict):
        # default node 暂时只用于退出graph, 后续会补充新功能
        print("------------------- goodbye -------------------")


class Router:
    id: int
    name: str
    node_ids: List[str]
    edge_ids: List[str]


class NodeManager:

    @staticmethod
    def get_nodes(node_ids: List[int]) -> List[NodeModel]:
        if not node_ids:
            return []
        from nlpbridge.config import CONFIG
        session = MySqlDBClient(CONFIG).get_session()
        return CRUDNode(session).get_by_ids(list_ids=node_ids)


class EdgeManager:
    @staticmethod
    def get_edges(edge_ids: List[int]) -> List[Edge]:
        if not edge_ids:
            return []
        from nlpbridge.config import CONFIG
        session = MySqlDBClient(CONFIG).get_session()
        return CRUDEdge(session).get_by_ids(list_ids=edge_ids)


class TemplateManager:
    @staticmethod
    def get_templates(template_ids: List[int]) -> List[Template]:
        if not template_ids:
            return []
        from nlpbridge.config import CONFIG
        session = MySqlDBClient(CONFIG).get_session()
        return CRUDTemplate(session).get_by_ids(list_ids=template_ids)


class GraphState(TypedDict):
    nodes: Optional[List[Node]]
    context: Any | Dict[str, Any]


class Condition(Callable[[dict], TypedDict]):
    def __init__(self, cur_node: Node, target_nodes: List[Node]):
        self.cur_node = cur_node
        self.target_nodes = target_nodes

    def call(self, node_state: TypedDict) -> str:
        # Randomly select the next node from the current node and the node pointed to by the node.
        # print("Condition-------", node_state)

        # 如果到graph的末端节点, 此时target node只剩下1个, 就直接返回自己; 并且如果chat_limit<=0就终止
        if len(self.target_nodes[:-1]) < 2:
            if self.cur_node.chat_limit <= 0:
                return self.target_nodes[-1].name
            return self.target_nodes[0].name

        # 更新condition weight
        self.update_condition_weight(node_state)

        # 根据weight进行随机
        weights = self.normalize([edge.weight for edge in self.cur_node.out_edges])

        next = random.choices(self.target_nodes[:-1], weights=weights)[0]
        logger.debug(f'({self.cur_node.name})[remains]: {self.cur_node.chat_limit}')
        if next.chat_limit <= 0:
            next = random.choices(self.target_nodes[1:-1], weights=weights[1:])[0]
        return next.name

    def __call__(self, node_state: TypedDict) -> str:
        if node_state.get("stop", False):
            logger.debug(f"stop signal received")
            # return "END"
            return self.target_nodes[-1].name

        return self.call(node_state)

    @classmethod
    def init_with_params(cls, cur_node, target_nodes):
        return cls(cur_node, target_nodes)

    def update_condition_weight(self, node_state) -> None:
        ...

    def normalize(self, data: list) -> list:
        if len(data) < 2:
            return [1]
        min_val = min(data)
        max_val = max(data)
        return [(x - min_val) / (max_val - min_val + 1e-5) for x in data]


class RouterManager:
    @staticmethod
    def get_router(router_id: int) -> Router:
        from nlpbridge.config import CONFIG
        session = MySqlDBClient(CONFIG).get_session()
        return CRUDRouter(session).get_by_id(id=router_id)

    def get_graph(self, chat_id: str, llm, router_id: int, condition_cls: Condition = Condition,
                  node_cls: Node = Node, **kwargs) -> Tuple[CompiledGraph, dict]:
        router = RouterManager.get_router(router_id)
        node_ids = router.node_ids
        edge_ids = router.edge_ids
        int_node_ids = [int(num) for num in node_ids.split(',')]
        int_edge_ids = [int(num) for num in edge_ids.split(',')]
        nodes = NodeManager.get_nodes(int_node_ids)
        edges = EdgeManager.get_edges(int_edge_ids)

        runnable_nodes = self.convert_to_runnable_node(nodes, edges, llm, chat_id, node_cls, **kwargs)

        # create default node
        default_node = DefaultNode()
        runnable_nodes.append(default_node)

        graph = self._create_graph(runnable_nodes, edges, condition_cls)
        cfg = {"configurable": {"thread_id": router_id}}
        graph.update_state(config=cfg, values={"nodes": nodes})
        return graph, cfg

    def _create_graph(self, nodes: List[Node], edges: List[Edge], condition_cls: Condition) -> CompiledGraph:
        graph = StateGraph(GraphState)
        for node in nodes:
            node_name = self.get_node_name(node)
            graph.add_node(node_name, node)
        # fixme confirm the start_node and end_node storage
        start_node = nodes[0]
        end_node = nodes[-1]
        graph.set_entry_point(self.get_node_name(start_node))
        graph.set_finish_point(self.get_node_name(end_node))
        self._create_conditional_edges(graph, nodes, edges, condition_cls)

        return graph.compile(checkpointer=memory)

    def _create_conditional_edges(self, graph: StateGraph, nodes: List[Node], edges: List[Edge],
                                  condition_cls: Condition) -> StateGraph:
        exist_start_ids = []
        for edge in edges:
            start_id = edge.start_id
            if start_id in exist_start_ids:
                continue
            exist_start_ids.append(start_id)

            target_edges = [edge for edge in edges if edge.start_id == start_id]
            target_ids = [edge.end_id for edge in target_edges]
            target_nodes = [node for node in nodes if node.id in target_ids]
            target_nodes.append(nodes[-1])
            target_node_names = [self.get_node_name(node) for node in target_nodes]

            cur_node = self.find_node(nodes, edge.start_id)
            cur_node_name = self.get_node_name(cur_node)
            path_map = {name: name for name in target_node_names}

            # add itself
            path_map[cur_node_name] = cur_node_name
            # add node:END to the all nodes:
            # TODO: replace END to Default node.
            # path_map["END"] = END
            # target_nodes.append(END)

            graph.add_conditional_edges(
                cur_node_name,
                condition_cls.init_with_params(cur_node, target_nodes),
                path_map
            )

        return graph

    @staticmethod
    def get_node_name(node: Node) -> str:
        node_name = node.name
        if node_name == "unnamed":
            if isinstance(node, Runnable):
                node_name = getattr(node, "__name__", node.__class__.__name__)
        return node_name

    @staticmethod
    def find_node(nodes: List[Node], start_id: str) -> Node:
        return next((node for node in nodes if node.id == start_id), None)

    @staticmethod
    def convert_to_runnable_node(nodes: List[NodeModel], edges: List[Edge], llm, chat_id: str, node_cls: Node,
                                 **kwargs) -> List[
        Node]:
        runnable_nodes = []
        for node in nodes:
            system_template_ids = [int(template_id) for template_id in
                                   node.system_template_ids.split(",")] if node.system_template_ids else []
            user_template_ids = [int(template_id) for template_id in
                                 node.user_template_ids.split(",")] if node.user_template_ids else []
            system_templates = TemplateManager.get_templates(system_template_ids)
            user_templates = TemplateManager.get_templates(user_template_ids)
            in_edges = [edge for edge in edges if edge.end_id == node.id]
            out_edges = [edge for edge in edges if edge.start_id == node.id]
            tools = [tool_list[name] for name in node.tool_names.split(",")] if node.tool_names else []

            runnable_node = node_cls.init_with_params(
                node.id,
                node.name,
                node.description,
                node.goal,
                node.chat_limit,
                system_template_ids,
                user_template_ids,
                system_templates,
                user_templates,
                tools,
                in_edges,
                out_edges,
                llm,
                chat_id,
                **kwargs
            )
            runnable_nodes.append(runnable_node)
        return runnable_nodes
