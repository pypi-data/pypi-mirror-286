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
"""Module for performing trends analysis.

Exposes a single class TrendAnalyzer that allows to get extract trends from
vector store based on provided LLM.
"""

from __future__ import annotations

import pathlib

import gaarf
import smart_open
from langchain_core import (
  language_models,
  output_parsers,
  prompts,
  pydantic_v1,
  runnables,
  vectorstores,
)


class Trend(pydantic_v1.BaseModel):
  """Defines structured output for LLM.

  Attributes:
    name: Name of the trend.
    growth: Relative growth associated with trend.
  """

  name: str = pydantic_v1.Field(description='trend name')
  growth: float = pydantic_v1.Field(description='trend growth')


def _format_docs(docs):
  return '\n\n'.join(doc.page_content for doc in docs)


class TrendsAnalyzer:
  """Handles prompts related to analyzing trends.

  Attributes:
    vect_store: Vector store containing data on trends.
    llm: LLM responsible to handle prompts.
  """

  def __init__(
    self,
    vect_store: vectorstores.VectorStore,
    llm: language_models.BaseLanguageModel,
  ) -> None:
    """Initializes TrendsAnalyzer based on vectorstore and LLM.

    Args:
      vect_store: Vector store containing data on trends.
      llm: LLM responsible to handle prompts.
    """
    self.vect_store = vect_store
    self.llm = llm

  @property
  def prompt(self) -> prompts.PromptTemplate:
    """Builds correct prompt to send to LLM.

    Prompt contains format instructions to get output result.
    """
    with smart_open.open(
      pathlib.Path(__file__).resolve().parent / 'template.txt',
      'r',
      encoding='utf-8',
    ) as f:
      template = f.readlines()
    return prompts.PromptTemplate(
      template=' '.join(template),
      input_variables=['question'],
      partial_variables={
        'format_instructions': self.output_parser.get_format_instructions(),
      },
    )

  @property
  def output_parser(self) -> output_parsers.BaseOutputParser:
    """Defines how LLM response should be formatted."""
    return output_parsers.JsonOutputParser(pydantic_object=Trend)

  def analyze(self, text: str) -> gaarf.report.GaarfReport:
    """Performs trend analysis based on a provided question.

    Args:
      text: Question to LLM.

    Returns:
      Report with trends data.
    """
    chain = (
      {
        'context': self.vect_store.as_retriever() | _format_docs,
        'question': runnables.RunnablePassthrough(),
      }
      | self.prompt
      | self.llm
      | self.output_parser
    )
    result = chain.invoke(text)
    results = []
    for r in result:
      results.append([*r.values()])
    return gaarf.report.GaarfReport(
      results=results, column_names=[*result[0].keys()]
    )
