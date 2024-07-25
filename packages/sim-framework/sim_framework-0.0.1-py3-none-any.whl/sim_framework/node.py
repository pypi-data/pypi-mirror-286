from .consts import CPU_REQUEST_KEY, MEMORY_REQUEST_KEY, POD_NAME_KEY

class Node:
    def __init__(self, per_instance_cpu, per_instance_memory_gib, default_pods):
        self.per_instance_cpu = per_instance_cpu
        self.per_instance_memory = per_instance_memory_gib * 1024 * 1024 * 1024
        self.used_cpu = 0
        self.used_memory = 0

        # Holds references to approximations of the parent workloads of scheduled pods.
        self.scheduled = set()

        # Static + DaemonSet pods are always scheduled onto the Node and take up capacity.
        for pod in default_pods:
          self.used_cpu += self.__calculate_pod_cpu_request(pod)
          self.used_memory += (pod[MEMORY_REQUEST_KEY] or 0)
        self.pods = default_pods.copy()
    
    # Pod can only fit if its CPU and memory requests are each <= remaining capacity.
    # Approximating intra-workload pod anti-affinity i.e. multiple pods with same parent workload cannot be hosted on the same node.
    def fits(self, pod):
        if self.__get_workload(pod) in self.scheduled:
          return False

        fits_cpu = (self.used_cpu + self.__calculate_pod_cpu_request(pod)) <= self.per_instance_cpu
        fits_memory = (self.used_memory + (pod[MEMORY_REQUEST_KEY] or 0)) <= self.per_instance_memory
        return fits_cpu and fits_memory
    
    def add_pod(self, pod):
        self.scheduled.add(self.__get_workload(pod))

        self.pods.append(pod)
        self.used_cpu += self.__calculate_pod_cpu_request(pod)
        self.used_memory += (pod[MEMORY_REQUEST_KEY] or 0)

    # Calculate the actuated CPU request of the Pod, factoring in ramp-up fraction.
    def __calculate_pod_cpu_request(self, pod):
      return pod[CPU_REQUEST_KEY]
    
    # Rough approximation of pod's parent workload.
    def __get_workload(self, pod):
      parts = pod[POD_NAME_KEY].split("-")
      return "-".join(parts[:-1])