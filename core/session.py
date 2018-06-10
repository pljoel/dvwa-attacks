from bs4 import BeautifulSoup
from requests.compat import urljoin
import sys, requests

class Session:
    def __init__(self, base_url):
        self.__session = requests
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

    def get_sess_infos(self, rel_url, cookie=None):
        if cookie is None:
            cookie = self.__cookies
        # Prepare the GET request
        req_url = urljoin(self.__base_url, rel_url)  # http://<dvwa_address>/<path>

        #Fetch CSRF token & cookies
        try:
            # Send the GET request
            r = self.__session.get(req_url, cookies=cookie)
            # Fetch CSRF token using CSS selector (google chrome: inspect element)
            self.__csrf = BeautifulSoup(r.text, 'html.parser').find("input", attrs={"name":"user_token"})["value"]
            # Fetch cookies (PHPSESSID & Security Level)
            self.__cookies.update(r.cookies.get_dict())
            return self.__csrf, self.__cookies
        except:
            print('Could not connect to DVWA server. Are you sure it is the right URL?')
            sys.exit(-1)

    # Log in + fetch CSRF token & cookies
    def login(self, rel_url, login_user, login_pass):
        data = {
            'username': login_user,
            'password': login_pass,
            'Login': 'Login',
            'user_token': self.__csrf
        }

        # GET request to fetch CSRF token and cookies
        self.get_sess_infos(rel_url)

        # Login attempt
        try:
            login_url = urljoin(self.__base_url, rel_url)
            r = self.__session.post(login_url, data=data, cookies=self.__cookies)
        except:
            print('Login attempt has failed.')
            sys.exit(-1)

        if r.status_code is not 200:
            print('DVWA server did not return expected status code. CODE: %d', r.status_code)
            sys.exit(-1)

        return r.text
