from config import *

@app.route("/api/v1/", defaults={"path": ""})
@app.route("/api/v1/<path:path>", methods = ["POST"])
def apiV4(path):      
    try:
        splitURL0 = api_splitURL(path,0)
        splitURL1 = api_splitURL(path,1)
        splitURL2 = api_splitURL(path,2)
        splitURL3 = api_splitURL(path,3)
        splitURL4 = api_splitURL(path,4)
        splitURL5 = api_splitURL(path,5)
        splitURL6 = api_splitURL(path,6)
        splitURL7 = api_splitURL(path,7)
        splitURL8 = api_splitURL(path,8)

        date_today_sql = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        date_now = datetime.now()
        v_useragent = api_userAgent(request)
        useragent = v_useragent["UserAgent"]
        validateSession = api_validateSession()
    
        if splitURL0 == "web":
            if validateSession == 0:
                if splitURL1 == "data":
                    if splitURL2 == "auth":
                        if splitURL3 == "sign-in" and splitURL4 is None:
                            if "email" not in request.form or len(request.form["email"]) <= 0:
                                return json.dumps({"success": False, "code": 200, "msg": "Email is empty."}), 200
                            elif "pass" not in request.form or len(request.form["pass"]) <= 0:
                                return json.dumps({"success": False, "code": 200, "msg": "Password is empty."}), 200                        

                            email = request.form["email"].lower()
                            passw = request.form["pass"]
                            
                            password_1 = hashlib.md5(passw.encode('utf-8')).hexdigest()
                            password_2 = hashlib.md5(password_1.encode('utf-8')).hexdigest()

                            cur = mysql.connection.cursor()
                            cur.execute("SELECT us_users.* FROM us_users WHERE us_users.us_email = %s AND us_users.us_password = %s",(email,password_2,))
                            userInfo = cur.fetchone()
                            cur.close()

                            if userInfo is None:
                                return json.dumps({"success": False, "code": 200, "msg": "¡Correo electrónico o contraseña incorrectos! Por favor verifíquelo e intenté de nuevo."}), 200   

                            sess_id = str(uuid.uuid1())

                            cur = mysql.connection.cursor()
                            cur.execute("INSERT INTO sess_usersessions(sess_id, sess_useragent, us_id) VALUES(%s, %s, %s)",(sess_id, useragent, userInfo["us_id"],))
                            mysql.connection.commit()
                            cur.close()

                            session["us_id"] = userInfo["us_id"]
                            session["sess_id"] = sess_id

                            return json.dumps({"success": True, "code": 200, "msg": "¡Inicio de sesión correcto! Bienvenido/a."}), 200 

                    return json.dumps({"success": False, "code": 404, "msg": "Page not found."}), 404            
            elif validateSession == 1:
                if splitURL1 == "data":
                    if splitURL2 == "pos":
                        if splitURL3 == "products": 
                            if splitURL4 is None:
                                return render_template("/widget/posproducts.html")
                            elif splitURL4 == "add" and splitURL5 is None:
                                if "sa_no" not in request.form or len(request.form["sa_no"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El numero del recibo está vacío! Llene el campo."}), 200 
                                elif "id" not in request.form or len(request.form["id"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El ID del producto está vacío! Llene el campo."}), 200   
                                elif "quantity" not in request.form or len(request.form["quantity"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La cantidad está vacía! Llene el campo."}), 200                     

                                sa_no = request.form["sa_no"]
                                pr_id = request.form["id"]
                                sd_quantity = request.form["quantity"]

                                if sd_quantity.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Cantidad es incorrecta! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT sa_sales.* FROM sa_sales WHERE sa_sales.sa_no = %s AND sa_sales.st_id = %s",(sa_no,27843,))
                                sale = cur.fetchone()
                                cur.close()

                                if sale is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡No se encontró la venta! Contacte a un administrador."}), 200                 

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT pr_products.* FROM pr_products WHERE pr_products.pr_id = %s AND pr_products.pr_status = %s",(pr_id,1,))
                                product = cur.fetchone()
                                cur.close()

                                if product is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡No se encontró el producto! Contacte a un administrador."}), 200   

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT sd_saledetails.* FROM sd_saledetails WHERE sd_saledetails.pr_id = %s AND sd_saledetails.sa_id = %s",(pr_id,sale["sa_id"],))
                                saledetail = cur.fetchone()
                                cur.close()

                                if saledetail is None:
                                    cur = mysql.connection.cursor()
                                    cur.execute("INSERT INTO sd_saledetails(sd_price, sd_quantity, sa_id, pr_id) VALUES(%s, %s, %s, %s)",(product["pr_price"],sd_quantity,sale["sa_id"],pr_id,))
                                    mysql.connection.commit()
                                    cur.close()
                                else:
                                    cur = mysql.connection.cursor()
                                    cur.execute("UPDATE sd_saledetails SET sd_quantity = sd_quantity + %s WHERE pr_id = %s AND sa_id = %s",(sd_quantity,pr_id,sale["sa_id"],))
                                    mysql.connection.commit()
                                    cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El producto se agregó correctamente."}), 200
                            elif splitURL4 == "edit" and splitURL5 is None:
                                if "sa_no" not in request.form or len(request.form["sa_no"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El numero del recibo está vacío! Llene el campo."}), 200 
                                elif "id" not in request.form or len(request.form["id"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El ID del producto está vacío! Llene el campo."}), 200   
                                elif "quantity" not in request.form or len(request.form["quantity"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La cantidad está vacía! Llene el campo."}), 200                     

                                sa_no = request.form["sa_no"]
                                sd_id = request.form["id"]
                                sd_quantity = request.form["quantity"]

                                if api_isfloat(sd_quantity) is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Cantidad es incorrecta! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                sd_quantity = float(sd_quantity)

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT sa_sales.* FROM sa_sales WHERE sa_sales.sa_no = %s AND sa_sales.st_id = %s",(sa_no,27843,))
                                sale = cur.fetchone()
                                cur.close()

                                if sale is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡No se encontró la venta! Contacte a un administrador."}), 200                   

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT sd_saledetails.* FROM sd_saledetails WHERE sd_saledetails.sd_id = %s AND sd_saledetails.sa_id = %s",(sd_id,sale["sa_id"],))
                                saledetail = cur.fetchone()
                                cur.close()

                                if sd_quantity <= 0:
                                    cur = mysql.connection.cursor()
                                    cur.execute("DELETE FROM sd_saledetails WHERE sd_id = %s AND sa_id = %s",(sd_id,sale["sa_id"],))
                                    mysql.connection.commit()
                                    cur.close()
                                else:
                                    cur = mysql.connection.cursor()
                                    cur.execute("UPDATE sd_saledetails SET sd_quantity = %s WHERE sd_id = %s AND sa_id = %s",(sd_quantity,sd_id,sale["sa_id"],))
                                    mysql.connection.commit()
                                    cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El producto se agregó correctamente."}), 200                            

                        elif splitURL3 == "fin" and splitURL4 is None:
                            if "sa_no" not in request.form or len(request.form["sa_no"]) <= 0:
                                return json.dumps({"success": False, "code": 200, "msg": "¡El numero del recibo está vacío! Llene el campo."}), 200 
                            elif "location" not in request.form or len(request.form["location"]) <= 0:
                                return json.dumps({"success": False, "code": 200, "msg": "¡La sucursal está vacía! Llene el campo."}), 200   
                            elif "paymentmethod" not in request.form or len(request.form["paymentmethod"]) <= 0:
                                return json.dumps({"success": False, "code": 200, "msg": "¡El metodo de pago esta vacío! Llene el campo."}), 200    
                            elif "pay" not in request.form or len(request.form["pay"]) <= 0:
                                return json.dumps({"success": False, "code": 200, "msg": "¡La cantidad está vacía! Llene el campo."}), 200                     

                            sa_no = request.form["sa_no"]
                            location = request.form["location"]
                            paymentmethod = request.form["paymentmethod"] 
                            pay = request.form["pay"] 

                            if api_isfloat(pay) is False:
                                return json.dumps({"success": False, "code": 200, "msg": "¡El pago es incorrecto! Verifíquelo e intente de nuevo."}), 200   

                            pay = float(pay)

                            cur = mysql.connection.cursor()
                            cur.execute("SELECT lo_locations.* FROM lo_locations WHERE lo_locations.lo_id = %s AND lo_locations.lo_status = %s",(location,1,))
                            locations = cur.fetchone()
                            cur.close()

                            if locations is None:
                                return json.dumps({"success": False, "code": 200, "msg": "¡No se encontró la sucursal! Contacte a un administrador."}), 200    

                            cur = mysql.connection.cursor()
                            cur.execute("SELECT pm_paymentmethods.* FROM pm_paymentmethods WHERE pm_paymentmethods.pm_id = %s AND pm_paymentmethods.pm_status = %s",(paymentmethod,1,))
                            paymentmethods = cur.fetchone()
                            cur.close()

                            if paymentmethods is None:
                                return json.dumps({"success": False, "code": 200, "msg": "¡No se encontró el metodo de pago! Contacte a un administrador."}), 200    
                            
                            cur = mysql.connection.cursor()
                            cur.execute("SELECT sa_sales.* FROM sa_sales WHERE sa_sales.sa_no = %s AND sa_sales.st_id = %s",(sa_no,27843,))
                            sale = cur.fetchone()
                            cur.close()

                            if sale is None:
                                return json.dumps({"success": False, "code": 200, "msg": "¡No se encontró la venta! Contacte a un administrador."}), 200   

                            cur = mysql.connection.cursor()
                            cur.execute("SELECT sd_saledetails.* FROM sd_saledetails WHERE sd_saledetails.sa_id = %s",(sale["sa_id"],))
                            saledetails = cur.fetchall()
                            cur.close()

                            if saledetails is None or len(saledetails) <= 0:
                                return json.dumps({"success": False, "code": 200, "msg": "¡No se encontró articulos en la venta! Verifíquelo e intente de nuevo."}), 200 

                            total = 0
                            for saledetail in saledetails:
                                total = total + (saledetail["sd_quantity"] * saledetail["sd_price"]) 

                            if pay < total:
                                return json.dumps({"success": False, "code": 200, "msg": "¡No se completó la venta! Verifique con cuanto pago."}), 200 

                            cur = mysql.connection.cursor()
                            cur.execute("UPDATE sa_sales SET sa_pay = %s, pm_id = %s, lo_id = %s, st_id = %s, sa_date = %s WHERE sa_id = %s",(pay, paymentmethod, location, 366175, date_today_sql, sale["sa_id"],))
                            mysql.connection.commit()
                            cur.close()
                            
                            return json.dumps({"success": True, "code": 200, "msg": "Venta finalizada correctamente."}), 200 

                    if splitURL2 == "admin":
                        if splitURL3 == "users":
                            if splitURL4 == "add" and splitURL5 is None:
                                if "fullname" not in request.form or len(request.form["fullname"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre completo está vacío! Llene el campo."}), 200   
                                elif "email" not in request.form or len(request.form["email"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El correo electrónico está vacío! Llene el campo."}), 200     
                                elif "pass" not in request.form or len(request.form["pass"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La contraseña está vacía! Llene el campo."}), 200 
                                elif "address" not in request.form or len(request.form["address"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La dirección está vacía! Llene el campo."}), 200  
                                elif "city" not in request.form or len(request.form["city"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La ciudad está vacía! Llene el campo."}), 200                    

                                us_fullname = request.form["fullname"]
                                us_email = request.form["email"]
                                us_password = request.form["pass"]
                                ad_id = str(random.randint(100000,999999))
                                ad_address = request.form["address"]
                                ci_id = request.form["city"]

                                if ci_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID de la ciudad incorrecta! Por favor verifíquela e intenté de nuevo."}), 200 

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT ci_cities.* FROM ci_cities WHERE ci_cities.ci_id = %s AND ci_status = %s",(ci_id,1,))
                                city = cur.fetchone()
                                cur.close()

                                if city is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡No se encontro la ciudad! Por favor verifíquelo e intenté de nuevo."}), 200

                                password_1 = hashlib.md5(us_password.encode('utf-8')).hexdigest()
                                password_2 = hashlib.md5(password_1.encode('utf-8')).hexdigest()

                                cur = mysql.connection.cursor()
                                cur.execute("INSERT INTO ad_addresses(ad_id, ad_address, ci_id) VALUES(%s, %s, %s)",(ad_id, ad_address, ci_id,))
                                mysql.connection.commit()
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("INSERT INTO us_users(us_id, us_fullname, us_email, us_password, ad_id, tu_id) VALUES(%s, %s, %s, %s, %s, %s)",(api_uniKey(), us_fullname, us_email, password_2, ad_id, 693004,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El usuario se agregó correctamente."}), 200 
                            if splitURL4 == "edit" and splitURL5 is None:
                                if "id" not in request.form or len(request.form["id"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El ID del usuario está vacío! Llene el campo."}), 200   
                                elif "typeuser" not in request.form or len(request.form["typeuser"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El tipo de usuario está vacío! Llene el campo."}), 200   
                                elif "fullname" not in request.form or len(request.form["fullname"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre completo está vacío! Llene el campo."}), 200   
                                elif "email" not in request.form or len(request.form["email"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El correo electrónico está vacío! Llene el campo."}), 200     
                                elif "address" not in request.form or len(request.form["address"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La dirección está vacía! Llene el campo."}), 200  
                                elif "city" not in request.form or len(request.form["city"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La ciudad está vacía! Llene el campo."}), 200           
                                
                                if "status" not in request.form or len(request.form["status"]) <= 0:
                                    us_status = 0    
                                else:
                                    us_status = request.form["status"]           

                                us_id = request.form["id"]
                                tu_id = request.form["typeuser"]
                                us_fullname = request.form["fullname"]
                                us_email = request.form["email"]
                                ad_address = request.form["address"]
                                ci_id = request.form["city"] 

                                userInfo = api_userInfo(us_id)

                                if userInfo is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Usuario no encontrado! Por favor verifíquelo e intenté de nuevo."}), 200 
                                elif tu_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID del tipo de usuario incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200 
                                elif ci_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID de la ciudad incorrecta! Por favor verifíquela e intenté de nuevo."}), 200 
                                
                                ad_id = userInfo["ad_id"]
                                
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT tu_typesusers.* FROM tu_typesusers WHERE tu_typesusers.tu_id = %s",(tu_id,))
                                typeuser = cur.fetchone()
                                cur.close()

                                if typeuser is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡No se encontro el tipo de usuario! Por favor verifíquelo e intenté de nuevo."}), 200
                                
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT ci_cities.* FROM ci_cities WHERE ci_cities.ci_id = %s AND ci_status = %s",(ci_id,1,))
                                city = cur.fetchone()
                                cur.close()

                                if city is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡No se encontro la ciudad! Por favor verifíquelo e intenté de nuevo."}), 200

                                if "pass" not in request.form or len(request.form["pass"]) <= 0:
                                    password_2 = userInfo["us_password"]
                                else:                 
                                    us_password = request.form["pass"]           
                                    password_1 = hashlib.md5(us_password.encode('utf-8')).hexdigest()
                                    password_2 = hashlib.md5(password_1.encode('utf-8')).hexdigest()

                                cur = mysql.connection.cursor()
                                cur.execute("UPDATE ad_addresses SET ad_address = %s, ci_id = %s WHERE ad_id = %s",(ad_address, ci_id, ad_id,))
                                mysql.connection.commit()
                                cur.close()

                                if us_status == "on":
                                    us_status = 1
                                else:
                                    us_status = 0

                                cur = mysql.connection.cursor()
                                cur.execute("UPDATE us_users SET us_fullname = %s, us_email = %s, us_password = %s, us_status = %s, tu_id = %s WHERE us_id = %s",(us_fullname, us_email, password_2, us_status, tu_id, us_id,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El usuario se editó correctamente."}), 200 
                        elif splitURL3 == "products":
                            if splitURL4 == "add" and splitURL5 is None:
                                if "img" not in request.files:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La imagen está vacía! Seleccione alguna."}), 200    
                                elif "category" not in request.form or len(request.form["category"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La categoría está vacía! Llene el campo."}), 200
                                elif "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200
                                elif "price" not in request.form or len(request.form["price"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El precio está vacío! Llene el campo."}), 200                   

                                pr_img = request.files["img"]
                                ca_id = request.form["category"]
                                pr_name = request.form["name"]
                                pr_price = request.form["price"]

                                ext = set(['jpg', 'jpeg'])

                                if pr_img.filename == '':                                                
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La imagen está vacía! Seleccione alguna."}), 200    
                                elif api_allowedFile(pr_img.filename, ext) is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Formato de imagen no soportado! Solo se permite el formato JPG."}), 200    
                                elif api_isfloat(pr_price) is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Precio incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200   
                                
                                pr_price = float(pr_price)

                                uuidName = str(uuid.uuid1())
                                pr_imgname = uuidName + "." + pr_img.filename.rsplit('.', 1)[1].lower()

                                filename = secure_filename(pr_imgname)
                                pr_img.save(os.path.join('static/images/products/', filename))

                                cur = mysql.connection.cursor()
                                cur.execute("INSERT INTO pr_products(pr_id, pr_name, pr_img, pr_price, ca_id) VALUES(%s, %s, %s, %s, %s)",(str(random.randint(100000,999999)),  pr_name, pr_imgname, pr_price, ca_id,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El producto se agregó correctamente."}), 200 
                            if splitURL4 == "edit" and splitURL5 is None:
                                if "img" not in request.files:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La imagen está vacía! Seleccione alguna."}), 200    
                                elif "id" not in request.form or len(request.form["id"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El ID está vacía! Llene el campo."}), 200
                                elif "category" not in request.form or len(request.form["category"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La categoría está vacía! Llene el campo."}), 200
                                elif "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200
                                elif "price" not in request.form or len(request.form["price"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El precio está vacío! Llene el campo."}), 200                   

                                if "status" not in request.form or len(request.form["status"]) <= 0:
                                    pr_status = 0    
                                else:
                                    pr_status = request.form["status"]       

                                pr_img = request.files["img"]
                                pr_id = request.form["id"]
                                ca_id = request.form["category"]
                                pr_name = request.form["name"]
                                pr_price = request.form["price"]

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT pr_products.* FROM pr_products WHERE pr_products.pr_id = %s",(pr_id,))
                                product = cur.fetchone()
                                cur.close()

                                if product is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El producto no existe! Por favor verifíquelo e intenté de nuevo."}), 200
                                elif api_isfloat(pr_price) is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Precio incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200   
                                
                                pr_price = float(pr_price)

                                ext = set(['jpg', 'jpeg'])

                                if pr_img.filename != '':
                                    if api_allowedFile(pr_img.filename, ext) is False:
                                        return json.dumps({"success": False, "code": 200, "msg": "¡Formato de imagen no soportado! Solo se permite el formato JPG."}), 200   
                                    
                                    filename = secure_filename(product["pr_img"])
                                    pr_img.save(os.path.join('static/images/products/', filename)) 

                                if pr_status == "on":
                                    pr_status = 1
                                else:
                                    pr_status = 0   

                                cur = mysql.connection.cursor()
                                cur.execute("UPDATE pr_products SET pr_name = %s, pr_price = %s, pr_status = %s, ca_id = %s WHERE pr_id = %s",(pr_name, pr_price, pr_status, ca_id, pr_id))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El producto se editó correctamente."}), 200 
                        elif splitURL3 == "categories":
                            if splitURL4 == "add" and splitURL5 is None:
                                if "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200                     

                                ca_name = request.form["name"]

                                cur = mysql.connection.cursor()
                                cur.execute("INSERT INTO ca_categories(ca_id, ca_name) VALUES(%s, %s)",(str(random.randint(100000,999999)), ca_name,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "La categoría se agregó correctamente."}), 200 
                            if splitURL4 == "edit" and splitURL5 is None:
                                if "id" not in request.form or len(request.form["id"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El ID está vacío! Llene el campo."}), 200     
                                elif "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200   
                                
                                if "status" not in request.form or len(request.form["status"]) <= 0:
                                    ca_status = 0    
                                else:
                                    ca_status = request.form["status"]                 

                                ca_id = request.form["id"]
                                ca_name = request.form["name"]                                

                                if ca_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200 
                                
                                if ca_status == "on":
                                    ca_status = 1
                                else:
                                    ca_status = 0   

                                cur = mysql.connection.cursor()
                                cur.execute("UPDATE ca_categories SET ca_name = %s, ca_status = %s WHERE ca_id = %s",(ca_name,ca_status,ca_id,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "La categoría se editó correctamente."}), 200 
                        elif splitURL3 == "locations":
                            if splitURL4 == "add" and splitURL5 is None:
                                if "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200
                                elif "city" not in request.form or len(request.form["city"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La ciudad está vacía! Llene el campo."}), 200                     

                                lo_name = request.form["name"]
                                ci_id = request.form["city"]

                                if ci_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID de la ciudad incorrecta! Por favor verifíquela e intenté de nuevo."}), 200 

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT ci_cities.* FROM ci_cities WHERE ci_cities.ci_id = %s AND ci_status = %s",(ci_id,1,))
                                city = cur.fetchone()
                                cur.close()

                                if city is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡No se encontro la ciudad! Por favor verifíquelo e intenté de nuevo."}), 200

                                cur = mysql.connection.cursor()
                                cur.execute("INSERT INTO lo_locations(lo_id, lo_name, ci_id) VALUES(%s, %s, %s)",(str(random.randint(100000,999999)), lo_name, ci_id,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "La ubicación se agregó correctamente."}), 200 
                            if splitURL4 == "edit" and splitURL5 is None:
                                if "id" not in request.form or len(request.form["id"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El ID está vacío! Llene el campo."}), 200     
                                elif "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200
                                elif "city" not in request.form or len(request.form["city"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡La ciudad está vacía! Llene el campo."}), 200   
                                
                                if "status" not in request.form or len(request.form["status"]) <= 0:
                                    lo_status = 0    
                                else:
                                    lo_status = request.form["status"]                 

                                lo_id = request.form["id"]
                                lo_name = request.form["name"]  
                                ci_id = request.form["city"]                              

                                if lo_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200 
                                elif ci_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID de la ciudad incorrecta! Por favor verifíquela e intenté de nuevo."}), 200 

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT ci_cities.* FROM ci_cities WHERE ci_cities.ci_id = %s AND ci_status = %s",(ci_id,1,))
                                city = cur.fetchone()
                                cur.close()

                                if city is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡No se encontro la ciudad! Por favor verifíquela e intenté de nuevo."}), 200
                                
                                if lo_status == "on":
                                    lo_status = 1
                                else:
                                    lo_status = 0   

                                cur = mysql.connection.cursor()
                                cur.execute("UPDATE lo_locations SET lo_name = %s, lo_status = %s, ci_id = %s WHERE lo_id = %s",(lo_name, lo_status, ci_id, lo_id,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "La ubicación se editó correctamente."}), 200 
                        elif splitURL3 == "paymentmethods":
                            if splitURL4 == "add" and splitURL5 is None:
                                if "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200                     

                                pm_name = request.form["name"]

                                cur = mysql.connection.cursor()
                                cur.execute("INSERT INTO pm_paymentmethods(pm_id, pm_name) VALUES(%s, %s)",(str(random.randint(100000,999999)), pm_name,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El método de pago se agregó correctamente."}), 200 
                            if splitURL4 == "edit" and splitURL5 is None:
                                if "id" not in request.form or len(request.form["id"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El ID está vacío! Llene el campo."}), 200     
                                elif "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200   
                                
                                if "status" not in request.form or len(request.form["status"]) <= 0:
                                    pm_status = 0    
                                else:
                                    pm_status = request.form["status"]                 

                                pm_id = request.form["id"]
                                pm_name = request.form["name"]                                

                                if pm_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200 
                                
                                if pm_status == "on":
                                    pm_status = 1
                                else:
                                    pm_status = 0   

                                cur = mysql.connection.cursor()
                                cur.execute("UPDATE pm_paymentmethods SET pm_name = %s, pm_status = %s WHERE pm_id = %s",(pm_name,pm_status,pm_id,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El método de pago se editó correctamente."}), 200 
                        elif splitURL3 == "states":
                            if splitURL4 == "add" and splitURL5 is None:
                                if "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200                     

                                sts_name = request.form["name"]

                                cur = mysql.connection.cursor()
                                cur.execute("INSERT INTO sts_states(sts_id, sts_name) VALUES(%s, %s)",(str(random.randint(100000,999999)), sts_name,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El estado se agregó correctamente."}), 200 
                            if splitURL4 == "edit" and splitURL5 is None:
                                if "id" not in request.form or len(request.form["id"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El ID está vacío! Llene el campo."}), 200     
                                elif "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200   
                                
                                if "status" not in request.form or len(request.form["status"]) <= 0:
                                    sts_status = 0    
                                else:
                                    sts_status = request.form["status"]                 

                                sts_id = request.form["id"]
                                sts_name = request.form["name"]                                

                                if sts_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200 
                                
                                if sts_status == "on":
                                    sts_status = 1
                                else:
                                    sts_status = 0   

                                cur = mysql.connection.cursor()
                                cur.execute("UPDATE sts_states SET sts_name = %s, sts_status = %s WHERE sts_id = %s",(sts_name,sts_status,sts_id,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "El estado se editó correctamente."}), 200 
                        elif splitURL3 == "cities":
                            if splitURL4 == "add" and splitURL5 is None:
                                if "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200   
                                elif "state" not in request.form or len(request.form["state"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El estado está vacío! Llene el campo."}), 200                     

                                ci_name = request.form["name"]
                                sts_id = request.form["state"]

                                if sts_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID del estado incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200 

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT sts_states.* FROM sts_states WHERE sts_states.sts_id = %s AND sts_status = %s",(sts_id,1,))
                                state = cur.fetchone()
                                cur.close()

                                if state is None:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡No se encontro el estado! Por favor verifíquelo e intenté de nuevo."}), 200

                                cur = mysql.connection.cursor()
                                cur.execute("INSERT INTO ci_cities(ci_id, ci_name, sts_id) VALUES(%s, %s, %s)",(str(random.randint(100000,999999)), ci_name, sts_id,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "La ciudad se agregó correctamente."}), 200 
                            if splitURL4 == "edit" and splitURL5 is None:
                                if "id" not in request.form or len(request.form["id"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El ID está vacío! Llene el campo."}), 200     
                                elif "name" not in request.form or len(request.form["name"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El nombre está vacío! Llene el campo."}), 200   
                                elif "state" not in request.form or len(request.form["state"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡El estado está vacío! Llene el campo."}), 200   
                                
                                if "status" not in request.form or len(request.form["status"]) <= 0:
                                    ci_status = 0    
                                else:
                                    ci_status = request.form["status"]                 

                                ci_id = request.form["id"]
                                ci_name = request.form["name"]     
                                sts_id = request.form["state"]                           

                                if ci_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200 
                                elif sts_id.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡ID del estado incorrecto! Por favor verifíquelo e intenté de nuevo."}), 200 
                                
                                if ci_status == "on":
                                    ci_status = 1
                                else:
                                    ci_status = 0   

                                cur = mysql.connection.cursor()
                                cur.execute("UPDATE ci_cities SET ci_name = %s, ci_status = %s, sts_id = %s WHERE ci_id = %s",(ci_name, ci_status, sts_id, ci_id,))
                                mysql.connection.commit()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "msg": "La ciudad se editó correctamente."}), 200 

                    return json.dumps({"success": False, "code": 404, "msg": "Page not found."}), 404   

                if splitURL1 == "widget":
                    if splitURL2 == "dashboard" and splitURL3 is None:
                        return json.dumps({"success": True, "code": 200, "html": render_template("/home/dashboard.html")}), 200 

                    if splitURL2 == "pos":
                        if splitURL3 is None:
                            cur = mysql.connection.cursor()
                            cur.execute("SELECT lo_locations.* FROM lo_locations WHERE lo_locations.lo_status = %s",(1,))
                            locations = cur.fetchall()
                            cur.close() 

                            cur = mysql.connection.cursor()
                            cur.execute("SELECT pm_paymentmethods.* FROM pm_paymentmethods WHERE pm_paymentmethods.pm_status = %s",(1,))
                            paymentmethods = cur.fetchall()
                            cur.close()    
                             
                            while True:                            
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT sa_sales.* FROM sa_sales WHERE us_id = %s AND st_id = %s ORDER BY sa_sales.sa_date DESC LIMIT 1", (session["us_id"], 27843,))
                                sale = cur.fetchone()
                                cur.close()

                                if sale is None:
                                    sa_id = str(uuid.uuid1())
                                    cur = mysql.connection.cursor()
                                    cur.execute("INSERT INTO sa_sales(sa_id, sa_no, sa_date, us_id, st_id) VALUES(%s, %s, %s, %s, %s)",(sa_id, str(random.randint(100000,999999)), date_today_sql, session["us_id"],27843,))
                                    mysql.connection.commit()
                                    cur.close()
                                else:
                                    break
                             
                            return json.dumps({"success": True, "code": 200, "html": render_template("/home/pos.html", sale = sale, locations = locations, paymentmethods = paymentmethods)}), 200  
                        
                        elif splitURL3 == "details" and splitURL4 is None:
                            if "sa_no" not in request.form or len(request.form["sa_no"]) <= 0:
                                return json.dumps({"success": False, "code": 200, "msg": "¡El numero del recibo está vacío! Llene el campo."}), 200              

                            sa_no = request.form["sa_no"]

                            cur = mysql.connection.cursor()
                            cur.execute("SELECT sa_sales.* FROM sa_sales WHERE sa_sales.sa_no = %s AND sa_sales.st_id = %s",(sa_no,27843,))
                            sale = cur.fetchone()
                            cur.close()

                            if sale is None:
                                return json.dumps({"success": False, "code": 200, "msg": "¡No se encontró la venta! Contacte a un administrador."}), 200  
                             
                            cur = mysql.connection.cursor()
                            cur.execute("SELECT sd_saledetails.*, pr_products.pr_name, pr_products.pr_img FROM sd_saledetails INNER JOIN pr_products ON pr_products.pr_id = sd_saledetails.pr_id WHERE sd_saledetails.sa_id = %s", (sale["sa_id"],))
                            saledetails = cur.fetchall()
                            cur.close()

                            total = 0
                            for saledetail in saledetails:
                                total = total + (saledetail["sd_quantity"] * saledetail["sd_price"])

                            return json.dumps({"success": True, "code": 200, "html": render_template("/widget/posdetails.html", saledetails = saledetails), "total": total}), 200  
                        
                        elif splitURL3 == "products":
                            if splitURL4 == "table" and splitURL5 is None:
                                if "search" not in request.form:
                                    return json.dumps({"success": False, "code": 200, "msg": "El buscador está vacío."}), 200
                                elif "page" not in request.form or len(request.form["page"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La página está vacía."}), 200                        

                                search = request.form["search"]
                                page = request.form["page"]
                                quantityShow = 10
                                like = f"%{search}%"   

                                if page.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Página no encontrada! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                page = int(page)

                                if page <= 0:
                                    page = 1

                                page_start = (page - 1) * quantityShow

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT pr_products.*, ca_categories.ca_name FROM pr_products INNER JOIN ca_categories ON ca_categories.ca_id = pr_products.ca_id WHERE pr_products.pr_status = %s AND (pr_products.pr_name LIKE %s OR ca_categories.ca_name LIKE %s) LIMIT %s, %s", (1,like,like,page_start,quantityShow,))
                                products = cur.fetchall()
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM pr_products INNER JOIN ca_categories ON ca_categories.ca_id = pr_products.ca_id WHERE pr_products.pr_status = %s AND (pr_products.pr_name LIKE %s OR ca_categories.ca_name LIKE %s)", (1,like,like,))
                                total = cur.fetchone()["total"]
                                cur.close()

                                pages = math.ceil(total / quantityShow)

                                return json.dumps({"success": True, "code": 200, "html": render_template("/widget/posproducts.html", products = products), "pages": pages}), 200  

                    if splitURL2 == "employee":
                        if splitURL3 == "sales":
                            if splitURL4 is None:
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM sa_sales WHERE sa_sales.st_id = %s", (366175,))
                                totalFin = cur.fetchone()["total"]
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "html": render_template("/employee/sales.html", totalFin = totalFin)}), 200 
                            elif splitURL4 == "table" and splitURL5 is None:
                                if "search" not in request.form:
                                    return json.dumps({"success": False, "code": 200, "msg": "El buscador está vacío."}), 200
                                elif "page" not in request.form or len(request.form["page"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La página está vacía."}), 200                        

                                search = request.form["search"]
                                page = request.form["page"]
                                quantityShow = 10
                                like = f"%{search}%"   

                                if page.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Página no encontrada! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                page = int(page)

                                if page <= 0:
                                    page = 1

                                page_start = (page - 1) * quantityShow

                                columns = ["ID", "Empleado", "Sucursal", "Método de pago", "Fecha de registro", "Estado", "Acciones"]

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT sa_sales.*, DATE_FORMAT(sa_sales.sa_date, '%%d/%%m/%%Y %%H:%%i %%p') AS sa_date_2, us_users.us_fullname, lo_locations.lo_name, pm_paymentmethods.pm_name FROM sa_sales INNER JOIN us_users ON us_users.us_id = sa_sales.us_id LEFT JOIN lo_locations ON lo_locations.lo_id = sa_sales.lo_id LEFT JOIN pm_paymentmethods ON pm_paymentmethods.pm_id = sa_sales.pm_id WHERE sa_sales.sa_id LIKE %s OR sa_sales.sa_no LIKE %s OR sa_sales.sa_date LIKE %s OR us_users.us_fullname LIKE %s OR lo_locations.lo_name LIKE %s OR pm_paymentmethods.pm_name LIKE %s ORDER BY sa_sales.sa_date DESC LIMIT %s, %s", (like, like, like, like, like, like, page_start, quantityShow,))
                                sales = cur.fetchall()
                                cur.close()

                                rows = []
                                for sale in sales:
                                    location = "-"
                                    if sale["lo_id"] is not None:
                                        location = sale["lo_name"]

                                    paymentmethod = "-"
                                    if sale["pm_id"] is not None:
                                        paymentmethod = sale["pm_name"]

                                    status = f"<span class='badge bg-success'><i class='fa-solid fa-check'></i> Venta finalizada</span>"
                                    actions = f"""<button class='btn btn-primary' onclick='openTicket("{sale["sa_id"]}")'><i class='fa-solid fa-file-invoice-dollar'></i> Ticket</button>"""

                                    if sale["st_id"] == 27843:
                                        status = f"<span class='badge bg-warning'><i class='fas fa-spinner fa-pulse'></i> Venta activa</span>"   
                                        actions = ""                                    

                                    rows.append([f"<span class='badge bg-primary'><i class='fa-solid fa-fingerprint'></i> {sale['sa_no']}</span>", sale["us_fullname"], location, paymentmethod, sale["sa_date_2"], status, actions])

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM sa_sales INNER JOIN us_users ON us_users.us_id = sa_sales.us_id LEFT JOIN lo_locations ON lo_locations.lo_id = sa_sales.lo_id LEFT JOIN pm_paymentmethods ON pm_paymentmethods.pm_id = sa_sales.pm_id WHERE sa_sales.sa_id LIKE %s OR sa_sales.sa_no LIKE %s OR sa_sales.sa_date LIKE %s OR us_users.us_fullname LIKE %s OR lo_locations.lo_name LIKE %s OR pm_paymentmethods.pm_name LIKE %s ORDER BY sa_sales.sa_date DESC", (like, like, like, like, like, like,))
                                total = cur.fetchone()["total"]
                                cur.close()

                                pages = math.ceil(total / quantityShow)

                                return json.dumps({"success": True, "code": 200, "html": render_template("/widget/table.html", columns = columns, rows = rows, pages = pages)}), 200
                        
                    if splitURL2 == "admin":
                        if splitURL3 == "users":
                            if splitURL4 is None:
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT ci_cities.*, sts_states.sts_name FROM ci_cities INNER JOIN sts_states ON sts_states.sts_id = ci_cities.sts_id WHERE ci_cities.ci_status = %s",(1,))
                                cities = cur.fetchall()
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT tu_typesusers.* FROM tu_typesusers")
                                typesusers = cur.fetchall()
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM us_users")
                                usersTotal = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM us_users WHERE us_status = %s",(1,))
                                usersTotalOn = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM us_users WHERE us_status = %s",(0,))
                                usersTotalOff = cur.fetchone()["total"]
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "html": render_template("/admin/users.html", usersTotal = usersTotal, usersTotalOn = usersTotalOn, usersTotalOff = usersTotalOff, cities = cities, typesusers = typesusers)}), 200 
                            elif splitURL4 == "table" and splitURL5 is None:
                                if "search" not in request.form:
                                    return json.dumps({"success": False, "code": 200, "msg": "El buscador está vacío."}), 200
                                elif "page" not in request.form or len(request.form["page"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La página está vacía."}), 200                        

                                search = request.form["search"]
                                page = request.form["page"]
                                quantityShow = 10
                                like = f"%{search}%"   

                                if page.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Página no encontrada! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                page = int(page)

                                if page <= 0:
                                    page = 1

                                page_start = (page - 1) * quantityShow

                                columns = ["ID", "Tipo de usuario", "Nombre completo", "Correo electrónico", "Dirección", "Estado", "Fecha de registro", "Acciones"]

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT us_users.*, tu_typesusers.tu_name, ad_addresses.ad_address, ci_cities.ci_id, ci_cities.ci_name, sts_states.sts_name, DATE_FORMAT(us_users.us_regdate, '%%d/%%m/%%Y %%H:%%i:%%s') AS us_regdate_2 FROM us_users INNER JOIN tu_typesusers ON tu_typesusers.tu_id = us_users.tu_id INNER JOIN ad_addresses ON ad_addresses.ad_id = us_users.ad_id INNER JOIN ci_cities ON ci_cities.ci_id = ad_addresses.ci_id INNER JOIN sts_states ON sts_states.sts_id = ci_cities.sts_id WHERE us_users.us_id LIKE %s OR us_users.us_fullname LIKE %s OR us_users.us_email LIKE %s LIMIT %s, %s", (like, like, like, page_start, quantityShow,))
                                users = cur.fetchall()
                                cur.close()

                                rows = []
                                for user in users:
                                    status = f"<span class='badge bg-success'><i class='fa-solid fa-user-check'></i> Activo/a</span>"
                                    if user["us_status"] == 0:
                                        status = f"<span class='badge bg-danger'><i class='fa-solid fa-user-slash'></i> Prohibido/a</span>"                                        

                                    rows.append([f"<span class='badge bg-primary'><i class='fa-solid fa-fingerprint'></i> {user['us_id']}</span>", user["tu_name"],user["us_fullname"], user["us_email"], f"{user['ad_address']}, {user['ci_name']}, {user['sts_name']}", status, user["us_regdate_2"], f"""<button class='btn btn-primary btn-modal' modalclass='modal-edit' onclick='setEdit("{user['us_id']}", "{user['tu_id']}","{user['us_fullname']}", "{user['us_email']}", "{user['us_status']}", "{user['ad_address']}", "{user['ci_id']}")'><i class='fa-solid fa-pen-to-square'></i> Editar</button>"""])

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM us_users INNER JOIN tu_typesusers ON tu_typesusers.tu_id = us_users.tu_id WHERE us_users.us_id LIKE %s OR us_users.us_fullname LIKE %s OR us_users.us_email LIKE %s",(like, like, like,))
                                total = cur.fetchone()["total"]
                                cur.close()

                                pages = math.ceil(total / quantityShow)

                                return json.dumps({"success": True, "code": 200, "html": render_template("/widget/table.html", columns = columns, rows = rows, pages = pages)}), 200
                        elif splitURL3 == "products":
                            if splitURL4 is None:   
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM pr_products")
                                productsTotal = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM pr_products WHERE pr_products.pr_status = %s",(1,))
                                productsTotalOn = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM pr_products WHERE pr_products.pr_status = %s",(0,))
                                productsTotalOff = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT ca_categories.* FROM ca_categories WHERE ca_categories.ca_status = %s",(1,))
                                categories = cur.fetchall()
                                cur.close()                        

                                return json.dumps({"success": True, "code": 200, "html": render_template("/admin/products.html", categories = categories, productsTotal = productsTotal, productsTotalOn = productsTotalOn, productsTotalOff = productsTotalOff)}), 200 
                            elif splitURL4 == "table" and splitURL5 is None:
                                if "search" not in request.form:
                                    return json.dumps({"success": False, "code": 200, "msg": "El buscador está vacío."}), 200
                                elif "page" not in request.form or len(request.form["page"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La página está vacía."}), 200                        

                                search = request.form["search"]
                                page = request.form["page"]
                                quantityShow = 10
                                like = f"%{search}%"   

                                if page.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Página no encontrada! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                page = int(page)

                                if page <= 0:
                                    page = 1

                                page_start = (page - 1) * quantityShow

                                columns = ["Imagen", "ID", "Código de barras", "Nombre", "Categoria", "Precio", "Estado", "Fecha de registro", "Acciones"]

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT pr_products.*, ca_categories.ca_name, DATE_FORMAT(pr_products.pr_regdate, '%%d/%%m/%%Y %%H:%%i:%%s') AS pr_regdate_2 FROM pr_products INNER JOIN ca_categories ON ca_categories.ca_id = pr_products.ca_id WHERE pr_products.pr_id LIKE %s OR pr_products.pr_name LIKE %s OR pr_products.pr_regdate LIKE %s OR ca_categories.ca_name LIKE %s LIMIT %s, %s", (like, like, like, like, page_start, quantityShow,))
                                products = cur.fetchall()
                                cur.close()

                                rows = []
                                for product in products:
                                    status = f"<span class='badge bg-success'><i class='fa-solid fa-eye'></i> Activo/a</span>"
                                    if product["pr_status"] == 0:
                                        status = f"<span class='badge bg-danger'><i class='fa-solid fa-eye-slash'></i> Inactivo/a</span>"                                        

                                    rows.append([f"<img src='/static/images/products/{product['pr_img']}' class='img-product'>", f"<span class='badge bg-primary'><i class='fa-solid fa-fingerprint'></i> {product['pr_id']}</span>", f"<img class='pr_barcode' data-value='{product['pr_id']}'>", product["pr_name"], product["ca_name"], f"${product['pr_price']}", status, product["pr_regdate_2"], f"""<button class='btn btn-primary btn-modal' modalclass='modal-edit' onclick='setEdit("{product['pr_id']}", "{product['ca_id']}", "{product['pr_name']}", "{product['pr_price']}", "{product['pr_status']}")'><i class='fa-solid fa-pen-to-square'></i> Editar</button>"""])

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM pr_products INNER JOIN ca_categories ON ca_categories.ca_id = pr_products.ca_id WHERE pr_products.pr_id LIKE %s OR pr_products.pr_name LIKE %s OR pr_products.pr_regdate LIKE %s OR ca_categories.ca_name LIKE %s",(like, like, like, like,))
                                total = cur.fetchone()["total"]
                                cur.close()

                                pages = math.ceil(total / quantityShow)

                                return json.dumps({"success": True, "code": 200, "html": render_template("/widget/table.html", columns = columns, rows = rows, pages = pages)}), 200
                        elif splitURL3 == "categories":
                            if splitURL4 is None:
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM ca_categories")
                                categoriesTotal = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM ca_categories WHERE ca_status = %s",(1,))
                                categoriesOn = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM ca_categories WHERE ca_status = %s",(0,))
                                categoriesOff = cur.fetchone()["total"]
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "html": render_template("/admin/categories.html", categoriesTotal = categoriesTotal, categoriesOn = categoriesOn, categoriesOff = categoriesOff)}), 200 
                            elif splitURL4 == "table" and splitURL5 is None:
                                if "search" not in request.form:
                                    return json.dumps({"success": False, "code": 200, "msg": "El buscador está vacío."}), 200
                                elif "page" not in request.form or len(request.form["page"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La página está vacía."}), 200                        

                                search = request.form["search"]
                                page = request.form["page"]
                                quantityShow = 10
                                like = f"%{search}%"   

                                if page.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Página no encontrada! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                page = int(page)

                                if page <= 0:
                                    page = 1

                                page_start = (page - 1) * quantityShow

                                columns = ["ID", "Nombre", "Estado", "Acciones"]

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT ca_categories.* FROM ca_categories WHERE ca_categories.ca_id LIKE %s OR ca_categories.ca_name LIKE %s LIMIT %s, %s", (like, like, page_start, quantityShow,))
                                categories = cur.fetchall()
                                cur.close()

                                rows = []
                                for category in categories:
                                    status = f"<span class='badge bg-success'><i class='fa-solid fa-eye'></i> Activo/a</span>"
                                    if category["ca_status"] == 0:
                                        status = f"<span class='badge bg-danger'><i class='fa-solid fa-eye-slash'></i> Inactivo/a</span>"                                        

                                    rows.append([f"<span class='badge bg-primary'><i class='fa-solid fa-fingerprint'></i> {category['ca_id']}</span>", category["ca_name"], status, f"""<button class='btn btn-primary btn-modal' modalclass='modal-edit' onclick='setEdit("{category['ca_id']}", "{category['ca_name']}", "{category['ca_status']}")'><i class='fa-solid fa-pen-to-square'></i> Editar</button>"""])

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM ca_categories WHERE ca_categories.ca_id LIKE %s OR ca_categories.ca_name LIKE %s",(like, like,))
                                total = cur.fetchone()["total"]
                                cur.close()

                                pages = math.ceil(total / quantityShow)

                                return json.dumps({"success": True, "code": 200, "html": render_template("/widget/table.html", columns = columns, rows = rows, pages = pages)}), 200
                        elif splitURL3 == "locations":
                            if splitURL4 is None:
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM lo_locations")
                                locationsTotal = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM lo_locations WHERE lo_status = %s",(1,))
                                locationsOn = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM lo_locations WHERE lo_status = %s",(0,))
                                locationsOff = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT ci_cities.* FROM ci_cities WHERE ci_cities.ci_status = %s",(1,))
                                cities = cur.fetchall()
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "html": render_template("/admin/locations.html", cities = cities, locationsTotal = locationsTotal, locationsOn = locationsOn, locationsOff = locationsOff)}), 200 
                            elif splitURL4 == "table" and splitURL5 is None:
                                if "search" not in request.form:
                                    return json.dumps({"success": False, "code": 200, "msg": "El buscador está vacío."}), 200
                                elif "page" not in request.form or len(request.form["page"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La página está vacía."}), 200                        

                                search = request.form["search"]
                                page = request.form["page"]
                                quantityShow = 10
                                like = f"%{search}%"   

                                if page.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Página no encontrada! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                page = int(page)

                                if page <= 0:
                                    page = 1

                                page_start = (page - 1) * quantityShow

                                columns = ["ID", "Nombre", "Ubicacion", "Estado", "Acciones"]

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT lo_locations.*, ci_cities.ci_name, sts_states.sts_name FROM lo_locations INNER JOIN ci_cities ON ci_cities.ci_id = lo_locations.ci_id INNER JOIN sts_states ON sts_states.sts_id = ci_cities.sts_id WHERE lo_locations.lo_id LIKE %s OR lo_locations.lo_name LIKE %s OR ci_cities.ci_name LIKE %s OR sts_states.sts_name LIKE %s LIMIT %s, %s", (like, like, like, like, page_start, quantityShow,))
                                locations = cur.fetchall()
                                cur.close()

                                rows = []
                                for location in locations:
                                    status = f"<span class='badge bg-success'><i class='fa-solid fa-eye'></i> Activo/a</span>"
                                    if location["lo_status"] == 0:
                                        status = f"<span class='badge bg-danger'><i class='fa-solid fa-eye-slash'></i> Inactivo/a</span>"                                        

                                    rows.append([f"<span class='badge bg-primary'><i class='fa-solid fa-fingerprint'></i> {location['lo_id']}</span>", location["lo_name"], f"{location['ci_name']}, {location['sts_name']}", status, f"""<button class='btn btn-primary btn-modal' modalclass='modal-edit' onclick='setEdit("{location['lo_id']}", "{location['lo_name']}", "{location['lo_status']}", "{location['ci_id']}")'><i class='fa-solid fa-pen-to-square'></i> Editar</button>"""])

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM lo_locations INNER JOIN ci_cities ON ci_cities.ci_id = lo_locations.ci_id INNER JOIN sts_states ON sts_states.sts_id = ci_cities.sts_id WHERE lo_locations.lo_id LIKE %s OR lo_locations.lo_name LIKE %s OR ci_cities.ci_name LIKE %s OR sts_states.sts_name LIKE %s", (like, like, like, like))
                                total = cur.fetchone()["total"]
                                cur.close()

                                pages = math.ceil(total / quantityShow)

                                return json.dumps({"success": True, "code": 200, "html": render_template("/widget/table.html", columns = columns, rows = rows, pages = pages)}), 200
                        elif splitURL3 == "paymentmethods":
                            if splitURL4 is None:
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM pm_paymentmethods")
                                paymentmethodsTotal = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM pm_paymentmethods WHERE pm_status = %s",(1,))
                                paymentmethodsOn = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM pm_paymentmethods WHERE pm_status = %s",(0,))
                                paymentmethodsOff = cur.fetchone()["total"]
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "html": render_template("/admin/paymentmethods.html", paymentmethodsTotal = paymentmethodsTotal, paymentmethodsOn = paymentmethodsOn, paymentmethodsOff = paymentmethodsOff)}), 200 
                            elif splitURL4 == "table" and splitURL5 is None:
                                if "search" not in request.form:
                                    return json.dumps({"success": False, "code": 200, "msg": "El buscador está vacío."}), 200
                                elif "page" not in request.form or len(request.form["page"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La página está vacía."}), 200                        

                                search = request.form["search"]
                                page = request.form["page"]
                                quantityShow = 10
                                like = f"%{search}%"   

                                if page.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Página no encontrada! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                page = int(page)

                                if page <= 0:
                                    page = 1

                                page_start = (page - 1) * quantityShow

                                columns = ["ID", "Nombre", "Estado", "Acciones"]

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT pm_paymentmethods.* FROM pm_paymentmethods WHERE pm_paymentmethods.pm_id LIKE %s OR pm_paymentmethods.pm_name LIKE %s LIMIT %s, %s", (like, like, page_start, quantityShow,))
                                paymentmethods = cur.fetchall()
                                cur.close()

                                rows = []
                                for paymentmethod in paymentmethods:
                                    status = f"<span class='badge bg-success'><i class='fa-solid fa-eye'></i> Activo/a</span>"
                                    if paymentmethod["pm_status"] == 0:
                                        status = f"<span class='badge bg-danger'><i class='fa-solid fa-eye-slash'></i> Inactivo/a</span>"                                        

                                    rows.append([f"<span class='badge bg-primary'><i class='fa-solid fa-fingerprint'></i> {paymentmethod['pm_id']}</span>", paymentmethod["pm_name"], status, f"""<button class='btn btn-primary btn-modal' modalclass='modal-edit' onclick='setEdit("{paymentmethod['pm_id']}", "{paymentmethod['pm_name']}", "{paymentmethod['pm_status']}")'><i class='fa-solid fa-pen-to-square'></i> Editar</button>"""])

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM pm_paymentmethods WHERE pm_paymentmethods.pm_id LIKE %s OR pm_paymentmethods.pm_name LIKE %s",(like, like,))
                                total = cur.fetchone()["total"]
                                cur.close()

                                pages = math.ceil(total / quantityShow)

                                return json.dumps({"success": True, "code": 200, "html": render_template("/widget/table.html", columns = columns, rows = rows, pages = pages)}), 200
                        elif splitURL3 == "states":
                            if splitURL4 is None:
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM sts_states")
                                statesTotal = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM sts_states WHERE sts_status = %s",(1,))
                                statesOn = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM sts_states WHERE sts_status = %s",(0,))
                                statesOff = cur.fetchone()["total"]
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "html": render_template("/admin/states.html", statesTotal = statesTotal, statesOn = statesOn, statesOff = statesOff)}), 200 
                            elif splitURL4 == "table" and splitURL5 is None:
                                if "search" not in request.form:
                                    return json.dumps({"success": False, "code": 200, "msg": "El buscador está vacío."}), 200
                                elif "page" not in request.form or len(request.form["page"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La página está vacía."}), 200                        

                                search = request.form["search"]
                                page = request.form["page"]
                                quantityShow = 10
                                like = f"%{search}%"   

                                if page.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Página no encontrada! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                page = int(page)

                                if page <= 0:
                                    page = 1

                                page_start = (page - 1) * quantityShow

                                columns = ["ID", "Nombre", "Estado", "Acciones"]

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT sts_states.* FROM sts_states WHERE sts_states.sts_id LIKE %s OR sts_states.sts_name LIKE %s LIMIT %s, %s", (like, like, page_start, quantityShow,))
                                states = cur.fetchall()
                                cur.close()

                                rows = []
                                for location in states:
                                    status = f"<span class='badge bg-success'><i class='fa-solid fa-eye'></i> Activo/a</span>"
                                    if location["sts_status"] == 0:
                                        status = f"<span class='badge bg-danger'><i class='fa-solid fa-eye-slash'></i> Inactivo/a</span>"                                        

                                    rows.append([f"<span class='badge bg-primary'><i class='fa-solid fa-fingerprint'></i> {location['sts_id']}</span>", location["sts_name"], status, f"""<button class='btn btn-primary btn-modal' modalclass='modal-edit' onclick='setEdit("{location['sts_id']}", "{location['sts_name']}", "{location['sts_status']}")'><i class='fa-solid fa-pen-to-square'></i> Editar</button>"""])

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM sts_states WHERE sts_states.sts_id LIKE %s OR sts_states.sts_name LIKE %s",(like, like,))
                                total = cur.fetchone()["total"]
                                cur.close()

                                pages = math.ceil(total / quantityShow)

                                return json.dumps({"success": True, "code": 200, "html": render_template("/widget/table.html", columns = columns, rows = rows, pages = pages)}), 200
                        elif splitURL3 == "cities":
                            if splitURL4 is None:
                                cur = mysql.connection.cursor()
                                cur.execute("SELECT sts_states.* FROM sts_states WHERE sts_states.sts_status = %s",(1,))
                                states = cur.fetchall()
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM ci_cities")
                                citiesTotal = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM ci_cities WHERE ci_status = %s",(1,))
                                citiesOn = cur.fetchone()["total"]
                                cur.close()

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM ci_cities WHERE ci_status = %s",(0,))
                                citiesOff = cur.fetchone()["total"]
                                cur.close()

                                return json.dumps({"success": True, "code": 200, "html": render_template("/admin/cities.html", states = states, citiesTotal = citiesTotal, citiesOn = citiesOn, citiesOff = citiesOff)}), 200 
                            elif splitURL4 == "table" and splitURL5 is None:
                                if "search" not in request.form:
                                    return json.dumps({"success": False, "code": 200, "msg": "El buscador está vacío."}), 200
                                elif "page" not in request.form or len(request.form["page"]) <= 0:
                                    return json.dumps({"success": False, "code": 200, "msg": "La página está vacía."}), 200                        

                                search = request.form["search"]
                                page = request.form["page"]
                                quantityShow = 10
                                like = f"%{search}%"   

                                if page.isnumeric() is False:
                                    return json.dumps({"success": False, "code": 200, "msg": "¡Página no encontrada! Por favor, corrígela y vuelva a intentarlo."}), 200        

                                page = int(page)

                                if page <= 0:
                                    page = 1

                                page_start = (page - 1) * quantityShow

                                columns = ["ID", "Nombre", "Estado", "Estatus", "Acciones"]

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT ci_cities.*, sts_states.sts_name FROM ci_cities INNER JOIN sts_states ON sts_states.sts_id = ci_cities.sts_id WHERE ci_cities.ci_id LIKE %s OR ci_cities.ci_name LIKE %s OR sts_states.sts_name LIKE %s LIMIT %s, %s", (like, like, like, page_start, quantityShow,))
                                cities = cur.fetchall()
                                cur.close()

                                rows = []
                                for city in cities:
                                    status = f"<span class='badge bg-success'><i class='fa-solid fa-eye'></i> Activo/a</span>"
                                    if city["ci_status"] == 0:
                                        status = f"<span class='badge bg-danger'><i class='fa-solid fa-eye-slash'></i> Inactivo/a</span>"                                        

                                    rows.append([f"<span class='badge bg-primary'><i class='fa-solid fa-fingerprint'></i> {city['ci_id']}</span>", city["ci_name"], city["sts_name"], status, f"""<button class='btn btn-primary btn-modal' modalclass='modal-edit' onclick='setEdit("{city['ci_id']}", "{city['ci_name']}", "{city['ci_status']}", "{city['sts_id']}")'><i class='fa-solid fa-pen-to-square'></i> Editar</button>"""])

                                cur = mysql.connection.cursor()
                                cur.execute("SELECT COUNT(*) AS total FROM ci_cities INNER JOIN sts_states ON sts_states.sts_id = ci_cities.sts_id WHERE ci_cities.ci_id LIKE %s OR ci_cities.ci_name LIKE %s OR sts_states.sts_name LIKE %s",(like, like, like,))
                                total = cur.fetchone()["total"]
                                cur.close()

                                pages = math.ceil(total / quantityShow)

                                return json.dumps({"success": True, "code": 200, "html": render_template("/widget/table.html", columns = columns, rows = rows, pages = pages)}), 200
                        
                    if splitURL2 == "employee":
                        pass
        return json.dumps({"success": False, "code": 404, "msg": "Page not found."}), 404
    except Exception as e:
        api_saveLog("log/api-error.txt", e, sys.exc_info()[-1].tb_lineno)
        return json.dumps({"success": False, "code": 500, "msg": f"[E{sys.exc_info()[-1].tb_lineno}] An error occurred while processing the request."}), 500