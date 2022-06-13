import requests, os


def take_name(url: str): -> str


    



def_path = os.getcwd()
url = 'https://ru.hexlet.io/courses'
r = requests.get(url, allow_redirects=True)

open('facebook.html', 'wb').write(r.content)