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
"""Provides CLI for text categorization."""

import argparse
import pathlib

import smart_open
from gaarf.cli import utils as gaarf_utils
from gaarf.executors import bq_executor
from gaarf.io import writer

from text_categorization import categorizer, llms, vectorstore


def read_examples(path: str | pathlib.Path) -> list[str]:
  """Reads examples of categorization from provided path.

  Args:
    path: Relative path to file with examples.

  Returns:
    Multiple example to help with categorization.
  """
  with smart_open.open(
    pathlib.Path(__file__).resolve().parent / path,
    'r',
    encoding='utf-8',
  ) as f:
    return f.readlines()


def read_example_from_bq(table_name: str) -> list[str]:
  """Reads examples of categorization from BigQuery.

  Example table should contains two columns (name and category).

  Args:
    table_name: Fully qualified table name (project_id.dataset.table).

  Returns:
    Multiple example to help with categorization.
  """
  project_id, *dataset_table = table_name.split('.')
  table_name = '.'.join(dataset_table)
  query_text = f'SELECT name, category FROM {table_name};'
  examples = bq_executor.BigQueryExecutor(project_id).execute(
    'examples', query_text
  )
  return [f'{data.name} - {data.category}' for data in examples.itertuples()]


def read_texts_from_bq(table_name: str) -> list[str]:
  """Reads texts for categorization from BigQuery.

  Table should contains one column called `name`.

  Args:
    table_name: Fully qualified table name (project_id.dataset.table).

  Returns:
    Texts for categorization.
  """
  project_id, *dataset_table = table_name.split('.')
  table_name = '.'.join(dataset_table)
  query_text = f'SELECT text FROM {table_name} LIMIT 2000;'
  texts = bq_executor.BigQueryExecutor(project_id).execute('texts', query_text)
  return [data.text for data in texts.itertuples()]


def main():  # noqa D103
  parser = argparse.ArgumentParser()
  parser.add_argument('texts', nargs='*')
  parser.add_argument('--llm', dest='llm')
  parser.add_argument('--output-type', dest='output', default='console')
  parser.add_argument(
    '--output-destination', dest='destination', default='results'
  )
  parser.add_argument(
    '--remote-texts',
    dest='remote_texts',
    default=None,
  )
  parser.add_argument(
    '--examples', dest='examples', default='../text_categorization/examples.txt'
  )

  args, kwargs = parser.parse_known_args()
  params = gaarf_utils.ParamsParser(['llm', args.output]).parse(kwargs)

  try:
    examples = read_example_from_bq(args.examples)
  except bq_executor.BigQueryExecutorException:
    examples = read_examples(args.examples)

  if remote_texts := args.remote_texts:
    texts = read_texts_from_bq(remote_texts)
  else:
    texts = []

  llm = llms.create_categorizer_llm(args.llm, params.get('llm'))
  text_categorizer = categorizer.TextCategorizer(
    llm=llm, vect_store=vectorstore.get_vector_store()
  )

  text_categorizer.add_examples(examples, load_to_vectorstore=True)
  result = text_categorizer.categorize(args.texts + texts)
  writer.create_writer(args.output, **params.get(args.output)).write(
    result, args.destination
  )


if __name__ == '__main__':
  main()
