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
"""Module for defining various LLMs for performing trends analysis."""

from __future__ import annotations

import langchain_google_vertexai
from langchain_core import language_models


def create_trend_analyzer_llm(
  llm_type: str, llm_parameters: dict[str, str] | None = None
) -> language_models.BaseLanguageModel:
  """Creates LLM based on type and parameters.

  Args:
    llm_type: Type of LLM to instantiate.
    llm_parameters: Various parameters to instantiate LLM.

  Returns:
    Initialized LLM.

  Raises:
    TrendsAnalyzerLLMError: When incorrect LLM type is specified.
  """
  mapping = {
    'gemini': langchain_google_vertexai.ChatVertexAI,
    'fake': language_models.FakeListLLM,
  }
  if llm := mapping.get(llm_type):
    if not llm_parameters:
      llm_parameters = {}
    return llm(**llm_parameters)
  raise TrendsAnalyzerLLMError(f'Unsupported LLM type: {llm_type}')


class TrendsAnalyzerLLMError(Exception):
  """Error when incorrect LLM type is specified."""
