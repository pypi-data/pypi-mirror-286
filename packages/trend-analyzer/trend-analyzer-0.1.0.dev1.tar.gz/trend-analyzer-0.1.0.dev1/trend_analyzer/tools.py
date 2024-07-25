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
"""Exposes trend analyzer as a tool for Langchain agents."""

import langchain_core

from trend_analyzer import analyzer, llms, vectorstore


class TrendsAnalyzerInput(langchain_core.pydantic_v1.BaseModel):
  """Input for text categorization."""

  question: str = langchain_core.pydantic_v1.Field(
    description='trend analysis question'
  )


class TrendsAnalyzerResults(langchain_core.tools.BaseTool):
  """Tools that performs trend analysis.

  Attributes:
    llm_type: Type of LLM to use for categorization.
    llm_parameters: Parameter for LLM initialization.
  """

  llm_type: str = 'gemini'
  llm_parameters: dict[str, str] = {'model': 'gemini-1.5-flash'}
  name: str = 'trend_analyzer_results_json'
  description: str = 'infers trends based on a vectorstore documents'
  args_schema: type[langchain_core.pydantic_v1.BaseModel] = TrendsAnalyzerInput

  def _run(
    self,
    question: str,
  ) -> list[dict[str, str]]:
    """Performs trend analysis based on LLM and vectorstore.

    Args:
      question: Question to LLM.

    Returns:
      Mappings between text and its category.
    """
    llm = llms.create_trend_analyzer_llm(self.llm_type, self.llm_parameters)
    trend_analyzer = analyzer.TrendsAnalyzer(
      llm=llm, vect_store=vectorstore.load_vectorstore()
    )
    return trend_analyzer.analyze(question).to_list(row_type='dict')
