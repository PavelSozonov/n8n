# n8n Helm Chart (Air-Gapped)

This chart packages the official n8n helm chart for air‑gapped Kubernetes clusters. It expects all container images to be available in an internal registry.

## Architecture

The deployment consists of:

- **n8n main pod** running the web interface and processing short jobs.
- **n8n worker pods** processing queued executions.
- **PostgreSQL** and **Redis** deployed via Bitnami sub‑charts.
- All images are pulled from an internal registry preloaded with the required images.

## Usage

1. Preload images into your internal registry:
   - n8n
   - redis
   - postgresql
   Use `helm template` and follow Replicated's [Packaging Air Gap Bundles for Helm Charts](https://help.replicated.com/docs/kots-airgap/packaging-airgap-bundles/).
2. Edit `values-test.yaml` to match your registry URLs and credentials.
3. Install the chart:

```bash
helm install my-n8n ./ -f values-test.yaml
```

## Configuration

Important options in `values-test.yaml`:

- `image.repository` – internal n8n image.
- `worker.enabled`, `worker.count`, `worker.concurrency` – enable queue workers.
- `config.executions.mode` – set to `queue` for worker mode.
- `nodes.installation.packages` – community nodes to install (example installs the Confluence node).


