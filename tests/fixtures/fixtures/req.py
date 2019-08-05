import requests

x = requests.get("https://httpbin.org/ip")
status = x.status_code
t = x.text
