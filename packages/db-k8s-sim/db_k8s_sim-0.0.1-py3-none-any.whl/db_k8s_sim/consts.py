CLUSTER_KEY = "cluster"
NODE_COUNT_KEY = "node_count"
INSTANCE_TYPE_KEY = "instance_type"
ALLOCATABLE_MEMORY_KEY = "allocatable_memory"
ALLOCATABLE_CPU_KEY = "allocatable_cpu"

NODE_NAME_KEY = "node_name"
NAMESPACE_KEY = "namespace"
POD_NAME_KEY = "pod_name"
NAME_KEY = "name"
OWNER_KIND_KEY = "owner_kind"
KIND_KEY = "kind"

AUTOPILOT_ENABLED_KEY = "autopilot_enabled"
MEMORY_REQUEST_KEY = "request_memory"
CPU_REQUEST_KEY = "request_cpu"
AUTOPILOT_CPU_REQUEST_KEY = "request_cpu_vpa"

SIM_NODE_COUNT_KEY = "simulated_node_count"
RAMP_UP_KEY = "ramp_up_fraction"

GENERAL_PURPOSE = "general_purpose"
MEMORY_OPTIMIZED = "memory_optimized"

NODE_PARENT = "Node"
DAEMONSET_PARENT = "DaemonSet"
STATEFULSET_PARENT = "StatefulSet"
DEPLOYMENT_PARENT = "Deployment"
ROLLOUT_PARENT = "Rollout"
REPLICASET_PARENT = "ReplicaSet"

AUTOPILOT_ENABLED = "autopilot_enabled"
AUTOPILOT_DISABLED = "autopilot_disabled"
AUTOPILOT_NOT_SET = "autopilot_not_set"
AUTOPILOT_UNSUPPORTED = "autopilot_unsupported"

SIZES = {
  "AWS_HighImpact": [
    "prod-aws-eu-central-1", "prod-aws-eu-west-1", "prod-aws-us-east-1", "prod-aws-us-west-2"
  ],
  "AWS_LowImpact": [
    "prod-aws-ca-central-1", "prod-aws-eu-west-2", "prod-aws-ap-south-1", "prod-aws-us-east-2", "prod-aws-eu-west-3", "prod-aws-sa-east-1", "prod-aws-ap-northeast-2", "prod-aws-ap-southeast-1", "prod-aws-ap-southeast-2", "prod-aws-ap-northeast-1"
  ],
  "Azure_HighImpact": [
    "prod-azure-australiaeast", "prod-azure-eastus2", "prod-azure-eastus2c2", "prod-azure-westeurope", "prod-azure-westeuropec2", "prod-azure-westus"
  ],
  "Azure_MediumImpact": [
    "prod-azure-canadacentral", "prod-azure-centralusc2", "prod-azure-eastusc3", "prod-azure-northcentralusc2", "prod-azure-northeuropec2", "prod-azure-southeastasia", "prod-azure-switzerlandnorth", "prod-azure-switzerlandwest"
  ],
  "Azure_LowImpact": [
    "prod-azure-brazilsouth", "prod-azure-centralindia", "prod-azure-eastasiac2", "prod-azure-eastus2c3", "prod-azure-francecentral", "prod-azure-germanywestcentral", "prod-azure-japaneast", "prod-azure-koreacentral", "prod-azure-qatarcentral", "prod-azure-southafricanorth", "prod-azure-swedencentral", "prod-azure-uaenorth", "prod-azure-ukwest", "prod-azure-westcentralus", "prod-azure-westus3", "prod-azure-chinanorth2", "prod-azure-norwayeast", "prod-azure-chinaeast2"
  ],
  "Gcp_HighImpact": [
    "prod-gcp-us-central1", "prod-gcp-us-west4"
  ],
  "Gcp_LowImpact": [
    "prod-gcp-europe-west1", "prod-gcp-us-east1", "prod-gcp-europe-west2", "prod-gcp-us-west1", "prod-gcp-us-west1", "prod-gcp-asia-northeast1", "prod-gcp-asia-southeast1", "prod-gcp-australia-southeast1", "prod-gcp-europe-west3", "prod-gcp-northamerica-northeast1", "prod-gcp-us-east4"
  ],
}

STAGES = {
  "stage1": [
    "prod-azure-norwayeast", "prod-azure-switzerlandwest", "prod-gcp-europe-west1", "prod-gcp-us-east1", "prod-aws-eu-west-2"
  ],
  "stage1.5": [
    "prod-azure-canadacentral", "prod-azure-centralindia", "prod-azure-germanywestcentral", "prod-azure-swedencentral", "prod-azure-switzerlandnorth", "prod-azure-westus", "prod-aws-ca-central-1","prod-aws-eu-central-1"
  ],
  "stage2": [
    "prod-azure-northeuropec2", "prod-azure-qatarcentral", "prod-azure-southafricanorth", "prod-azure-uaenorth", "prod-azure-ukwest", "prod-azure-westcentralus", "prod-azure-westeurope", "prod-azure-westeuropec2", "prod-azure-westus3", "prod-gcp-europe-west2", "prod-gcp-us-central1", "prod-gcp-us-west1", "prod-aws-us-east-2", "prod-aws-us-west-2", "prod-aws-ap-southeast-1"
  ],
  "stage3am": [
    "prod-azure-australiaeast", "prod-azure-chinaeast2", "prod-azure-chinanorth2", "prod-azure-eastasiac2", "prod-azure-japaneast", "prod-azure-koreacentral", "prod-azure-southeastasia", "prod-gcp-asia-northeast1", "prod-gcp-asia-southeast1", "prod-gcp-australia-southeast1", "prod-aws-ap-south-1", "prod-aws-ap-northeast-2", "prod-aws-ap-southeast-2", "prod-aws-ap-northeast-1"
  ],
  "stage3": [
    "prod-azure-brazilsouth", "prod-azure-centralusc2", "prod-azure-eastusc3", "prod-azure-eastus2", "prod-azure-eastus2c2", "prod-azure-eastus2c3", "prod-azure-francecentral", "prod-azure-northcentralusc2", "prod-gcp-europe-west3", "prod-gcp-northamerica-northeast1", "prod-gcp-us-east4", "prod-gcp-us-west4", "prod-aws-eu-west-1", "prod-aws-us-east-1", "prod-aws-eu-west-3", "prod-aws-sa-east-1"
  ],
}