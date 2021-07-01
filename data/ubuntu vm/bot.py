import requests
import os
import subprocess
import locale
import datetime

locale.setlocale( locale.LC_ALL, '' )

def telegram_bot_sendtext(message):

    bot_token = ''
    chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chatID + '&text=' + message
    requests.get(send_text)

    return

cmd1 = ['pgrep', '-f', 'anon_analysis.py']
cmd2 = ['df', '-h']
cmd3 = ['df', '-i']

#Function to check if process is running
def check_proc(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    return o.decode('ascii')!=''

def check_mem(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    return o.decode().split()[23]

def get_status():

    with open("data/progress.txt", "r") as text_file:
        count = int(text_file.readline())
    text_file.close()
    count_str = locale.format("%d", count, grouping=True)
    dumped_percent = float(count)/2112472*100

    script_status = ('Running' if check_proc(cmd1) else 'Down')
    mem_usage = check_mem(cmd2)
    inode_usage = check_mem(cmd3)

    with open("data/inputs_count.txt", "r") as text_file:
        inputs_count = int(text_file.readline())
    text_file.close()

    with open("data/deanon_inputs.txt", "r") as text_file:
        deanon_inputs = int(text_file.readline())
    text_file.close()

    deanon_ratio = float(deanon_inputs)/float(inputs_count)

    if script_status == 'Down':
        with open("data/anon_analysis.out",'r') as file:
	    try:
              error_msg = file.readlines()[-1]
	    except: error_msg = "No error msg"
        file.close()
        timestamp = datetime.datetime.fromtimestamp(os.path.getmtime("data/anon_analysis.out"))
    else:
        error_msg = 'NIL'
        timestamp = 'NIL'

    return "================================\nAnonymity analysis untill block {} ({}%).\n\nAnonymity analysis script status: {}.\n\nDeanon ratio: {}\n\nError message: {}\n\nTimestamp: {}\n\nMemory usage: {}\n================================".format(count_str, dumped_percent, script_status, deanon_ratio, error_msg, timestamp, mem_usage)

telegram_bot_sendtext(get_status())
