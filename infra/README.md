# Infrastructure Notes

`infra/` now contains a practical managed-cloud starter pack in addition to
general deployment notes.

Included in `v4.1.0`:

- `k8s/namespace.yaml`
- `k8s/configmap.example.yaml`
- `k8s/backend-deployment.yaml`
- `k8s/frontend-deployment.yaml`
- `k8s/services.yaml`
- `k8s/ingress.example.yaml`

The primary baseline path is still documented in [`DEPLOYMENT.md`](../DEPLOYMENT.md)
and [`DEPLOYMENT_RU.md`](../DEPLOYMENT_RU.md), while the Kubernetes pack gives
teams a repo-native starting point for DigitalOcean Kubernetes, GKE, and EKS.
