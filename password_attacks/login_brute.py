bruteforce_path = 'vulnerabilities/brute/'


def login_brute():
    r = self.__session.get(url=login_url, params=data, cookies=self.__cookies)
    # r = self.__session.post(url=login_url, data=data, cookies=self.__cookies) ######## NEED to do a POST for IMPOSSIBLE