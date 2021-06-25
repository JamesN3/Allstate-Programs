import requests

payload = {"username": "Corey", "password": "testing"}
r = requests.post("https://httpbin.org/post", data=payload)

r_dict = r.json()
print(r_dict["headers"])

r1 = requests.get(
    "https://httpbin.org/basic-auth/corey/testing",
    timeout=10,
    auth=("corey", "testing"),
)

print(r1.text)
