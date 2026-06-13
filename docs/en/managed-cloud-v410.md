# Managed Cloud Pack v4.1.0

`v4.1.0` now includes a repo-ready managed cloud deployment pack instead of
leaving this path fully outside the project.

## Included assets

- `infra/k8s/namespace.yaml`
- `infra/k8s/configmap.example.yaml`
- `infra/k8s/backend-deployment.yaml`
- `infra/k8s/frontend-deployment.yaml`
- `infra/k8s/services.yaml`
- `infra/k8s/ingress.example.yaml`

## Target environments

- DigitalOcean Kubernetes
- GKE
- EKS

## Practical rollout

1. Build and publish backend/frontend images.
2. Create secrets for database, app secret, and provider keys.
3. Apply namespace and config objects.
4. Apply backend/frontend deployments and services.
5. Attach ingress and TLS.
6. Run `/healthz`, `/readyz`, and scanner smoke checks.

## What this means

This is a real managed-cloud deployment pack inside the repo.
It is not the same thing as OpenAI-style hosted SaaS operated by the repo
maintainer.
