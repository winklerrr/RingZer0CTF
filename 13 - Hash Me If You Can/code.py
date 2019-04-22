import hashlib
import re
import requests


CHALLENGE = 13
URL = f"https://ringzer0ctf.com/challenges/{CHALLENGE}"

RE_MESSAGE = re.compile(r"----- BEGIN MESSAGE -----<br />[\n\r\s]*(\w+)")
RE_FLAG = re.compile(r"FLAG-(\w+)")
    
ERROR = "Wrong answer or too slow!"
LOGIN = "Website Login"


def get_message(cookie) -> str:
    text: str = requests.get(URL, cookies=cookie).text

    if LOGIN in text:
        print("Error: SessionID is not logged in!")
        return None

    match = RE_MESSAGE.search(text)
    if match:
        return match.group(1)
    
    print("Error: Message can not be found!")
    return None


def get_hash(message) -> str:
    return hashlib.sha512(message.encode()).hexdigest()
    

def send_hash(cookie, hash_value) -> str:
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
    cookie = input("Cookie PHPSESSID: ")
    main(dict(PHPSESSID=cookie))