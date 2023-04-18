from config import *
from api import *

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods = ['GET'])
def webMain(path):    
    try:
        validateSession = api_validateSession()

        if validateSession == 1:
            return render_template("/index.html") 
        
        return render_template("/auth/index.html")
    except Exception as e:
        api_saveLog("log/api-error.txt", e, sys.exc_info()[-1].tb_lineno)
        return "ENIGMA"

@app.route("/api/v1/security/token/csrf", methods = ["POST"])
@csrf.exempt
def api_securityTKCSRF():    
    return json.dumps({"success": True, "token":  generate_csrf()}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)