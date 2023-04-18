from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect, generate_csrf
from datetime import datetime
from dateutil.relativedelta import relativedelta
from werkzeug.utils import secure_filename
import json, uuid, requests, re, math, time, sys, hashlib, random, shutil, os

csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)

app.secret_key = "SeCrEt_G0cE3r8277"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456789"
app.config["MYSQL_DB"] = "pos"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

def api_validateSession():
    #0 = No Logged
    #1 = Logged

    if "us_id" not in session:
        return 0
    
    if "sess_id" not in session:
        return 0

    return 1

def api_userInfo(us_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT us_users.* FROM us_users WHERE us_users.us_id = %s",(us_id,))
    userInfo = cur.fetchone()
    cur.close()

    return userInfo

def api_splitURL(path,no):
    try:
        response = path.split("/")[no]
    except:
        response = None

    return response

def api_emailValid(email):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email) is not None

def api_uniKey():
    date_today = datetime.today()
    
    abecedario = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]     
    keyUniList = [date_today.strftime("%y"), date_today.strftime("%m"), date_today.strftime("%d"), date_today.strftime("%H"), date_today.strftime("%M")]

    uniKey = ""

    for i in range(6):
        keyUniList.append(random.choice(abecedario))
    
    random.shuffle(keyUniList)

    for i in keyUniList:
        uniKey = uniKey + i
        
    return uniKey

def api_uniKey6():
    date_today = datetime.today()
    
    abecedario = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]     
    keyUniList = []

    uniKey = ""

    for i in range(6):
        keyUniList.append(random.choice(abecedario))
    
    random.shuffle(keyUniList)

    for i in keyUniList:
        uniKey = uniKey + i
        
    return uniKey

def api_userAgent(r):
    try:
        useragent = str(r.headers.get('User-Agent'))
        result = re.findall(r"\((.*?)\)(\s|$)|(.*?)\/(.*?)(\s|$)", useragent)
        userdevice = str(result[1][0])           
    except:
        try:
            useragent = str(r.headers.get('User-Agent'))
            userdevice = useragent
        except:
            useragent = 'Not available'
            userdevice = 'Not available'

    return {'UserAgent': useragent, 'UserDevice': userdevice}

def api_saveLog(d, error, code = "0"):
    try:
        with app.app_context():
            fileToWrite = open(d, "a+")
            fileToWrite.write(f"[E{code}] {error}\n\n")
            fileToWrite.close()
            
        return True
    except:
        return False

def api_permissions(mem_id):
    if mem_id == 1:
        return [1,2,3,4,5,6,7,8]
    elif mem_id == 2:
        return [1,2,3,4,5,6,7,8]
    elif mem_id == 3:
        return [3,4,5,6,7,8]
    elif mem_id == 4:
        return [4,5,6,7,8]
    elif mem_id == 5:
        return [5,6]
    elif mem_id == 6:
        return [6]
    elif mem_id == 7:
        return [6,7]
    elif mem_id == 8:
        return [6,7,8]
    
    return [6] 

def api_isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def api_isBoolean(parameter1):
    try:
        bool(parameter1)
        return True
    except ValueError:
        return False

def api_randomLine(afile):
    lines = open(afile).read().splitlines()
    myline = random.choice(lines)
    return myline

def api_allowedFile(filename, ext):     
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ext