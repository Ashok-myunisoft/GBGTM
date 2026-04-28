import json
from services.erp_client import post_api
from config.criteria import (
    LEAVE_TYPE_CRITERIA,
    LEAVE_REASON_CRITERIA
)


def _normalize_rows(data):

    if data is None:
        return []

    if isinstance(data, str):
        text = data.strip()

        if not text:
            return []

        try:
            parsed = json.loads(text)
        except Exception:
            return []

        return _normalize_rows(parsed)

    if isinstance(data, list):
        rows = []

        for row in data:
            if isinstance(row, dict):
                rows.append(row)
                continue

            if isinstance(row, str):
                try:
                    parsed = json.loads(row)
                except Exception:
                    continue

                rows.extend(_normalize_rows(parsed))

        return rows

    if isinstance(data, dict):
        for key in (
            "response",
            "Response",
            "body",
            "Body",
            "contents",
            "Contents",
            "rows",
            "Rows",
            "data",
            "Data",
        ):
            value = data.get(key)

            rows = _normalize_rows(value)

            if rows:
                return rows

        if isinstance(data.get("Body"), str):
            body = data["Body"].strip()

            if body:
                try:
                    parsed_body = json.loads(body)
                    rows = _normalize_rows(parsed_body)

                    if rows:
                        return rows
                except Exception:
                    pass

        if all(not isinstance(value, (list, dict)) for value in data.values()):
            return [data]

    return []


def _row_name(row):

    for key in (
        "Name",
        "Description",
        "LeaveTypeName",
        "LeaveType",
        "ReasonName",
    ):
        value = row.get(key)

        if value:
            return str(value).strip().lower()

    return ""


def _row_id(row, *keys):

    candidates = keys or (
        "LeaveTypeId",
        "ReasonId",
        "Id",
        "ID",
    )

    for key in candidates:
        value = row.get(key)

        if value not in (None, ""):
            return value

    return None


def _lookup_alias_ids():

    return {
        "cl": ["casual", "casual leave"],
        "casual": ["casual leave"],
        "sl": ["sick", "sick leave"],
        "sick": ["sick leave"],
        "el": ["earned", "earned leave"],
        "earned": ["earned leave"],
        "pl": ["paid", "paid leave"],
        "paid": ["paid leave"],
        "lwp": ["leave without pay", "loss of pay", "lop"],
        "lop": ["leave without pay", "loss of pay"],
    }


def _normalize_leave_label(value: str):

    text = str(value or "").strip().lower()

    replacements = {
        "leave without pay": "lwp",
        "loss of pay": "lwp",
        "loss pay": "lwp",
        "lop": "lwp",
        "casual leave": "cl",
        "sick leave": "sl",
        "earned leave": "el",
        "paid leave": "pl",
    }

    for source, target in replacements.items():
        text = text.replace(source, target)

    return " ".join(text.split())


def _build_broad_leave_criteria():

    return {
        "SectionCriteriaList": [
            {
                "SectionId": 0,
                "AttributesCriteriaList": [
                    {
                        "FieldName": "Name",
                        "FieldValue": "",
                        "InArray": None,
                        "JoinType": 0,
                        "OperationType": 2
                    }
                ],
                "OperationType": 0
            }
        ]
    }


def _get_leave_rows(login_dto, broad: bool = False):

    url = login_dto["BaseURL"] + "/prs/Leave.svc/SelectList"
    criteria = (
        _build_broad_leave_criteria()
        if broad
        else LEAVE_TYPE_CRITERIA
    )

    return _normalize_rows(post_api(
        url,
        criteria,
        login_dto
    ))


def _match_leave_name(needle: str, row_name: str):

    if not needle:
        return True

    needle = _normalize_leave_label(needle)
    row_name = _normalize_leave_label(row_name)

    if needle in row_name or row_name in needle:
        return True

    tokens = [token for token in needle.split() if token]

    if any(token in row_name for token in tokens):
        return True

    alias_map = _lookup_alias_ids()
    aliases = alias_map.get(needle, [])

    reverse_matches = []

    for key, values in alias_map.items():
        if needle == key or needle in values:
            reverse_matches.append(key)
            reverse_matches.extend(values)

    return any(
        alias in row_name
        or row_name in alias
        for alias in (aliases + reverse_matches)
    )


# ======================================================
# Leave Types
# ======================================================

def get_leave_types(login_dto):
    return _get_leave_rows(login_dto, broad=False)


def get_leave_type_id(login_dto, leave_name: str):
    needle = str(leave_name or "").strip().lower()

    for rows in (
        _get_leave_rows(login_dto, broad=False),
        _get_leave_rows(login_dto, broad=True),
    ):
        for row in rows:
            row_name = _row_name(row)

            if _match_leave_name(needle, row_name):
                value = _row_id(
                    row,
                    "LeaveTypeId",
                    "LeaveType.Id",
                    "Id"
                )

                if value is not None:
                    return value

        for row in rows:
            value = _row_id(
                row,
                "LeaveTypeId",
                "LeaveType.Id",
                "Id"
            )

            if value is not None:
                return value

    raise Exception(
        f"Leave type not found for '{leave_name}'"
    )


# ======================================================
# Reasons
# ======================================================

def get_reasons(login_dto):

    url = login_dto["BaseURL"] + "/ads/Reason.svc/SelectList"

    return post_api(
        url,
        LEAVE_REASON_CRITERIA,
        login_dto
    )


def get_reason_id(login_dto, reason_name: str):

    rows = _normalize_rows(get_reasons(login_dto))

    needle = str(reason_name or "").strip().lower()

    for row in rows:
        row_name = _row_name(row)

        if needle and (
            needle in row_name
            or row_name in needle
            or any(token in row_name for token in needle.split() if token)
        ):
            value = _row_id(row, "ReasonId", "Id")

            if value is not None:
                return value

    # fallback first reason
    if rows:
        value = _row_id(rows[0], "ReasonId", "Id")

        if value is not None:
            return value

    raise Exception(
        f"Reason not found for '{reason_name}'"
    )


# ======================================================
# Employee Shift
# ======================================================

def get_employee_shift(login_dto):

    user_id = login_dto["UserId"]

    url = (
        login_dto["BaseURL"]
        + f"/prs/Employee.svc/?EmployeeId={user_id}"
    )

    from services.erp_client import get_api

    data = get_api(url, login_dto)

    if isinstance(data, list) and len(data) > 0:
        data = data[0]

    return {
        "ShiftId": data.get("ShiftId", "-1499999997"),
        "ShiftDescription": data.get(
            "ShiftDescription",
            "General Shift"
        )
    }
