from flask import Flask, request, render_template
import pandas as pd
import os
import logging
import urllib
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
params = urllib.parse.quote_plus(
    "DRIVER={SQL Server};SERVER=LAPTOP-OLBB6UPV\SQLEXPRESS;DATABASE=PRNDB;UID=RGCHECK;PWD=COGNIZANTUG2026"
)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Registered(db.Model):
    prn = db.Column(db.String(20), primary_key=True)

class Used(db.Model):
    prn = db.Column(db.String(20), primary_key=True)    

registered_df = pd.read_csv('RGCognizant-UG2026.csv')
registered_df.columns = registered_df.columns.str.strip()
registered_prns = set(registered_df['PRN'].astype(str))

used_prns_file = 'used_prns.csv'

if os.path.exists(used_prns_file):
    used_df = pd.read_csv(used_prns_file)
    used_prns = set(used_df['PRN'].astype(str))
else:
    used_prns = set()

logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def check():
    status = None
    if request.method == 'POST':
        prn = request.form['prn'].strip()
        if not prn.isdigit():
            status = "❌ Invalid PRN format."
        elif Registered.query.get(prn):
            if Used.query.get(prn):
                status = "⚠️ Already Verified"
            else:
                status = "✅ You are Registered!"
                db.session.add(Used(prn=prn))
                db.session.commit()
        else:
            status = "❌ You are Not Registered."
    return render_template('qrcognizantrg.html', status=status)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
