# Home web page server
# AngryKirC, 2021
from bottle import Bottle, static_file, template, request, response, redirect, abort
from sys import argv
from server_rigmon import rigmonApp

# Server Port and Interface(IP)
my_host = "0.0.0.0"
my_port = 8001

def gen_error(error):
    return template("error", status = error.status_code, text = error.body)

class CustomizeBottle(Bottle):
    def default_error_handler(self, error):
        return gen_error(error)
        
mainApp = CustomizeBottle()

@mainApp.route("/static/<filename:path>", method="GET")
def send_static(filename):
    return static_file(filename, root="./static/")
    
@mainApp.get("/favicon.ico")
def send_favicon():
    return static_file("favicon.ico", root="./static/")
    
@mainApp.get("/")
def slash_main():
    return template("main_page")

# if -test parameter is given, run tests only
def is_test_run():
    if "-test" in argv:
        return True
    return False

if __name__ == "__main__":
    if not is_test_run():
        # start web server
        mainApp.merge(rigmonApp)
        mainApp.run(server="waitress", host=my_host, port=my_port)
