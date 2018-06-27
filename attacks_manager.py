import configparser
import argparse
from datetime import datetime
from core.session import Session
from scanning import scanning
from attacks.password_attacks.dictionary import dictionary
from attacks.sqli import sqli
from attacks.file_inclusion import lfi
from attacks.xss import xss_d
from attacks.xss import xss_r
from attacks.xss import xss_s

# Arguments parser
parser = argparse.ArgumentParser(description="Execute attacks against a DVWA server.",
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("attacks", type=int, nargs=1, help ="Attack no to perform\n"
                                                        "1. Password attacks (Default: dictionary)")
parser.add_argument("-u", "--users", type=str, nargs='+', help="Specify users to try instead of using user dictionaries"
                                                               " in the config file. Password attacks only.")
parser.add_argument("-p", "--passw",  type=str, nargs='+', help="Specify passwords to try instead of using password "
                                                                "dictionaries in the config file. "
                                                                "Password attacks only.")
args = parser.parse_args()

# Variables from the config file
config = configparser.ConfigParser()
config.read('config.ini')
base_url = config['server']['url']
dvwa_user = config['credentials']['username']
dvwa_pass = config['credentials']['password']
## Credentials for password attacks (from cli)
users = []
passw = []


# Populate global variables and fetch attack number
def get_args():
    if args.attacks[0] is 1:
        if args.users is not None:
            users.extend(args.users)
        if args.passw is not None:
            passw.extend(args.passw)
    return args.attacks[0]


def log_time_attack(str):
    f = open("attacks_log.txt", "a+")
    f.write(
        "\tExecuting {} at {} \n".format(str, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    f.close()


def execute_attack(attack_no, session, log=True):
    if attack_no is 0:
        if log: log_time_attack("Network/Webserver scan")
        print("[0] Scanning the network and web server")
        scanning.scan_manager(session)
    if attack_no is 1:
        if log: log_time_attack("Dictionary attack")
        print("[1] Executing dictionary attack")
        dictionary.attack(session, users, passw)
    if attack_no is 2:
        if log: log_time_attack("Command injection")
        print("[2] Executing command injection")
        pass
    if attack_no is 3:
        if log: log_time_attack("CSRF")
        print("[3] Executing CSRF")
        pass
    if attack_no is 4:
        if log: log_time_attack("File inclusion")
        print("[4] Executing file inclusion")
        lfi.attack(session)
    if attack_no is 5:
        if log: log_time_attack("File upload")
        print("[5] Executing file upload")
        lfi.attack(session)
    if attack_no is 6:
        if log: log_time_attack("Insecure CAPTCHA")
        print("[6] Executing insecure CAPTCHA")
        pass
    if attack_no is 7:
        if log: log_time_attack("SQLi")
        print("[7] Executing SQL injection")
        sqli.attack(session)
    if attack_no is 8:
        if log: log_time_attack("Blind SQLi")
        print("[8] Executing SQL injection (blind)")
        sqli.attack(session, True)
    if attack_no is 9:
        if log: log_time_attack("Weak Session IDs")
        print("[9] Executing Weak Session IDs")
        pass
    if attack_no is 10:
        if log: log_time_attack("DOM XSS")
        print("[10] Executing XSS (DOM)")
        xss_d.attack(session)
    if attack_no is 11:
        if log: log_time_attack("Reflected XSS")
        print("[11] Executing XSS (Reflected)")
        xss_r.attack(session)
    if attack_no is 12:
        if log: log_time_attack("Stored XSS")
        print("[12] Executing XSS (Stored)")
        xss_s.attack(session)
    exit(0)


def main():
    print("Trying to login as {}...".format(dvwa_user))
    sess = Session(base_url)
    sess.login('login.php', dvwa_user, dvwa_pass)
    print("Logged in as {}!".format(dvwa_user))

    execute_attack(get_args(), sess)


if __name__ == "__main__":
    main()