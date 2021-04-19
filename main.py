#!/usr/bin/env python3

################################################################################

repsy_repo_name = 'default' # change if different than default
repsy_username = 'FIX ME'
repsy_password = 'FIX ME'
destination_directory = '/path/to/local/backup/dir'

################################################################################

import requests
import base64
import json
import sys
import os

def login() -> str:
    response = requests.post(
        'https://panel.repsy.io/be/auth/login',
        json = {'usernameOrEmail': repsy_username, 'password': repsy_password},
        headers = {'content-type': 'application/json'}
    )

    if response.status_code != 200:
        print('Error authenticating repsy', response.text)
        sys.exit(1)

    return response.json()['data']['token']


def basic_auth(username: str, password: str) -> None:
    return base64.b64encode((username + ':' + password).encode('ascii')).decode('ascii')


def download(path: str) -> None:
    response = requests.get(
        'https://repo.repsy.io/mvn/' + repsy_username + '/' + repsy_repo_name + path,
        headers = {'Authorization': 'Basic ' + basic_auth(repsy_username, repsy_password)}
    )
    fd = os.open(destination_directory + path, os.O_RDWR|os.O_CREAT)
    os.write(fd, response.content)
    os.close(fd)


def walk(path: str, token: str) -> None:

    try:
        os.mkdir(destination_directory + path)
    except FileExistsError:
        pass

    response = requests.get(
        'https://panel.repsy.io/api/mvn/repo/' + repsy_repo_name + '/content?path=' + path,
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    )

    if response.status_code != 200:
        print('cannot fetch directory', response.text)
        sys.exit(1)

    directory_list = response.json()['data']

    for item in directory_list:
        item_name = item['name']
        
        if item_name == '../':
            pass
        elif item_name.endswith('/'):
            walk(path + item_name, token)
        else:
            download(path + item_name)

walk('/', login())
