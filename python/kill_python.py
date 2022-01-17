#杀掉python程序
import psutil
import os
pids = psutil.pids()
for pid in pids:
    p = psutil.Process(pid)
    # print('pid-%s,pname-%s' % (pid, p.name()))
    if p.name() == 'python.exe':
        cmd = 'taskkill /F /IM python.exe'
        os.system(cmd)
