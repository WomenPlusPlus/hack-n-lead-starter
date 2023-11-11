import os
import openai

from qdrant_client import QdrantClient, models
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.schema.document import Document

api_key = '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'
url = 'https://api.openai.com/v1/'
embedding_name = 'text-embedding-ada-002'
size = 1536

collection_name = 'swiss-law'

openai.api_key = api_key
openai.api_base = url

collections = ['swiss-law']
COLLECTION_NAME = collections[0]

embeddings_model = OpenAIEmbeddings(
    model=embedding_name,
    openai_api_key=api_key,
    openai_organization = 'org-66N72mGO3XwF80FfTwkYtkqT',
    openai_api_base=url
)

client = QdrantClient(host="localhost", port=6333, prefer_grpc=False)

vector_params = models.VectorParams(
    size=size,
    distance=models.Distance.COSINE
)


# eventual list of articles
articles = ["texts/article1.txt"]


def read_article(article_path: list):
    # This is a long document we can split up
    with open(article_path) as f:
        article = f.read()
        document_article = Document(page_content=article)
        metadata_point = os.path.basename(f.name).split('.')[0]
        document_article.metadata.update(topic=metadata_point, url=metadata_point)
    return document_article

document_article = read_article(articles[0])


def make_chunks(original_articles: str):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=30,
    length_function = len,
    is_separator_regex=False
    )

    splitted_articles = text_splitter.split_documents([original_articles])

    return splitted_articles


text = make_chunks(document_article)

vectorstore = Qdrant(client, collection_name=collection_name, embeddings=embeddings_model)
vectorstore.add_documents(text)