import os 
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Api key not found")
client=Groq(api_key=api_key)
response=client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role":"user",
            "content":"Explain me the basic components of LLaMA model"
        }
        
    ],
    max_completion_tokens=400,
    temperature=0.3
)
answer = response.choices[0].message.content
print("\nAssistant:", answer)



usage = response.usage

print("\nToken usage:")

if usage is not None:
    print("Input tokens:", usage.prompt_tokens)
    print("Output tokens:", usage.completion_tokens)
    print("Total tokens:", usage.total_tokens)
else:
    print("Token usage information was not returned by the API.")
