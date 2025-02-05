import os
import anthropic
from dotenv import load_dotenv

from prompts import system_prompt, get_more_info_tool, all_done_tool
from computer import ComputerUseAction
from utils import pil_to_b64

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

starting_action = ComputerUseAction("screenshot")
starting_action.run_action()
og_screenshot = starting_action.result

in_progress = True
action_result_img_b64 = pil_to_b64(og_screenshot)

while in_progress:
    response = client.beta.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=[
            {
                "type": "computer_20241022",
                "name": "computer",
                "display_width_px": 3024,
                "display_height_px": 1964,
                "display_number": 1,
            },
            {"type": "text_editor_20241022", "name": "str_replace_editor"},
            {"type": "bash_20241022", "name": "bash"},
            get_more_info_tool,
            all_done_tool,
        ],
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "source": {
                            "data": action_result_img_b64,
                            "media_type": "image/png",
                            "type": "base64",
                        },
                        "type": "image",
                    }
                ],
            }
        ],
        betas=["computer-use-2024-10-22"],
    )

    breakpoint()

    tool_input = None
    tool_name = None
    for content_block in response.content:
        if content_block.type == "tool_use":
            tool_name = content_block.name
            tool_input = content_block.input

    if tool_input is not None:
        if tool_name == "computer":
            action = tool_input["action"]

            del tool_input["action"]
            kwargs = tool_input

            next_action = ComputerUseAction(action=action, **kwargs)
            next_action.run_action()

            action_result_img_b64 = pil_to_b64(next_action.result)
        if tool_name == "all_done":
            in_progress = False
    else:
        print("AI didn't use any tools... doing nothing")
