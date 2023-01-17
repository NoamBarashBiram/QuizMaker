#!/usr/bin/python3

from os import system
import random
from sys import stdout, executable
from time import sleep
from subprocess import check_call


def tryImport(package, *things):
    module = None
    try:
        module = __import__(package)
    except ImportError:
        print(f"{package} doesn't seems to be installed on your device")
        inp = input("would you like it to be installed? [Y/N] ").lower()
        while inp not in ["y", "n"]:
            inp = input("[Y/N] ")

        if inp == "y":
            check_call([executable, "-m", "pip", "install", "colorama"])
        else:
            print("Alright, but you won't be able to use this script until you install it")
            exit(1)

        module = __import__(package)

    for thing in things:
        globals()[thing] = eval(f"module.{thing}")


tryImport("readchar", "readchar", "key")
tryImport("colorama", "Fore", "Style", "Back", "Cursor")

welcome_message = f"""{Style.BRIGHT}=========================================
= Welcome to the {Back.LIGHTBLACK_EX}QuizMaker{Back.RESET} By {Back.LIGHTBLACK_EX}@Puffin42{Back.RESET} =
========================================={Style.RESET_ALL}
What would you like to do?
1. Make a {Back.LIGHTBLACK_EX}quiz{Back.RESET}
2. Run an existing {Back.LIGHTBLACK_EX}quiz{Back.RESET}{Cursor.UP(2)}{Cursor.FORWARD(4)}"""

quiz_message = f"""{Style.BRIGHT}================================
= Are you ready to be {Back.LIGHTBLACK_EX}Quiz{Back.RESET}zed? =
================================{Style.RESET_ALL}"""

make_message = f"""{Style.BRIGHT}==================
= Making a {Back.LIGHTBLACK_EX}Quiz{Back.RESET}! =
=================={Style.RESET_ALL}"""


def clear():
    system("cls | clear")


def getQuiz(quizFile):
    with open(quizFile, "r") as file:
        quiz_data = file.readlines()

    questions = [[]]

    for line in quiz_data:
        if line == "\n":
            questions[-1][-1] = int(questions[-1][-1])
            questions.append([])
        else:
            questions[-1].append(line.replace("\n", ""))

    questions[-1][-1] = int(questions[-1][-1])

    return questions


def askToExit():
    print("\nDo you want to exit? [Y/N] ", end="")
    stdout.flush()
    ans = ""
    while ans not in ["y", "n"]:
        ans = readchar().lower()

    print()

    if ans == "y":
        print("Alright. Bye!")
        exit(0)


def showQuiz(quizFile):
    quiz = getQuiz(quizFile)
    quiz.sort(key=lambda x: random.randint(0, 1000))

    right = 0

    for i in range(len(quiz)):
        clear()
        question = quiz[i]

        stats = f"You got {right}/{len(quiz)} ({round(right / len(quiz) * 100, 2)}%) right"
        progress = f"Question {i + 1} out of {len(quiz)}: "
        border_len = max(len(stats), len(progress)) + 4
        msg = f"{Style.BRIGHT}{'=' * border_len}\n= {stats} {' ' * ((border_len - 4) - len(stats))}=\n" \
              f"= {progress} {' ' * ((border_len - 4) - len(progress))}=\n{'=' * border_len}{Style.RESET_ALL}\n"

        print(msg)

        print(question[0])

        for j in range(1, len(question) - 1):
            print(f"{j}) {question[j]}")

        print("And your answer: ", end="")
        stdout.flush()

        ans = readchar()
        while not ans.isdigit() or int(ans) not in range(1, len(question) - 1):
            if ans in ["q", key.CTRL_C, key.ESC]:
                askToExit()
                print("So your answer: ", end="")
                stdout.flush()
            ans = readchar()

        print(ans)

        if int(ans) == question[-1]:
            print(Fore.GREEN + "That's right!" + Style.RESET_ALL)
            sleep(1)
            right += 1
        else:
            print(Fore.RED + "Not exactly..." + Style.RESET_ALL)
            sleep(1)

    clear()

    stats = f"You got {right}/{len(quiz)} ({round(right / len(quiz) * 100, 2)}%) right, " + \
            ("Excellent!" if right / len(quiz) > 0.9 else "Nice!" if right / len(quiz) > 0.7 else "Maybe next time")

    border_len = len(stats) + 4
    msg = f"{Style.BRIGHT}{'=' * border_len}\n" \
          f"= {stats} =\n" \
          f"{'=' * border_len}{Style.RESET_ALL}"

    print(msg)


def runQuiz():
    clear()
    print(quiz_message)
    quiz_file = input("Please Enter a quiz file path: ")
    while True:
        try:
            showQuiz(quiz_file)
            return
        except FileNotFoundError:
            clear()
            print(quiz_message)
            print(f"Can't open file {Back.LIGHTBLACK_EX}{quiz_file}{Back.RESET}")
            quiz_file = input("Please try another file: ")


def save(questions):
    filename = input("Your file? ")
    with open(filename, "w") as f:
        for q in questions:
            for a in q:
                f.write(a + "\n")
            f.write("\n")
    print("File was successfully saved!")


def makeQuiz():
    clear()
    print(make_message)
    questions = []
    while True:
        question = input("Enter a question or q to exit: ")
        if question == "q":
            save(questions)
            break
        else:
            questions += [[question]]
            while True:
                answer = input("Enter an answer or done if done: ")
                if answer.lower() == "done":
                    break
                else:
                    questions[-1] += [answer]
            right = "-1"
            while not right.isdigit() or int(right) < 1 or int(right) > len(questions[-1]):
                right = input("Enter the number of the right answer: ")

            questions[-1] += [right]


def menu():
    clear()
    print(welcome_message, end="")

    ans = readchar()

    while True:
        if ans == key.CTRL_C:
            clear()
            print("Going so soon? :(")
            return
        elif ans == "1":
            makeQuiz()
            return
        elif ans == "2":
            runQuiz()
            return
        ans = readchar()


def main():
    menu()


if __name__ == '__main__':
    main()
