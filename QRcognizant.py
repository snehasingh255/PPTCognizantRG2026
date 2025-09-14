from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# Load registered PRNs
registered_df = pd.read_csv(r'C:\Users\Sneha Singh\OneDrive\Desktop\Projects\QRcognizant2026RG\RGCognizant-UG2026.csv')
registered_df.columns = registered_df.columns.str.strip()
registered_prns = set(registered_df['PRN'].astype(str))

# Load used PRNs (or create empty set if file doesn't exist)
used_prns_file = r'C:\Users\Sneha Singh\OneDrive\Desktop\Projects\QRcognizant2026RG\used_prns.csv'
if os.path.exists(used_prns_file):
    used_df = pd.read_csv(used_prns_file)
    used_prns = set(used_df['PRN'].astype(str))
else:
    used_prns = set()


@app.route('/', methods=['GET', 'POST'])
def check():
    status = None
    if request.method == 'POST':
        prn = request.form['prn'].strip()
        if prn in registered_prns:
            if prn in used_prns:
                status = "⚠️ Already Verified"
            else:
                status = "✅ You are Registered!"
                with open(used_prns_file, 'a') as f:
                    f.write(f"{prn}\n")
                used_prns.add(prn)
        else:
            status = "❌ You are Not Registered."
    return render_template('qrcognizantrg.html', status=status)

if __name__ == '__main__':
    app.run(debug=True)