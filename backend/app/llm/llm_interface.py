from abc import ABC, abstractmethod


class LLMInterface(ABC):
    """
    Provider-independent interface for the LLM layer.

    The memory system talks to this interface instead of
    directly depending on Groq or Ollama.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """
        Generate a response from the language model.
        """
        pass