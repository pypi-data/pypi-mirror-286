import re
from cwstorm.dsl.dag_node import DagNode



class WorkNode(DagNode):
    
    """
Abstract base class nodes that do some work.

Work nodes can be set to be in a holding state initially, or to start immediately. Tasks, and integrations are work nodes. The Job node does not do work. It only provides information. In the future there may be other types that only provide information.
    """
    
    BASE_ATTRS = {
        "initial_state": {
            "type": "str",
            "validator": re.compile(r"^(hold|start)$"),
            "default": "hold",
            "description": "Whether the node should start when all it's inputs are complete, or be held and wait for manual approval to unhold.",
        },
    }
    ATTRS = {}
    ORDER = 25
