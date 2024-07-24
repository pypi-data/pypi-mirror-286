from NanonisClass import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(('10.0.0.37', 6501))
test = Nanonis(s)
test.returnDebugInfo(0)
print((test.OneDSwp_LimitsGet()[2])[1])
