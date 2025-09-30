from src.stores import LLMInterface
from src.stores import CoHereEnums, DocumentTypeEnums

import cohere
import logging


class CoHereProvider(LLMInterface):

    def __init__(self, api_key: str, 
                 default_input_max_characters: int=1000,
                 default_generation_max_output_tokens: int=1000,
                 default_generation_temperature: float=0.1):
        
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.ClientV2(api_key=self.api_key)

        self.enums = CoHereEnums
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None, 
                    temperature: float=None):

        if not self.client:
                self.logger.error("OpenAI client was not initialized.")
                return None

        if not self.generation_model_id:
            self.logger.error("Generation model for openai was not set.")
            return None 

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

# system_message = "You respond concisely, in about 5 words or less"
# res = co.chat(
#     model="command-a-03-2025",
#     messages=[
#         {"role": "system", "content": system_message},

#         {"role": "user", "content": "Write a title for a blog post about API design. Only output the title text.",},
#         {"role": "assistant", "content": "Designing Perfect APIs"},
#         {"role": "user","content": "Another one about generative AI.",},
#     ],
# )

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=CoHereEnums.USER.value)
        )

        response = self.client.chat(  # https://docs.cohere.com/docs/chat-api
            model = self.generation_model_id,
            messages = chat_history,

            max_tokens = max_output_tokens,
            temperature = temperature
        )

        # if not response or not response['message'] or not response['message']["content"] or len(response['message']["content"]) == 0 or not response['message']["content"][0]["text"]:
        if not response or not response.message or not response.message.content or len(response.message.content) == 0 or not response.message.content[0].text:
        
        # if not response or not response.message or not response.message.


            self.logger.error("No text returned from OpenAI.")
            return None


        return response.message.content[0].text
    
    def embed_text(self, text: str, document_type: str=None):

        if not self.client:
            self.logger.error("OpenAI client was not initialized.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for openai was not set.")
            return None
        
        input_type = CoHereEnums.DOCUMENT
        if document_type == DocumentTypeEnums.QUERY.value:
            input_type = CoHereEnums.QUERY

        response = self.client.embed(
            model = self.embedding_model_id,
            texts = [self.process_text(text)],
            input_type = input_type,
            embedding_types=["float"],
        )

        # .embeddings.float

        if not response or not response.embeddings or not response.embeddings.float :
            self.logger.error("No embedding returned from OpenAI.")
            return None
        
        return response.embeddings.float[0]


    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role, 
            "content": prompt
        }


if __name__ == "__main__":
    res = {
        "id": "5a50480a-cf52-46f0-af01-53d18539bd31",
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "The Art of API Design: Crafting Elegant and Powerful Interfaces",
                }
            ],
        },
        "finish_reason": "COMPLETE",
        "meta": {
            "api_version": {"version": "2", "is_experimental": True},
            "warnings": [
                "You are using an experimental version, for more information please refer to https://docs.cohere.com/versioning-reference"
            ],
            "billed_units": {"input_tokens": 17, "output_tokens": 12},
            "tokens": {"input_tokens": 215, "output_tokens": 12},
        },
    }

    # print(res)
    # print(res['message'])
    # print(res['message']["content"])
    # print(res['message']["content"][0])
    # print(res['message']["content"][0]["text"])

    if not res or not res['message'] or not res['message']["content"] or len(res['message']["content"]) == 0 or not res['message']["content"][0]["text"]:
        print("No text returned from CoHere.")
    else:
        print(res['message']["content"][0]["text"])


    # res = co.chat(
    # model="command-a-03-2025",
    system_message = "jhbdhjd"
    messages=[
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": "Write a title for a blog post about API design. Only output the title text.",
            },
            {"role": "assistant", "content": "Designing Perfect APIs"},
            {
                "role": "user",
                "content": "Another one about generative AI.",
            },
        ]
    # print(len(messages)) # 4
    user_input = {
        "role": "user",
        "content": "Write a title for a blog post about API design. Only output the title text.",
    }
    messages.append(user_input)
    print(messages) # len => 5



# to run: python src/stores/llm/providers/CoHere_Provider.py 
