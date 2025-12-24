#Copy of code from original

import random
import json
import sys
import re
from datetime import date, timedelta
from pyfiglet import Figlet

class Pokemon:
    STARTERS = {
        "1":["Igglypuff","Jigglypuff","Wigglytuff"],
        "2":["Gastly", "Haunter", "Gengar"],
        "3":["Dratini", "Dragonair", "Dragonite"],
        "4":["Chikorita", "Bayleef", "Meganium"],
        "5":["Togepi", "Togetic", "Togekiss"],
    }

    @classmethod
    def starter_selection(cls, name):
        starter = random.choice(list(cls.STARTERS.values()))
        print(f"Hello, {name}! Your starter is...✨✨✨", starter[0])
        return starter

def main():
    figlet = Figlet()
    figlet.setFont(font="drpepper")
    print (figlet.renderText("Welcome to\nPokeTracker"), "Gotta' catch all your dollars ヾ(≧ ▽ ≦)ゝ")

    state = load_state() #function that loads the game play if old user, new user state returns none
    if state == None: #if state is None
        print("Welcome to PokeTracker. This app is made to help you manage your finances and meet your financial goals alongside a pokemon friend this year!")
        print("This app applies your yearly income to the 50/30/20 rule to help you save money to defeat gyms(reach milestones).")
        print("Continue fighting gyms to grow your Pokemon and evolve them\n")

        name = input("What is your name trainor: ")

        while True:
            try:
                yearly_income = input("Enter your yearly income: ").strip()
                if re.fullmatch(r"\d*(?:\.\d\d)?", yearly_income):
                    yearly_income = float(yearly_income)
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Yearly income has to be digits with no commas or characters")

        while True:
            try:
                whataremilestones = input("Enter 3 or more of your major finacial milestones(seperated by ,): ").strip()
                if re.fullmatch(r"(\d*,){2,}(\d+)", whataremilestones):
                    whataremilestones = whataremilestones.split(",")
                    milestones = [float(x) for x in whataremilestones]
                    milestones.sort()
                    x = 1
                    while (x) < len(milestones):
                        milestones[x] = milestones[x-1] + milestones[x]
                        x += 1
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Milestones has in be in format of x,x,x..., where x are digits")

        expenses = {"needs": 0.0, "wants": 0.0, "savings": 0.0}
        total_saved = 0.0
        streak = 0
        last_saved_date = None
        pokemon = Pokemon.starter_selection(name)

        state = {
            "yearly_income": yearly_income,
            "milestones": milestones,
            "expenses": expenses,
            "total_saved": total_saved,
            "streak": streak,
            "last_saved_date": last_saved_date,
            "pokemon": pokemon
        }

    else: #if state is defined with something
        print("...Loaded your previous progress...")

    while True:
        print(figlet.renderText("Menu:"))
        print("1. Log Expenses")
        print("2. Log Savings")
        print("3. View 50/30/20 Targets Summary")
        print("4. View Pokemon Progress")
        print("5. Change Income")
        print("6. Quit")
        choice = input("Input choice: ").strip()

        if choice == "1":
            while True:
                try:
                    c = input("Category (needs/wants): ").strip().lower()
                    if c == "needs" or c == "wants":
                        amount = float(input("Amount: "))
                        state["expenses"][c]+= amount
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Category is not valid, type 'needs' or 'wants'")

        elif choice == "2":
            progress_before = update_progress(state["total_saved"], state["milestones"])
            stage_name_before = state["pokemon"][progress_before["stage"] - 1]

            amount = float(input("Savings Deposit: "))
            state["expenses"]["savings"] += amount
            state["total_saved"] += amount

            progress_after = update_progress(state["total_saved"], state["milestones"])
            stage_name_after = state["pokemon"][progress_after["stage"] - 1]

            if progress_before["stage"] == progress_after["stage"]:
                pass
            else:
                print(f"Congrats! Your pokemon has evolved from {stage_name_before} to {stage_name_after}.")


        elif choice == "3":
            results = compute_target(state["expenses"], state["yearly_income"])
            print("Targets:", results["targets"])
            print("Remaining against Target:", results["deltas"])

            gyms = gyms_milestones(state["total_saved"], state["milestones"])
            print(f"You have beaten {gyms} gym(s) out of {len(state["milestones"])} by saving ${state["total_saved"]:.2f}!")

        elif choice == "4":
            if state["last_saved_date"]:
                last = date.fromisoformat(state["last_saved_date"])
                if date.today() - last == timedelta(days=1):
                    state["streak"] += 1
                elif date.today() == last:
                    pass # same day, no streak change
                else:
                    state["streak"] = 1
            else:
                state["last_saved_date"] = str(date.today())
                state["streak"] = 1

            progress = update_progress(state["total_saved"], state["milestones"])
            stage_name = state["pokemon"][progress["stage"] - 1]
            print(f"Your Pokemon is {stage_name}! Level is {progress["level"]}, XP is {progress["xp"]}%")
            print(f"Savings streak: {state["streak"]} days")

        elif choice == "5":
            while True:
                try:
                    yearly_income = input("Enter your new yearly income: ").strip()
                    if re.fullmatch(r"\d*", yearly_income):
                        state["yearly_income"] = float(yearly_income)
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Yearly income has to be digits with no commas or characters")

        elif choice == "6":
            save_state(state) #saves game progress
            print("Progress saved. Goodluck Trainor!")
            sys.exit(0)

        else:
            print("Invalid Choice. Ensure you input a valid integer associated with your choice")

def save_state(state):
    with open("save.json", "w") as file:
        json.dump(state, file)

def load_state():
    try:
        with open("save.json") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def compute_target(expenses, yearly_income):
    """
    Compute how spending compares to the 50/30/20 budgeting rule
    Returns dict with targets and deltas
    """
    targets = {
        "needs": round(0.5*yearly_income, 2),
        "wants": round(0.3*yearly_income, 2),
        "savings": round(0.2*yearly_income, 2)
    }
    deltas = {target: targets[target] - expenses.get(target, 0) for target in targets}
    return {"targets": targets, "deltas": deltas}

def gyms_milestones(total_saved, milestones):
    """
    Count how many savings milestones the user has reached
    Returns int value of milestones completed
    """
    return sum(1 for m in milestones if total_saved >= m)
def update_progress(total_saved, milestones):
    """
    Provides user with a progress update on their milestones
    Pokemon evolves to stage 2 when half the milestones have been accomplished. Stage 3 when completed all milestones.
    Returns a dict object with the level, stage, and xp
    """
    reached = gyms_milestones(total_saved, milestones)
    level = 1 + reached
    n = len(milestones)
    if n == 0:
        stage = 1
    elif reached >= n:
        stage = 3
    elif reached >= round(n / 2):
        stage = 2
    else:
        stage = 1
    if not milestones:
        xp = 0.0
    else:
        if reached == 0:
            prev = 0
        else:
            prev = milestones[reached - 1]

        if reached < n:
            next = milestones[reached]
        else: #when reached is equal to n
            next = milestones[-1]
        try:
            span = next - prev
            xp = (total_saved - prev) / span * 100
        except ZeroDivisionError:
            xp = 100

    return {"level": level, "stage": int(stage), "xp": round(xp, 2)}

if __name__ == "__main__":
    main()
