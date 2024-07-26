import re
import os
import platform
from cwstorm.dsl.dag_node import DagNode
from cwstorm import __schema_version__

 
def _get_username():
    """Return the username of the current user."""
    result = (
        os.environ.get("USERNAME")
        if platform.system() == "Windows"
        else os.environ.get("USER")
    )
    if not result:
        result = "unknown"
    return result


class Job(DagNode):
    """
The single node that represents the entire submission job.

Conceptually, a job is what the other nodes in the graph are working towards.
    """

    ORDER = 20
    ATTRS = {
        "comment": {
            "type": "str",
            "validator": re.compile(r'^[_a-z0-9 ,.!?\'"]+$', re.IGNORECASE),
            "description": "A comment about the job that can appear in the job index.",
        },
        "project": {
            "type": "str",
            "validator": re.compile(r"^[a-z0-9_\-\.\s]+$", re.IGNORECASE),
            "description": "The Conductor project with which this job is associated.",
        },
        "author": {
            "type": "str",
            "validator": re.compile(r"^[a-z\s]+$", re.IGNORECASE),
            "default": _get_username(),
            "description": "The user who submitted the job. This should be controlled by client tools in order to ensure the user is who they say they are.",
        },
        "location": {
            "type": "str",
            "validator": re.compile(
                r"^(?:[a-z][a-z0-9]*$|([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|^$)",
                re.IGNORECASE,
            ),
            "description": "The location tag allows the uploader and downloader daemons to limit themselves to specific jobs with matching locations.",
        },
        "schema_version": {
            "type": "str",
            "validator": re.compile(r"^\d{1,2}\.\d{1,2}.\d{1,2}$"),
            "default": __schema_version__,
            "description": "The clientside schema version.",
        },
    }

    def is_original(self, _):
        """Always true."""
        return True

    def is_reference(self, _):
        """Always false."""
        return False
