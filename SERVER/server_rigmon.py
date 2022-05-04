# Mining rig monitor server 
# AngryKirC, 2021
from bottle import Bottle, static_file, template, request, response, redirect, abort
from module_auth import check_login, check_rate, add_login
from module_rigmon import get_all_rigs, check_rig_exists, add_new_rig, get_rig_by_name, build_response, process_request

rigmonApp = Bottle()

# Shared Secret must be same for client and server
shared_secret = "321"
# Protocol version marker
server_version = 2
# UI password (hardcoded yea)
server_password = "123"

@rigmonApp.post("/login2")
def process_login():
    cook = request.get_cookie("auth")
    if check_login(cook):
        response.status = 200
        return "Already logged in!"
    else:
        if check_rate(request.environ.get("REMOTE_ADDR")):
            abort(429, "too many requests")
    
        passw = request.forms.get("pass")
        if passw == server_password: 
            response.set_cookie("auth", add_login())
            response.status = 200
            return "You logged in!"
            
    abort(401, "invalid password")

@rigmonApp.get("/login")
def do_login():
    return template("login_page")
    
@rigmonApp.get("/rig_config")
def do_config():
    if not "r" in request.query:
        abort(400, "no rig name provided")

    # Auth wall
    cook = request.get_cookie("auth")
    if not check_login(cook):
        redirect("/login?r=rigs")
        return ""
        
    rigname = request.query["r"]
    if not check_rig_exists(rigname):
        abort(400, "specified rig does not exist")
    
    rig = get_rig_by_name(rigname)
    return template("rig_settings", rg = rig, gs = rig.gpus)
    
@rigmonApp.get("/rigs")
def do_rigs():
    cook = request.get_cookie("auth")
    if not check_login(cook):
        redirect("/login?r=rigs")
        return ""
    
    return template("rigs_page", rs = get_all_rigs())

@rigmonApp.post("/rigcb")
def rig_callback():
    rig_json = request.json
    rig_ver = rig_json["version"]
    if rig_ver < server_version:
        print("outdated client called rigcb! v." + str(rig_ver))
        abort(401, "outdated client")
        
    rig_host = rig_json["rig_id"]
    rig_sec = rig_json["shared"]
    if rig_sec == shared_secret:
        r = get_rig_by_name(rig_host) 
        if not check_rig_exists(rig_host):
            r = add_new_rig(rig_host)
        
        process_request(r, rig_json)
        r.update_last_seen()
        r.last_ip = request.environ.get("REMOTE_ADDR")
        return build_response(r, 1)
    else:
        abort(401, "bad secret")
        
    abort(400, "bad runtime logic")
    
@rigmonApp.get("/rig_setcmd")
def rig_set_command():
    if not "r" in request.query:
        abort(400, "no rig name provided")
        
    if not "c" in request.query:
        abort(400, "no command provided")

    # Auth wall
    cook = request.get_cookie("auth")
    if not check_login(cook):
        redirect("/login?r=rigs")
        return ""
        
    rigname = request.query["r"]
    if not check_rig_exists(rigname):
        abort(400, "specified rig does not exist")
    
    rig = get_rig_by_name(rigname)
    # If no command had been already scheduled, set a new one
    if rig.command == "":
        rig.command = request.query["c"]
        return "ok"
    else:
        return "fail"