# ==========================================
# services/mock_inventory.py
# GoodBooks Mock Inventory Services
# ==========================================


# ==================================================
# STOCK CHECK
# ==================================================

def stock_check(item_id: str):

    return {
        "status": "success",
        "item_id": item_id,
        "item_name": "HP Laser Printer",
        "available_stock": 42,
        "reserved_stock": 5,
        "uom": "Nos",
        "warehouse": "Main Store"
    }


# ==================================================
# ITEM DETAILS
# ==================================================

def item_details(item_id: str):

    return {
        "status": "success",
        "item_id": item_id,
        "item_name": "HP Laser Printer",
        "category": "Electronics",
        "brand": "HP",
        "reorder_level": 10,
        "current_stock": 42
    }


# ==================================================
# LOW STOCK ITEMS
# ==================================================

def low_stock_items():

    return {
        "status": "success",
        "count": 3,
        "items": [
            {
                "item_id": "ITM-101",
                "item_name": "A4 Paper Bundle",
                "stock": 4
            },
            {
                "item_id": "ITM-202",
                "item_name": "USB Keyboard",
                "stock": 2
            },
            {
                "item_id": "ITM-303",
                "item_name": "Mouse Pad",
                "stock": 1
            }
        ]
    }