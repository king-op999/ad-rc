# ============================================
# 🚗 BRONX VEHICLE RC API V6.0
# Clean List Format • Proper Mobile • Advanced
# ============================================
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

CREDIT = "@BRONX_ULTRA"
DEVELOPER = "@BRONX_ULTRA"

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
<title>🚗 BRONX RC API V6</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#000a14;color:#d0d8f0;font-family:'Rajdhani',sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}}
body::before{{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(0,150,255,.06),transparent 60%),radial-gradient(ellipse at 80% 100%,rgba(139,0,255,.04),transparent 60%);pointer-events:none;z-index:0}}
.card{{background:rgba(5,15,35,.9);border:1px solid rgba(0,150,255,.1);border-radius:20px;padding:30px;max-width:600px;width:100%;text-align:center;position:relative;z-index:1;backdrop-filter:blur(20px)}}
h1{{font-family:'Orbitron',sans-serif;font-size:26px;background:linear-gradient(90deg,#0096ff,#00d4ff,#8b00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px}}
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
<h1>🚗 BRONX RC API V6</h1>
<p style="color:#667;font-size:12px">Clean List • Owner Info First • Advanced</p>
<div style="margin:10px 0">
<span class="badge">👤 Owner</span><span class="badge">📱 Mobile</span><span class="badge">🚗 Vehicle</span><span class="badge">🏢 RTO</span>
</div>
<div class="section"><p style="color:#0096ff;font-weight:700">🔗 API</p><code>GET /rc?num=MH02FZ0555</code></div>
<input type="text" id="rcInput" placeholder="RC Number (e.g., MH02FZ0555)">
<button onclick="lookup()">🔍 LOOKUP</button>
<div class="result" id="result"><pre id="resultData"></pre></div>
<p style="color:#667;font-size:10px;margin-top:14px">@BRONX_ULTRA</p>
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

# ============ SOURCE 2: VahanX ============
def get_vahanx_data(rc_number):
    url = f"https://vahanx.in/rc-search/{rc_number}"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()
        
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
        
        father = gv("Father's Name")
        if not father:
            so = re.search(r'(S/O|D/O|W/O)\s*SH\.?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
            if so: father = f"{so.group(1)} SH. {so.group(2).strip()}"
        
        return {
            "father_name": father,
            "owner_name": gv("Owner Name"),
            "phone": gv("Phone"),
            "address": gv("Address"),
            "city": gv("City Name"),
            "rto": gv("Registered RTO"),
            "reg_date": gv("Registration Date"),
            "model": gv("Model Name"),
            "fuel": gv("Fuel Type"),
            "insurance_company": gv("Insurance Company"),
            "insurance_upto": gv("Insurance Upto"),
            "fitness_upto": gv("Fitness Upto"),
            "tax_upto": gv("Tax Upto"),
            "puc_upto": gv("PUC Upto"),
        }
    except: return {}

# ============ SOURCE 3: Bronx Veh2Num ============
def get_bronx_veh2num(rc_number):
    try:
        url = f"{BRONX_VEH2NUM_API}?key=op&vehicle={rc_number}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data and data.get('mobile_number'):
            return data.get('mobile_number')
        if data and isinstance(data, dict):
            # Search for mobile number in response
            for key in ['mobile_number', 'mobile', 'phone', 'number', 'owner_number']:
                if data.get(key): return str(data[key])
        return None
    except: return None

# ============ SOURCE 4: CarInfo RTO ============
def get_carinfo_rto(rc_number):
    url = f"https://www.carinfo.app/rto-vehicle-registration-detail/rto-details/{rc_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        info = {}
        match = re.match(r'^([A-Z]{2}\d{2})', rc_number)
        if match: info["rto_code"] = match.group(1)
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    k = cells[0].get_text(strip=True).lower()
                    v = cells[1].get_text(strip=True)
                    if 'state' in k: info['state'] = v
                    elif 'address' in k: info['rto_address'] = v
                    elif 'phone' in k: info['rto_phone'] = v
                    elif 'email' in k: info['rto_email'] = v
                    elif 'city' in k: info['rto_city'] = v
        return info if len(info) > 1 else None
    except: return None

# ============ MAIN RC ENDPOINT ============
@app.route('/rc')
def rc_lookup():
    rc_number = request.args.get('num', '').strip().upper().replace(' ', '').replace('-', '')
    
    if not rc_number:
        return jsonify({"status": "error", "message": "Missing RC number", "credit": CREDIT}), 400
    
    # Get all data
    ft = get_ft_osint_data(rc_number)
    vx = get_vahanx_data(rc_number)
    v2n = get_bronx_veh2num(rc_number)
    rto = get_carinfo_rto(rc_number)
    
    if not ft and not vx:
        return jsonify({"status": "error", "message": "No data found", "credit": CREDIT}), 404
    
    # ============ BUILD CLEAN RESPONSE ============
    result = {
        "status": "success",
        "rc_number": rc_number,
        "credit": CREDIT,
        "powered_by": "@BRONX_ULTRA"
    }
    
    # ============ 👤 OWNER INFORMATION ============
    ft_owner = ft.get("owner", {}) if ft else {}
    ft_addr = ft.get("address", {}) if ft else {}
    ft_reg = ft.get("registration", {}) if ft else {}
    ft_rto_contact = ft.get("rto_contact", {}) if ft else {}
    
    owner_name = ft_owner.get("name") or vx.get("owner_name") or "N/A"
    father_name = ft_owner.get("father_name") or vx.get("father_name") or "N/A"
    owner_mobile = v2n or vx.get("phone") or ft_rto_contact.get("phone") or "N/A"
    rto_phone = ft_rto_contact.get("phone") or (rto.get("rto_phone") if rto else None) or "N/A"
    
    present_addr = ft_addr.get("present", "").strip(", ") or vx.get("address") or "N/A"
    permanent_addr = ft_addr.get("permanent", "").strip(", ") or present_addr
    city = ft_addr.get("city") or vx.get("city") or "N/A"
    pincode = ft_addr.get("pincode") or "N/A"
    state = (rto.get("state") if rto else None) or "N/A"
    
    result["👤_owner_details"] = {
        "owner_name": owner_name,
        "father_name": father_name,
        "owner_mobile_number": owner_mobile,
        "rto_phone_number": rto_phone,
        "present_address": present_addr,
        "permanent_address": permanent_addr,
        "city": city,
        "pincode": pincode,
        "state": state,
    }
    
    # ============ 🚗 VEHICLE INFORMATION ============
    if ft:
        vh = ft.get("vehicle", {}) or {}
        result["🚗_vehicle_details"] = {
            "manufacturer": vh.get("manufacturer"),
            "model": vh.get("model"),
            "variant": vh.get("variant"),
            "fuel_type": vh.get("fuel"),
            "engine_cc": vh.get("cc"),
            "vehicle_class": vh.get("class"),
            "seating_capacity": vh.get("seating"),
            "vehicle_type": vh.get("type"),
            "commercial": vh.get("commercial"),
        }
    
    # ============ 📅 REGISTRATION DETAILS ============
    if ft:
        result["📅_registration_details"] = {
            "rto_code": ft_reg.get("rto_code"),
            "rto_name": ft_reg.get("rto"),
            "authority": ft_reg.get("authority"),
            "registration_date": ft_reg.get("date") or vx.get("reg_date"),
        }
    
    # ============ 🛡️ INSURANCE DETAILS ============
    if ft:
        ins = ft.get("insurance", {}) or {}
        if ins:
            result["🛡️_insurance_details"] = {
                "company": ins.get("company") or vx.get("insurance_company"),
                "valid_upto": ins.get("valid_upto") or vx.get("insurance_upto"),
                "expired": ins.get("expired"),
                "policy_number": ins.get("policy_no"),
            }
    
    # ============ 🔢 IDENTIFICATION ============
    if ft:
        ident = ft.get("identification", {}) or {}
        if ident:
            result["🔢_identification"] = {
                "chassis_number": ident.get("chassis"),
                "engine_number": ident.get("engine"),
            }
    
    # ============ 💰 FINANCIER ============
    if ft:
        fin = ft.get("financier", {}) or {}
        if fin.get("name"):
            result["💰_financier"] = {"financier_name": fin["name"]}
    
    # ============ ✅ FITNESS & TAX ============
    fit_data = {}
    if ft:
        fit = ft.get("fitness", {}) or {}
        if fit.get("fitness_upto") or vx.get("fitness_upto"):
            fit_data["fitness_valid_upto"] = fit.get("fitness_upto") or vx.get("fitness_upto")
        if fit.get("tax_upto") or vx.get("tax_upto"):
            fit_data["tax_valid_upto"] = fit.get("tax_upto") or vx.get("tax_upto")
    if fit_data:
        result["✅_fitness_tax"] = fit_data
    
    # ============ 🌿 PUC ============
    if ft:
        puc = ft.get("puc", {}) or {}
        if puc.get("valid_upto") or vx.get("puc_upto"):
            result["🌿_puc_details"] = {
                "puc_valid_upto": puc.get("valid_upto") or vx.get("puc_upto"),
                "puc_number": puc.get("no"),
            }
    
    # ============ 🏢 RTO CONTACT ============
    if rto:
        result["🏢_rto_contact"] = {k: v for k, v in rto.items() if v}
    elif ft_rto_contact:
        result["🏢_rto_contact"] = {"rto_phone": ft_rto_contact.get("phone")}
    
    return jsonify(result)

# ============ TEST ============
@app.route('/test')
def test():
    return jsonify({
        "status": "✅ BRONX RC API V6 ONLINE",
        "endpoint": "/rc?num=MH02FZ0555",
        "format": "Clean List • Owner First",
        "credit": CREDIT
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "home": "/", "test": "/test", "api": "/rc?num=RC_NUMBER"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print("🚗 BRONX VEHICLE RC API V6")
    print(f"🚀 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port)
