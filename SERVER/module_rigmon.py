from datetime import datetime
from time import time
import enum

rigs = dict()

def get_all_rigs():
    return rigs.values()

def check_rig_exists(name):
    if name in rigs:
        return True
    return False
    
def add_new_rig(name):
    r = monitor_rig_data()
    rigs[name] = r
    return r
    
# Returns Rig class by its hostname, or None if not present
def get_rig_by_name(name):
    if not name in rigs:
        return None
        
    return rigs[name]
    
def build_response(rig, num):
    s = dict()
    s["result"] = num
    c = rig.config
    if rig.config_ver == 0:
        s["new_config_ver"] = 1
        s["update_time"] = c.update_time
        s["software"] = c.software.value
        s["miner_alg"] = c.miner_alg
        s["miner_pool"] = c.miner_pool
        s["miner_user"] = c.miner_user
        s["miner_cmd"] = c.miner_cmd
    
    if rig.command != "":
        s["action"] = rig.command
        rig.command = "" # reset command/action
        
    return s

def get_test_config():
    config = stored_rig_data()
    config.update_time = 5
    config.software = MinerSoftware.LOLMINER
    config.miner_alg = "ETHASH"
    config.miner_pool = "stratum+ssl://ru.ezil.me:2443"
    config.miner_user = "0x61d7868ca9a1e4e873db2508dac7768a6b950d76.test2"
    config.miner_cmd = ""
    return config

def process_request(m, j):
    # parse overall stats
    m.client_ver = j["version"]
    m.hostname = j["rig_id"]
    m.config_ver = j["config_ver"]
    m.lasterror = j["lasterror"]
    m.miner_active = j["active"]
    m.start_time = j["start_time"]
    # parse miner stats
    if "sw" in j:
        print("parsing SW")
        m.software = j["sw"]
    if "st" in j:
        print("parsing ST")
        m.miner_start_time = j["st"]
        m.uptime = j["up"]
    if "ws" in j and "as" in j:
        print("parsing WS+AS")
        if len(j["as"]) > 0:
            alg = j["as"][0]
            m.pool = alg["Pool"]
            hr = alg["Worker_Performance"]
            ac = alg["Worker_Accepted"]
            rj = alg["Worker_Rejected"]
            st = alg["Worker_Stales"]
            er = alg["Worker_Errors"]
            n = 0
            m.clear_all_gpus()
            for i in j["ws"]:
                mgd = monitor_gpu_data()
                mgd.name = i["Name"]
                mgd.power = round(i["Power"], 2)
                mgd.core_temp = i["Core_Temp"]
                mgd.fan_speed = i["Fan_Speed"]
                mgd.pcie_address = i["PCIE_Address"]
                mgd.hashrate = round(hr[n], 2)
                mgd.accepted = ac[n]
                mgd.rejected = rj[n]
                mgd.stales = st[n]
                mgd.errors = er[n]
                mgd.cclk = i["CCLK"]
                mgd.mclk = i["MCLK"]
                n = n + 1
                m.gpus.append(mgd)
    
class MinerSoftware(enum.IntEnum):
    NONE = 0
    LOLMINER = 1
    
class stored_rig_data:
    def __init__(self):
        #self.hostname = "rig"
        self.update_time = 5
        self.software = MinerSoftware.NONE
        self.miner_alg = ""
        self.miner_pool = ""
        self.miner_user = ""
        self.miner_cmd = ""
    
class monitor_gpu_data:
    def __init__(self):
        self.name = ""
        self.power = 0
        self.core_temp = 0
        self.fan_speed = 0
        self.pcie_address = ""
        self.hashrate = 0
        self.accepted = 0
        self.rejected = 0
        self.stales = 0
        self.errors = 0
        self.cclk = 0
        self.mclk = 0

class monitor_rig_data: 
    def __init__(self):
        self.gpus = []
        # acquired from client
        self.client_ver = 0
        self.lasterror = ""
        self.miner_active = False
        self.hostname = "rig"
        self.software = ""
        self.start_time = 0
        self.miner_start_time = 0
        self.uptime = 0
        self.last_seen = 0
        self.pool = ""
        self.last_ip = ""
        self.config_ver = 0
        # from sql
        self.config = get_test_config()
        # transferred back to client
        self.command = ""
    
    def get_human_start_time(self):
        return datetime.fromtimestamp(self.miner_start_time).strftime('%Y-%m-%d %H:%M:%S')
        
    def get_human_last_seen(self):
        return datetime.fromtimestamp(self.last_seen).strftime('%Y-%m-%d %H:%M:%S')

    def get_total_hashrate(self):
        t = 0
        for g in self.gpus:
            t += g.hashrate
        return round(t, 2)
        
    def get_total_power(self):
        t = 0
        for g in self.gpus:
            t += g.power
        return round(t, 2)
        
    def count_gpus(self):
        return len(self.gpus)
        
    def get_human_total_hashrate(self):
        return "{} ({} GPUs)".format(self.get_total_hashrate(), self.count_gpus())
        
    def clear_all_gpus(self):
        self.gpus.clear()
        
    def update_last_seen(self):
        self.last_seen = time()


