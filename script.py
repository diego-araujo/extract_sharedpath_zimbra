import sys
import threading
from subprocess import PIPE, Popen
#import json
import simplejson as json

def storepath(path):
   hs = open("allsharedpath.txt","a")
   hs.write(path)
   hs.write("\n")
   hs.close()

def process_account(account):
    print(account)
    command = ['/opt/zimbra/bin/zmmailbox', '-z', '-m', account, 'gaf', '-v']
    folders = Popen(command, stdout=PIPE)
    cmd_response = ''
    for item in folders.stdout:
        cmd_response += item.rstrip()
    json_response = json.loads(cmd_response)
    if "subFolders" in json_response and len(json_response['subFolders']) > 0:
        for item in json_response['subFolders']:
            if item['defaultView'] == "message":
                if 'ownerId' in item:
                    storepath(item["pathURLEncoded"]+";"+item['ownerDisplayName'])

def task(account):
    smphr.acquire()
#    print("Start process for {0}".format(threading.currentThread().getName()))
    print("Start process for %s ") % threading.currentThread().getName()
    process_account(account)
#    print("Exiting process for {0}".format(threading.currentThread().getName()))
    print("Exiting process for %s ") % threading.currentThread().getName()
    smphr.release()

if __name__ == '__main__':
    smphr = threading.Semaphore(value=2)
    threads = list()
    filepath = sys.argv[1]
    if filepath is not None:
        fp = open(filepath)
        for cnt, line in enumerate(fp):
            # process_account(account)
            th = threading.Thread(name=line.strip(), target=task, args=(line.strip(),))
            th.daemon = True
            threads.append(th)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    else:
        print('filepath not provided')
