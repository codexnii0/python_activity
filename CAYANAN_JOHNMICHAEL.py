def get_class_standing():
    activities = []
    total_score = 0
    total_items = 0

    num_activities = int(input("\nEnter number of activities: "))

    for i in range(num_activities):
        print(f"\nActivity {i+1}")
        score = float(input("  Enter score: "))
        items = float(input("  Enter total items: "))
        activities.append((f"Activity {i+1}", score, items))
        total_score += score
        total_items += items

    if total_items == 0:
        print("Error: Total items cannot be zero.")
        return [], 0.0, 0.0, 0.0

    percentage = (total_score / total_items) * 100
    class_standing_grade = percentage * 0.40

    return activities, total_score, total_items, class_standing_grade


def get_major_exam():
    exams = []
    total_score = 0
    total_items = 0

    num_exams = int(input("\nEnter number of major exams taken: "))

    for i in range(num_exams):
        print(f"\nExam {i+1}")
        score = float(input("  Enter score: "))
        items = float(input("  Enter total items: "))
        exams.append((f"Exam {i+1}", score, items))
        total_score += score
        total_items += items

    if total_items == 0:
        print("Error: Total items cannot be zero.")
        return [], 0.0, 0.0, 0.0

    percentage = (total_score / total_items) * 100
    exam_grade = percentage * 0.40

    return exams, total_score, total_items, exam_grade


def get_final_project():
    projects = []
    total_score = 0
    total_items = 0

    num_projects = int(input("\nEnter number of final projects made: "))

    for i in range(num_projects):
        print(f"\nProject {i+1}")
        score = float(input("  Enter score: "))
        items = float(input("  Enter total items: "))
        projects.append((f"Project {i+1}", score, items))
        total_score += score
        total_items += items

    if total_items == 0:
        print("Error: Total items cannot be zero.")
        return [], 0.0, 0.0, 0.0

    percentage = (total_score / total_items) * 100
    project_grade = percentage * 0.20

    return projects, total_score, total_items, project_grade


def print_results(title, records, total_score, total_items, weight_label, grade, max_grade):
    header_width = 38
    section_header = f"|{title} : {weight_label}|"
    border = "-" * header_width
    middle_header = "             | Score |     | Items |"

    print(border)
    print(section_header.center(header_width))
    print(border)
    print(middle_header.center(header_width))
    print(border)

    for name, score, items in records:
        print(f"{name:<13} | {score:<5.1f} |     | {items:<5.1f} |")
        print(border)

    print(f"{title} Grade: {grade:.2f} / {max_grade:.2f}")
    print(border)
    print()
    print()
    


def main():
    print("             === Grade Calculator ===")

    # Collect all data without printing
    activities, cs_score, cs_items, cs_grade = get_class_standing()
    exams, me_score, me_items, me_grade = get_major_exam()
    projects, fp_score, fp_items, fp_grade = get_final_project()

    final_grade = cs_grade + me_grade + fp_grade

    print("\n\n    === Final Grade Computation ===")

    print_results("Class Standing", activities, cs_score, cs_items, "40%", cs_grade, 40)
    print_results("Major Exam", exams, me_score, me_items, "40%", me_grade, 40)
    print_results("Final Project", projects, fp_score, fp_items, "20%", fp_grade, 20)

    print(f"\nYour Total Grade is {final_grade:.2f} / 100.00")\

    # Total Grade Conversion
    # 4 = 96 - 100
    # 3.5 = 90 - 95
    # 3 = 84 - 89
    # 2.5 = 78 - 83
    # 2 = 72 - 77
    # 1.5 =  66 - 71
    # 1 = 60 - 65
    # 59 below = R 

    if final_grade >= 96 and final_grade <= 100:
        print("Your Grade is 4.00 and you've passed!")
    elif final_grade >= 90 and final_grade <= 95:
        print("Your Grade is 3.50 and you've passed!")
    elif final_grade >= 84 and final_grade <= 89:
        print("Your Grade is 3.00 and you've passed!")
    elif final_grade >= 78 and final_grade <= 83:
        print("Your Grade is 2.50 and you've passed!")
    elif final_grade >= 72 and final_grade <= 77:
        print("Your Grade is 2.00 and you've passed!")
    elif final_grade >= 66 and final_grade <= 71:
        print("Your Grade is 1.50 and you've passed!")
    elif final_grade >= 60 and final_grade <= 65:
        print("Your Grade is 1.00 and you've passed!")
    else:
        print(f"I'm sorry but your grade is {final_grade} and you have failed this subject.")
        print()
        print("Note: You need a minimum final grade of 60.00 in order to pass.")
    print()
            
if __name__ == "__main__":
    main()
