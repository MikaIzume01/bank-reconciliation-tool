from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reconcile', methods=['POST'])
def reconcile():
    if 'bank_file' not in request.files or 'ledger_file' not in request.files:
        return redirect(url_for('index'))
    
    bank_file = request.files['bank_file']
    ledger_file = request.files['ledger_file']
    
    if bank_file.filename == '' or ledger_file.filename == '':
        return redirect(url_for('index'))
    
    bank_path = os.path.join(app.config['UPLOAD_FOLDER'], 'bank.csv')
    ledger_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ledger.csv')
    
    bank_file.save(bank_path)
    ledger_file.save(ledger_path)
    
    try:
        # Load CSV files (expected columns: tanggal, keterangan, jumlah)
        df_bank = pd.read_csv(bank_path)
        df_ledger = pd.read_csv(ledger_path)
        
        # Standardize column names (case-insensitive search or expected format)
        # Expected: Date, Description, Amount
        df_bank.columns = [c.lower().strip() for c in df_bank.columns]
        df_ledger.columns = [c.lower().strip() for c in df_ledger.columns]
        
        # Rename common variations
        col_map = {'tanggal': 'date', 'tgl': 'date', 'keterangan': 'desc', 'ket': 'desc', 'jumlah': 'amount', 'nominal': 'amount'}
        df_bank = df_bank.rename(columns=col_map)
        df_ledger = df_ledger.rename(columns=col_map)
        
        # Ensure amount is numeric
        df_bank['amount'] = pd.to_numeric(df_bank['amount'].astype(str).str.replace('[^0-9.-]', '', regex=True))
        df_ledger['amount'] = pd.to_numeric(df_ledger['amount'].astype(str).str.replace('[^0-9.-]', '', regex=True))
        
        # Reconciliation logic: match by amount (exact match)
        bank_records = df_bank.to_dict('records')
        ledger_records = df_ledger.to_dict('records')
        
        matched = []
        unmatched_bank = []
        unmatched_ledger = list(ledger_records)
        
        for b in bank_records:
            found = False
            for l in unmatched_ledger:
                if abs(b['amount'] - l['amount']) < 0.01: # Amount match
                    matched.append({'bank': b, 'ledger': l})
                    unmatched_ledger.remove(l)
                    found = True
                    break
            if not found:
                unmatched_bank.append(b)
                
        return render_template('result.html', matched=matched, unmatched_bank=unmatched_bank, unmatched_ledger=unmatched_ledger)
        
    except Exception as e:
        return f"Terjadi kesalahan saat memproses file: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
