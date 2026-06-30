# ============================================
# 🚗 BRONX VEHICLE RC DETAILS API
# your-app.vercel.app/rc?num=MH02FZ0555
# ============================================
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

# ============ CONFIG ============
CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"

# ============ CORS ============
@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# ============ HOME PAGE ============
@app.route('/')
def home():
    base_url = request.host_url.rstrip('/')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>🚗 BRONX VEHICLE RC API</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{background:#000a14;color:#d0d8f0;font-family:'Rajdhani',sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}}
        body::before{{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(0,150,255,.06),transparent 60%);pointer-events:none;z-index:0}}
        .card{{background:rgba(5,15,35,.9);border:1px solid rgba(0,150,255,.1);border-radius:20px;padding:35px;max-width:600px;width:100%;text-align:center;position:relative;z-index:1;backdrop-filter:blur(20px)}}
        h1{{font-family:'Orbitron',sans-serif;font-size:26px;background:linear-gradient(90deg,#0096ff,#00d4ff,#8b00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}}
        .badge{{display:inline-block;background:rgba(0,255,136,.06);color:#00ff88;padding:4px 14px;border-radius:20px;font-size:10px;border:1px solid rgba(0,255,136,.12);margin:4px}}
        .section{{background:rgba(0,0,0,.5);border:1px solid rgba(0,150,255,.08);border-radius:12px;padding:16px;margin:14px 0;text-align:left}}
        code{{color:#00ff88;font-family:monospace;font-size:11px;word-break:break-all;display:block;margin:6px 0;background:rgba(0,0,0,.3);padding:8px;border-radius:6px}}
        input{{width:100%;padding:12px;background:rgba(0,0,0,.5);border:1px solid rgba(0,150,255,.08);border-radius:10px;color:#fff;font-size:14px;outline:none;margin:8px 0;font-family:'Rajdhani',sans-serif}}
        input:focus{{border-color:#0096ff}}
        button{{width:100%;padding:14px;background:linear-gradient(135deg,#0096ff,#0066cc);color:#fff;border:none;border-radius:10px;font-weight:700;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:14px;margin:6px 0;transition:.3s}}
        button:hover{{transform:scale(1.02);box-shadow:0 0 25px rgba(0,150,255,.2)}}
        .result{{background:rgba(0,0,0,.5);border:1px solid rgba(0,255,136,.08);border-radius:10px;padding:14px;margin-top:10px;text-align:left;display:none;max-height:400px;overflow:auto}}
        .result.show{{display:block}}
        pre{{color:#00ff88;font-family:monospace;font-size:10px;white-space:pre-wrap}}
    </style>
</head>
<body>
<div class="card">
    <h1>🚗 BRONX VEHICLE RC API</h1>
    <p style="color:#667;font-size:12px">Vehicle Registration Details Lookup</p>
    <div style="margin:10px 0">
        <span class="badge">🚗 Vehicle</span>
        <span class="badge">📋 RC Details</span>
        <span class="badge">⚡ Fast</span>
    </div>
    
    <div class="section">
        <p style="color:#0096ff;font-weight:700">🔗 API ENDPOINT</p>
        <code>GET /rc?num=MH02FZ0555</code>
        <p style="color:#ffb400;font-size:10px;margin-top:4px">Example: MH02FZ0555, DL1AB1234, KA01AB1234</p>
    </div>
    
    <input type="text" id="rcInput" placeholder="Enter RC Number (e.g., MH02FZ0555)">
    <button onclick="lookup()">🔍 LOOKUP</button>
    
    <div class="result" id="result"><pre id="resultData"></pre></div>
    
    <p style="color:#667;font-size:10px;margin-top:14px">Created by BRONX_ULTRA</p>
</div>
<script>
async function lookup(){{
    var num = document.getElementById('rcInput').value.trim();
    if(!num) return alert('Enter RC number!');
    var resultDiv = document.getElementById('result');
    var resultData = document.getElementById('resultData');
    resultDiv.classList.add('show');
    resultData.style.color = '#ffb400';
    resultData.textContent = '🔍 Searching...';
    try{{
        var resp = await fetch('/rc?num=' + encodeURIComponent(num));
        var data = await resp.json();
        resultData.style.color = '#00ff88';
        resultData.textContent = JSON.stringify(data, null, 2);
    }}catch(e){{
        resultData.style.color = '#ff3366';
        resultData.textContent = '❌ Error: ' + e.message;
    }}
}}
</script>
</body></html>'''

# ============ RC API ENDPOINT ============
@app.route('/rc')
def rc_lookup():
    rc_number = request.args.get('num', '').strip().upper()
    
    if not rc_number:
        return jsonify({
            "status": "error",
            "message": "Missing RC number. Use: /rc?num=MH02FZ0555",
            "credit": CREDIT,
            "example": f"{request.host_url.rstrip('/')}/rc?num=MH02FZ0555"
        }), 400
    
    url = f"https://vahanx.in/rc-search/{rc_number}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": f"Network error: {str(e)}",
            "credit": CREDIT
        }), 500
    
    def get_value(label):
        try:
            span = soup.find("span", string=label)
            if span:
                div = span.find_parent("div")
                if div:
                    p = div.find("p")
                    if p:
                        return p.get_text(strip=True)
            return None
        except:
            return None
    
    data = {
        "status": "success",
        "rc_number": rc_number,
        "credit": CREDIT,
        "developer": DEVELOPER,
        "powered_by": "BRONX ULTRA API",
        "result": {
            "Owner Details": {
                "Owner Name": get_value("Owner Name"),
                "Owner Serial No": get_value("Owner Serial No"),
                "Financier Name": get_value("Financier Name"),
                "City": get_value("City Name"),
                "Phone": get_value("Phone"),
            },
            "Vehicle Details": {
                "Model Name": get_value("Model Name"),
                "Maker Model": get_value("Maker Model"),
                "Vehicle Class": get_value("Vehicle Class"),
                "Fuel Type": get_value("Fuel Type"),
                "Fuel Norms": get_value("Fuel Norms"),
            },
            "Registration Details": {
                "Registered RTO": get_value("Registered RTO"),
                "Registration Date": get_value("Registration Date"),
            },
            "Insurance Details": {
                "Insurance Company": get_value("Insurance Company"),
                "Insurance Expiry": get_value("Insurance Expiry"),
                "Insurance Upto": get_value("Insurance Upto"),
            },
            "Compliance Details": {
                "Fitness Upto": get_value("Fitness Upto"),
                "Tax Upto": get_value("Tax Upto"),
                "PUC Upto": get_value("PUC Upto"),
            },
            "Address Details": {
                "Address": get_value("Address"),
                "City Name": get_value("City Name"),
            }
        }
    }
    
    # Remove None values
    def clean_dict(d):
        if isinstance(d, dict):
            return {k: clean_dict(v) for k, v in d.items() if v is not None}
        return d
    
    data["result"] = clean_dict(data["result"])
    
    return jsonify(data)

# ============ TEST ENDPOINT ============
@app.route('/test')
def test():
    return jsonify({
        "status": "✅ BRONX RC API ONLINE",
        "endpoint": "/rc?num=MH02FZ0555",
        "credit": CREDIT,
        "developer": DEVELOPER
    })

# ============ 404 ============
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "message": "Not found. Use /rc?num=RC_NUMBER",
        "home": "/",
        "test": "/test",
        "credit": CREDIT
    }), 404

# ============ VERCEL HANDLER ============
def handler(request):
    return app(request.environ, request.start_response)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 3000))
    print("🚗 BRONX VEHICLE RC API")
    print(f"🚀 Running on port {port}")
    app.run(host='0.0.0.0', port=port)
