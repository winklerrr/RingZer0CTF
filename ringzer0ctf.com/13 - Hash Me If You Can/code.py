import hashlib
import re
import requests
import time


CHALLENGE = 13
URL = f"https://ringzer0ctf.com/challenges/{CHALLENGE}"

RE_MESSAGE = re.compile(r"----- BEGIN MESSAGE -----<br />[\n\r\s]*(\w+)")
RE_FLAG = re.compile(r"FLAG-(\w+)")
    
ERROR = "Wrong answer or too slow!"
LOGIN = "Website Login"


def get_message(cookie) -> str:
    print("> Starting challenge")

    # start timer
    global START 
    START = time.time()

    text: str = requests.get(URL, cookies=cookie).text
    if LOGIN in text:
        print("Error: PHPSESSID wrong or not logged in!")
        return None

    match = RE_MESSAGE.search(text)
    if match:
        message = match.group(1)
        print(f"> Message found: {message[:50]}...")
        return message
    
    print("Error: Message can not be found!")
    return None


def get_hash(message) -> str:
    hash_value = hashlib.sha512(message.encode()).hexdigest()
    print(f"> Sha512 hash: {hash_value}")
    return hash_value
    

def send_hash(cookie, hash_value) -> str:
    print(f"> Sending hash (time used: {time.time() - START:.2} seconds)")
    return requests.post(f"{URL}/{hash_value}", cookies=cookie).text


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
    message = get_message(cookie)
    if message:
        hash_value = get_hash(message)
        response = send_hash(cookie, hash_value)
        return check_response(response)

    return None


if __name__ == "__main__":
    print(f"** RingZer0 CTF Challenge {CHALLENGE} **")
    cookie = input("Enter cookie PHPSESSID: ")
    main(dict(PHPSESSID=cookie))