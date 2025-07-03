from datetime import datetime, timedelta
import os
from random import randint
from flask import Flask, redirect, render_template, request, send_from_directory, session
import mysql.connector
import hashlib

import mysql.connector.pooling

principal = Flask(__name__)
cursor= mysql.connector.cursor(host="localhost",
                                port="3306",
                                user="root",  
                                password="",
                                database="dbtrastearte")
principal.config['CARPETAU'] = os.path.join('uploads')
principal.secret_key = str(randint(10000,99999))  
principal.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=10)

if __name__ == '__main__':
    principal.run(debug=True, host='0.0.0.0')
              