from stores import LLMEnums 
from stores import CoHere_Provider, OpenAI_Provider

class LLMProviderFactory:
    def __init__(self, config:dict):
        self.config = config

    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAI_Provider(
                api_key=self.config.api_key,
                api_url=self.config.api_url,
                default_input_max_characters=self.config.default_input_max_characters,
                default_generation_max_output_tokens=self.config.default_generation_max_output_tokens,
                default_generation_temperature=self.config.default_generation_temperature
            )

        if provider == LLMEnums.COHERE.value:
            return CoHere_Provider(
                api_key=self.config.api_key,
                api_url=self.config.api_url,
                default_input_max_characters=self.config.default_input_max_characters,
                default_generation_max_output_tokens=self.config.default_generation_max_output_tokens,
                default_generation_temperature=self.config.default_generation_temperature
            )
        return None