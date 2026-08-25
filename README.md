# Counsellor Contact Form (Flask)

## Kya hai isme
- Home page (`/`) par counsellors ki cards dikhti hain, har card me naam + short description + **"Contact Now"** button.
- Button dabate hi ek chhota popup aata hai jisme visitor apna naam/phone (optional) daal sakta hai.
- Submit karte hi:
  1. Visitor ko seedha WhatsApp (`wa.me/...`) par pehle se type kiya hua message ke sath redirect kar diya jaata hai.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Browser me kholein: `http://localhost:5000`

## Counsellors edit karna

`app.py` file me upar `COUNSELLORS` list hai. Har counsellor ke liye:

```python
{
    "id": "priya",                 # unique code, URL me use hota hai
    "name": "Priya Sharma",
    "desc": "Short description yahan likhein.",
    "whatsapp": "919876543210",    # country code sahit, bina + ya space
    "message": "Default WhatsApp message jo pehle se type ho jayega",
}
```

Naye counsellor add karne ke liye bas ek naya dictionary is list me jod dein.

## Important notes
- WhatsApp number format: country code + number, bina `+`, bina space (jaise India: `91` + 10 digit number = `919876543210`).
- Local test ke baad, ise Render, PythonAnywhere, Railway, ya kisi bhi Python-hosting server par deploy kar sakte ho taaki link sabko share ho sake.
