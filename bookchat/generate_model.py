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
from .models import Book, Chat

class ChainManager:
    def __init__(self, id, user):
        self.id = id
        self.user = user
        self.chain = None

    def get_previous_chat(self):
        chat_list = Chat.objects.filter(user=self.user)
        previous_chat = ""
        for chat in chat_list:
            previous_chat += chat.msg
        print(previous_chat)
        return previous_chat

    def make_retriever(self):
        book = Book.objects.get(id=self.id)
        path = os.path.join(settings.MEDIA_ROOT, book.pickle.path)
        with open(os.path.join(path), "rb") as f:
            vector_store = pickle.load(f)
        retriever = vector_store.as_retriever(search_kwargs={"k": 2})
        return retriever

    def make_llm(self):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=1000)  # Modify model_name if you have access to GPT-4
        return llm

    def make_prompt(self):
        book = Book.objects.get(id=self.id)
        previous_chat = self.get_previous_chat()
        print(previous_chat)
        system_template = '''
        You should do a role play. You are the author of this book given to you named'''+ book.title+'''
        You should debate with the user about the book, so you sometimes need to make questions during the debate.
        Since you are the author of the book, you should give clear answer to the question based on the content of the book.
        And since you are doing debate, you sometimes need to acknowledge the user's point of view.
        The previous chatting log is '''+previous_chat+'''
        {summaries}
        You MUST answer in Korean and in Markdown format.
        If the counterpart uses informal words, you should use informal words.
        Informal words are shorter than formal words in Korea, like using 했어 instead of 했습니다.
        Do not answer too long, just give your point briefly.
        keep in mind that you are the author of the book:'''
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        return prompt

    def make_chain(self):
        prompt = self.make_prompt()
        self.get_previous_chat()
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
