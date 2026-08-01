# simpleapp

Flask sample app.

## Run locally

```bash
poetry install
poetry run simpleapp
# http://0.0.0.0:8080
```

## Build the image

```bash
docker build -t simpleapp:0.2.0 .
docker run --rm -p 8080:8080 simpleapp:0.2.0
```

Load the image into your cluster nodes (or push to a registry and update `k8s/deployment.yaml` to that image).

## Deploy with kubectl

```bash
kubectl apply -f k8s/
kubectl -n simpleapp get deploy,svc,httproute,pods
```

Manifests create namespace `simpleapp`, a Deployment (2 replicas), Service, and HTTPRoute for host `simple.lab.local`.

## Deploy with Argo CD

Point an Argo CD Application at this repository:

- **repo:** `https://github.com/karimakhter/simpleapp.git`
- **revision:** `main`
- **path:** `k8s`
- **destination namespace:** `simpleapp`

Example:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: simpleapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/karimakhter/simpleapp.git
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: simpleapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

```bash
kubectl apply -f application.yaml
```

After changing app code, rebuild/reload the image and restart the Deployment

```bash
docker build -t simpleapp:0.2.0 .
kubectl -n simpleapp rollout restart deploy/simpleapp
```

## API endpoints

| Method | Path | Notes |
|--------|------|--------|
| GET | `/` | Welcome page |
| GET | `/healthz` | Liveness |
| GET | `/readyz` | Readiness |
| GET | `/api/host` | Hostname / OS |
| GET | `/api/info` | App info |
| GET/POST | `/api/echo` | Echo |
| GET | `/api/headers` | Headers |
| GET | `/api/time` | UTC time |
| GET | `/api/env` | Env vars |
| GET | `/api/status/<code>` | Force status |
| GET | `/api/slow?seconds=1` | Delay |
| GET/POST/DELETE | `/api/items[/<id>]` | In-memory CRUD |
