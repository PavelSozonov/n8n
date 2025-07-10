from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
import os
import logging
import requests
from ldap3 import Server, Connection, ALL, NTLM

app = FastAPI()

LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://ldap.local")
LDAP_USER_DN = os.getenv("LDAP_USER_DN", "")
LDAP_SEARCH_BASE = os.getenv("LDAP_SEARCH_BASE", "dc=example,dc=com")
N8N_URL = os.getenv("N8N_URL", "https://n8n.local")
N8N_BASIC_USER = os.getenv("N8N_BASIC_USER", "admin")
N8N_BASIC_PASS = os.getenv("N8N_BASIC_PASS", "admin")
VERIFY_SSL = os.getenv("VERIFY_SSL", "true").lower() == "true"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/invite")
async def invite(username: str = Form(...), password: str = Form(...)):
    server = Server(LDAP_SERVER, get_info=ALL)
    try:
        conn = Connection(server, user=f"{LDAP_USER_DN}\\{username}", password=password, authentication=NTLM)
        if not conn.bind():
            logger.warning("LDAP authentication failed for %s", username)
            raise HTTPException(status_code=401, detail="Invalid credentials")
        conn.search(LDAP_SEARCH_BASE, f"(sAMAccountName={username})", attributes=['mail'])
        if not conn.entries:
            raise HTTPException(status_code=404, detail="User not found")
        email = conn.entries[0].mail.value
    except Exception as e:
        logger.exception("LDAP error")
        raise HTTPException(status_code=500, detail="LDAP error") from e
    finally:
        if 'conn' in locals():
            conn.unbind()

    payload = {"email": email, "role": "member"}
    try:
        resp = requests.post(
            f"{N8N_URL}/admin/users/invite",
            json=payload,
            auth=(N8N_BASIC_USER, N8N_BASIC_PASS),
            verify=VERIFY_SSL,
            timeout=10,
        )
        resp.raise_for_status()
    except Exception as e:
        logger.exception("n8n API call failed")
        raise HTTPException(status_code=500, detail="n8n API error") from e

    data = resp.json()
    link = data.get("invitationLink")
    return JSONResponse({"link": link})
