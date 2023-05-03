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

@app.route('/api/v1/ticket/<sa_id>', methods = ['GET'])
def api_ticket(sa_id):    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT sa_sales.*, DATE_FORMAT(sa_sales.sa_date, '%%d/%%m/%%Y %%h:%%i %%p') AS sa_date_2, lo_locations.lo_name, us_users.us_fullname FROM sa_sales INNER JOIN lo_locations ON lo_locations.lo_id = sa_sales.lo_id INNER JOIN us_users ON us_users.us_id = sa_sales.us_id WHERE sa_sales.sa_id = %s AND st_id = %s",(sa_id,366175,))
        sale = cur.fetchone()
        cur.close()

        if sale is None:
            return json.dumps({"success": True, "msg":  "La venta no se encontro"}), 200
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT sd_saledetails.*, pr_products.pr_name, ca_categories.ca_name FROM sd_saledetails INNER JOIN pr_products ON pr_products.pr_id = sd_saledetails.pr_id INNER JOIN ca_categories ON ca_categories.ca_id = pr_products.ca_id WHERE sd_saledetails.sa_id = %s",(sa_id,))
        saledetails = cur.fetchall()
        cur.close()

        total = 0
        for saledetail in saledetails:
            total = total + (saledetail["sd_quantity"] * saledetail["sd_price"])
        
        return render_template("/home/ticket.html", sale = sale, saledetails = saledetails, total = total)
    except Exception as e:
        api_saveLog("log/api-error.txt", e, sys.exc_info()[-1].tb_lineno)
        return "ENIGMA"

@app.route("/api/v1/security/token/csrf", methods = ["POST"])
@csrf.exempt
def api_securityTKCSRF():    
    return json.dumps({"success": True, "token":  generate_csrf()}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)