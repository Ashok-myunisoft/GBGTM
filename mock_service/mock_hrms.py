def apply_leave(args):

    return {
        "status": "success",
        "leave_id": "LV-1023",
        "message": "Leave applied successfully",
        "approval_status": "Pending Manager Approval",
        "data": args
    }


def leave_balance():

    return {
        "casual_leave": 4,
        "sick_leave": 2,
        "earned_leave": 10
    }


def attendance_summary():

    return {
        "present_days": 22,
        "absent_days": 1,
        "late_marks": 2
    }
