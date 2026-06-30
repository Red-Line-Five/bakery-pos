# 🧁 Bakery POS System

A web-based **Point-of-Sale application** built with HTML, CSS, and JavaScript — designed for bakeries and retail businesses operating across multiple branches.

---

## ✨ Features

- 🏪 **Multi-location Support** — manage multiple branches from a single system
- 🧾 **Invoicing** — generate and print professional invoices for every sale
- 💰 **Pricing Management** — set and update product prices per branch or globally
- 📦 **Product Management** — add, edit, and organize products with categories
- 📊 **Sales Reports** — track daily, weekly, and monthly revenue per branch
- 🔐 **User Roles** — cashier and admin access levels

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Markup | HTML5 |
| Styling | CSS3 |
| Logic | JavaScript (Vanilla) |

---

## 🚀 Getting Started

No installation required — runs directly in the browser.

1. Clone the repository
```bash
git clone https://github.com/Red-Line-Five/bakery-pos.git
```

2. Open `bakery-pos.html` in your browser

---

## 🔐 License setup for `server.py`

When the app is opened through the local server, license values are read from:

1. Environment variables: `ASLI_LICENSE_KEY` and `ASLI_LICENSE_EXPIRY`
2. Windows Registry: `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\AsliPOS`
3. Windows Registry fallback: `Computer\HKEY_CURRENT_USER\SOFTWARE\AsliPOS`

If `http://localhost:5050/api/license` returns:

```json
{"licenseKey": "", "licenseExpiry": "", "source": "missing"}
```

then no license has been configured yet.

### Option A — fill license with environment variables

PowerShell example:

```powershell
$env:ASLI_LICENSE_KEY="ASLI-YOURKEY"
$env:ASLI_LICENSE_EXPIRY="2027-06-30"
python server.py
```

### Option B — fill license in Windows Registry

Run PowerShell as Administrator for `HKEY_LOCAL_MACHINE`:

```powershell
New-Item -Path "HKLM:\SOFTWARE\AsliPOS" -Force
New-ItemProperty -Path "HKLM:\SOFTWARE\AsliPOS" -Name "LicenseKey" -Value "ASLI-YOURKEY" -PropertyType String -Force
New-ItemProperty -Path "HKLM:\SOFTWARE\AsliPOS" -Name "LicenseExpiry" -Value "2027-06-30" -PropertyType String -Force
```

For a non-admin per-user install, use `HKEY_CURRENT_USER`:

```powershell
New-Item -Path "HKCU:\SOFTWARE\AsliPOS" -Force
New-ItemProperty -Path "HKCU:\SOFTWARE\AsliPOS" -Name "LicenseKey" -Value "ASLI-YOURKEY" -PropertyType String -Force
New-ItemProperty -Path "HKCU:\SOFTWARE\AsliPOS" -Name "LicenseExpiry" -Value "2027-06-30" -PropertyType String -Force
```

### Generate the expected license key

The key must match the bakery name and expiry date. Use the same bakery name saved in Settings:

```powershell
python -c "shop='Forn Al Asli'; expiry='2027-06-30'; raw=shop.strip().upper()+'|'+expiry+'|ASLI-POS'; h=0
for ch in raw:
    h=((h<<5)-h)+ord(ch); h=((h+2**31)%2**32)-2**31
chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'; n=abs(h); out='0' if n==0 else ''
while n:
    n,r=divmod(n,36); out=chars[r]+out
print('ASLI-'+out)"
```

Or generate it from the browser console while the POS is open:

```javascript
buildLicenseKey('Forn Al Asli', '2027-06-30')
```

Then copy the returned value into `ASLI_LICENSE_KEY` or the Registry `LicenseKey`.

---


## 📌 Correct Project Listing Entry

If you are listing this repository in a portfolio table, use the following corrected row:

| Project | Description | Stack |
|--------|-------------|-------|
| [**bakery pos**](https://github.com/Red-Line-Five/bakery-pos) | Web-based bakery point-of-sale system with invoicing, product/pricing management, and multi-branch reporting | HTML5 · CSS3 · JavaScript (Vanilla) |

---

## 👨‍💻 Author

**Charbel Feghaly** — Senior C# / .NET Software Engineer  
[LinkedIn](https://www.linkedin.com/in/charbel-feghaly-916473103) · [GitHub](https://github.com/Red-Line-Five)

---

## 📄 License

This project is licensed under the MIT License.
