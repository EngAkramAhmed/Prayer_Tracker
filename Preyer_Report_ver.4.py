from reportlab.lib.pagesizes import letter, landscape # type: ignore
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer) # type: ignore
from reportlab.lib import colors                      # type: ignore
from reportlab.lib.styles import getSampleStyleSheet  # type: ignore
from reportlab.lib.units import inch                  # type: ignore

total_days = 7 # Total days in the period being analyzed (Ex. -> Week = 7)
filename = "Report_2.pdf" # Output PDF file name
PDF_title = "2st week of May (from 9 to 15) --- VS --- 3nd week of May (from 16 to 22)"


students = [

  # ("Student Name", [Missing Prayers, Unknown Days] -> for 1st & 2nd periods)

    ("01. Akram Ahmed",          [2, 0], [0, 0]),
    ("02. Ali Mohammed",         [3, 0], [0, 0]),
    ("03. Ahmed Nasr",           [5, 0], [0, 0]),
    ("04. Karim Mohammed",       [8, 1], [0, 0]),
    ("05. Omar Anwar",           [9, 0], [0, 0]),
    ("06. Youssef Hussein",      [4, 0], [0, 0]),
    ("07. Sayed Al-Ghannam",     [3, 3], [0, 0]),
    ("08. Ahmed Mohammed",       [2, 4], [0, 0]),
    ("09. Saleh Mahmoud",        [0, 0], [0, 0]),
    ("10. Ahmed Hamada",         [6, 0], [0, 0]),
    ("11. Ahmed El-Shahat",      [6, 3], [0, 0]),
    ("12. Mohammed Abu-Saree",   [9, 0], [0, 0]),
    ("13. Osama Kamal",          [6, 2], [0, 0]),
    ("14. Ibrahim Kamal",        [4, 2], [0, 0]),
    ("15. AbdelRahman Mohammed", [1, 5], [0, 0])

]


def makeDashboardPDF(rows):

    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(letter),
        rightMargin=25,
        leftMargin=25,
        topMargin=25,
        bottomMargin=25
    )

    elements = []

    styles = getSampleStyleSheet()

    # ===== TITLE =====
    title = Paragraph(PDF_title, styles["Title"])

    elements.append(title)
    elements.append(Spacer(1, 20))

    # ===== TABLE DATA =====
    data = [[
            "Student Name",
            "1st week of May", "Unknown1",
            "2nd week of May", "Unknown2",
            "Difference"
        ]]

    data.extend(rows)

    # ===== TABLE =====
    col_widths = []

    for column in zip(*data):

        longest = max(len(str(cell)) for cell in column)

        width = min(longest * 0.13 * inch, 3.5 * inch)

        col_widths.append(width)

    table = Table(
        data,
        colWidths=col_widths
    )

    # ===== STYLE =====
    style = TableStyle([

        # Header
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E4053")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("ALIGN", (0, 0), (-1, 0), "CENTER"),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),

        # Body
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 12),

        # Alignment
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),

        # Grid
        ("GRID", (0, 0), (-1, -1), 0.7, colors.grey),

        # Padding
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

    ])

    # ===== Alternating Row Colors =====
    for i in range(1, len(data)):

        if i %2 == 0:
            style.add(
                "BACKGROUND",
                (0, i),
                (-1, i),
                colors.HexColor("#F4F6F7")
            )

    # ===== Difference Colors =====
    for i in range(1, len(data)):

        diff = data[i][5]

        if "+" in diff:
            style.add("TEXTCOLOR", (3, i), (3, i), colors.green)
        elif "-" in diff:
            style.add("TEXTCOLOR", (3, i), (3, i), colors.red)
        else:
            style.add("TEXTCOLOR", (3, i), (3, i), colors.blue)

        if "+" in diff:
            style.add("TEXTCOLOR", (5, i), (5, i), colors.green)
        elif "-" in diff:
            style.add("TEXTCOLOR", (5, i), (5, i), colors.red)
        else:
            style.add("TEXTCOLOR", (5, i), (5, i), colors.blue)

    table.setStyle(style)

    elements.append(table)

    doc.build(elements)


def Data(students):

    def percentage(missing_prayers, unknown_days):

        known_days    =   total_days  -  unknown_days
        total_prayers =   known_days  * 5 # prayers per day.
        prayed        = total_prayers - missing_prayers

        return (prayed / total_prayers) * 100

    names       = []
    differences = []
    rows        = []

    for name, period_1, period_2 in students:

        percent_1 = percentage(period_1[0], period_1[1])
        percent_2 = percentage(period_2[0], period_2[1])

        diff = (percent_2 - percent_1) # improvement_difference

        if diff > 0 and period_2[0] == 0:
            diff_text = f"✔ +{diff:.1f}%"
        elif diff > 0:
            diff_text = f"+{diff:.1f}%"
        elif diff < 0:
            diff_text = f"✘ {diff:.1f}%"
        elif period_1[0] == 0 and period_2[0] == 0:
            diff_text = "✔✔"
        else:
            diff_text = "Constant"

        unknown1 = "•" if period_1[1] == 0 else period_1[1]

        unknown2 = "•" if period_2[1] == 0 else period_2[1]

        rows.append([

            name,

            f"{percent_1:.1f}%",
            unknown1,

            f"{percent_2:.1f}%",
            unknown2,

            diff_text
        ])

    makeDashboardPDF(rows)


Data(students)
