from cwstorm.dsl.work_node import WorkNode

class Shotgrid(WorkNode):
    """
A Shotgrid node is a bot that sends a notification to a Shotgrid channel.
    """
    ORDER = 80
    ATTRS = {
        "entity": {
            "type": "dict",
            "default": {"type": "Shot", "id": 0},
            "description": "The entity that can be configured and sent to Shotgrid.",
        },
    }