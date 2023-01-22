import requests
import random,math
otp = ""
for i in range(1,7):
    a = random.random()
    b = math.floor(a*10)
    otp += str(b)
print(otp)


# url = "https://www.fast2sms.com/dev/bulkV2"
# message = otp
# numbers = 9973884727
# payload = f"sender_id=TXTIND&message={message}&route=v3&language=english&numbers=9973884727"

# headers = {
#     'authorization': "aiLHjGsN0AKYPUqTFp3lM5weZzct4xhE9VXI2yCDBnoR6gJvrOFE0Hr9UQcWn4vePkmwxfVdGjIb6Aga",
#     'Content-Type': "application/x-www-form-urlencoded",
#     'Cache-Control': "no-cache",
#     }


# response = requests.request("POST", url, data=payload, headers=headers)

# # print(response.text)