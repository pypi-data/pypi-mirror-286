from anthropic import Anthropic, AI_PROMPT, HUMAN_PROMPT

class ResponseGenerator:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def generate_response(self, prompt, max_tokens=100):
        response = self.client.completions.create(
            prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
            max_tokens_to_sample=max_tokens
        )
        return response.completion
