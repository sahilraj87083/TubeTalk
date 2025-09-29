from langchain.text_splitter import RecursiveCharacterTextSplitter

def format_docs(retrieved_docs):
    return "\n".join(doc.page_content for doc in retrieved_docs)


def text_spilliter (docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([docs])
    return chunks