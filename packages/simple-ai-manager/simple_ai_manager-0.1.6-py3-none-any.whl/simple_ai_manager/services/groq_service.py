import os
import groq

class GroqService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = groq.Groq(api_key=self.api_key)
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
            full_prompt = "\n".join([f"{'Human' if msg['role'] == 'user' else 'AI'}: {msg['content']}" for msg in history])
            full_prompt += f"\nHuman: {prompt}\nAI:"
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=self.default_max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error in continuing conversation: {str(e)}")