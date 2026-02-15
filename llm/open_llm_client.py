import requests


class OpenLLMClient:
    def __init__(self,
                 model="mistral",
                 base_url="http://127.0.0.1:11434",
                 temperature=0.2,
                 max_tokens=512,

                 ):
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, system_prompt, user_prompt):
        """
        Generate text using a local open model via Ollama.
        Returns raw text.
        """
        prompt = self._build_prompt(system_prompt, user_prompt)
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                },
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()

        return response.json()["response"].strip()

    @staticmethod
    def _build_prompt(system_prompt, user_prompt):

        return f"""
        [System Instruction]
        {system_prompt}

        [User Input]
        {user_prompt}

        [Assistant]
        Return ONLY valid JSON.
        """
