from openai import OpenAI
import openai


class GPT:
    def __init__(self, api_key, model) -> None:
        self.client = OpenAI(api_key=api_key)
        self.instruction = None
        self.model = model
        self.model_emb = "text-embedding-3-large"
        openai.api_key = api_key
        self.params = {
            "response_format" :
                {"type": "json_object"},
            "max_tokens": 200,
            "temperature": 0.9,
            "seed": 0,
        }
    
    def set_param(self, **kwargs):
        self.params.update(kwargs)
        print(f'Now gpt_params : {self.params}')
        
    def set_instruction(self, instruction):
        self.instruction = instruction
        print("Instruction is set")

    def set_model(self, model_name):
        self.model = model_name
        print("Model is set to ", self.model)

    def chat(self, comment, return_all=False):
        messages = [{"role": "user", "content": comment}]
        if self.instruction:
            messages.insert(0, {"role": "system", "content": self.instruction})

        completion = self.client.chat.completions.create(
            model=self.model, messages=messages, **self.params
        )
        if not return_all:
            return completion.choices[0].message.content
        else:
            return completion

    def embed(self, texts, return_all=False):
        if isinstance(texts, str):
            texts = [texts]
        # response = self.client.embeddings.create(model=self.model, input=texts)
        response = openai.embeddings.create(input=texts, model=self.model_emb)
        if not return_all:
            return [r.embedding for r in response.data]
        else:
            return response

    # def list_models(self):
    #     models = self.client.models.list()
    #     return [model["id"] for model in models["data"]]

    # def summarize(self, text):
    #     summary_instruction = "Please provide a concise summary of the following text."
    #     completion = self.client.chat.completions.create(
    #         model=self.model,
    #         messages=[
    #             {"role": "system", "content": summary_instruction},
    #             {"role": "user", "content": text},
    #         ],
    #     )
    #     return completion.choices[0].message.content
