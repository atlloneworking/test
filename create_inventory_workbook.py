from datetime import date
from xml.sax.saxutils import escape

OUTPUT_FILE = "inventory_tracking_template.xml"

CATEGORIES = "Consumables,Electrical,Hardware,PPE,Tools,Vehicle,Other"


def cell(value, cell_type="String"):
    if value is None:
        return "<Cell/>"
    return f"<Cell><Data ss:Type=\"{cell_type}\">{escape(str(value))}</Data></Cell>"


def formula_cell(formula):
    return f"<Cell ss:Formula=\"{formula}\"><Data ss:Type=\"Number\">0</Data></Cell>"


def row(cells):
    return f"<Row>{''.join(cells)}</Row>"


def worksheet(name, rows):
    return f"<Worksheet ss:Name=\"{escape(name)}\"><Table>{''.join(rows)}</Table></Worksheet>"


def build_inventory_sheet():
    headers = [
        "Item ID", "Item Name", "Category", "Unit Cost", "Opening Qty", "Stock In", "Stock Out",
        "Closing Qty", "Closing Value", "Equipment?", "Location", "Last Updated", "Notes"
    ]
    rows = [row([cell(h) for h in headers])]

    for r in range(2, 302):
        rows.append(row([
            cell(None), cell(None), cell(None), cell(None), cell(None), cell(None), cell(None),
            formula_cell("=RC[-3]+RC[-2]-RC[-1]"),
            formula_cell("=RC[-1]*RC[-5]"),
            cell(None), cell(None), cell(None), cell(None),
        ]))
    return worksheet("A_Inventory_Tracking", rows)


def build_equipment_sheet():
    headers = [
        "Equipment ID", "Equipment Name", "Category", "Purchase Cost", "Purchase Date", "Condition",
        "Assigned To", "Current Location", "Status", "Last Service Date", "Next Service Due", "Notes"
    ]
    rows = [row([cell(h) for h in headers])]
    for _ in range(2, 302):
        rows.append(row([cell(None) for _ in headers]))
    return worksheet("B_Equipment_Tracking", rows)


def build_allocated_sheet():
    headers = [
        "Allocation ID", "Date Allocated", "Van/Team", "Item ID", "Item Name", "Category",
        "Qty Allocated", "Unit Cost", "Allocated Value", "Status", "Expected Return/Use Date", "Notes"
    ]
    rows = [row([cell(h) for h in headers])]
    for _ in range(2, 302):
        rows.append(row([
            cell(None), cell(None), cell(None), cell(None), cell(None), cell(None),
            cell(None), cell(None), formula_cell("=RC[-2]*RC[-1]"), cell(None), cell(None), cell(None)
        ]))
    return worksheet("C_Allocated_Tracking", rows)


def build_monthly_sheet():
    headers = [
        "Month", "Category", "Start Value", "Stock In Value", "Stock Out Value", "End Value",
        "Used Value (Calc)", "Variance Notes"
    ]
    rows = [row([cell(h) for h in headers])]
    rows.append(row([
        cell(date.today().strftime("%Y-%m")), cell(None), cell(None), cell(None), cell(None), cell(None),
        formula_cell("=RC[-4]+RC[-3]-RC[-1]"), cell(None)
    ]))
    for _ in range(3, 302):
        rows.append(row([
            cell(None), cell(None), cell(None), cell(None), cell(None), cell(None),
            formula_cell("=RC[-4]+RC[-3]-RC[-1]"), cell(None)
        ]))
    return worksheet("D_Monthly_Figures", rows)


def build_readme_sheet():
    lines = [
        "How to use this workbook",
        "1) A_Inventory_Tracking: main stock list with costs and quantity movement.",
        "2) B_Equipment_Tracking: equipment register (items marked as equipment).",
        "3) C_Allocated_Tracking: items placed in vans/teams but not yet used.",
        "4) D_Monthly_Figures: monthly value summary for start/end, stock in/out, and used value.",
        f"Suggested categories: {CATEGORIES}",
        "Tip: In Excel/Sheets, add dropdown validation for Category/Status columns using your preferred list.",
    ]
    rows = [row([cell(text)]) for text in lines]
    return worksheet("README", rows)


def build_workbook_xml():
    worksheets = [
        build_inventory_sheet(),
        build_equipment_sheet(),
        build_allocated_sheet(),
        build_monthly_sheet(),
        build_readme_sheet(),
    ]
    return f'''<?xml version="1.0"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:html="http://www.w3.org/TR/REC-html40">
{''.join(worksheets)}
</Workbook>
'''


def main():
    xml = build_workbook_xml()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Created {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
