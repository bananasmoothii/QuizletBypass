import sys

from selenium import webdriver
from selenium.webdriver.common.by import By

Card = tuple[str, str]

if __name__ == '__main__':
    link = input("Paste the link of your quizlet: ")
    browser = input("""What browser do you want to use (default: Chrome)
Chrome (0)
Firefox (1)
Edge (2)
Safari (3)""")
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
    items: list[Card] = []
    for container in containers:
        spans = container.find_elements(By.TAG_NAME, "span")
        if len(spans) < 2:
            continue
        items.append((spans[0].text, spans[1].text))
    print(items)

