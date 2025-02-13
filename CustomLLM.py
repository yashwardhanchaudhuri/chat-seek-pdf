from typing import Any, Dict, Optional
import openai
from langchain.llms.base import LLM


class CustomLLM(LLM):
    """Custom LLM class that interfaces with OpenAI-compatible APIs.
    
    This class implements a custom Language Learning Model (LLM) that works with
    OpenAI-compatible APIs, specifically designed for use with local deployments
    like Ollama.

    Attributes:
        model_name (str): Name of the model to use (default: "deepseek-r1:14b")
        base_url (str): Base URL for the API endpoint (default: "http://localhost:11434/v1")
        api_key (str): API key for authentication (default: "ollama")
        temperature (float): Sampling temperature between 0 and 1 (default: 0.6)
    """

    model_name: str = "deepseek-r1:14b"
    base_url: str = "http://localhost:11434/v1"
    api_key: str = "ollama"
    temperature: float = 0.6

    def __init__(
        self,
        model_name: str = "deepseek-r1:14b",
        base_url: str = "http://localhost:11434/v1",
        api_key: str = "ollama",
        temperature: float = 0.6
    ) -> None:
        """Initialize the CustomLLM instance.

        Args:
            model_name: Name of the model to use
            base_url: Base URL for the API endpoint
            api_key: API key for authentication
            temperature: Sampling temperature between 0 and 1
        """
        super().__init__()
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = api_key
        self.temperature = temperature
        openai.api_key = api_key
        openai.api_base = base_url
    
    def _call(self, prompt: str, **kwargs: Any) -> str:
        """Generate a response for the given prompt.

        Args:
            prompt: The input text to generate a response for
            **kwargs: Additional keyword arguments passed to the API

        Returns:
            str: The generated response text

        Raises:
            openai.error.OpenAIError: If the API request fails
        """
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content.split("</think>")[-1]

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get parameters that identify this LLM implementation."""
        return {"model_name": self.model_name, "temperature": self.temperature}

    @property
    def _llm_type(self) -> str:
        """Get the type identifier for this LLM implementation."""
        return "custom_openai"
    