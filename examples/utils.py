import os

from beeai_framework.backend import ChatModel


llm = ChatModel.from_name("openai:gpt-4o-mini", {"api_key": os.getenv("OPENAI_API_KEY")})
