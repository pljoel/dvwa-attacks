import subprocess


def scan_by_nmap(session):
    r = session.get_session().get(session.get_base_url(), stream=True)
    ip = r.raw._connection.sock.getpeername()[0]
    subprocess.call("nmap {}".format(ip), shell=True)


def scan_by_nikto(session):
    subprocess.call("nikto -h {} -ask no".format(session.get_base_url()), shell=True)
    subprocess.call("nikto -Cgidirs all -h {} -ask no".format(session.get_base_url()), shell=True)


def scan_by_dirb(session):
    subprocess.call("dirb {}".format(session.get_base_url()), shell=True)


def scan_manager(session):
    scan_by_nmap(session)
    scan_by_nikto(session)
    scan_by_dirb(session)
