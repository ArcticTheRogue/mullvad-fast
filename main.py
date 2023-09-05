import json
import requests
import subprocess

api = requests.get("https://api.mullvad.net/www/relays/wireguard/")

servers = json.loads(api.text)
clock = 0

# Country Code Option
country_code = "us"

print(type(servers))
near_serv = []

for key in servers:
    serv = servers[clock]
    if serv["country_code"] == country_code:
        near_serv.append(serv)
    clock = clock + 1

clock = 0
sonic = 0
sonic_time = 0
last = 999
ping_time = 0

for key in near_serv:
    serv = near_serv[clock]
    ip = serv["ipv4_addr_in"]
    ping_pong = subprocess.run(["ping", "-n", "1", ip], capture_output=True)
    err = ping_pong.returncode
    if err == 0:
        ping_result = ping_pong.stdout.decode()
        ping_time = ping_result.split("Average = ", 1)[1]
        ping_time = ping_time.replace("ms", "")
        ping_time = int(ping_time)
    print(ip)
    print(f"Ping Time: {ping_time}")
    print(f"Last Ping Time: {last}")
    print(f"Fastest Time: {sonic_time}")
    if sonic_time == 0:
        sonic_time = ping_time
    if clock > 0:
        if ping_time <= last & ping_time <= sonic_time:
            sonic = clock
            sonic_time = ping_time
    clock = clock + 1
    last = ping_time

fastest = near_serv[sonic]
fastest = fastest["hostname"]
print(f"\nFastest Server: {fastest}")
