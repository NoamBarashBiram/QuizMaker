from os import system
import random
from sys import stdout
from time import sleep

import colorama
from readchar import readchar


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


def showQuiz(quizFile):
    quiz = getQuiz(quizFile)
    quiz.sort(key=lambda x: random.randint(0, 1000))

    right = 0

    clear()
    for i in range(len(quiz)):
        question = quiz[i]
        print(f"You got {right}/{len(quiz)} ({round(right / len(quiz) * 100, 2)}%) right")
        print(f"Question {i + 1} out of {len(quiz)}: ")

        print(question[0])

        for j in range(1, len(question) - 1):
            print(f"{j}) {question[j]}")

        print("And your answer: ", end="")
        stdout.flush()

        ans = readchar()
        while not ans.isdigit() or int(ans) not in range(1, len(question) - 1):
            ans = readchar()

        print(ans)

        if int(ans) == question[-1]:
            print(colorama.Fore.GREEN + "That's right!" + colorama.Style.RESET_ALL)
            sleep(1)
            right += 1
        else:
            print(colorama.Fore.RED + "Not exactly..." + colorama.Style.RESET_ALL)
            sleep(1)


def main():
    showQuiz("quiz.qz")


if __name__ == '__main__':
    main()
