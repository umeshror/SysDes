import json
from bs4 import BeautifulSoup

with open("blind75-spa.html", "r") as f:
    soup = BeautifulSoup(f, "html.parser")

items = soup.select(".q-item")
questions = []
for item in items:
    q_name = item.select_one(".q-name").text.strip()
    questions.append(q_name)

print(json.dumps(questions, indent=2))
