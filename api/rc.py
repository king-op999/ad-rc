# ============================================
# 🚗 BRONX VEHICLE RC API V4.0
# VahanX + CarInfo + VehicleDetail + Bronx APIs
# Father Name + Owner Number Included!
# ============================================
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"

# Bronx APIs
BRONX_VEHICLE_API = "https://bronx-web-api.onrender.com/api/key-bronx/vehicle"
BRONX_VEH2NUM_API = "https://bronx-web-api.onrender.com/api/key-bronx/veh2num"

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# ============ HOME ============
@app.route('/')
def home():
    base = request.host_url.rstrip('/')
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🚗 BRONX RC API V4</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#000a14;color:#d0d8f0;font-family:'Rajdhani',sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}}
body::before{{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(0,150,255,.06),transparent 60%),radial-gradient(ellipse at 80% 100%,rgba(139,0,255,.04),transparent 60%);pointer-events:none;z-index:0}}
.card{{background:rgba(5,15,35,.9);border:1px solid rgba(0,150,255,.1);border-radius:20px;padding:35px;max-width:600px;width:100%;text-align:center;position:relative;z-index:1;backdrop-filter:blur(20px)}}
h1{{font-family:'Orbitron',sans-serif;font-size:26px;background:linear-gradient(90deg,#0096ff,#00d4ff,#8b00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}}
.badge{{display:inline-block;background:rgba(0,255,136,.06);color:#00ff88;padding:4px 14px;border-radius:20px;font-size:10px;border:1px solid rgba(0,255,136,.12);margin:4px}}
.section{{background:rgba(0,0,0,.5);border:1px solid rgba(0,150,255,.08);border-radius:12px;padding:16px;margin:14px 0;text-align:left}}
code{{color:#00ff88;font-family:monospace;font-size:10px;word-break:break-all;display:block;margin:6px 0;background:rgba(0,0,0,.3);padding:8px;border-radius:6px}}
input{{width:100%;padding:12px;background:rgba(0,0,0,.5);border:1px solid rgba(0,150,255,.08);border-radius:10px;color:#fff;font-size:14px;outline:none;margin:8px 0;font-family:'Rajdhani',sans-serif}}
input:focus{{border-color:#0096ff}}
button{{width:100%;padding:14px;background:linear-gradient(135deg,#0096ff,#0066cc);color:#fff;border:none;border-radius:10px;font-weight:700;cursor:pointer;font-family:'Orbitron',sans-serif;font-size:14px;margin:6px 0;transition:.3s}}
button:hover{{transform:scale(1.02);box-shadow:0 0 25px rgba(0,150,255,.2)}}
.result{{background:rgba(0,0,0,.5);border:1px solid rgba(0,255,136,.08);border-radius:10px;padding:14px;margin-top:10px;text-align:left;display:none;max-height:500px;overflow:auto}}
.result.show{{display:block}}
pre{{color:#00ff88;font-family:monospace;font-size:10px;white-space:pre-wrap}}
</style></head>
<body>
<div class="card">
<h1>🚗 BRONX RC API V4</h1>
<p style="color:#667;font-size:12px">VahanX + CarInfo + Bronx APIs + Father Name</p>
<div style="margin:10px 0">
<span class="badge">🚗 VahanX</span><span class="badge">🏢 RTO</span><span class="badge">👤 Father Name</span><span class="badge">📱 Owner#</span><span class="badge">🔧 Bronx</span>
</div>
<div class="section">
<p style="color:#0096ff;font-weight:700">🔗 API</p>
<code>GET /rc?num=MH02FZ0555</code>
</div>
<input type="text" id="rcInput" placeholder="RC Number (e.g., MH02FZ0555)">
<button onclick="lookup()">🔍 LOOKUP</button>
<div class="result" id="result"><pre id="resultData"></pre></div>
<p style="color:#667;font-size:10px;margin-top:14px">BRONX_ULTRA</p>
</div>
<script>
async function lookup(){{
var n=document.getElementById('rcInput').value.trim();if(!n)return alert('Enter RC!');
var d=document.getElementById('result'),p=document.getElementById('resultData');
d.classList.add('show');p.style.color='#ffb400';p.textContent='🔍 Searching 5 sources...';
try{{var r=await fetch('/rc?num='+encodeURIComponent(n));var j=await r.json();p.style.color='#00ff88';p.textContent=JSON.stringify(j,null,2)}}catch(e){{p.style.color='#ff3366';p.textContent='❌ '+e.message}}}}
</script>
</body></html>'''

# ============ SOURCE 1: VahanX (WITH FATHER NAME) ============
def get_vahanx_data(rc_number):
    url = f"https://vahanx.in/rc-search/{rc_number}"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        def gv(label):
            try:
                span = soup.find("span", string=label)
                if span:
                    div = span.find_parent("div")
                    if div:
                        p = div.find("p")
                        if p: return p.get_text(strip=True)
                return None
            except: return None
        
        # ✅ FATHER NAME - Try multiple patterns
        father_name = gv("Father's Name")
        if not father_name:
            # Try to find from text
            text = soup.get_text()
            father_match = re.search(r"Father'?s?\s*Name\s*[:]?\s*([A-Za-z.\s]+?)(?=Owner|Phone|Address|$)", text, re.IGNORECASE)
            if father_match: father_name = father_match.group(1).strip()
            # Try S/O, D/O, W/O pattern
            so_match = re.search(r'(S/O|D/O|W/O)\s*SH\.?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
            if so_match: father_name = f"{so_match.group(1)} SH. {so_match.group(2).strip()}"
        
        data = {
            "owner_name": gv("Owner Name"),
            "father_name": father_name,
            "owner_serial": gv("Owner Serial No"),
            "financier": gv("Financier Name"),
            "phone": gv("Phone"),
            "model": gv("Model Name"),
            "maker": gv("Maker Model"),
            "vehicle_class": gv("Vehicle Class"),
            "fuel": gv("Fuel Type"),
            "fuel_norms": gv("Fuel Norms"),
            "rto": gv("Registered RTO"),
            "reg_date": gv("Registration Date"),
            "insurance_company": gv("Insurance Company"),
            "insurance_expiry": gv("Insurance Expiry"),
            "insurance_upto": gv("Insurance Upto"),
            "fitness_upto": gv("Fitness Upto"),
            "tax_upto": gv("Tax Upto"),
            "puc_upto": gv("PUC Upto"),
            "address": gv("Address"),
            "city": gv("City Name"),
        }
        return {k: v for k, v in data.items() if v} if any(data.values()) else None
    except: return None

# ============ SOURCE 2: CarInfo RTO ============
def get_carinfo_rto(rc_number):
    url = f"https://www.carinfo.app/rto-vehicle-registration-detail/rto-details/{rc_number}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        rto_info = {}
        match = re.match(r'^([A-Z]{2}\d{2})', rc_number)
        if match: rto_info["rto_code"] = match.group(1)
        tables = soup.find_all('table')
        for table in tables:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True).lower()
                    val = cells[1].get_text(strip=True)
                    if 'state' in key: rto_info['state'] = val
                    elif 'rto' in key: rto_info['rto_name'] = val
                    elif 'address' in key: rto_info['address'] = val
                    elif 'phone' in key: rto_info['phone'] = val
                    elif 'email' in key: rto_info['email'] = val
                    elif 'pin' in key: rto_info['pincode'] = val
                    elif 'city' in key: rto_info['city'] = val
        if not rto_info.get('state'):
            text = soup.get_text()
            patterns = {'state': r'State\s*[:]?\s*([A-Za-z\s]+)', 'phone': r'Phone\s*[:]?\s*([+\d\s/-]+)'}
            for key, pat in patterns.items():
                if not rto_info.get(key):
                    m = re.search(pat, text)
                    if m: rto_info[key] = m.group(1).strip()
        return rto_info if len(rto_info) > 1 else None
    except: return None

# ============ SOURCE 3: VehicleDetail.info ============
def get_vehicledetail_info(rc_number):
    url = "https://know.vehicledetail.info/index.php"
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"}
    try:
        resp = requests.post(url, headers=headers, data={"number": rc_number}, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        info = {}
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True).lower().replace(' ', '_')
                    val = cells[1].get_text(strip=True)
                    if key and val: info[key] = val
        if not info:
            text = soup.get_text()
            patterns = {'city': r'City\s*[:]?\s*([A-Za-z\s]+)', 'state': r'State\s*[:]?\s*([A-Za-z\s]+)', 'pin_code': r'PIN\s*Code\s*[:]?\s*(\d+)'}
            for key, pat in patterns.items():
                m = re.search(pat, text)
                if m: info[key] = m.group(1).strip()
        return info if info else None
    except: return None

# ============ SOURCE 4: Bronx Vehicle API ============
def get_bronx_vehicle_data(rc_number):
    try:
        url = f"{BRONX_VEHICLE_API}?key=op&vehicle={rc_number}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data and not data.get('error'):
            return data
        return None
    except: return None

# ============ SOURCE 5: Bronx Veh2Num API (Owner Number) ============
def get_bronx_veh2num_data(rc_number):
    try:
        url = f"{BRONX_VEH2NUM_API}?key=op&vehicle={rc_number}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data and not data.get('error'):
            return data
        return None
    except: return None

# ============ MAIN RC ENDPOINT ============
@app.route('/rc')
def rc_lookup():
    rc_number = request.args.get('num', '').strip().upper().replace(' ', '').replace('-', '')
    
    if not rc_number:
        return jsonify({"status": "error", "message": "Missing RC number. Use: /rc?num=MH02FZ0555", "credit": CREDIT}), 400
    
    result = {
        "status": "success",
        "rc_number": rc_number,
        "credit": CREDIT,
        "developer": DEVELOPER,
        "powered_by": "BRONX ULTRA API"
    }
    
    # Get data from ALL 5 sources
    vahanx = get_vahanx_data(rc_number)
    rto = get_carinfo_rto(rc_number)
    vd = get_vehicledetail_info(rc_number)
    bronx_vehicle = get_bronx_vehicle_data(rc_number)
    bronx_veh2num = get_bronx_veh2num_data(rc_number)
    
    if vahanx:
        result["vahanx_details"] = vahanx
    
    if rto:
        result["rto_details"] = rto
    
    if vd:
        result["vehicle_detail_info"] = vd
    
    # ✅ HIGHLIGHTED Bronx Vehicle Details
    if bronx_vehicle:
        result["🔧_bronx_vehicle_api"] = bronx_vehicle
    
    # ✅ HIGHLIGHTED Owner Number from Veh2Num
    if bronx_veh2num:
        result["📱_owner_number_api"] = {
            "source": "Bronx Veh2Num API",
            "data": bronx_veh2num,
            "note": "⚠️ Vehicle to Owner Number Lookup"
        }
    
    # If nothing found
    if not any([vahanx, rto, vd, bronx_vehicle, bronx_veh2num]):
        result["status"] = "error"
        result["message"] = "No data found. Try a different RC number."
        return jsonify(result), 404
    
    # ✅ HIGHLIGHTED SUMMARY
    summary = {}
    if vahanx:
        # Highlight Father Name
        if vahanx.get('father_name'):
            summary["👤_father_name"] = vahanx['father_name']
        if vahanx.get('owner_name'):
            summary["👤_owner_name"] = vahanx['owner_name']
        if vahanx.get('phone'):
            summary["📱_phone"] = vahanx['phone']
        if vahanx.get('model'):
            summary["🚗_vehicle"] = vahanx['model']
        if vahanx.get('fuel'):
            summary["⛽_fuel"] = vahanx['fuel']
    
    if rto:
        summary.update({f"🏢_rto_{k}": v for k, v in rto.items() if v})
    
    if bronx_veh2num:
        summary["📱_owner_number_highlighted"] = bronx_veh2num
    
    result["⚡_highlighted_summary"] = summary
    
    return jsonify(result)

# ============ TEST ============
@app.route('/test')
def test():
    return jsonify({
        "status": "✅ BRONX RC API V4 ONLINE",
        "endpoint": "/rc?num=MH02FZ0555",
        "sources": ["VahanX (Father Name)", "CarInfo RTO", "VehicleDetail.info", "Bronx Vehicle API", "Bronx Veh2Num API"],
        "features": ["Father Name", "Owner Number", "RTO Details", "Vehicle Details"],
        "credit": CREDIT,
        "developer": DEVELOPER
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "home": "/", "test": "/test", "api": "/rc?num=RC_NUMBER"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print("🚗 BRONX VEHICLE RC API V4")
    print(f"🚀 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port)
