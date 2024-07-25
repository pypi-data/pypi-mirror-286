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
"""Provides HTTP endpoint for trend analysis."""

import fastapi
from langchain_google_vertexai import ChatVertexAI

from trend_analyzer import analyzer, vectorstore

app = fastapi.FastAPI()
llm = ChatVertexAI(model='gemini-1.5-flash-001')
trend_analyzer = analyzer.TrendsAnalyzer(
  vect_store=vectorstore.load_vectorstore(), llm=llm
)


@app.post('/')
def categorize(
  data: dict[str, str] = fastapi.Body(embed=True),
) -> list[dict[str, str | float]]:
  """Performs text categorization.

  Args:
    data: Contains texts for categorization.

  Returns:
    Category for each text.
  """
  return trend_analyzer.analyze(data.get('question')).to_list(row_type='dict')
