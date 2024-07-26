chain = (
  {
    'examples': self.vect_store.as_retriever() | vectorstore.format_docs,
    'question': runnables.RunnablePassthrough(),
  }
  | self.prompt
  | self.llm
  | self.output_parser
)<F3>оолё
