# MineRigCtrl client 
# AngryKirC, 2021
# maybe it was a better idea to implement multiple jobs support instead of a 'satellite' for a single software instance?
from requests import post, get
from platform import node
import time 
from subprocess import call, Popen
from os import path, _exit
import enum
#import msgpack

class MinerSoftware(enum.IntEnum):
    NONE = 0
    LOLMINER = 1

class rig_config:
    def __init__(self):
        # Incrementing version marker (changed by server whenever there is a change in rig config)
        self.rig_config_ver = 0
        # Interval, in seconds, before each 'update data' message to the server
        self.update_time = 5
        # Miner software to be run 
        self.software = MinerSoftware.NONE
        # Coin or Algorithm
        self.miner_alg = ""
        # Pool address
        self.miner_pool = ""
        # Pool user
        self.miner_user = ""
        # Miner custom settings
        self.miner_cmd = ""
    
# Protocol version marker
mrc_client_version = 2
# Control Server URL
mrc_server_url = "http://battlecruiser.lan:8001/rigcb"
# Shared Secret must be same for client and server
mrc_shared_secret = "321"
# LolMiner API URL
lolminer_api_url = "http://127.0.0.1:7321/"
# LolMiner executable path
lolminer_path = "/home/miner/lolminer/lolMiner"

# Unique ID of this rig
rig_id = node()
# Pointer to current configuration
config = rig_config()
# Pointer to mining software process
miner_process = None
# Start time of miner software
miner_start_time = 0
# Last error description (human readable)
lasterror = ""
# True to enable mining software
enable_mining = True

def change_hostname(name):
    call(['hostname', name])
    
def update_config_from_server(json):
    if "new_config_ver" in json:
        ver = int(json["new_config_ver"])
        if ver > config.rig_config_ver:
            # Update config
            config.rig_config_ver = ver
            config.update_time = int(json["update_time"])
            config.software = MinerSoftware(int(json["software"]))
            config.miner_alg = json["miner_alg"]
            config.miner_pool = json["miner_pool"]
            config.miner_user = json["miner_user"]
            config.miner_cmd = json["miner_cmd"] 
    
def parse_server_action(json):
    global miner_process
    if "action" in json:
        a = json["action"]
        print("got command: " + a)
        if a == "pause":
            if miner_process != None:
                miner_process.kill()
                time.sleep(1)
                
            enable_mining = False
            
        elif a == "start":
            enable_mining = True
            
        elif a == "reboot":
            if miner_process != None:
                miner_process.kill()
                time.sleep(1)
                
            call("reboot") # systemctl reboot -i"
            _exit(0)

def try_launch_miner():
    global miner_process
    # If mining is enabled by server
    if miner_process == None and config.rig_config_ver > 0:
        # Miner was not started yet, and configuration is already obtained from server
        if config.software == MinerSoftware.LOLMINER:
            a = [lolminer_path, "--algo", config.miner_alg, "--pool", config.miner_pool, "--user", config.miner_user, "--apiport", "7321", config.miner_cmd]
            miner_process = Popen(a)
            miner_start_time = time.time()
    
def is_miner_active():
    if miner_process == None:
        return False
        
    if miner_process.poll() == None:
        return True
        
    return False
    
def try_collect_miner_log():
    d = None
    try:
        a = get(url=lolminer_api_url)
        d = a.json()
    except: 
        print("error while trying to collect data from miner API")
        return None
        
    r = dict()
    # New api
    if "Software" in d:
        r["sw"] = d["Software"]
        
    if "Session" in d:
        sess = d["Session"]
        if "Startup" in sess:
            r["st"] = sess["Startup"]
        if "Uptime" in sess:
            r["up"] = sess["Uptime"]
    
    if "Workers" in d:
        r["ws"] = d["Workers"]
    
    if "Algorithms" in d:
        r["as"] = d["Algorithms"]
        
    return r

print("RigMon client started")

# Main loop
while True:
    # Report to server first 
    j = dict()
    j["version"] = mrc_client_version
    j["shared"] = mrc_shared_secret
    j["rig_id"] = rig_id
    j["config_ver"] = config.rig_config_ver
    j["lasterror"] = lasterror
    j["active"] = is_miner_active()
    j["start_time"] = miner_start_time
    # Iterate GPUS
    r = try_collect_miner_log()
    if r != None:
        j.update(r)
    
    resp = None
    try:
        resp = post(url=mrc_server_url, json=j)
    except:
        print("Failed to connect to monitoring server!")
        
    if resp != None:
        if resp.status_code != 200:
            print("server reports status code != 200, it is " + str(resp.status_code))
        else:
            d = resp.json()
            # Fetch new config data if present
            update_config_from_server(d)
            # Fetch an order/action for the miner if present
            parse_server_action(d)
            # Start mining software
            if enable_mining:
                try_launch_miner()
    
    time.sleep(config.update_time)