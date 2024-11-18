from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY=os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    api_key=API_KEY,
    max_retries=2,
    # other params...
)

# ai_msg=llm.invoke("What is the meaning of life?")

# print(ai_msg)