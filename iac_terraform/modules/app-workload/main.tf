resource "kubernetes_namespace" "this" {
  metadata {
    name = var.namespace
    labels = {
      "app.kubernetes.io/managed-by" = "opentofu"
      "lab.example/tier"             = "application"
    }
  }
}

resource "kubernetes_persistent_volume_claim" "data" {
  metadata {
    name      = "${var.name}-data"
    namespace = kubernetes_namespace.this.metadata[0].name
  }

  spec {
    access_modes       = ["ReadWriteOnce"]
    storage_class_name = var.storage_class_name

    resources {
      requests = {
        storage = var.storage_request
      }
    }
  }
}

resource "kubernetes_deployment_v1" "this" {
  metadata {
    name      = var.name
    namespace = kubernetes_namespace.this.metadata[0].name
    labels = {
      "app.kubernetes.io/name" = var.name
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        "app.kubernetes.io/name" = var.name
      }
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name" = var.name
        }
      }

      spec {
        security_context {
          run_as_non_root = true
          fs_group        = 10001
        }

        container {
          name  = var.name
          image = var.image

          port {
            container_port = var.container_port
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }

            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
          }

          security_context {
            allow_privilege_escalation = false
            read_only_root_filesystem  = false
            run_as_user                = 10001
            run_as_group               = 10001
          }

          readiness_probe {
            http_get {
              path = "/ready"
              port = var.container_port
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          liveness_probe {
            http_get {
              path = "/healthz"
              port = var.container_port
            }
            initial_delay_seconds = 15
            period_seconds        = 20
          }

          volume_mount {
            name       = "data"
            mount_path = "/var/lib/internal-app"
          }
        }

        volume {
          name = "data"

          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.data.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "this" {
  metadata {
    name      = var.name
    namespace = kubernetes_namespace.this.metadata[0].name
  }

  spec {
    selector = {
      "app.kubernetes.io/name" = var.name
    }

    port {
      port        = 80
      target_port = var.container_port
    }
  }
}

resource "kubernetes_ingress_v1" "this" {
  metadata {
    name      = var.name
    namespace = kubernetes_namespace.this.metadata[0].name
    annotations = {
      "nginx.ingress.kubernetes.io/backend-protocol" = "HTTP"
    }
  }

  spec {
    ingress_class_name = "nginx"

    tls {
      secret_name = var.tls_secret_name
      hosts       = ["${var.name}.${var.base_domain}"]
    }

    rule {
      host = "${var.name}.${var.base_domain}"

      http {
        path {
          path      = "/"
          path_type = "Prefix"

          backend {
            service {
              name = kubernetes_service.this.metadata[0].name

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

resource "kubernetes_pod_disruption_budget_v1" "this" {
  metadata {
    name      = var.name
    namespace = kubernetes_namespace.this.metadata[0].name
  }

  spec {
    min_available = "1"

    selector {
      match_labels = {
        "app.kubernetes.io/name" = var.name
      }
    }
  }
}

resource "kubernetes_network_policy_v1" "this" {
  metadata {
    name      = "${var.name}-default-deny"
    namespace = kubernetes_namespace.this.metadata[0].name
  }

  spec {
    pod_selector {
      match_labels = {
        "app.kubernetes.io/name" = var.name
      }
    }

    ingress {
      from {
        namespace_selector {}
      }

      ports {
        port     = var.container_port
        protocol = "TCP"
      }
    }

    policy_types = ["Ingress", "Egress"]
  }
}
