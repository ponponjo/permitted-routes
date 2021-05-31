'''
Functions to pull latest data from RG API
'''

import os
import zipfile

import requests

AUTH_URL = 'https://opendata.nationalrail.co.uk/authenticate'
AUTH_PWD = os.getenv('NR_AUTH_PWD')

RG_URL = 'https://opendata.nationalrail.co.uk/api/staticfeeds/2.0/routeing'


def refresh_credentials() -> str:
    '''
    Refreshes credentials for connecting to RG API
    '''
    data = {
        'username': 'josephpontin@outlook.com',
        'password': AUTH_PWD
    }

    response = requests.post(
        url=AUTH_URL,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data=data)

    os.environ["NR_TOKEN"] = response.json()['token']

    return response.json()['token']


def pull_data() -> None:
    '''
    Pulls latest zip file from RG API and unzips
    '''
    token = os.getenv('NR_TOKEN')

    if not token:
        token = refresh_credentials()

    response = requests.get(
        url=RG_URL,
        headers={
            'x-auth-token': token
        }
    )

    with open('../.download.zip', 'wb') as zip_file:
        for chunk in response.iter_content():
            zip_file.write(chunk)

    with zipfile.ZipFile('../.download.zip', 'r') as zip_ref:
        zip_ref.extractall('../.download')
