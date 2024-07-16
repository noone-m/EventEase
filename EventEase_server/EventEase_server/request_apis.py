import requests 
import django
import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventEase_server.settings')  # Replace 'myprojec
django.setup()



from accounts.models import User


                ### creating super user ####
print('creating super user ....')
superuser1 = User.objects.create_superuser(first_name= 'mahdi', last_name='abo tafish', phone = '+963935925081' , email= 'mahdi@gmail.com', password= '1234')
print('super users login ....')

log_in = requests.post('http://127.0.0.1:8000/api/accounts/log-in/',
                      data={'email' : 'mahdi@gmail.com', 'password' : '1234'})

print(log_in.status_code)
print(log_in.text)
superuser1_token = log_in.json().get('token')
superuser1_headers = {'Authorization' : f'Token {superuser1_token}'}
                ### registration ###
print('registration >>>>>')
user1 = requests.post('http://127.0.0.1:8000/api/accounts/register/',
                      data={'first_name' : 'mahdi', 'last_name': 'at','email': 'm1hdi1t@gmail.com','password' : '1234', 'password2' : '1234', 'phone' : '+963935925081'})
print(user1.status_code)
print(user1.text)

user2 = requests.post('http://127.0.0.1:8000/api/accounts/register/',data={'first_name' : 'danial', 'last_name': 'daibs','email': 'danial@gmail.com','password' : '1234', 'password2' : '1234', 'phone' : '+963935925081'})
print(user2.status_code)
print(user2.text)

user3 = requests.post('http://127.0.0.1:8000/api/accounts/register/',data={'first_name' : 'abo jood', 'last_name': 'sobh','email': 'abojood@gmail.com','password' : '1234', 'password2' : '1234', 'phone' : '+963935925081'})
print(user3.status_code)
print(user3.text)

                ### Auth Headers ###
print(user1)
print(user1.json())
user1_token = user1.json().get('Token')
user2_token = user2.json().get('Token')
user3_token = user3.json().get('Token')

user1_headers = {'Authorization': f'Token {user1_token}'}
user2_headers = {'Authorization': f'Token {user2_token}'}
user3_headers = {'Authorization': f'Token {user3_token}'}

                ### Generating and Verifying Codes ###

print('generating and verifying codes .....')

user1_code_response = requests.get('http://127.0.0.1:8000/api/accounts/code-generate', headers=user1_headers)
print(user1_code_response.status_code)
print(user1_code_response.json())

code1 = user1_code_response.json().get('code')
user1_verify_response = requests.post(
    'http://127.0.0.1:8000/api/accounts/code-verify/',
    data={'code': code1},
    headers=user1_headers 
)
print(user1_verify_response.status_code)
print(user1_verify_response.json())


print('verifying user2 phone....')
user2_code_response = requests.get('http://127.0.0.1:8000/api/accounts/code-generate', headers=user2_headers)
print(user2_code_response.status_code)
print(user2_code_response.json())

code2 = user2_code_response.json().get('code')
user2_verify_response = requests.post(
    'http://127.0.0.1:8000/api/accounts/code-verify/',
    data={'code': code2},
    headers=user2_headers 
)
print(user2_verify_response.status_code)
print(user2_verify_response.json())


# print('verifying user3 phone ....')
# user3_code_response = requests.get('http://127.0.0.1:8000/api/accounts/code-generate', headers=user3_headers)
# print(user3_code_response.status_code)
# print(user3_code_response.json())

# code3 = user3_code_response.json().get('code')
# user3_verify_response = requests.post(
#     'http://127.0.0.1:8000/api/accounts/code-verify/',
#     data={'code': code3},
#     headers=user3_headers
# )
# print(user3_verify_response.status_code)
# print(user3_verify_response.json())

print('generating and verifying token for email verification .....')


user1_code_response = requests.get('http://127.0.0.1:8000/api/accounts/verification-link', headers=user1_headers)
print(user1_code_response.status_code)
print(user1_code_response.json())

token1 = user1_code_response.json().get('Token')
user1_verify_response = requests.post(
    'http://127.0.0.1:8000/api/accounts/verify-email/',
    params={'Token': token1},
    headers=user1_headers 
)
print(user1_verify_response.status_code)
print(user1_verify_response.json())


print('verifying user2 email....')
user2_code_response = requests.get('http://127.0.0.1:8000/api/accounts/verification-link', headers=user2_headers)
print(user2_code_response.status_code)
print(user2_code_response.json())

token2 = user2_code_response.json().get('Token')
user2_verify_response = requests.post(
    'http://127.0.0.1:8000/api/accounts/verify-email/',
    params={'Token': token2},
    headers=user2_headers  
)
print(user2_verify_response.status_code)
print(user2_verify_response.json())


# print('verifying user3 email....')
# user3_code_response = requests.get('http://127.0.0.1:8000/api/accounts/verification-link', headers=user3_headers)
# print(user3_code_response.status_code)
# print(user3_code_response.json())

# token3 = user3_code_response.json().get('Token')
# user3_verify_response = requests.post(
#     'http://127.0.0.1:8000/api/accounts/verify-email/',
#     params={'Token': token3},
#     headers=user3_headers  
# )
# print(user3_verify_response.status_code)
# print(user3_verify_response.json())




                ####service type###

print('service type ......')

type1 = requests.post(
    'http://127.0.0.1:8000/api/services/type/',
    data={'type' : 'food'},
    headers=superuser1_headers 
)
print(type1.status_code)
print(type1.text)


                ### applying on service povider application ### 

print('applying on service provider application ......')

with open('F:\\IT\\سنة ثالثة\\2023-2024\\Second Semester 2\\idfront.jpg', 'rb') as front, \
    open('F:\\IT\\سنة ثالثة\\2023-2024\\Second Semester 2\\idback.jpg', 'rb') as back:
    files = {
        'national_identity_front': ('front.jpg', front, 'image/jpeg'),
        'national_identity_back': ('back.jpg', back, 'image/jpeg')
    }
    application1 = requests.post(
        'http://127.0.0.1:8000/api/services/applications/',
        data={'latitude': '33.51035', 'longitude': '36.31989', 'name': 'Grilling master', 'description': 'I provide variety of delicious grilled meats in homemade way', 'service_type': '1', 'phone': '+963947741054'},
        files=files,
        headers=user1_headers
    )
    print(application1.status_code)
    print(application1.text)

print('approving on service provder application ......')

application1 = requests.post(
    f'http://127.0.0.1:8000/api/services/applications/1/approve/',
    headers=superuser1_headers 
)

print(application1.status_code)
print(application1.text)

