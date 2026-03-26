variable "name" {
  type = string
}

variable "namespace" {
  type = string
}

variable "base_domain" {
  type = string
}

variable "tls_secret_name" {
  type = string
}

variable "storage_class_name" {
  type = string
}

variable "image" {
  type = string
}

variable "replicas" {
  type = number
}

variable "container_port" {
  type = number
}

variable "storage_request" {
  type = string
}
