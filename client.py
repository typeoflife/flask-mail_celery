import requests

HOST = 'http://127.0.0.1:8080/'

# response = requests.post(HOST + 'user',
#                          json={'username': 'Denis', 'email': 'cospubartu@vusra.com', 'password': '***'})
#
# print(response.status_code)
# print(response.json())

#
# response = requests.get(HOST + f'user/{1}')
# print(response)
# print(response.status_code)
# print(response.text)
#
# response = requests.post(HOST + 'adv',
#                          json={'title': 'newtitle', 'text': 'newarticle', 'user_id': 1})
# print(HOST + 'adv')
# print(response.status_code)
# print(response.json())

# response = requests.delete(HOST + f'adv/{2}')
# print(HOST + 'adv')
# print(response.status_code)
# print(response.json())

response = requests.post(HOST + 'send_emails')
print(response.status_code)
print(response.text)