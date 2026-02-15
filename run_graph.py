import sys
import traceback

from utils.logger import setup_logger
from llm.claude_client import ClaudeClient
from llm.open_llm_client import OpenLLMClient
from llm.llm_router import LLMRouter
from agent.email_agent import EmailCleanupAgent
from graph.email_graph import build_email_graph


def main():
    logger = setup_logger()
    logger.info("===== Gmail Agent Run Started =====")

    llm = LLMRouter(
        # primary_llm=ClaudeClient(model="claude-3-haiku-20240307")
        primary_llm=ClaudeClient(model="claude-3-sonnet-20240229"),
        fallback_llm=OpenLLMClient(model="mistral"),
    )

    email_agent = EmailCleanupAgent(llm)

    graph = build_email_graph(email_agent, logger)

    graph.invoke({
        "emails": [],
        "decisions": [],
        "stats": {},
    })

    logger.info("===== Gmail Agent Run Completed Successfully =====")


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)

    except Exception as e:
        logger = setup_logger()
        logger.error("===== Gmail Agent Run Failed =====")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        sys.exit(1)


