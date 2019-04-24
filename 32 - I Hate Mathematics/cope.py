import hashlib
import re
import requests
import time


CHALLENGE = 32
URL = f"https://ringzer0ctf.com/challenges/{CHALLENGE}"

RE_MESSAGE = re.compile(r"----- BEGIN MESSAGE -----<br />[\n\r\s]*(\w+) \+ (\w+) - (\w+)")
RE_FLAG = re.compile(r"FLAG-(\w+)")
    
ERROR = "Wrong answer or too slow!"
LOGIN = "Website Login"

START = None


def equation(terms: tuple):
    return f"{terms[0]} + {terms[1]} - {terms[2]}"


def get_equation_terms(cookie: str) -> tuple:
    print("> Starting challenge")
    
    # start timer
    global START 
    START = time.time()

    text: str = requests.get(URL, cookies=cookie).text
    if LOGIN in text:
        print("Error: PHPSESSID wrong or not logged in!")
        return None

    match: re.match = RE_MESSAGE.search(text)
    if match:
        terms = match.group(1, 2, 3)
        print(f"> Equation found: {equation(terms)}")
        return terms
    
    print("Error: Equation can not be found!")
    return None


def convert_terms(terms: tuple) -> tuple:
    terms = (int(terms[0]), int(terms[1], 16), int(terms[2], 2))
    print(f"> Equation converted: {equation(terms)}") 
    return terms


def calculate_solution(terms: tuple) -> int:
    solution = terms[0] + terms[1] - terms[2]
    print(f"> Equation solved: {solution}")
    return solution


def send_solution(cookie, solution) -> str:
    print(f"> Sending hash (time used: {time.time() - START:.2} seconds)")
    return requests.post(f"{URL}/{solution}", cookies=cookie).text


def check_response(response) -> str:
    if ERROR in response:
        print(f"Error: {ERROR}")
        return None
    
    match = RE_FLAG.search(response)
    if match:
        flag = match.group(1)
        print(f"Success: FLAG-{flag}")
        return flag
    
    print("Error: Flag can not be found!")
    return None


def main(cookie) -> str:
    terms = get_equation_terms(cookie)
    if terms:
        terms = convert_terms(terms)
        solution = calculate_solution(terms)
        response = send_solution(cookie, solution)
        return check_response(response)

    return None


if __name__ == "__main__":
    print(f"** RingZer0 CTF Challenge {CHALLENGE} **")
    cookie = input("Enter Cookie PHPSESSID: ")
    main(dict(PHPSESSID=cookie))
