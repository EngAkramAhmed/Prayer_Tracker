import matplotlib.pyplot as plt


students = [

    {
        "name": "1. Akram", #1
        "week1_missing": 3,
        "week1_unknown": 0,
        "week2_missing": 1,
        "week2_unknown": 0
    },

    {
        "name": "2. Ali", #2
        "week1_missing": 1,
        "week1_unknown": 0,
        "week2_missing": 3,
        "week2_unknown": 0
    },

    {
        "name": "3. Ahmed Nasr", #3
        "week1_missing": 2,
        "week1_unknown": 3,
        "week2_missing": 5,
        "week2_unknown": 0
    },

    {
        "name": "4. Karim", #4
        "week1_missing": 6,
        "week1_unknown": 1,
        "week2_missing": 6,
        "week2_unknown": 2
    },

    {
        "name": "5. Omar", #5
        "week1_missing": 9,
        "week1_unknown": 1,
        "week2_missing": 7,
        "week2_unknown": 0
    },

    {
        "name": "6. Youssef", #6
        "week1_missing": 3,
        "week1_unknown": 1,
        "week2_missing": 3,
        "week2_unknown": 0
    },

    {
        "name": "7. Sayed", #7
        "week1_missing": 3,
        "week1_unknown": 4,
        "week2_missing": 2,
        "week2_unknown": 4
    },

    {
        "name": "8. Ahmed Mohamed ", #8
        "week1_missing": 1,
        "week1_unknown": 4,
        "week2_missing": 1,
        "week2_unknown": 4
    },

    {
        "name": "9. Saleh", #9
        "week1_missing": 1,
        "week1_unknown": 2,
        "week2_missing": 0,
        "week2_unknown": 0
    },

    {
        "name": "10. Ahmed Hamada", #10
        "week1_missing": 4,
        "week1_unknown": 0,
        "week2_missing": 5,
        "week2_unknown": 0
    },

    {
        "name": "11. Ahmed El-Shahat", #11
        "week1_missing": 2,
        "week1_unknown": 6,
        "week2_missing": 7,
        "week2_unknown": 2
    },

    {
        "name": "12. Mohamed AbuSaree", #12
        "week1_missing": 2,
        "week1_unknown": 2,
        "week2_missing": 10,
        "week2_unknown": 0
    }

    # {
    #     "name": "Sayed", #13
    #     "week1_missing": 5,
    #     "week1_unknown": 0,
    #     "week2_missing": 3,
    #     "week2_unknown": 1
    # },

    # {
    #     "name": "Ahmed Mohamed", #14
    #     "week1_missing": 7,
    #     "week1_unknown": 2,
    #     "week2_missing": 2,
    #     "week2_unknown": 0
    # },

    # {
    #     "name": "Saleh", #15
    #     "week1_missing": 1,
    #     "week1_unknown": 0,
    #     "week2_missing": 4,
    #     "week2_unknown": 0
    # }
]


def percentage(missing_prayers, unknown_days):

    known_days = 7 - unknown_days
    total_prayers = known_days * 5
    prayed = total_prayers - missing_prayers

    return prayed / total_prayers * 100


def makePdf(names, differences, real_diff):

    plt.figure(figsize=(10, 6))

    bars = plt.barh(names, differences)

    for bar, val, real in zip(bars, differences, real_diff):

        if real == 0:
            text = "0.0%"

        else:
            sign = "+" if real > 0 else "-"
            text = f"{sign}{abs(real):.1f}%"

        if real == 0:
            plt.text(
                val + 0.5,
                bar.get_y() + bar.get_height() / 2,
                text,
                ha='left',
                va='center',
                color='black',
                fontweight='bold'
            )
        else:
            plt.text(
                val / 2,
                bar.get_y() + bar.get_height() / 2,
                text,
                ha='center',
                va='center',
                color='white',
                fontweight='bold'
            )

    plt.title("Prayer Improvement Between Two Weeks (3 to 9) vs (10 to 16) in May")

    plt.tight_layout()
    plt.savefig("Prayer_Report.pdf")
    plt.show()


def Data(students):

    names = []
    differences = []
    real_diff = []

    print("_" * 90)

    print(f"{'Name':<22}{'Week 1':<13}{'Week 2':<11}{'Difference':<20}")

    print("_" * 90)

    for student in students:

        week1 = percentage(
            student["week1_missing"],
            student["week1_unknown"])

        week2 = percentage(
            student["week2_missing"],
            student["week2_unknown"])

        difference = week2 - week1

        names.append(student["name"])

        real_diff.append(difference)
        differences.append(abs(difference))

        sign = "+" if difference >= 0 else "-"

        print(
            f"{student['name']:<22}"
            f"{week1:.1f}%{'':<8}"
            f"{week2:.1f}%{'':<8}"
            f"{sign}{abs(difference):.1f}%"
        )

    print("_" * 90)

    # makePdf(names, differences, real_diff)


Data(students)