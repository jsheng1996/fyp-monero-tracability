import requests
import os
import subprocess
import locale
import datetime

cmd1 = ['pgrep', '-f', 'anon_analysis.py']

#Function to check if process is running
def check_proc(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    return o.decode('ascii')!=''

if not check_proc(cmd1):
    with open('/home/VMadmin/data/progress.txt') as file:
        n = int(file.readline())
    file.close()
    if n!=1980622:
        os.system('python /home/VMadmin/data/anon_analysis_cleanup.py')
        os.system('python /home/VMadmin/data/anon_analysis.py &> anon_analysis.out &')

        with open("/home/VMadmin/data/logs/restart_log2", 'a') as file:
            file.write("Restart at {}\n".format(datetime.datetime.now()))
        file.close()
    else:
        pass
