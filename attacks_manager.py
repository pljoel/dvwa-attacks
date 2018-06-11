import configparser
import argparse
from core.session import Session
from password_attacks.dictionary import dictionary


# Arguments parser
parser = argparse.ArgumentParser(description="Execute attacks against a DVWA server.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("attacks", type=int, nargs=1, help ="Attack no to perform\n"
                                                        "1. Password attacks (Default: dictionary)")
parser.add_argument("-u", "--users", type=str, nargs='+', help="Specify users to try instead of using user dictionaries in the config file. Password attacks only.")
parser.add_argument("-p", "--passw",  type=str, nargs='+', help="Specify passwords to try instead of using user dictionaries in the config file. Password attacks only.")
args = parser.parse_args()

# Variables from the config file
config = configparser.ConfigParser()
config.read('config.ini')
base_url = config['server']['url']
dvwa_user = config['credentials']['username']
dvwa_pass = config['credentials']['password']
## Credentials for password attacks (from config file & cli)
dict_user = config['dictionaries']['users'].split('\n')
dict_pass = config['dictionaries']['passwords'].split('\n')
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

def execute_attack(attack_no, session):
    if attack_no is 1:
        print("[1] Executing dictionary attack")
        dictionary.attack(session, dict_user, users, dict_pass, passw)
    exit(0)


def main():
    print("Trying to login as {}...".format(dvwa_user))
    sess = Session(base_url)
    sess.login('login.php', dvwa_user, dvwa_pass)
    print("Logged in as {}!".format(dvwa_user))

    execute_attack(get_args(), sess)


if __name__ == "__main__":
    main()