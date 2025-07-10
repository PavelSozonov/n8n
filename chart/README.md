# n8n Helm Chart (Air-Gapped)

This chart wraps the official [n8n Helm chart](https://github.com/8gears/n8n-helm-chart) and adds PostgreSQL and Valkey dependencies. It is designed for air‑gapped Kubernetes clusters and expects all container images to be pulled from an internal registry.

## Architecture

The deployment consists of:

- **n8n main pod** running the web interface and processing short jobs.
- **n8n worker pods** processing queued executions.
- **PostgreSQL** and **Valkey** (Redis) provided by Bitnami sub‑charts.
- All images are pulled from an internal registry preloaded with the required images.

## Usage

1. Preload images (n8n, postgresql, valkey) into your internal registry. Use `helm template` and follow Replicated's [Packaging Air Gap Bundles for Helm Charts](https://help.replicated.com/docs/kots-airgap/packaging-airgap-bundles/).
2. Edit `values-test.yaml` to match your registry URLs and credentials.
3. Install the chart:

```bash
helm install my-n8n ./ -f values-test.yaml
```

## Configuration

Important options in `values-test.yaml`:

- `image.repository` – internal n8n image.
- `n8n.worker.enabled`, `n8n.worker.replicaCount`, `n8n.worker.concurrency` – worker settings.
- `n8n.main.config.executions.mode` – set to `queue` for worker mode.
- `nodes.installation.packages` – community nodes to install (example installs the Confluence node).


