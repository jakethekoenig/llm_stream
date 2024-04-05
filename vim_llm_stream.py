import pynvim
import litellm

@pynvim.plugin
class VimLLMStream(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('LLMStream', nargs='*', range='')
    def llm_stream(self, args, range):
        buffer_contents = "\n".join(self.nvim.current.buffer[:])
        cursor_position = self.nvim.current.window.cursor
        request_content = " ".join(args)

        response = litellm.completion(
            model="claude-3-opus-20240229",
            messages=[
                {"content": f"Buffer contents:\n{buffer_contents}\nCursor position: {cursor_position}", "role": "system"},
                {"content": request_content, "role": "user"}
            ],
            max_tokens=10
        )

        # Assuming response is a string of vim key presses
        for key_press in response:
            self.nvim.input(key_press)