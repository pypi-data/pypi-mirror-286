from .node import Node 
import random
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType


def get_simulation_node_count(per_instance_cpu, per_instance_memory_gib, default_pods, pods_to_schedule):
    nodes = []

    def make_node():
      node =  Node(per_instance_cpu=per_instance_cpu, per_instance_memory_gib=per_instance_memory_gib, default_pods=default_pods)
      nodes.append(node)
      return node

    # Static/DaemonSet pods need to go on every node.
    random.shuffle(pods_to_schedule)

    for pod in pods_to_schedule:
        # Schedule according to LeastAllocated scoring policy.
        candidates = [node for node in nodes if node.fits(pod)]
        candidates.sort(key=lambda x: (x.used_cpu / x.per_instance_cpu + x.used_memory / x.per_instance_memory), reverse=False)
        if len(candidates) > 0:
          candidates[0].add_pod(pod)
          continue

        # If no node can accommodate the pod, create a new node.
        new_node = make_node()
        new_node.add_pod(pod)

    return len(nodes)
    
    
def do_multiple_sims(simulation_context, per_instance_cpu = 50, per_instance_memory_gib = 50, num_runs = 10):
  default_pods =  simulation_context.get_default_pods()
  pods_to_sched = simulation_context.get_pods_to_schedule()
  sim_udf = udf(lambda _: get_simulation_node_count(per_instance_cpu,per_instance_memory_gib,default_pods, pods_to_sched), IntegerType())
  sims_df = simulation_context.spark.range(num_runs).withColumn("simulation_result", sim_udf("id"))
  return sims_df