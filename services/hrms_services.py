
from services.erp_client import post_api
from utils.wfc import to_wcf_date
from utils.time_utils import hhmm_to_minutes

from services.biz_transaction_services import (
    get_biz_transaction_type_id
)

from services.masterdata_service import (
    get_leave_type_id,
    get_reason_id,
    get_employee_shift
)


# ==========================================================
# LEAVE BALANCE
# ==========================================================

def leave_balance(login_dto):

    url = (
        login_dto["BaseURL"]
        + "/prs/Leave.svc/LeaveStatusReport/?FirstNumber=-1&MaxResult=-1"
    )

    payload = {
        "SectionCriteriaList": [
            {
                "SectionId": 0,
                "AttributesCriteriaList": [
                    {
                        "FieldName": "EmployeeId",
                        "FieldValue": 0,
                        "InArray": None,
                        "JoinType": 2,
                        "OperationType": 1
                    }
                ],
                "OperationType": 0
            }
        ]
    }

    return post_api(url, payload, login_dto)


# ==========================================================
# APPLY LEAVE
# User sends only:
# leave_type, leave_date, reason
# ==========================================================

def apply_leave(
    login_dto,
    leave_type,
    leave_date,
    reason
):
    try:

        # --------------------------------------
        # Dynamic Lookup Values
        # --------------------------------------

        biz_id = get_biz_transaction_type_id(
            transaction_class_id=1,
            login_dto=login_dto,
            transaction_name="leave"
        )

        leave_type_id = get_leave_type_id(
            login_dto,
            leave_type
        )

        reason_id = get_reason_id(
            login_dto,
            reason
        )

        # --------------------------------------
        # URL
        # --------------------------------------

        url = login_dto["BaseURL"] + "/prs/TLeave.svc/"

        wcf = to_wcf_date(leave_date)

        # --------------------------------------
        # Payload
        # --------------------------------------

        payload = {
            "BizTransactionTypeId": str(biz_id),
            "EmployeeName": login_dto["UserName"],
            "GuId": "",
            "OUId": login_dto["WorkOUId"],
            "PeriodId": login_dto["WorkPeriodId"],
            "ReasonId": str(reason_id),
            "TAvailabeLeave": 0,
            "TLeaveDayType": "FullDay",

            "TLeaveDetailArray": [
                {
                    "DayType": "0",
                    "EmployeeId": login_dto["UserId"],
                    "EmployeeName": login_dto["UserName"],
                    "LeaveDayName": "",
                    "LeaveTypeId": leave_type_id,
                    "TLeaveDetailLeaveDate": wcf,
                    "TLeaveDetailLeaveDayType": "0",
                    "TLeaveDetailNumberOfDays": "1",
                    "TLeaveDetailSlNo": 1,
                    "TLeaveDetailValidTill": wcf
                }
            ],

            "TLeaveId": 0,
            "TLeaveLeaveDate": wcf,
            "TLeaveLeaveNumber": "",
            "TLeaveNumberOfDays": "1",
            "TLeaveReferenceDate": wcf,
            "TLeaveReferenceNumber": "0",
            "TLeaveRemarks": reason,
            "TLeaveStatus": 1,
            "TLeaveType": leave_type,
            "TLeaveVersion": 1
        }

        return post_api(url, payload, login_dto)

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ==========================================================
# APPLY PERMISSION
# User sends only:
# date, from_time, to_time, reason
# ==========================================================

def apply_permission(
    login_dto,
    shift_id=None,
    shift_name=None,
    department_name=None,
    designation_name=None,
    date=None,
    from_time=None,
    to_time=None,
    reason=None
):

    # --------------------------------------
    # Dynamic Lookup Values
    # --------------------------------------

    biz_id = get_biz_transaction_type_id(
        transaction_class_id=8,
        login_dto=login_dto,
        transaction_name="permission"
    )

    reason_id = get_reason_id(
        login_dto,
        reason
    )

    if shift_id is None or shift_name is None:
        shift = get_employee_shift(login_dto)

        if shift_id is None:
            shift_id = shift["ShiftId"]

        if shift_name is None:
            shift_name = shift["ShiftDescription"]

    # Optional fallback values
    if department_name is None:
        department_name = login_dto.get(
            "DepartmentName",
            ""
        )

    if designation_name is None:
        designation_name = login_dto.get(
            "DesignationName",
            ""
        )

    # --------------------------------------
    # Time Convert
    # --------------------------------------

    start = hhmm_to_minutes(from_time)
    end = hhmm_to_minutes(to_time)
    duration = end - start

    duration_text = (
        f"{duration // 60:02d}:{duration % 60:02d}"
    )

    wcf = to_wcf_date(date)

    # --------------------------------------
    # URL
    # --------------------------------------

    url = login_dto["BaseURL"] + "/prs/TimeSlip.svc/"

    # --------------------------------------
    # Payload
    # --------------------------------------

    payload = {
        "TimeSlipId": 0,
        "BizTransactionTypeId": str(biz_id),
        "OrganizationUnitId": login_dto["WorkOUId"],
        "PeriodId": login_dto["WorkPeriodId"],
        "TimeSlipNumber": 0,
        "TimeSlipDate": wcf,

        "EmployeeId": login_dto["UserId"],
        "EmployeeName": login_dto["UserName"],
        "EmployeeCode": login_dto["UserCode"],

        "ShiftId": shift_id,
        "ShiftDescription": shift_name,

        "TimeSlipAttendanceDate": wcf,
        "TimeSlipType": "1",
        "TimeSlipDuration": duration,
        "TimeSlipTimeSlipStartTime": start,
        "TimeSlipTimeSlipEndTime": end,

        "DepartmentName": department_name,
        "DesignationName": designation_name,

        "TimeSlipFromTimeMailTemplate": from_time,
        "TimeSlipToTimeMailTemplate": to_time,
        "TimeSlipToDurtionMailTemplate": duration_text,

        "ApprovedById": -1,
        "TimeSlipReason": reason,
        "TimeSlipOnDutyLocation": "",

        "FromTimeForPrint": from_time,
        "ToTimeForPrint": to_time,

        "TimeSlipStatus": 1,
        "TimeSlipPermissionHoursMailTemplate": "0:00",
        "TimeSlipVersion": 1,

        "PermissionReasonId": str(reason_id)
    }

    return post_api(url, payload, login_dto)
