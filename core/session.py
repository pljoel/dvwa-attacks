import sys
import requests
from bs4 import BeautifulSoup
from requests.compat import urljoin


class Session:
    def __init__(self, base_url):
        self.__session = requests.session()
        self.__base_url = base_url
        self.__csrf = None
        self.__cookies = {
            'PHPSESSID': None,
            'security': None
        }

    def get_session(self):
        return self.__session

    def get_base_url(self):
        return self.__base_url

    def get_csrf(self):
        return self.__csrf

    def get_cookies(self):
        return self.__cookies

    def get_sess_infos(self, rel_url):
        # Prepare the GET request
        req_url = urljoin(self.__base_url, rel_url)  # http://<dvwa_address>/<path>

        # Fetch CSRF token & cookies
        try:
            # Send the GET request
            r = self.__session.get(req_url, cookies=self.__cookies)
            # Fetch CSRF token
            soup = BeautifulSoup(r.text, 'html.parser')
            token_list = soup("input", {"name": "user_token"})
            print("TOKEN LIST")
            print(token_list)
            if len(token_list):
                self.__csrf = token_list[0]["value"]
            else:
                self.__csrf = None
            # Fetch cookies (PHPSESSID & Security Level)
            if len(r.cookies.items()):
                self.__cookies.update(r.cookies.get_dict())
            return self.__csrf, self.__cookies
        except:
            print('Could not connect to DVWA server. Are you sure it is the right URL?')
            sys.exit(-1)

    # Log in + fetch CSRF token & cookies
    def login(self, rel_url, login_user, login_pass):
        # Update CSRF token and cookies
        self.get_sess_infos(rel_url)
        print("CSRF")
        print(self.__csrf)
        if self.__csrf is None:
            data = {
                'username': login_user,
                'password': login_pass,
                'Login': 'Login'
            }
        else:
            data = {
                'username': login_user,
                'password': login_pass,
                'Login': 'Login',
                'user_token': self.__csrf
            }
        print("DATA")
        print(data)
        print("COOKIES")
        print(self.__cookies)
        # Login attempt
        try:
            login_url = urljoin(self.__base_url, rel_url)
            print(login_url)
            r = requests.post(url=login_url, data=data, cookies=self.__cookies, allow_redirects=False)
            print(r.url)
            print(r.headers)
            print(r.request)
        except:
            print('Login attempt has failed.')
            sys.exit(-1)

        if r.status_code is not 200:
            print('DVWA server did not return expected status code. CODE: {}'.format(r.status_code))
            sys.exit(-1)

        print("\n")
        print(r.text)
        return r
