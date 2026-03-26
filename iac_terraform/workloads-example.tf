module "internal_app" {
  source             = "./modules/app-workload"
  name               = "internal-app"
  namespace          = "apps"
  base_domain        = var.base_domain
  tls_secret_name    = var.tls_secret_name
  storage_class_name = var.default_storage_class
  image              = "ghcr.io/example/internal-app:1.4.2"
  replicas           = 2
  container_port     = 8080
  storage_request    = "10Gi"
}
