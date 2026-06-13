# Managed Cloud Pack v4.1.0

В `v4.1.0` появился repo-ready пакет для managed cloud deployment, а не просто
вынесение этой темы за пределы проекта.

## Что входит

- `infra/k8s/namespace.yaml`
- `infra/k8s/configmap.example.yaml`
- `infra/k8s/backend-deployment.yaml`
- `infra/k8s/frontend-deployment.yaml`
- `infra/k8s/services.yaml`
- `infra/k8s/ingress.example.yaml`

## Целевые окружения

- DigitalOcean Kubernetes
- GKE
- EKS

## Практический rollout

1. Соберите и опубликуйте backend/frontend images.
2. Создайте secrets для базы, app secret и provider keys.
3. Примените namespace и config objects.
4. Примените backend/frontend deployments и services.
5. Подключите ingress и TLS.
6. Прогоните `/healthz`, `/readyz` и scanner smoke checks.

## Что это означает

Это реальный managed-cloud deployment pack внутри репозитория.
Это не то же самое, что полностью управляемый SaaS, который оператор проекта
хостит за вас.
