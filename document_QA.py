from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
import os

from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain


os.environ["OPENAI_API_KEY"] = os.getenv('OPEN_AI_KEY')

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=os.getenv('OPEN_AI_KEY'))

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

persist_directory = 'docs/chroma/'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
retriever=vectordb.as_retriever()

def load_db(file, chain_type, k):
    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    # define embedding
    embeddings = OpenAIEmbeddings()
    # create vector database from data
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    # define retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    # create a chatbot chain. Memory is managed externally.

    qa = ConversationalRetrievalChain.from_llm(
        llm,
        chain_type=chain_type,
        retriever=retriever,
        memory=memory
    )
    return qa


def main():
    loaded_file = "docs/gemini_in_medecine.pdf"
    qa = load_db(loaded_file, "stuff", 4)
    prompt = ""
    while prompt != "0":
        print("You can ask me any question related to Capabilities of Gemini Models in Medicine or 0 to exit")
        question = str(input())
        result = qa({"question": question})
        print(result["answer"])

if __name__ == "__main__":
    main()