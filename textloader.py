from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
model =ChatOpenAI()
prompt= PromptTemplate(
    template='Explain the context of given {information}',
    input_variables=["information"]
)
parser=StrOutputParser()

loader =TextLoader("TEXTLOADER.txt",encoding="utf-8")
docs= loader.load()
print(docs)
print(len(docs))
print(docs[0].page_content)
print(docs[0].metadata)

chain = prompt | model | parser
print(chain.invoke)