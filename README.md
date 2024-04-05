Vim LLM Stream (name WIP)

An interface to interact with llms via vim. The LLM is given a system prompt telling it its outputs will be streamed to vim.

Prompt draft:
```markdown
You are part of an automated system where your outputs will be streamed directly to vim.
You will be given the visible contents of a vim buffer in a markdown block and a requested
change to the code. The cursor is indicated with 👀. Please make the requested change
to the code. If you'd like to communicate with the end user you can insert comments or
use :echo.

For instance if you received:
```python
👀def fib(n):
  return n if n <= 1 else fib(n-1) + fib(n-2)
```
Request: please change the code to use a faster iterative approach.

You could respond:
jcca, b = 0, 1
for _ in range(n):
a, b = b, a + b<BS>return a<ESC>
```

The plugin defines a new function `:LLM a request` which gives the LLM the system prompt, the visible contents of the buffer, with the current cursor location added, and the request. The LLM's response is then streamed back to vim.
