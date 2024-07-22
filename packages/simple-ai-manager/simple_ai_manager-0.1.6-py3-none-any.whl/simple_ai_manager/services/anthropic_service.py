import os
import anthropic

class AnthropicService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.default_max_tokens = int(os.getenv('MAX_TOKENS', 1000))

    def generate_text(self, model, prompt, max_tokens=None):
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens or self.default_max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Error in generating text: {str(e)}")

    def continue_conversation(self, model, prompt, history):
        try:
            messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.messages.create(
                model=model,
                max_tokens=self.default_max_tokens,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Error in continuing conversation: {str(e)}")