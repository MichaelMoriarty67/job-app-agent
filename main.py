import os
import anthropic
from dotenv import load_dotenv

from prompts import system_prompt, get_more_info_tool, all_done_tool
from computer import ComputerUseAction
from utils import pil_to_b64
from config import resume

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# starting screenshot
starting_action = ComputerUseAction("screenshot")
starting_action.run_action()
action_result_img_b64 = starting_action.result

in_progress = True
messages = [
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
]

# agent conversation loop
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
            all_done_tool,
        ],
        system=system_prompt.replace("[RESUME]", resume),
        messages=messages,
        betas=["computer-use-2024-10-22"],
    )

    breakpoint()

    next_assistant_message = {"role": "assistant", "content": []}

    # extracts the tool use data
    tool_input = None
    tool_use_id = None
    tool_name = None
    for content_block in response.content:
        if content_block.type == "tool_use":
            tool_name = content_block.name
            tool_input = content_block.input
            tool_use_id = content_block.id

        next_assistant_message["content"].append(content_block)

    messages.append(next_assistant_message)

    # executes the tool use
    if tool_input is not None:
        if tool_name == "computer":
            action = tool_input["action"]

            del tool_input["action"]
            kwargs = tool_input

            next_action = ComputerUseAction(action=action, **kwargs)
            next_action.run_action()

            with open("last_img.txt", "w") as f:
                f.write(next_action.result)

            next_user_message = {"role": "user", "content": []}
            tool_use_result_block = {
                "tool_use_id": tool_use_id,
                "type": "tool_result",
                "content": [
                    {
                        "source": {
                            "data": next_action.result,
                            "media_type": "image/png",
                            "type": "base64",
                        },
                        "type": "image",
                    }
                ],
            }
            next_user_message["content"].append(tool_use_result_block)

            messages.append(next_user_message)

        if tool_name == "all_done":
            in_progress = False
    else:
        print("AI didn't use any tools... doing nothing")
