from langchain_groq import ChatGroq

GROQ_API_KEY = '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'

def load_llm():
  llm = ChatGroq(
      groq_api_key = GROQ_API_KEY,
      model_name = 'Llama3-8b-8192',
      temperature=0.2,
      top_p = 0.6,
      max_tokens = 1024,
  )
  return llm