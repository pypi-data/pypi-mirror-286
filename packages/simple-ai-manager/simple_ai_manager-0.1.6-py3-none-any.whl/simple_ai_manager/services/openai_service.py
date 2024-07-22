from openai import OpenAI
import os

class OpenAIService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.default_max_tokens = int(os.getenv('MAX_TOKENS', 1000))

    def generate_text(self, model, prompt, max_tokens=None):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens or self.default_max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error in generating text: {str(e)}")

    def continue_conversation(self, model, prompt, history):
        try:
            messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=self.default_max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error in continuing conversation: {str(e)}")