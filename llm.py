from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpointEmbeddings, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv


load_dotenv()

hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id='openai/gpt-oss-20b',
    task='text-generation',
    huggingfacehub_api_token=hf_token
)

model = ChatHuggingFace(llm=llm)
embedding_model = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-mpnet-base-v2")
parser = StrOutputParser()