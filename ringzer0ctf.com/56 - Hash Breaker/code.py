import re
import requests
import time


CHALLENGE = 56
URL = f"https://ringzer0ctf.com/challenges/{CHALLENGE}"

RE_MESSAGE = re.compile(r"----- BEGIN HASH -----<br />[\n\r\s]*(\w+)")
RE_FLAG = re.compile(r"FLAG-(\w+)")
    
ERROR = "Wrong answer or too slow!"
LOGIN = "Website Login"
START = None

SHA1_REVERSE_LOOKUP = "https://sha1.gromweb.com/?hash={}"
RE_SHA1_REVERSE_VALUE = re.compile(r'<em class="long-content string">(\w+)')


def get_SHA1_hash_value(cookie: str) -> str:
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
        hash_value = match.group(1)
        print(f"> SHA1 hash value found: {hash_value}")
        return hash_value
    
    print("Error: SHA1 hash value can not be found!")
    return None


def reverse_lookup(hash_value: str) -> str:
    text: str = requests.get(SHA1_REVERSE_LOOKUP.format(hash_value)).text

    match = RE_SHA1_REVERSE_VALUE.search(text)
    if match:
        original_value = match.group(1)
        print(f"> Original value found: {original_value}")
        return original_value

    print("Error: Reverse lookup failed!")
    return None


def send_original_value(cookie, original_value) -> str:
    print(f"> Sending hash (time used: {time.time() - START:.2} seconds)")
    return requests.post(f"{URL}/{original_value}", cookies=cookie).text


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
    hash_value = get_SHA1_hash_value(cookie)
    if hash_value:
        original_value = reverse_lookup(hash_value)
        response = send_original_value(cookie, original_value)
        return check_response(response)

    return None


if __name__ == "__main__":
    print(f"** RingZer0 CTF Challenge {CHALLENGE} **")
    cookie = input("Enter Cookie PHPSESSID: ")
    main(dict(PHPSESSID=cookie))
