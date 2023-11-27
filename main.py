import sys
import random
import Levenshtein as lv
import re

from selenium import webdriver
from selenium.webdriver.common.by import By

Card = tuple[str, str]

maxAcceptableDistance = 1

splitAnswer = re.compile(r"[/,;]")
splitReplacer = "' or '"


def learnProcess(terms: list[Card]):
    learnt = []
    doShuffle = input("Do you want to shuffle the cards? (Y/n)").lower() in ["", "y", "yes"]
    if doShuffle:
        random.shuffle(terms)
    groupSizeStr = input("How many cards do you want to learn at once? (default: 10)")
    if groupSizeStr == "":
        groupSizeStr = "10"
    groupSize = int(groupSizeStr)

    sideOfCardsStr = input("Which side of the cards do you want to learn? (default: 1)\n0: front\n1: back\n2: both\n")
    if sideOfCardsStr == "":
        sideOfCardsStr = "1"
    sideOfCards = int(sideOfCardsStr)
    if sideOfCards == 0:
        sideFct = lambda: 1
    elif sideOfCards == 1:
        sideFct = lambda: 0
    elif sideOfCards == 2:
        sideFct = lambda: random.randint(0, 1)
    else:
        print("invalid value, please input 0, 1 or 2")
        sys.exit(1)

    learning = []
    for i in range(0, len(terms), groupSize):
        group = terms[i:i + groupSize]
        learning.append(group)

    for i, group in enumerate(learning):
        # print progress
        print(f"Learning group {i + 1} of {len(learning)}")
        print(f"Cards learnt: {len(learnt)} of {len(terms)}")

        # learn
        while len(group) > 0:
            print(f"Cards left in group: {len(group)}")
            card = group.pop(-1)
            questionSide = sideFct()
            correctAnswers = [a.strip() for a in splitAnswer.split(card[1 - questionSide])]
            answer = input(card[questionSide] + " : ").strip()
            distance = min(lv.distance(answer, correctAnswer, score_cutoff=maxAcceptableDistance) for correctAnswer in correctAnswers)

            if distance == 0:
                # perfect answer
                start = random.choice(["Perfect!", "Great!", "Awesome!", "Good job!", "Nice!"])
                cancel = input(f"{start} If you were wrong, type 'x' and press enter, else press enter\n") == "x"
                if cancel:
                    group.insert(0, card)
                else:
                    learnt.append(card)
            elif distance <= maxAcceptableDistance:
                # almost perfect answer
                start = (random.choice(["Almost!", "Close!", "Not quite!", "Nearly!"]) +
                         f" The correct answer was '{splitReplacer.join(correctAnswers)}' but I gotchu")
                cancel = input(f"{start} If you were wrong, type 'x' and press enter, else press enter\n") == "x"
                if cancel:
                    group.insert(0, card)
                else:
                    learnt.append(card)
            else:
                # wrong answer
                start = (random.choice(["Wrong.", "Incorrect.", "Not at all...", "Nope."]) +
                         f" The correct answer was '{splitReplacer.join(correctAnswers)}'")
                iWasCorrect = input(f"{start} If you were right, type 'x' and press enter, else press enter\n") == "x"
                if iWasCorrect:
                    learnt.append(card)
                else:
                    group.insert(0, card)
        print("Group learnt!")
    print("All cards learnt! Congratulations!")


if __name__ == '__main__':
    link = input("Paste the link of your quizlet: ")
    browser = input("""What browser do you want to use (default: Chrome)
Chrome (0)
Firefox (1)
Edge (2)
Safari (3)
""")
    print("Starting browser, please wait...")
    if browser in ["", "0"]:
        driver = webdriver.Chrome()
    elif browser == "1":
        driver = webdriver.Firefox()
    elif browser == "2":
        driver = webdriver.Edge()
    elif browser == "3":
        driver = webdriver.Safari()
    else:
        print("invalid value, please input nothing, 0, 1, 2 or 3")
        sys.exit(1)
    driver.get(link)

    containers = driver.find_elements(By.CLASS_NAME, "SetPageTerm-content")
    if len(containers) == 0:
        print("No cards found, please check if the link is correct")
        sys.exit(0)

    items: list[Card] = []
    for container in containers:
        spans = container.find_elements(By.TAG_NAME, "span")
        if len(spans) < 2:
            continue
        items.append((spans[0].text, spans[1].text))

    driver.close()

    learnProcess(items)
