from __future__ import print_function
import sys, getopt
import requests, time


def start(script_name, argv):
    '''
    Usage: python script.py -e 'Example String'
    '''
    try:
        opts, args = getopt.getopt(
            argv,
            'hu:w:f:',
            [
                'help',
                'url=',
                'wait=',
                'file='
            ])
    except getopt.GetoptError:
        usage(script_name)
        sys.exit(2)
    url = None
    wait = None
    filename = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(script_name)
            sys.exit()
        elif opt in ('-u', '--url'):
            url = arg
        elif opt in ('-w', '--wait'):
            wait = arg
        elif opt in ('-f', '--file'):
            filename = arg
    wait_download(url, filename, wait)
                

def wait_download(url, filename, wait=None):
    # http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
    if not url:
        print('URL required')
        sys.exit(2)
    if wait is None:
        wait = 300
    while True:
        resp = requests.get(url, stream=True)
        if resp.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("File {} saved.".format(filename))
            sys.exit()
        else:
            print("URL Not Available. Status {}".format(resp.status_code))
            print("Waiting {} seconds.".format(wait))
            time.sleep(int(wait))
        

def usage(script_name):
    print('Usage: python {}'.format(script_name))

if __name__=='__main__':
    start(sys.argv[0], sys.argv[1:])
