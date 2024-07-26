from cwstorm.dsl.work_node import WorkNode
import re


class Slack(WorkNode):
    """
A Slack node is a bot that sends a notification to a Slack channel.
    """

    ORDER = 70
    ATTRS = {
        "token": {
            "type": "str",
            "default": "xoxb-000000000000",
            "validator": re.compile(r"^[xoxb-][a-zA-Z0-9-]+$"),
            "description": "The Slack API token.",
        },
        "channel": {
            "type": "str",
            "default": "#storm-renders",
            "description": "The Slack channel to send the message to. This can be a channel name or ID.",
        },
        "message": {
            "type": "str",
            "default": "Completed ${workflow-id}",
            "validator": re.compile(r"^[\s\S]*$", re.IGNORECASE),
            "description": "The message to send to the channel.",
        },
        "username": {
            "type": "str",
            "validator": re.compile(r"^[a-zA-Z0-9._-]+$"),
            "default": "storm-bot",
            "description": "The username that will appear in the message.",
        },
        "icon_emoji": {
            "type": "str",
            "validator": re.compile(r"^:[a-zA-Z0-9_\-]+:$"),
            "default": ":grapes:",
            "description": "An emoji that will show up in the message on Slack.",
        },
    }