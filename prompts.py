system_prompt = """You are an ai agent (codename "portal") that is tasked with applying to jobs for me.

Your goal is to successfully submit an application for a software developer job.

Here is my resume:
resume

If at any point you need more information than what's on my resume, you can call the get_more_info function with your query to a vector db to get more answers.

Once you've succesfully completed an application, call the all_done function."""


get_more_info_tool = {
    "name": "get_more_info",
    "description": "Get more information about Michael for the job application.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_query": {
                "type": "string",
                "description": "A brief description of what else you need to know about Michael.",
            },
        },
        "required": ["search_query"],
    },
}

all_done_tool = {
    "name": "all_done",
    "description": "Signal that you've succesfully completed a job application.",
    "input_schema": {
        "type": "object",
        "properties": {
            "is_done": {
                "type": "boolean",
                "description": "True if you've succesffuly completed a job application.",
            },
        },
        "required": ["is_done"],
    },
}
