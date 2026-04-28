# ==========================================
# services/biz_transaction_services.py
# Resilient BizTransactionType lookup
# ==========================================

import base64
import gzip
import json

import requests


DEFAULT_FALLBACK_CLASS_IDS = [
    1, 2, 3, 5, 8, 10, 11, 15, 18, 21, 25
]


# ==========================================================
# BUILD CRITERIA
# ==========================================================

def build_criteria(transaction_class_id: int, login_dto: dict):

    return {
        "SectionCriteriaList": [
            {
                "SectionId": 0,
                "AttributesCriteriaList": [
                    {
                        "FieldName": "BIZTransactionTypeClassId",
                        "OperationType": 1,
                        "FieldValue": transaction_class_id,
                        "InArray": None,
                        "JoinType": 2,
                    },
                    {
                        "FieldName": "OrganizationUnit.Id",
                        "OperationType": 1,
                        "FieldValue": login_dto["WorkOUId"],
                        "InArray": None,
                        "JoinType": 2,
                    },
                    {
                        "FieldName": "Period.Id",
                        "OperationType": 1,
                        "FieldValue": login_dto["WorkPeriodId"],
                        "InArray": None,
                        "JoinType": 0,
                    },
                ],
                "OperationType": 0,
            }
        ]
    }


def build_broad_criteria():

    return {
        "SectionCriteriaList": [
            {
                "SectionId": 0,
                "AttributesCriteriaList": [],
                "OperationType": 0,
            }
        ]
    }


# ==========================================================
# DECODE ADS RESPONSE
# ==========================================================

def decode_ads(body64: str):

    raw = base64.b64decode(body64)
    text = gzip.decompress(raw).decode("utf-8")

    return json.loads(text)


def _maybe_json(value):

    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value

    return value


def _extract_rows(data):

    data = _maybe_json(data)

    if isinstance(data, list):
        rows = []

        for item in data:
            item = _maybe_json(item)

            if isinstance(item, dict):
                rows.append(item)

        if rows:
            return rows

    if isinstance(data, dict):

        for key in (
            "contents",
            "Contents",
            "rows",
            "Rows",
            "data",
            "Data",
        ):
            value = data.get(key)

            if isinstance(value, list) and value:
                return [
                    item for item in value
                    if isinstance(item, dict)
                ]

            if isinstance(value, dict):
                nested_rows = _extract_rows(value)

                if nested_rows:
                    return nested_rows

        body = data.get("Body")

        if isinstance(body, str):
            try:
                decoded = decode_ads(body)
                nested_rows = _extract_rows(decoded)

                if nested_rows:
                    return nested_rows
            except Exception:
                pass

        if all(not isinstance(v, (list, dict)) for v in data.values()):
            return [data]

    return []


def _extract_row_id(row):

    for key in (
        "BizTransactionTypeId",
        "BIZTransactionTypeId",
        "Id",
        "ID",
    ):
        if key in row and row[key] not in (None, ""):
            return int(row[key])

    return None


def _row_text(row):

    parts = []

    for key in (
        "Name",
        "Description",
        "Code",
        "TransactionTypeName",
        "BizTransactionTypeName",
    ):
        value = row.get(key)

        if value:
            parts.append(str(value).lower())

    return " ".join(parts)


def _post_select_list(login_dto: dict, payload: dict):

    url = (
        login_dto["BaseURL"]
        + "/ads/BizTransactionType.svc/SelectList"
    )

    headers = {
        "Content-Type": "application/json",
        "Login": json.dumps(login_dto),
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=60,
        )

        response.raise_for_status()

        return _extract_rows(_response_data(response))
    except Exception:
        return []


def _response_data(response):

    try:
        raw = response.content or b""
        text = raw.decode(
            response.encoding or "utf-8",
            errors="ignore"
        ).strip()
    except Exception:
        text = ""

    if not text:
        return None

    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff").strip()

    # Many ERP endpoints return HTML or plain text on errors.
    # In those cases we prefer to treat the response as empty rather than crash.
    if text.startswith("<"):
        return None

    if text[:1] not in ("{", "["):
        return text

    try:
        return json.loads(text)
    except Exception:
        pass

    # Attempt to recover embedded JSON from wrapper text.
    for open_char, close_char in (("{", "}"), ("[", "]")):
        start = text.find(open_char)
        end = text.rfind(close_char)

        if start != -1 and end != -1 and end > start:
            snippet = text[start : end + 1]

            try:
                return json.loads(snippet)
            except Exception:
                continue

    return text


def fetch_single_class_id(
    transaction_class_id: int,
    login_dto: dict
):

    rows = _post_select_list(
        login_dto,
        build_criteria(transaction_class_id, login_dto),
    )

    if rows:
        row_id = _extract_row_id(rows[0])

        if row_id is not None:
            return row_id

    return None


def _find_by_name(rows, transaction_name: str):

    if not transaction_name:
        return None

    needle = transaction_name.strip().lower()

    for row in rows:
        row_text = _row_text(row)

        if needle and needle in row_text:
            row_id = _extract_row_id(row)

            if row_id is not None:
                return row_id

    return None


def _first_row_id(rows):

    for row in rows:
        row_id = _extract_row_id(row)

        if row_id is not None:
            return row_id

    return None


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def get_biz_transaction_type_id(
    transaction_class_id: int,
    login_dto: dict,
    transaction_name: str | None = None,
):

    # Allow explicit overrides from login context if the tenant has a known ID.
    for key in (
        "BizTransactionTypeId",
        "LeaveBizTransactionTypeId",
        "PermissionBizTransactionTypeId",
        "TransactionTypeId",
    ):
        value = login_dto.get(key)

        if value not in (None, ""):
            try:
                return int(value)
            except Exception:
                pass

    # ----------------------------------------------
    # Build a ranked list of search terms
    # ----------------------------------------------

    search_terms = []

    if transaction_name:
        search_terms.append(transaction_name)

    if transaction_class_id == 1:
        search_terms.extend(["leave", "leave application", "tleave"])
    elif transaction_class_id == 8:
        search_terms.extend(["permission", "timeslip", "time slip"])

    seen_terms = set()
    ranked_terms = []

    for term in search_terms:
        normalized = str(term).strip().lower()

        if normalized and normalized not in seen_terms:
            seen_terms.add(normalized)
            ranked_terms.append(normalized)

    # ----------------------------------------------
    # First Try Given Class ID
    # ----------------------------------------------

    result = None

    try:
        result = fetch_single_class_id(
            transaction_class_id,
            login_dto,
        )
    except Exception:
        result = None

    if result:
        return result

    # ----------------------------------------------
    # Try Common Class IDs
    # ----------------------------------------------

    for class_id in DEFAULT_FALLBACK_CLASS_IDS:

        if class_id == transaction_class_id:
            continue

        try:
            result = fetch_single_class_id(
                class_id,
                login_dto,
            )

            if result:
                return result
        except Exception:
            pass

    # ----------------------------------------------
    # Final Fallback: search all rows by name
    # ----------------------------------------------

    try:
        rows = _post_select_list(
            login_dto,
            build_broad_criteria(),
        )
    except Exception:
        rows = []

    for term in ranked_terms:
        result = _find_by_name(rows, term)

        if result:
            return result

    # ----------------------------------------------
    # Last resort: any row id
    # ----------------------------------------------

    result = _first_row_id(rows)

    if result is not None:
        return result

    raise Exception(
        f"BizTransactionTypeId not found for class id "
        f"{transaction_class_id}"
    )
