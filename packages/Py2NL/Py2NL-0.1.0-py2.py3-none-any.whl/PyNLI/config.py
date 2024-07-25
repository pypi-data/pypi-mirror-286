from pydantic import BaseModel


class Config(BaseModel):
    iteration_confirmation_interval: int = 10
    max_iterations: int = 100
    agent_model_name: str = 'gpt-4-1106-preview'
    assistant_model_name: str = 'gpt-3.5-turbo-1106'

    lazy_files: bool = True

default_config = Config()


