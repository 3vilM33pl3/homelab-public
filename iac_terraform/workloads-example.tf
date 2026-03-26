locals {
  app_name  = "internal-app"
  namespace = "apps"
}

resource "kubernetes_namespace" "apps" {
  metadata {
    name = local.namespace
    labels = {
      "app.kubernetes.io/managed-by" = "opentofu"
      "lab.example/tier"             = "application"
    }
  }
}

resource "kubernetes_secret" "app_tls" {
  metadata {
    name      = var.tls_secret_name
    namespace = kubernetes_namespace.apps.metadata[0].name
  }

  type = "kubernetes.io/tls"

  data = {
    "tls.crt" = "EXTERNAL_VALUE"
    "tls.key" = "EXTERNAL_VALUE"
  }
}

resource "kubernetes_persistent_volume_claim" "app_data" {
  metadata {
    name      = "${local.app_name}-data"
    namespace = kubernetes_namespace.apps.metadata[0].name
  }

  spec {
    access_modes       = ["ReadWriteOnce"]
    storage_class_name = var.default_storage_class

    resources {
      requests = {
        storage = "10Gi"
      }
    }
  }
}

resource "kubernetes_service" "app" {
  metadata {
    name      = local.app_name
    namespace = kubernetes_namespace.apps.metadata[0].name
  }

  spec {
    selector = {
      "app.kubernetes.io/name" = local.app_name
    }

    port {
      port        = 80
      target_port = 8080
    }
  }
}

resource "kubernetes_ingress_v1" "app" {
  metadata {
    name      = local.app_name
    namespace = kubernetes_namespace.apps.metadata[0].name
    annotations = {
      "nginx.ingress.kubernetes.io/backend-protocol" = "HTTP"
    }
  }

  spec {
    ingress_class_name = "nginx"

    tls {
      secret_name = kubernetes_secret.app_tls.metadata[0].name
      hosts       = ["${local.app_name}.${var.base_domain}"]
    }

    rule {
      host = "${local.app_name}.${var.base_domain}"

      http {
        path {
          path      = "/"
          path_type = "Prefix"

          backend {
            service {
              name = kubernetes_service.app.metadata[0].name

              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}
