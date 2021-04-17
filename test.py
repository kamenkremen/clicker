from requests import get, post, delete
from pprint import pprint


# print(get('http://localhost:5000/api/v1/upgrades').json())
'''
print(post('http://localhost:5000/api/v1/upgrades', 
           json={
                'name': 'first upgrade',
                'money_price': 25,
                'experience_price': 15,
                'active_income': 3,
                'passive_income': 1,
                'requirements': 50,
                'requirements_amount': 100,
           }).json())
'''

pprint(get('http://localhost:5000/api/v1/upgrades').json())
'''
pprint(post('http://localhost:5000/api/v1/users', 
           json={
                'name': 'Dio',
                'email': '@mail',
                'hashed_password': '123',
                'upgrades': '1, 3',
           }).json())
'''
pprint(get('http://localhost:5000/api/v1/users').json())