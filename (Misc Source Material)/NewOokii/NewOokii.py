i=3164

import os, time

os.system("rm 1")
os.system("rm 2")
os.system("rm 3")
t=time.time()
os.system('wget --post-data="[]\n" http://ookii.org/api/egscomicapi/1')
while time.time()<(t+1):
    print("I wait")
t=time.time()
os.system('wget --post-data="[]\n" http://ookii.org/api/egscomicapi/2')
while time.time()<(t+1):
    print("I wait")
t=time.time()
os.system('wget --post-data="[]\n" http://ookii.org/api/egscomicapi/3')
while time.time()<(t+1):
    print("I wait")
t=time.time()

while 1:
    os.system("wget http://ookii.org/api/egscomicapi/%d"%i)
    i+=1
    while time.time()<(t+1):
        print("I wait")
    t=time.time()