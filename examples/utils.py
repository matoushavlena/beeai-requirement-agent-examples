import os
from dotenv import load_dotenv

from beeai_framework.backend import ChatModel

load_dotenv()

model = os.getenv("MODEL", "openai:gpt-5-nano")
llm = ChatModel.from_name(model, {"api_key": os.getenv("API_KEY")})
