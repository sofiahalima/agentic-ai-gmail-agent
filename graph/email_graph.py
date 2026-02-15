from langgraph.graph import StateGraph, END
from graph.state import EmailGraphState
from graph.nodes import build_nodes


def build_email_graph(agent, logger):

    fetch_node, decide_node, delete_node, log_node, summary_node = build_nodes(agent, logger)

    builder = StateGraph(EmailGraphState)

    builder.add_node("fetch", fetch_node)
    builder.add_node("decide", decide_node)
    builder.add_node("delete", delete_node)
    builder.add_node("log", log_node)
    builder.add_node("summary", summary_node)

    builder.set_entry_point("fetch")

    builder.add_edge("fetch", "decide")
    builder.add_edge("decide", "delete")
    builder.add_edge("delete", "log")
    builder.add_edge("log", "summary")
    builder.add_edge("summary", END)

    return builder.compile()
