
import logging

logger = logging.getLogger(__name__)


class LLMRouter:
    def __init__(self, primary_llm, fallback_llm):
        self.primary = primary_llm
        self.fallback = fallback_llm

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        # Try primary (Claude)
        try:
            logger.info("Using primary LLM (Claude)")
            return self.primary.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        except Exception as e:
            logger.warning(f"Primary LLM failed: {e}")

        # Fallback to open model
        try:
            logger.info("Falling back to open LLM")
            return self.fallback.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        except Exception as e:
            logger.error(f"Fallback LLM failed: {e}")
            raise RuntimeError("All LLMs failed")
