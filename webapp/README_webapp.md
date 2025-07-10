# n8n Invite Web App

This simple application provides an interface for users to authenticate with LDAP and obtain an n8n invite link. It consists of a React frontend and a FastAPI backend.

## Architecture

```
React frontend -> FastAPI backend -> LDAP -> n8n Admin API
```

- **Frontend**: Presents a login form and displays the invite link.
- **Backend**: Authenticates against LDAP and calls the n8n Admin API `/admin/users/invite`.

## Setup

1. Build Docker images:

```bash
docker build -t registry.internal.local/n8n-frontend ./frontend
docker build -t registry.internal.local/n8n-backend ./backend
```

2. Push images to your internal registry.
3. Deploy containers behind TLS termination (e.g. Ingress controller with HTTPS).
4. Configure environment variables for the backend:
   - `LDAP_SERVER`, `LDAP_USER_DN`, `LDAP_SEARCH_BASE`
   - `N8N_URL`, `N8N_BASIC_USER`, `N8N_BASIC_PASS`

## Security Notes

- Always use HTTPS when exposing the frontend and backend.
- Store secrets such as LDAP and n8n credentials in Kubernetes Secrets or a vault system.
- Limit network access from the backend only to LDAP and n8n APIs.

