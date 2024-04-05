let s:path = expand('<sfile>:p:h')

call remote#host#RegisterPlugin('python3', s:path.'/llm_stream.py', [
      \ {'sync': v:false, 'name': 'LLMStream', 'type': 'function', 'opts': {'nargs': '*'}},
      \ ])

command! -nargs=+ LLM :call LLMStream(<f-args>)

