import hashlib
import re
import requests


CHALLENGE = 14
URL = f"https://ringzer0ctf.com/challenges/{CHALLENGE}"

RE_MESSAGE = re.compile(r"----- BEGIN MESSAGE -----<br />[\n\r\s]*(\w+)")
RE_FLAG = re.compile(r"FLAG-(\w+)")
    
ERROR = "Wrong answer or too slow!"
LOGIN = "Website Login"


def get_binary_message(cookie) -> str:
    text: str = requests.get(URL, cookies=cookie).text

    if LOGIN in text:
        print("Error: SessionID is not logged in!")
        return None

    match = RE_MESSAGE.search(text)
    if match:
        message = match.group(1)
        return message
    
    print("Error: Message can not be found!")
    return None


def get_message(binary) -> str:
    message = ""
    binary.split()
    for byte in [binary[step*8:step*8+8] for step in range(0, int(len(binary)/8))]:
        message += chr(int(byte, 2))
    
    print(f"Message: {message}")
    return message


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
    binary = get_binary_message(cookie)
    message = get_message(binary)
    if message:
        hash_value = get_hash(message)
        response = send_hash(cookie, hash_value)
        return check_response(response)

    return None


if __name__ == "__main__":
    print(f"** RingZer0 CTF Challenge {CHALLENGE} **")
    cookie = input("Cookie PHPSESSID: ")
    main(dict(PHPSESSID=cookie))