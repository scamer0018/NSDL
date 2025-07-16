import io
import contextlib
from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "eval",
                "category": "dev",
                "description": {
                    "content": "Evaluate Python code.",
                    "usage": "<code>",
                },
                "exp": 1,
                "devOnly": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        if not contex.text:
            return self.client.reply_message(
                "⚠️ Please provide some Python code to evaluate.", M
            )

        code = contex.text.strip()
        env = {
            "self": self,
            "client": self.client,
            "M": M,
            "__name__": "__main__",
        }

        stdout = io.StringIO()
        try:
            code = self._clean_code(code)

            exec_code = f"def __eval_func():\n"
            for line in code.splitlines():
                exec_code += f"    {line}\n"

            exec(exec_code, env)
            with contextlib.redirect_stdout(stdout):
                result = env["__eval_func"]()

            output = stdout.getvalue()
            result_output = (
                f"{output}{result}"
                if result is not None
                else output or "✅ Done"
            )

            self.client.reply_message(
                f"📤 *Eval Result:*\n```{result_output.strip()}```", M
            )

        except Exception as e:
            self.client.reply_message(f"❌ *Error:*\n```{str(e)}```", M)

    def _clean_code(self, code: str) -> str:
        # Remove code block formatting if any
        if code.startswith("```") and code.endswith("```"):
            code = "\n".join(code.split("\n")[1:-1])
        return code.strip()
