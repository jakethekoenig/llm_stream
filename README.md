Vim LLM Stream (final name TBD)

An plugin to give an llm control of vim. The plugin defines a new command `:LLM a request` which gives the LLM the system prompt, the contents of the buffer, with the current cursor location added with 👀, and the request. The LLM's response is then streamed back to vim.

TODO:
tell the llm indent settings and other information that may affect how the response appears.
add a setting to change the model.
voice to text
