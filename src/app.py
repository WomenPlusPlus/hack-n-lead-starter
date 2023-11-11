import openai
import streamlit as st

from qdrant_client import QdrantClient, models
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.vectorstores import Qdrant

TITLE = "LEX'N'BOT"
api_key = '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'
url = 'https://api.openai.com/v1/'
model_name = 'gpt-4'
embedding_name = 'text-embedding-ada-002'
COLLECTIONS = ['swiss-law']

openai.api_key = api_key
openai.api_base = url


collections = ['swiss-law']
COLLECTION_NAME = collections[0]

client = QdrantClient("localhost", port=6333)

vector_params = models.VectorParams(
    size=1536,
    distance=models.Distance.COSINE
)

embeddings_model = OpenAIEmbeddings(
    model=embedding_name,
    openai_api_key=api_key,
    openai_organization = 'org-66N72mGO3XwF80FfTwkYtkqT',
    openai_api_base=url
)

retrievers = {
    name: Qdrant(client, collection_name=name, embeddings=embeddings_model) for name in COLLECTIONS
}

identity = """ You are a helpful AI legal assistant having a conversation with a human. You are honest and provide as much details as possible."""

def create_sources(documents):
    unique_sources = {
        document.metadata['url']: {'topic': document.metadata['topic'], 'title': document.metadata['url']} for document in documents}
    return '\n' + '\n'.join(
        [f"- [{metadata['topic']} - {metadata['title']}]({topic})" for topic, metadata in unique_sources.items()])

def create_chain(memory, temperature=0.1, top_p=0.9, max_length=100, top_k_documents=5, collection_name='swiss-law'):
    system_message = (f"""
    Your identity is: {identity}
    Only use the information provided in the Context below. Do not make things up. If you do not know the answer, say: "I do not know".
    """)
    template = system_message + """
    Context:
    {context}

    conversation_history:
    {chat_history}
    Human: {question}
    assistant:
    """

    llm = OpenAI(
        model_name=model_name,
        openai_api_key=api_key, 
        # openai_organization='org-66N72mGO3XwF80FfTwkYtkqT', 
        temperature=0)

    qa_prompt = PromptTemplate(input_variables=['chat_history', 'question', 'context'], template=template)
    retriever = retrievers[collection_name].as_retriever(search_kwargs={'k': top_k_documents})
    chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={'prompt': qa_prompt},
        verbose=True
    )
    chain.return_source_documents=True
    return chain

msgs = StreamlitChatMessageHistory()

memory = ConversationBufferMemory(memory_key='chat_history', chat_memory=msgs, return_messages=True, output_key='answer')

if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

st.set_page_config(page_title=TITLE, initial_sidebar_state='collapsed', layout='wide')

with st.sidebar:
    st.title(TITLE)
    identity = st.sidebar.text_area('system_prompt', value=identity)
    top_k_documents = st.sidebar.slider('top_k_documents', min_value=1, max_value=10, value=3, step=1)
    collection = st.sidebar.selectbox(
        "Which collection",
        COLLECTIONS,
        index=0
    )

avatars = {'human': 'user', 'ai': 'assistant'}

for msg in msgs.messages:
    content = msg.content
    print(content)
    if 'source' in msg.additional_kwargs:
        content += msg.additional_kwargs['source']
    st.chat_message(avatars[msg.type]).write(content)

def clear_chat_history():
    msgs.clear()


st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

if prompt := st.chat_input('Tell me what you want to find'):

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        container = st.container()
        st_callback = StreamlitCallbackHandler(container)
        llm_chain = create_chain(memory, temperature=0.1, top_p=0.5, max_length=100, top_k_documents=top_k_documents, collection_name=collection)
        response=llm_chain({"question": prompt}, callbacks=[st_callback])
        st_callback._complete_current_thought("Completed")

        source = "\n\nSources:" + create_sources(documents=response['source_documents'])
        response['answer'] += source
        print(response['answer'])

        msgs.messages[-1].additional_kwargs['source'] = source

        container.markdown(response['answer'])
