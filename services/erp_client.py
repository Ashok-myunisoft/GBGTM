# ==========================================
# services/erp_client.py
# FULL FIXED VERSION
# ==========================================

import requests
import json


# ==================================================
# POST API
# ==================================================

def post_api(url: str, payload: dict, login_dto: dict):

    headers = {
        "Content-Type": "application/json",
        "Login": json.dumps(login_dto)
    }

    response = requests.post(
        url=url,
        json=payload,
        headers=headers,
        timeout=60
    )

    response.raise_for_status()

    try:
        return response.json()

    except Exception:
        return {
            "status": "success",
            "response": response.text
        }


# ==================================================
# GET API
# ==================================================

def get_api(url: str, login_dto: dict):

    headers = {
        "Content-Type": "application/json",
        "Login": json.dumps(login_dto)
    }

    response = requests.get(
        url=url,
        headers=headers,
        timeout=60
    )

    response.raise_for_status()

    try:
        return response.json()

    except Exception:
        return {
            "status": "success",
            "response": response.text
        }