from backend.app.llm.llm_interface import LLMInterface
from backend.app.llm.groq_client import GroqClient


class GroqProvider(LLMInterface):
    """
    Groq implementation of the provider-independent
    LLM interface.
    """

    def __init__(
        self,
        model: str = "openai/gpt-oss-20b",
    ):
        self.client = GroqClient(
            model=model
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        return self.client.generate(
            messages=messages,
            temperature=0.7,
        )