import json
import requests
import subprocess

api = requests.get("https://api.mullvad.net/www/relays/wireguard/")

servers = json.loads(api.text)
clock = 0

print(type(servers))
x = servers[0]
y = 0
near_serv = []
print(x["country_code"])

for key in servers:
    serv = servers[clock]
    if serv["country_code"] == "us":
        near_serv.append(serv)
    clock = clock + 1

# ping_pong = subprocess.run(["ping", "-n", "1", "1.1.1.1"], capture_output=True)
# ping_result = ping_pong.stdout.decode()
# ping_time = ping_result.split("Average = ", 1)[1]
# print(ping_time)
clock = 0
sonic = 0
last = 999

for key in near_serv:
    # if clock > len(near_serv):
    #    break
    serv = near_serv[clock]
    ip = serv["ipv4_addr_in"]
    ping_pong = subprocess.run(["ping", "-n", "1", ip], capture_output=True)
    ping_result = ping_pong.stdout.decode()
    ping_time = ping_result.split("Average = ", 1)[1]
    ping_time = ping_time.replace("ms", "")
    ping_time = int(ping_time)
    print(ip)
    print(ping_time)
    if clock > 0:
        if ping_time < last:
            sonic = clock
    clock = clock + 1
    last = ping_time
