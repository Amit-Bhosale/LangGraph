from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    api_key="",
    max_retries=2,
    # other params...
)

# ai_msg=llm.invoke("What is the meaning of life?")

# print(ai_msg)