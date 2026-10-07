#!/usr/bin/env python3
"""
==============================================================
  GRADEX  |  Student Grade Calculator using Python
  Internship Project - JECRC Foundation
==============================================================
  Pipeline:  Input (Marks) -> Calculation -> Grade -> Result

  Concepts demonstrated:
    * input / output          * functions
    * loops                   * conditions (if / elif / else)
    * lists & dictionaries    * exception handling (try / except)
    * file handling (CSV)     * modular, readable code

  Runs on any machine with Python 3.8+  (no external libraries)
==============================================================
"""

import csv
import os
import sys
import time
from datetime import datetime

# --------------------------------------------------------------
#  CONFIGURATION
# --------------------------------------------------------------
SUBJECTS = ["Python Programming", "Mathematics", "English", "Physics", "Computer Science"]
MAX_MARKS = 100          # maximum marks per subject
PASS_MARKS = 40          # minimum marks needed in EACH subject
WIDTH = 62               # width of the result card

records = []             # every student evaluated in this session


# --------------------------------------------------------------
#  TERMINAL STYLING
# --------------------------------------------------------------
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


if os.name == "nt":      # enables ANSI colours on Windows terminals
    os.system("")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def typewriter(text, delay=0.012, color=C.WHITE):
    """Prints text one character at a time for a cinematic feel."""
    for ch in text:
        sys.stdout.write(f"{color}{ch}{C.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loading(message, steps=24, delay=0.03):
    """Animated progress bar."""
    for i in range(steps + 1):
        filled = "█" * i
        empty = "░" * (steps - i)
        pct = int(i / steps * 100)
        sys.stdout.write(f"\r  {C.CYAN}{message} {C.BLUE}[{filled}{empty}] {C.WHITE}{pct:3d}%{C.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def banner():
    clear()
    art = r"""
   ██████╗ ██████╗  █████╗ ██████╗ ███████╗██╗  ██╗
  ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝
  ██║  ███╗██████╔╝███████║██║  ██║█████╗   ╚███╔╝
  ██║   ██║██╔══██╗██╔══██║██║  ██║██╔══╝   ██╔██╗
  ╚██████╔╝██║  ██║██║  ██║██████╔╝███████╗██╔╝ ██╗
   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
"""
    colors = [C.CYAN, C.CYAN, C.BLUE, C.BLUE, C.MAGENTA, C.MAGENTA]
    for line, col in zip(art.strip("\n").split("\n"), colors):
        print(f"{C.BOLD}{col}{line}{C.RESET}")
    print(f"\n  {C.BOLD}{C.WHITE}STUDENT GRADE CALCULATOR{C.RESET}  {C.DIM}|  Built with Python{C.RESET}")
    print(f"  {C.DIM}JECRC Foundation  •  Internship Project{C.RESET}")
    print(f"  {C.BLUE}{'━' * (WIDTH - 2)}{C.RESET}")
    flow = ["Input", "Calculation", "Grade", "Result"]
    print("  " + f" {C.YELLOW}➜{C.RESET} ".join(f"{C.BOLD}{C.CYAN}{s}{C.RESET}" for s in flow))
    print(f"  {C.BLUE}{'━' * (WIDTH - 2)}{C.RESET}\n")


# --------------------------------------------------------------
#  STEP 1 : INPUT  (accept student marks)
# --------------------------------------------------------------
def ask_text(prompt, upper=False):
    while True:
        value = input(f"  {C.CYAN}{prompt}{C.RESET} ").strip()
        if value:
            return value.upper() if upper else value.title()
        print(f"  {C.RED}✖ This field cannot be empty.{C.RESET}")


def ask_marks(subject):
    """Keeps asking until a valid number between 0 and MAX_MARKS is entered."""
    while True:
        try:
            marks = float(input(f"  {C.YELLOW}▸{C.RESET} {subject:<20} (0-{MAX_MARKS}): "))
            if 0 <= marks <= MAX_MARKS:
                return marks
            print(f"    {C.RED}✖ Marks must be between 0 and {MAX_MARKS}.{C.RESET}")
        except ValueError:
            print(f"    {C.RED}✖ Please enter a valid number.{C.RESET}")


def accept_student_marks():
    print(f"  {C.BOLD}{C.MAGENTA}STEP 1  ➜  ENTER STUDENT DETAILS{C.RESET}\n")
    name = ask_text("Student Name :")
    roll = ask_text("Roll Number  :", upper=True)
    print(f"\n  {C.DIM}Enter marks out of {MAX_MARKS} for each subject{C.RESET}\n")
    marks = {subject: ask_marks(subject) for subject in SUBJECTS}
    return name, roll, marks


# --------------------------------------------------------------
#  STEP 2 : CALCULATION  (total / percentage)
# --------------------------------------------------------------
def calculate(marks):
    total = sum(marks.values())
    maximum = MAX_MARKS * len(marks)
    percentage = total / maximum * 100
    return total, maximum, percentage


# --------------------------------------------------------------
#  STEP 3 : GRADE  (determine grade using conditions)
# --------------------------------------------------------------
def determine_grade(percentage):
    if percentage >= 90:
        return "A+", "Outstanding", C.GREEN
    elif percentage >= 80:
        return "A", "Excellent", C.GREEN
    elif percentage >= 70:
        return "B", "Very Good", C.CYAN
    elif percentage >= 60:
        return "C", "Good", C.CYAN
    elif percentage >= 50:
        return "D", "Satisfactory", C.YELLOW
    elif percentage >= PASS_MARKS:
        return "E", "Needs Improvement", C.YELLOW
    else:
        return "F", "Fail", C.RED


def check_pass(marks):
    """A student passes only if every subject meets the pass mark."""
    failed = [s for s, m in marks.items() if m < PASS_MARKS]
    return len(failed) == 0, failed


# --------------------------------------------------------------
#  STEP 4 : RESULT  (display final result)
# --------------------------------------------------------------
def bar(value, width=20):
    filled = round(value / MAX_MARKS * width)
    color = C.GREEN if value >= 75 else C.YELLOW if value >= PASS_MARKS else C.RED
    return f"{color}{'█' * filled}{C.DIM}{'░' * (width - filled)}{C.RESET}"


def row(plain, colored=None):
    """Prints one line of the result card with correct padding."""
    colored = colored if colored is not None else plain
    pad = WIDTH - 4 - len(plain)
    print(f"  {C.BLUE}┃{C.RESET} {colored}{' ' * max(pad, 0)} {C.BLUE}┃{C.RESET}")


def display_result(name, roll, marks, total, maximum, percentage, grade, remark, gcolor, passed, failed):
    print(f"\n  {C.BOLD}{C.MAGENTA}STEP 4  ➜  FINAL RESULT{C.RESET}\n")
    print(f"  {C.BLUE}┏{'━' * (WIDTH - 2)}┓{C.RESET}")
    title = "REPORT CARD"
    row(title.center(WIDTH - 4), f"{C.BOLD}{C.WHITE}{title.center(WIDTH - 4)}{C.RESET}")
    print(f"  {C.BLUE}┣{'━' * (WIDTH - 2)}┫{C.RESET}")
    row(f"Name  : {name}", f"{C.DIM}Name  :{C.RESET} {C.BOLD}{name}{C.RESET}")
    row(f"Roll  : {roll}", f"{C.DIM}Roll  :{C.RESET} {C.BOLD}{roll}{C.RESET}")
    row(f"Date  : {datetime.now():%d %b %Y, %I:%M %p}",
        f"{C.DIM}Date  :{C.RESET} {datetime.now():%d %b %Y, %I:%M %p}")
    print(f"  {C.BLUE}┣{'━' * (WIDTH - 2)}┫{C.RESET}")

    for subject, m in marks.items():
        plain = f"{subject:<20} {m:6.1f}/{MAX_MARKS}  " + "#" * 20
        colored = f"{subject:<20} {m:6.1f}/{MAX_MARKS}  {bar(m)}"
        row(plain, colored)

    print(f"  {C.BLUE}┣{'━' * (WIDTH - 2)}┫{C.RESET}")
    row(f"Total      : {total:.1f} / {maximum}",
        f"{C.DIM}Total      :{C.RESET} {C.BOLD}{total:.1f} / {maximum}{C.RESET}")
    row(f"Percentage : {percentage:.2f}%",
        f"{C.DIM}Percentage :{C.RESET} {C.BOLD}{percentage:.2f}%{C.RESET}")
    row(f"Grade      : {grade}  ({remark})",
        f"{C.DIM}Grade      :{C.RESET} {C.BOLD}{gcolor}{grade}{C.RESET}  {gcolor}({remark}){C.RESET}")
    status = "PASS" if passed else "FAIL"
    icon = "✔" if passed else "✖"
    scolor = C.GREEN if passed else C.RED
    row(f"Status     : {icon} {status}",
        f"{C.DIM}Status     :{C.RESET} {C.BOLD}{scolor}{icon} {status}{C.RESET}")
    if failed:
        row(f"Re-attempt : {', '.join(failed)}"[:WIDTH - 4],
            f"{C.DIM}Re-attempt :{C.RESET} {C.RED}{', '.join(failed)}{C.RESET}"[:WIDTH + 20])
    print(f"  {C.BLUE}┗{'━' * (WIDTH - 2)}┛{C.RESET}")

    if passed and percentage >= 90:
        typewriter("\n  🏆  Brilliant performance! Top of the class material.", color=C.GREEN)
    elif passed:
        typewriter("\n  🎉  Congratulations! Keep up the great work.", color=C.GREEN)
    else:
        typewriter("\n  💪  Don't give up. Every expert was once a beginner.", color=C.YELLOW)


# --------------------------------------------------------------
#  EXTRA FEATURES : leaderboard + CSV export
# --------------------------------------------------------------
def show_leaderboard():
    banner()
    print(f"  {C.BOLD}{C.MAGENTA}🏆  SESSION LEADERBOARD{C.RESET}\n")
    if not records:
        print(f"  {C.YELLOW}No students evaluated yet. Choose option 1 first.{C.RESET}")
        return
    ranked = sorted(records, key=lambda r: r["percentage"], reverse=True)
    print(f"  {C.BOLD}{'Rank':<6}{'Name':<20}{'Roll':<12}{'%':>8}  Grade{C.RESET}")
    print(f"  {C.BLUE}{'─' * 56}{C.RESET}")
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for i, r in enumerate(ranked, start=1):
        medal = medals.get(i, f"{i:>2}")
        print(f"  {medal:<5} {r['name']:<20}{r['roll']:<12}{r['percentage']:>7.2f}%  "
              f"{r['gcolor']}{C.BOLD}{r['grade']}{C.RESET}")


def export_csv():
    if not records:
        print(f"\n  {C.YELLOW}Nothing to export yet. Evaluate a student first.{C.RESET}")
        return
    filename = f"grade_report_{datetime.now():%Y%m%d_%H%M%S}.csv"
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Roll"] + SUBJECTS + ["Total", "Percentage", "Grade", "Status"])
            for r in records:
                writer.writerow([r["name"], r["roll"]] + list(r["marks"].values()) +
                                [r["total"], f"{r['percentage']:.2f}", r["grade"], r["status"]])
        loading("Saving report", steps=18)
        print(f"\n  {C.GREEN}✔ Report saved as {C.BOLD}{filename}{C.RESET}")
    except OSError as err:
        print(f"\n  {C.RED}✖ Could not save file: {err}{C.RESET}")


# --------------------------------------------------------------
#  MAIN FLOW
# --------------------------------------------------------------
def evaluate_student():
    banner()
    name, roll, marks = accept_student_marks()

    print()
    loading("Calculating total & percentage")
    total, maximum, percentage = calculate(marks)

    loading("Determining grade            ")
    grade, remark, gcolor = determine_grade(percentage)
    passed, failed = check_pass(marks)
    if not passed and grade != "F":
        grade, remark, gcolor = "F", "Fail (below pass marks in a subject)", C.RED

    display_result(name, roll, marks, total, maximum, percentage,
                   grade, remark, gcolor, passed, failed)

    records.append({
        "name": name, "roll": roll, "marks": marks, "total": total,
        "percentage": percentage, "grade": grade, "gcolor": gcolor,
        "status": "PASS" if passed else "FAIL",
    })


def menu():
    print(f"\n  {C.BLUE}{'━' * (WIDTH - 2)}{C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}MAIN MENU{C.RESET}")
    print(f"   {C.CYAN}[1]{C.RESET} Evaluate a student")
    print(f"   {C.CYAN}[2]{C.RESET} View leaderboard")
    print(f"   {C.CYAN}[3]{C.RESET} Export report to CSV")
    print(f"   {C.CYAN}[4]{C.RESET} Exit")
    return input(f"\n  {C.YELLOW}Choose an option ➜ {C.RESET}").strip()


def main():
    banner()
    typewriter("  Welcome to GRADEX - where marks become meaning.", color=C.CYAN)
    time.sleep(0.4)

    while True:
        choice = menu()
        if choice == "1":
            evaluate_student()
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            export_csv()
        elif choice == "4":
            print()
            typewriter("  Thank you for using GRADEX. Keep learning, keep building. 🚀", color=C.MAGENTA)
            break
        else:
            print(f"\n  {C.RED}✖ Invalid choice. Please select 1-4.{C.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.YELLOW}Session ended. Goodbye!{C.RESET}")
