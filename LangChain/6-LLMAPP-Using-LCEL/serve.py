from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv
load_dotenv()


## Model initilzation
groq_api_key= os.getenv("GROQ_API_KEY")

llm_model = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)

# Create Prompt Template 
system_template = "Translate the following into {language}"

prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_template),
                ("user", "{text}")
            ]
)

output_parser = StrOutputParser()

## Create Chain
chain = prompt_template | llm_model | output_parser

app = FastAPI(title="Langchain Serve",
              version="1.0",
              description="A Simple API Server using Langchain runnable interface")
add_routes(
    app,
    chain,
    path="/chain"
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
