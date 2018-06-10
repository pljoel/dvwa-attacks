from core.session import Session


def attack(session, dict_user, users, dict_pass, passw):
    usernames=[]
    passwords=[]

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

    #for u in usernames:
    #    u = u.rstrip('\n')
    #    print(u)

    #session.get_sess_infos('vulnerabilities/brute/', session.get_cookies())

    dvwa_creds = {
        'user': 'admin',
        'pass': 'password'
    }
    print('\n\n\n')
    session.login('vulnerabilities/brute/', dvwa_creds)

    #print(session.get_session().text)

