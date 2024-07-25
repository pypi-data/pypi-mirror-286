# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for defining vector store.

Vectorstore contains necessary data to improve LLM results.
"""

import itertools
import pathlib

import chromadb
import langchain_chroma
import langchain_text_splitters
from langchain_community import document_loaders, embeddings
from langchain_core import vectorstores


def get_vector_store(
  vectorstore_type: vectorstores.VectorStore = langchain_chroma.Chroma,
  vector_store_directory: str = './../assistant_db',
  embedding_function=embeddings.FakeEmbeddings(size=1352),
):
  """Loads or creates vectorstore."""
  if not vector_store_directory:
    return load_vectorstore(
      vectorstore_type, vector_store_directory, embedding_function
    )
  return vectorstore_type(
    persist_directory=vector_store_directory,
    embedding_function=embedding_function,
    client_settings=chromadb.config.Settings(anonymized_telemetry=False),
  )


def load_vectorstore(
  vectorstore_type: vectorstores.VectorStore = langchain_chroma.Chroma,
  samples_directory: pathlib.Path = pathlib.Path(__file__).resolve().parent
  / 'files',
  embedding_function=embeddings.FakeEmbeddings(size=1352),
) -> langchain_chroma.Chroma:
  """Creates vectorstore from documents and embeddings."""
  splits = []
  for file in samples_directory.iterdir():
    if file.is_file():
      loader = document_loaders.JSONLoader(
        file_path=file, jq_schema='.results', text_content=False
      )
      docs = loader.load()

      text_splitter = (
        langchain_text_splitters.character.RecursiveCharacterTextSplitter(
          chunk_size=1000, chunk_overlap=200
        )
      )
    splits.append(text_splitter.split_documents(docs))
  return vectorstore_type.from_documents(
    documents=itertools.chain.from_iterable(splits),
    embedding=embedding_function,
  )
