import pynvim
import os
import datetime
import json
import litellm

system_prompt = """
You are part of an automated system where your outputs will be streamed directly to vim.
You will be given the visible contents of a vim buffer in a markdown block and a requested
change to the code. The cursor is indicated with 👀. Please make the requested change
to the code. If you'd like to communicate with the end user you can insert comments or
use :echo. You can use <bs>, <esc>, <c-...> and the like to insert control sequences.

For instance if you received:
```
👀def fib(n):
  return n if n <= 1 else fib(n-1) + fib(n-2)
```
REQUEST: please change the code to use a faster iterative approach.

You could respond:
jcca, b = 0, 1
for _ in range(n):
a, b = b, a + b<BS>return a<ESC>
--------------------------------------------------------------------------------
Or if you receive:
```
👀
```
REQUEST: please open my vimrc file.

You could respond:
:e ~/.vimrc<CR>
--------------------------------------------------------------------------------
Or if you receive:
```
let mapleader = "-"
let maplocalleader = "="
syntax on

set number rnu
set cursorline cursorcolumn
set scrolloff=5

" Tmux color fix
set background=dark
set t_Co=256
" Needed to backspace over eol on mac
set backspace=2
set noerrorbells

set smartcase ignorecase noincsearch
set path+=**3
set wildmenu

set autoread

set nosplitbelow splitright

set softtabstop=4
set autoindent expandtab
set shiftwidth=4

" I'm always making these typos
command! Wq :wq
command! WQ :wq
command! Q :q
command! W :w
command! Wqa :wqa

" Linear Algebra
AbbrevWord ind independent
AbbrevWord indy independently
AbbrevWord indc independence
AbbrevWord linind linearly independent
AbbrevWord codim codimension
AbbrevWord cok cokernel
AbbrevWord dmn dimension
AbbrevWord dmnl dimensional
AbbrevWord vs vector space
AbbrevWord rel relationship

" General Math
AbbrevWord poly polynomial
AbbrevWord seq sequence
AbbrevWord ctns continuous
iabbrev i I
AbbrevWord y why
AbbrevWord b be
AbbrevWord dont don't
AbbrevWord cant can't
AbbrevWord ab about
AbbrevWord mb maybe
AbbrevWord bt but
AbbrevWord wev whatever

" MTG
AbbrevWord gy graveyard
AbbrevWord bf battlefield
```
REQUEST: please delete my abbreviations for i, y, and bf

You could respond:
/iabbrev i<CR>2ddGdd
"""

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_dir = f"{os.path.dirname(os.path.abspath(__file__))}/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    with open(f"{log_dir}/log_{timestamp}.log", "w") as f:
        f.write(message)
    with open(f"{log_dir}/last_log", "w") as f:
        f.write(message)

@pynvim.plugin
class VimLLMStream:
    def __init__(self, nvim):
        self.nvim = nvim

    def print(self, *args):
        self.nvim.command(f'echom "{args}"')

    @pynvim.function('LLMStream')
    def llm_stream(self, args):
        buffer_contents = self.nvim.current.buffer[:]
        line, col = self.nvim.current.window.cursor
        line -= 1
        buffer_contents[line] = buffer_contents[line][:col] + "👀" + buffer_contents[line][col:]
        buffer_contents = "\n".join(buffer_contents)

        request_content = " ".join(args)

        messages = [
                {"content": system_prompt, "role": "system"},
                {"content": f"```\n{buffer_contents}\n```\nREQUEST: {request_content}", "role": "user"},
            ]

        response = litellm.completion(
            model="claude-3-opus-20240229",
            messages=messages,
            max_tokens=4000,
            stream=True
        )
        self.nvim.feedkeys("\x1b")

        to_send = ""
        full = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                to_send += chunk.choices[0].delta.content
                full += chunk.choices[0].delta.content
                if '<' not in to_send[-8:]: # <right> is 7 characters
                    to_send = self.nvim.replace_termcodes(to_send)
                    self.nvim.feedkeys(to_send)
                    to_send = ""
        messages.append({"content": full, "role": "assistant"})
        log(json.dumps(messages, indent=4))
        to_send = self.nvim.replace_termcodes(to_send)
        self.nvim.feedkeys(to_send)

