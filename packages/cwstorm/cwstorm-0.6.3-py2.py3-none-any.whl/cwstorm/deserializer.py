import logging


from cwstorm.dsl.job import Job
from cwstorm.dsl import factory

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Function to turn a dictionary containing nodes and edges back into a DAG graph
def deserialize(spec):
    nodes = {}
    job = None
    
    # Create nodes
    for data in [node["data"] for node in spec["nodes"]]:
        node = factory.get(data)
        if isinstance(node, Job):
            job = node
        nodes[data["id"]] = node

    # Create edges
    for data in [edge["data"] for edge in spec["edges"]]:
        source_node = nodes[data["source"]]
        target_node = nodes[data["target"]]
        target_node.add(source_node)

    return job
