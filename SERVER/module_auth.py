import time
import random

# authentication timeout in minutes
login_timeout = 10
# authentication cookies list (cookie:time)
login_cookie = dict()
# authentication attempt timeout list (IP:time)
login_limit = dict()


def delta_mins(tstamp1, tstamp2):
    td = tstamp2 - tstamp1
        
    return int(round(td / 60))
    
# Check if authentication attempt timeout is reached for given IP
def check_rate(ip):
    if ip in login_limit:
        if delta_mins(login_limit[ip], time.time()) < 2:
            return True
    
    login_limit[ip] = time.time()
    
    return False

# Checks if login cookie is set and is not timed out. If timed out, forcefully removes it
def check_login(cook):
    if cook in login_cookie:
        to = delta_mins(login_cookie[cook], time.time())

        if to < login_timeout:
            return True
        else: # Timed out
            del login_cookie[cook]
            
    return False

# Adds a new login cookie to entry
def add_login():
    cook = random.getrandbits(32)
    while cook in login_cookie:
        cook = random.getrandbits(32)
    
    cook = str(cook)
    print(cook + " logged in.");
    login_cookie[cook] = time.time()
    return cook
