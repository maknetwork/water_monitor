import subprocess
p = subprocess.Popen(['ping','192.168.0.101','-c','1'])
# Linux Version p = subprocess.Popen(['ping','127.0.0.1','-c','1',"-W","2"])
# The -c means that the ping will stop afer 1 package is replied
# and the -W 2 is the timelimit
p.wait()
if p.poll():
    print(" is down")
else:
    print(" is up")
