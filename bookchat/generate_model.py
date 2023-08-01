import os
import pickle
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from django.conf import settings
from .models import Books

class ChainManager:
    def __init__(self, id):
        self.id = id
        self.chain = None

    def make_retriever(self):
        book = Books.objects.get(id=self.id)
        path = os.path.join(settings.MEDIA_ROOT, book.pickle.path)
        with open(os.path.join(path), "rb") as f:
            vector_store = pickle.load(f)
        retriever = vector_store.as_retriever(search_kwargs={"k": 2})
        return retriever

    def make_llm(self):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=1000)  # Modify model_name if you have access to GPT-4
        return llm

    def make_prompt(self):
        system_template = """Use the following pieces of context to answer the users question shortly.
        Given the following summaries of a long document and a question, create a final answer with references ("SOURCES"), use "SOURCES" in capital letters regardless of the number of sources.
        If you don't know the answer, just say that "I don't know", don't try to make up an answer.
        ----------------
        {summaries}
        You MUST answer in Korean and in Markdown format:"""
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        return prompt

    def make_chain(self):
        prompt = self.make_prompt()
        chain_type_kwargs = {"prompt": prompt}
        llm = self.make_llm()
        retriever = self.make_retriever()

        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs,
            reduce_k_below_max_tokens=True,
        )
        return chain

    def make_answer(self, query):
        if self.chain is None:
            self.chain = self.make_chain()
        result = self.chain(query)
        return result['answer']
