from reportlab.lib.pagesizes import letter, landscape        # type: ignore
from reportlab.platypus import (                             # type: ignore
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer)
from reportlab.lib import colors                             # type: ignore
from reportlab.lib.styles import getSampleStyleSheet         # type: ignore
from reportlab.lib.units import inch                         # type: ignore

total_days = 7             # Total days in the period being analyzed (Week)


students = [

    ("01. Akram Ahmed",        [3, 0], [1, 0]),
    ("02. Ali Mohammed",       [1, 0], [3, 0]),
    ("03. Ahmed Nasr",         [2, 3], [5, 0]),
    ("04. Karim Mohammed",     [6, 1], [6, 2]),
    ("05. Omar Anwar",         [9, 1], [7, 0]),
    ("06. Youssef Hussein",    [3, 1], [3, 0]),
    ("07. Sayed Al-Ghannam",   [3, 4], [2, 4]),
    ("08. Ahmed Mohammed",     [1, 4], [1, 4]),
    ("09. Saleh Mahmoud",      [1, 2], [0, 0]),
    ("10. Ahmed Hamada",       [4, 0], [5, 0]),
    ("11. Ahmed El-Shahat",    [2, 6], [7, 2]),
    ("12. Mohammed Abu-Saree", [2, 2], [10, 0])

]


def percentage(missing_prayers, unknown_days):

    known_days    =   total_days  -  unknown_days
    total_prayers =   known_days  * 5 # prayers per day.
    prayed        = total_prayers - missing_prayers

    return (prayed / total_prayers) * 100


def makeDashboardPDF(rows, filename="Report.pdf"):

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
    title = Paragraph(
        f"1st week of May (from 3 to 9) --- VS --- 2nd week of May (from 10 to 16)",
        styles["Title"]
    )

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

        if "+" in diff:
            style.add("TEXTCOLOR", (5, i), (5, i), colors.green)
        elif "-" in diff:
            style.add("TEXTCOLOR", (5, i), (5, i), colors.red)

    table.setStyle(style)

    elements.append(table)

    doc.build(elements)


def Data(students):

    names       = []
    differences = []
    real_diff   = []
    rows        = []

    name_w = max(len(student_name) for student_name, _, _ in students) + 5

    week1_w = len("Week 1") + 10
    week2_w = len("Week 2") + 10
    diff_w  = len("Difference") + 10

    table_width = name_w + week1_w + week2_w + diff_w

    print("-" * table_width)

    print(
        f"{'Name':<{name_w}}"
        f"{'Week 1':<{week1_w}}"
        f"{'Week 2':<{week2_w}}"
        f"{'Difference':<{diff_w}}"
    )

    print("-" * table_width)

    for student_name, period_1, period_2 in students:

        percentage_1 = percentage(period_1[0], period_1[1])
        percentage_2 = percentage(period_2[0], period_2[1])
        difference = (percentage_2 - percentage_1) # improvement_difference

        names.append(student_name)

        real_diff.append(difference)

        differences.append(abs(difference))

        sign = "+" if difference >= 0 else "-"

        rows.append([
            student_name,

            f"{percentage_1:.1f}%",
            period_1[1],

            f"{percentage_2:.1f}%",
            period_2[1],

            f"{sign}{abs(difference):.1f}%"
        ])

        print(
            f"{student_name:<{name_w}}"
            f"{f'{percentage_1:.1f}%':<{week1_w}}"
            f"{f'{percentage_2:.1f}%':<{week2_w}}"
            f"{f'{sign}{abs(difference):.1f}%':<{diff_w}}"
        )

    print("-" * table_width)

    # makePdf(names, differences, real_diff)
    makeDashboardPDF(rows)


Data(students)