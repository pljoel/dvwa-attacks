Barebone scripts for providing attack data. Right now partly tailored for DVWA but can be extended for actual engagements.

Example Usages (See tool help for more options)

`~$ ./attacks.py -u http://192.168.10.5 -l /vulnerabilities/fi/?page= -o windows -t 5 -a /login.php -p 4`

The above command initiates an lfi test against the url `http://192.168.10.5/vulnerabilities/fi/?page=` for a DVWA webserver running on windows, requiring authentication at http://192.168.10.5/login.php. 5 threads will be issued per attack task and the max depth of path to traverse below the webroot is 4

`~$ ./attacks.py -u http://192.168.10.5 -x /vulnerabilities/xss_d/?default= -t 5 -a /login.php --param default`

The above command initiates an xss test against the url `http://192.168.10.5/vulnerabilities/xss_d/?default=` for a DVWA instance requiring authentication at http://192.168.10.5/login.php. 5 threads will be issued per task and the parameter or body key to test is `default`

`~$ ./attacker.sh http://192.168.10.5`

The above command initiates a variety of scans and attacks featuring the following tools: `sqlmap`, `dirb`, `nikto`, `patator`

As earlier mentioned, these scripts are just good for the data but can be extended to verify results of test, true positives and support any web application.

Credits to OWASP for XSS attack strings
Credits to the following for providing lists of sensitive files in windows and Linux

1. https://medium.com/@hakluke/sensitive-files-to-grab-in-windows-4b8f0a655f40

2. https://blog.rapid7.com/2016/07/29/pentesting-in-the-real-world-local-file-inclusion-with-windows-server-files/

3. http://pwnwiki.io/#!presence/windows/blind.md

4. https://digi.ninja/blog/when\_all\_you\_can\_do\_is\_read.php

5. https://www.facebook.com/notes/security-training-share/useful-list-file-for-local-file-inclusion/762408313789674/
