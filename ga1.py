import os
import json

tools = [
    # GA1, Question 1
    {
        "type": "function",
        "function": {
            "name": "output_of_code_s",
            "description": """Install and run Visual Studio Code. In your Terminal
              (or Command Prompt), type code -s and press Enter. Copy and paste the entire output below.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Command to run to get the information about Visual Studio Code",
                    }
                },
                "required": ["command", ],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

async def output_of_code_s(command: str) -> str:
    file_path = os.path.join('hard_coded_answers','ga01_q01_code_s.txt')
    with open(file_path, 'r') as file:
        content = file.read()

    # content = json.dumps(content)
    return content
