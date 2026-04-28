def create_purchase_order(args):

    total = (
        args["quantity"] *
        args["unit_price"]
    )

    return {
        "status": "success",
        "po_number": "PO-2026-451",
        "total_value": total,
        "approval_status": "Pending Finance Approval"
    }

