from dotenv import load_dotenv

from prompt_hacker.interface import ChatBaseModel

load_dotenv(verbose=True)


class ModelClient(ChatBaseModel):
    ...
