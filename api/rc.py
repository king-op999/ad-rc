# ============================================
# 🚗 BRONX VEHICLE RC API V5.0
# Clean Response – Owner Info First!
# VahanX + FT-OSINT + Veh2Num + RTO
# ============================================
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"

# APIs
FT_OSINT_API = "https://ft-osint-api.duckdns.org/api/vehicle"
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
<title>🚗 BRONX RC API V5</title>
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
<h1>🚗 BRONX RC API V5</h1>
<p style="color:#667;font-size:12px">Owner Info First • FT-OSINT • Veh2Num • RTO</p>
<div style="margin:10px 0">
<span class="badge">👤 Owner First</span><span class="badge">🔧 FT-OSINT</span><span class="badge">📱 Veh2Num</span><span class="badge">🏢 RTO</span>
</div>
<div class="section"><p style="color:#0096ff;font-weight:700">🔗 API</p><code>GET /rc?num=KA01AB1234</code></div>
<input type="text" id="rcInput" placeholder="RC Number (e.g., KA01AB1234)">
<button onclick="lookup()">🔍 LOOKUP</button>
<div class="result" id="result"><pre id="resultData"></pre></div>
<p style="color:#667;font-size:10px;margin-top:14px">BRONX_ULTRA</p>
</div>
<script>
async function lookup(){{
var n=document.getElementById('rcInput').value.trim();if(!n)return alert('Enter RC!');
var d=document.getElementById('result'),p=document.getElementById('resultData');
d.classList.add('show');p.style.color='#ffb400';p.textContent='🔍 Searching...';
try{{var r=await fetch('/rc?num='+encodeURIComponent(n));var j=await r.json();p.style.color='#00ff88';p.textContent=JSON.stringify(j,null,2)}}catch(e){{p.style.color='#ff3366';p.textContent='❌ '+e.message}}}}
</script>
</body></html>'''

# ============ SOURCE 1: FT-OSINT Vehicle API ============
def get_ft_osint_data(rc_number):
    try:
        url = f"{FT_OSINT_API}?key=bronx&vehicle={rc_number}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data and data.get('success'):
            return data
        return None
    except: return None

# ============ SOURCE 2: VahanX (For Father Name) ============
def get_vahanx_father_name(rc_number):
    url = f"https://vahanx.in/rc-search/{rc_number}"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()
        
        # Try Father's Name span
        father_name = None
        try:
            span = soup.find("span", string="Father's Name")
            if span:
                div = span.find_parent("div")
                if div:
                    p = div.find("p")
                    if p: father_name = p.get_text(strip=True)
        except: pass
        
        if not father_name:
            so_match = re.search(r'(S/O|D/O|W/O)\s*SH\.?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
            if so_match: father_name = f"{so_match.group(1)} SH. {so_match.group(2).strip()}"
        
        # Try Owner Name
        owner_name = None
        try:
            span = soup.find("span", string="Owner Name")
            if span:
                div = span.find_parent("div")
                if div:
                    p = div.find("p")
                    if p: owner_name = p.get_text(strip=True)
        except: pass
        
        # Try Phone
        phone = None
        try:
            span = soup.find("span", string="Phone")
            if span:
                div = span.find_parent("div")
                if div:
                    p = div.find("p")
                    if p: phone = p.get_text(strip=True)
        except: pass
        
        return {
            "father_name": father_name,
            "owner_name": owner_name,
            "phone": phone
        }
    except: return {}

# ============ SOURCE 3: Bronx Veh2Num ============
def get_bronx_veh2num_data(rc_number):
    try:
        url = f"{BRONX_VEH2NUM_API}?key=op&vehicle={rc_number}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data and not data.get('error'):
            return data
        return None
    except: return None

# ============ SOURCE 4: CarInfo RTO ============
def get_carinfo_rto(rc_number):
    url = f"https://www.carinfo.app/rto-vehicle-registration-detail/rto-details/{rc_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
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
                    elif 'address' in key: rto_info['address'] = val
                    elif 'phone' in key: rto_info['phone'] = val
        return rto_info if len(rto_info) > 1 else None
    except: return None

# ============ MAIN RC ENDPOINT ============
@app.route('/rc')
def rc_lookup():
    rc_number = request.args.get('num', '').strip().upper().replace(' ', '').replace('-', '')
    
    if not rc_number:
        return jsonify({"status": "error", "message": "Missing RC number. Use: /rc?num=KA01AB1234", "credit": CREDIT}), 400
    
    # Get data from all sources
    ft_data = get_ft_osint_data(rc_number)
    vahanx = get_vahanx_father_name(rc_number)
    veh2num = get_bronx_veh2num_data(rc_number)
    rto = get_carinfo_rto(rc_number)
    
    # ============ BUILD RESPONSE ============
    result = {
        "status": "success",
        "rc_number": rc_number,
        "credit": CREDIT,
        "developer": DEVELOPER,
        "powered_by": "BRONX ULTRA API"
    }
    
    # ============ PRIMARY OWNER INFO (FIRST) ============
    owner_info = {}
    
    # Owner Name
    owner_info["owner_name"] = (
        (ft_data.get("owner", {}) or {}).get("name") or 
        vahanx.get("owner_name") or 
        "N/A"
    )
    
    # Father Name
    owner_info["father_name"] = (
        (ft_data.get("owner", {}) or {}).get("father_name") or 
        vahanx.get("father_name") or 
        "N/A"
    )
    
    # Owner Mobile Number
    owner_mobile = "N/A"
    if veh2num:
        owner_mobile = veh2num.get("number") or veh2num.get("mobile") or veh2num.get("phone") or str(veh2num)
    if owner_mobile == "N/A" and vahanx.get("phone"):
        owner_mobile = vahanx["phone"]
    if owner_mobile == "N/A" and ft_data:
        rto_contact = ft_data.get("rto_contact", {}) or {}
        owner_mobile = rto_contact.get("phone", "N/A")
    owner_info["owner_mobile_number"] = owner_mobile
    
    # Address
    address_info = (ft_data.get("address", {}) or {})
    owner_info["address"] = address_info.get("present") or address_info.get("permanent") or "N/A"
    
    # City
    owner_info["city"] = (
        address_info.get("city") or 
        (ft_data.get("registration", {}) or {}).get("authority", "").split(",")[-1].strip() or 
        "N/A"
    )
    
    # Pincode
    owner_info["pincode"] = address_info.get("pincode") or "N/A"
    
    # State
    owner_info["state"] = rto.get("state") if rto else "N/A"
    
    # ✅ PUT OWNER INFO FIRST
    result["📋_owner_info"] = owner_info
    
    # ============ VEHICLE INFO ============
    if ft_data:
        vehicle_data = ft_data.get("vehicle", {}) or {}
        result["🚗_vehicle_info"] = {
            "manufacturer": vehicle_data.get("manufacturer"),
            "model": vehicle_data.get("model"),
            "variant": vehicle_data.get("variant"),
            "fuel": vehicle_data.get("fuel"),
            "cc": vehicle_data.get("cc"),
            "class": vehicle_data.get("class"),
            "seating": vehicle_data.get("seating"),
            "type": vehicle_data.get("type"),
            "commercial": vehicle_data.get("commercial")
        }
    
    # ============ REGISTRATION INFO ============
    if ft_data:
        reg_data = ft_data.get("registration", {}) or {}
        result["📅_registration_info"] = {
            "rto_code": reg_data.get("rto_code"),
            "rto_name": reg_data.get("rto"),
            "authority": reg_data.get("authority"),
            "registration_date": reg_data.get("date")
        }
    
    # ============ RTO CONTACT ============
    if ft_data:
        rto_contact = ft_data.get("rto_contact", {}) or {}
        if rto_contact.get("phone"):
            result["🏢_rto_contact"] = rto_contact
    
    # ============ INSURANCE INFO ============
    if ft_data:
        insurance_data = ft_data.get("insurance", {}) or {}
        if insurance_data:
            result["🛡️_insurance_info"] = {
                "company": insurance_data.get("company"),
                "valid_upto": insurance_data.get("valid_upto"),
                "expired": insurance_data.get("expired")
            }
    
    # ============ FINANCIER ============
    if ft_data:
        financier = ft_data.get("financier", {}) or {}
        if financier.get("name"):
            result["💰_financier"] = financier
    
    # ============ IDENTIFICATION ============
    if ft_data:
        ident = ft_data.get("identification", {}) or {}
        if ident:
            result["🔢_identification"] = ident
    
    # ============ FITNESS & TAX ============
    if ft_data:
        fitness = ft_data.get("fitness", {}) or {}
        if fitness:
            result["✅_fitness_tax"] = fitness
    
    # ============ PUC ============
    if ft_data:
        puc = ft_data.get("puc", {}) or {}
        if puc.get("valid_upto"):
            result["🌿_puc"] = puc
    
    # ============ ADDITIONAL RTO INFO ============
    if rto:
        result["🏢_additional_rto"] = rto
    
    # If nothing found
    if not ft_data and not vahanx and not veh2num:
        result["status"] = "error"
        result["message"] = "No data found. Try a different RC number."
        return jsonify(result), 404
    
    return jsonify(result)

# ============ TEST ============
@app.route('/test')
def test():
    return jsonify({
        "status": "✅ BRONX RC API V5 ONLINE",
        "endpoint": "/rc?num=KA01AB1234",
        "sources": ["FT-OSINT API", "VahanX (Father Name)", "Bronx Veh2Num", "CarInfo RTO"],
        "features": ["Owner Info First", "Father Name", "Mobile Number", "Address", "City", "Pincode"],
        "credit": CREDIT
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "home": "/", "test": "/test", "api": "/rc?num=RC_NUMBER"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print("🚗 BRONX VEHICLE RC API V5")
    print(f"🚀 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port)
