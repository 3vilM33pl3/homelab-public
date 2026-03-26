variable "kubeconfig_path" {
  description = "Path to the kubeconfig used by OpenTofu."
  type        = string

  validation {
    condition     = length(trimspace(var.kubeconfig_path)) > 0
    error_message = "kubeconfig_path must be set explicitly."
  }
}

variable "default_storage_class" {
  description = "Storage class used by stateful workloads."
  type        = string
  default     = "distributed-storage"

  validation {
    condition     = length(trimspace(var.default_storage_class)) > 0
    error_message = "default_storage_class must not be empty."
  }
}

variable "base_domain" {
  description = "Base domain for internal ingress."
  type        = string
  default     = "lab.example"

  validation {
    condition     = can(regex("^[a-z0-9.-]+\\.[a-z]{2,}$", var.base_domain))
    error_message = "base_domain must look like a valid domain name."
  }
}

variable "tls_secret_name" {
  description = "Name of a TLS secret created outside Terraform."
  type        = string
  default     = "internal-app-tls"

  validation {
    condition     = can(regex("^[a-z0-9]([-a-z0-9]*[a-z0-9])?$", var.tls_secret_name))
    error_message = "tls_secret_name must be a valid Kubernetes object name."
  }
}
