import functools, random
from .consts import NODE_PARENT, DAEMONSET_PARENT, OWNER_KIND_KEY, NODE_NAME_KEY

class SimulationContext:

  def __init__(self, spark, pods, cluster):
    self.spark = spark
    self.cluster = cluster
    self.pods = pods

  @functools.cache
  def get_pods_to_schedule(self):
    pods_to_schedule = self.pods[~self.pods[OWNER_KIND_KEY].isin([NODE_PARENT, DAEMONSET_PARENT])]
    return [row.asDict() for row in pods_to_schedule.collect()]

  @functools.cache
  def get_default_pods(self):
    default_pods = self.pods[self.pods[OWNER_KIND_KEY].isin([NODE_PARENT, DAEMONSET_PARENT]) & (self.pods[NODE_NAME_KEY] == self.pods.select(NODE_NAME_KEY).first()[0])]
    return [row.asDict() for row in default_pods.collect()]