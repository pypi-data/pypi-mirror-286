import functools, random
from .sim_context import SimulationContext

class SimulatorFramework:
  
  def __init__(self, spark):
    self.pods = self._get_pods(spark).cache()
    self.pods_by_cluster = self._separate_pods_by_cluster()

  def new_simulation_context(self, cluster):
    return SimulationContext(self.spark, self.pods_by_cluster[cluster], cluster)

  def get_all_clusters(self):
    return list(self.pods_by_cluster.keys())
  
  def _get_pods(self, spark):
    query = """
    SELECT 
    cluster,
    node_name,
    container_info.owner_kind,
    container_info.namespace,
    pod_name,
    COUNT(*) AS container_count,
    SUM(request_cpu) AS request_cpu,
    SUM(request_memory) AS request_memory,
    SUM(
        CASE
        WHEN vpa_query.request_cpu_vpa IS NULL THEN request_cpu
        WHEN limit_cpu IS NOT NULL AND vpa_query.request_cpu_vpa > limit_cpu THEN limit_cpu
        WHEN vpa_query.request_cpu_vpa < 0.02 THEN 0.02
        WHEN vpa_query.request_cpu_vpa > request_cpu AND owner_kind = "DaemonSet" THEN request_cpu
        ELSE vpa_query.request_cpu_vpa * 1.15
        END
    ) AS request_cpu_vpa
    FROM (
    SELECT
        nodes.cluster AS cluster,
        nodes.metadata.name AS node_name,
        pods.metadata.owner_references[0].kind AS owner_kind,
        pods.metadata.namespace AS namespace,
        pods.metadata.name AS pod_name,
        EXPLODE(pods.pod.spec.containers) AS container,
        COALESCE(container.resources.requests.cpu, 0) AS request_cpu,
        container.resources.limits.cpu AS limit_cpu,
        container.resources.requests.memory AS request_memory
    FROM `main`.`eng_kubernetes`.`objects_snapshot_daily` pods
    INNER JOIN `main`.`eng_kubernetes`.`objects_snapshot_daily` nodes 
        ON pods.pod.spec.node_name = nodes.metadata.name
    WHERE
        pods.date = "2024-02-01"
        AND nodes.date = pods.date
        AND pods.cluster LIKE "prod-%"
        AND pods.cluster NOT REGEXP 'general|kafka|meta|mlserv|nephos|obs|sawless|tidb'
        AND nodes.cluster = pods.cluster
        AND pods.kind = "Pod"
        AND nodes.kind = "Node"
        AND nodes.metadata.labels["pool"] = "default"
    ) AS container_info
    LEFT JOIN (
    SELECT
        _shard_name,
        metadata.namespace AS namespace,
        container_rec.container_name AS container_name,
        MAX(container_rec.target.cpu_millicores) / 1000 AS request_cpu_vpa
    FROM main.eng_lumberjack.prod_kubernetes_object_log
    LATERAL VIEW EXPLODE(vpa.status.conditions) AS condition
    LATERAL VIEW EXPLODE(vpa.status.container_recommendations) AS container_rec
    WHERE vpa IS NOT NULL
        AND _partition_date > date_sub("2024-02-01", 14)
        AND update_type = "UPDATE_TYPE_SYNC"
        AND _shard_name LIKE "prod-%"
        AND _shard_name NOT REGEXP 'general|kafka|meta|mlserv|nephos|obs|sawless|tidb'
        AND kind = "VerticalPodAutoscaler"
        AND condition.condition_type = "RecommendationProvided"
    GROUP BY _shard_name, namespace, container_name
    ) AS vpa_query 
    ON container_info.cluster = vpa_query._shard_name 
    AND container_info.namespace = vpa_query.namespace
    AND container_info.container.name = vpa_query.container_name 
    GROUP BY cluster, node_name, container_info.owner_kind, container_info.namespace, pod_name, node_name
    """
    pod_df = spark.sql(query)
    return pod_df

  def _separate_pods_by_cluster(self):
    clusters = self.pods.select("cluster").distinct().collect()
    pods_by_cluster = {cluster["cluster"]: self.pods.filter(self.pods.cluster == cluster["cluster"]).cache() for cluster in clusters}
    return pods_by_cluster
  


