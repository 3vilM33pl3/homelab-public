variable "kubeconfig_path" {
  description = "Path to the kubeconfig used by OpenTofu."
  type        = string
  default     = "~/.kube/config"
}

variable "default_storage_class" {
  description = "Storage class used by stateful workloads."
  type        = string
  default     = "distributed-storage"
}

variable "base_domain" {
  description = "Base domain for internal ingress."
  type        = string
  default     = "lab.example"
}

variable "tls_secret_name" {
  description = "TLS secret name injected by an external secret process."
  type        = string
  default     = "internal-app-tls"
}
