import requests
from requests.compat import urljoin

bruteforce_path = 'vulnerabilities/brute/'
data = {
    'username': "",
    'password': "",
    'Login': 'Login',
    'user_token': ""
}


def login_brute(session, u, p):
    r = None
    session.get_sess_infos(bruteforce_path)
    brute_url = urljoin(session.get_base_url(), bruteforce_path)
    data["username"] = u
    data["password"] = p
    data["user_token"] = session.get_csrf()
    if (session.get_cookies()["security"] == "low" or
            session.get_cookies()["security"] == "medium" or
            session.get_cookies()["security"] == "high"):
        r = requests.get(url=brute_url, params=data, cookies=session.get_cookies())
    elif session.get_cookies()["security"] == "impossible":
        r = requests.post(url=brute_url, data=data, cookies=session.get_cookies())

    return r
