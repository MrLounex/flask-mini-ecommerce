from flask import Flask, render_template, redirect, url_for, session, request, send_file
import os, json, datetime
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "rahasia_super"

# ===== Dummy data produk (20 item, each has images list and main image) =====
products = [
    {
        "id": 1,
        "name": "Laptop Gaming",
        "price": 15000000,
        "description": "Laptop dengan spesifikasi tinggi untuk gaming.",
        "images": [
            "https://images.unsplash.com/photo-1640955014216-75201056c829?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Z2FtaW5nJTIwbGFwdG9wfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1640695257754-7e2932f9ad0f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8Z2FtaW5nJTIwbGFwdG9wfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1684127987312-43455fd95925?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Z2FtaW5nJTIwbGFwdG9wfGVufDB8fDB8fHww"
        ]
    },
    {
        "id": 2,
        "name": "Smartphone",
        "price": 7000000,
        "description": "Smartphone flagship dengan kamera canggih.",
        "images": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1200",
            "https://images.unsplash.com/photo-1720048171731-15b3d9d5473f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fHNtYXJ0cGhvbmV8ZW58MHx8MHx8fDA%3D",
            "https://plus.unsplash.com/premium_photo-1680985551009-05107cd2752c?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8c21hcnRwaG9uZXxlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    {
        "id": 3,
        "name": "Headphone",
        "price": 150000,
        "description": "Headphone wired dengan kualitas suara jernih.",
        "images": [
            "https://plus.unsplash.com/premium_photo-1679513691474-73102089c117?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aGVhZHBob25lc3xlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1484704849700-f032a568e944?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fGhlYWRwaG9uZXN8ZW58MHx8MHx8fDA%3D",
            "https://images.unsplash.com/photo-1505740106531-4243f3831c78?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fGhlYWRwaG9uZXxlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    {
        "id": 4,
        "name": "Smartwatch",
        "price": 2500000,
        "description": "Jam tangan pintar dengan berbagai fitur kesehatan.",
        "images": [
            "https://images.unsplash.com/photo-1617625802912-cde586faf331?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8c21hcnR3YXRjaHxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c21hcnQlMjB3YXRjaHxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1517420879524-86d64ac2f339?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8c21hcnQlMjB3YXRjaHxlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    {
        "id": 5,
        "name": "Tablet",
        "price": 5000000,
        "description": "Tablet untuk kerja dan hiburan.",
        "images": [
            "https://images.unsplash.com/photo-1542751110-97427bbecf20?fm=jpg&q=60&w=1200",
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?fm=jpg&q=60&w=1200",
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?fm=jpg&q=60&w=1200"
        ]
    },
    {
        "id": 6,
        "name": "Kamera DSLR",
        "price": 12000000,
        "description": "Kamera DSLR untuk fotografi profesional.",
        "images": [
            "https://images.unsplash.com/photo-1504215680853-026ed2a45def?auto=format&fit=crop&w=1200",
            "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=1200",
            "https://images.unsplash.com/photo-1473654729523-203e25dfda10?auto=format&fit=crop&w=1200"
        ]
    },
    {
        "id": 7,
        "name": "Drone",
        "price": 8000000,
        "description": "Drone dengan kamera 4K.",
        "images": [
            "https://images.unsplash.com/photo-1456615913800-c33540eac399?fm=jpg&q=60&w=1200",
            "https://images.unsplash.com/photo-1507582020474-9a35b7d455d9?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8ZHJvbmVzfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1508566418226-fde6ae1c12dc?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fGRyb25lc3xlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    {
        "id": 8,
        "name": "Keyboard Mechanical",
        "price": 1200000,
        "description": "Keyboard mechanical untuk gaming.",
        "images": [
            "https://plus.unsplash.com/premium_photo-1664194583917-b0ba07c4ce2a?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8bWVjaGFuaWNhbCUyMGtleWJvYXJkfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1558050032-160f36233a07?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8bWVjaGFuaWNhbCUyMGtleWJvYXJkfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1602025882379-e01cf08baa51?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bWVjaGFuaWNhbCUyMGtleWJvYXJkfGVufDB8fDB8fHww"
        ]
    },
    {
        "id": 9,
        "name": "Mouse Wireless",
        "price": 350000,
        "description": "Mouse wireless dengan sensor presisi tinggi.",
        "images": [
            "https://images.unsplash.com/photo-1660491083562-d91a64d6ea9c?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8d2lyZWxlc3MlMjBtb3VzZXxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1707592691247-5c3a1c7ba0e3?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8d2lyZWxlc3MlMjBtb3VzZXxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1586349906319-48d20e9d17e5?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8d2lyZWxlc3MlMjBtb3VzZXxlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    {
        "id": 10,
        "name": "Speaker Bluetooth",
        "price": 800000,
        "description": "Speaker portable dengan suara bass kuat.",
        "images": [
            "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Ymx1ZXRvb3RoJTIwc3BlYWtlcnxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1598034989845-48532781987e?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGJsdWV0b290aCUyMHNwZWFrZXJ8ZW58MHx8MHx8fDA%3D",
            "https://images.unsplash.com/photo-1529359744902-86b2ab9edaea?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8Ymx1ZXRvb3RoJTIwc3BlYWtlcnxlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    
    {
        "id": 11,
        "name": "Monitor 4K",
        "price": 6000000,
        "description": "Monitor resolusi tinggi 4K untuk kerja & gaming.",
        "images": [
            "https://images.unsplash.com/photo-1614624532983-4ce03382d63d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8bW9uaXRvcnxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1534972195531-d756b9bfa9f2?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTd8fG1vbml0b3J8ZW58MHx8MHx8fDA%3D",
            "https://images.unsplash.com/photo-1671523435843-e3cd426c24e4?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDI5fHx8ZW58MHx8fHx8"
        ]
    },
    {
        "id": 12,
        "name": "Printer",
        "price": 2500000,
        "description": "Printer multifungsi dengan fitur scan & copy.",
        "images": [
            "https://images.unsplash.com/photo-1706895040634-62055892cbbb?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8cHJpbnRlcnxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1650094980833-7373de26feb6?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cHJpbnRlcnxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1625961332771-3f40b0e2bdcf?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHByaW50ZXJ8ZW58MHx8MHx8fDA%3D"
        ]
    },
    {
        "id": 13,
        "name": "Router WiFi",
        "price": 900000,
        "description": "Router WiFi kecepatan tinggi untuk rumah & kantor.",
        "images": [
            "https://images.unsplash.com/photo-1606904825846-647eb07f5be2?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8d2lmaSUyMHJvdXRlcnxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1516044734145-07ca8eef8731?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cm91dGVyfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1606421753414-8d165c9d48e5?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8cm91dGVyfGVufDB8fDB8fHww"
        ]
    },
    {
        "id": 14,
        "name": "Powerbank",
        "price": 400000,
        "description": "Powerbank kapasitas besar untuk smartphone.",
        "images": [
            "https://images.unsplash.com/photo-1586253634019-c77872f966f0?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8cG93ZXJiYW5rfGVufDB8fDB8fHww   ",
            "https://images.unsplash.com/photo-1619489646924-b4fce76b1db5?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cG9ydGFibGUlMjBjaGFyZ2VyfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1614399113305-a127bb2ca893?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cG93ZXJiYW5rfGVufDB8fDB8fHww"
        ]
    },
    {
        "id": 15,
        "name": "Smart TV",
        "price": 7000000,
        "description": "Smart TV 50 inch dengan dukungan Netflix & YouTube.",
        "images": [
            "https://images.unsplash.com/photo-1461151304267-38535e780c79?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c21hcnQlMjB0dnxlbnwwfHwwfHx8MA%3D%3D",
            "https://plus.unsplash.com/premium_photo-1661386068437-3c1134b4d46b?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8c21hcnQlMjB0dnxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1601944179066-29786cb9d32a?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8c21hcnQlMjB0dnxlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    {
        "id": 16,
        "name": "Console Game",
        "price": 6500000,
        "description": "Konsol game next-gen untuk hiburan keluarga.",
        "images": [
            "https://images.unsplash.com/photo-1593118247619-e2d6f056869e?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8Z2FtaW5nJTIwY29uc29sZXxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1604846887565-640d2f52d564?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Z2FtaW5nJTIwY29uc29sZXxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1507457379470-08b800bebc67?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8dmlkZW8lMjBnYW1lc3xlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    {
        "id": 17,
        "name": "Projector",
        "price": 5500000,
        "description": "Proyektor portable untuk presentasi & film.",
        "images": [
            "https://images.unsplash.com/photo-1535016120720-40c646be5580?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cHJvamVjdG9yfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1589113050289-1c654e7e305d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8cHJvamVjdG9yfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1528395874238-34ebe249b3f2?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cHJvamVjdG9yfGVufDB8fDB8fHww"
        ]
    },
    {
        "id": 18,
        "name": "Microphone",
        "price": 1200000,
        "description": "Microphone condenser untuk recording & streaming.",
        "images": [
            "https://images.unsplash.com/photo-1485579149621-3123dd979885?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bWljcm9waG9uZXxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1516280440614-37939bbacd81?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDEwfHx8ZW58MHx8fHx8",
            "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8bWljcm9waG9uZXxlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    {
        "id": 19,
        "name": "External Harddisk",
        "price": 1500000,
        "description": "Harddisk eksternal 1TB untuk backup data.",
        "images": [
            "https://plus.unsplash.com/premium_photo-1723651280322-513220315969?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZXh0ZXJuYWwlMjBoYXJkJTIwZHJpdmV8ZW58MHx8MHx8fDA%3D",
            "https://images.unsplash.com/photo-1720048169707-a32d6dfca0b3?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8aGFyZCUyMGRyaXZlfGVufDB8fDB8fHww",
            "https://images.unsplash.com/photo-1624895608078-e9f564cbe3fa?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGhhcmQlMjBkcml2ZXxlbnwwfHwwfHx8MA%3D%3D"
        ]
    },
    {
        "id": 20,
        "name": "Flashdisk",
        "price": 150000,
        "description": "Flashdisk 64GB dengan kecepatan tinggi.",
        "images": [
            "https://images.unsplash.com/photo-1477949331575-2763034b5fb5?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8dXNifGVufDB8fDB8fHww",
            "https://image.idntimes.com/post/20250523/sara-kurfess-9eid2zc-veo-unsplash-5325d04a68d88ac3db35f4d98aa13a53-e043e970f0125ed556a399a44574b015.jpg?tr=w-1200,f-webp,q-75&width=1200&format=webp&quality=75",
            "https://swalayankomputer.com/wp-content/uploads/2024/04/Flashdisk-64-GB-Kelebihannya-Sebagai-Penyimpanan-Data.jpg"
        ]
    }
]

# Ensure each product has 'image' (main) and 'images' list
for p in products:
    imgs = p.get("images") or []
    if isinstance(imgs, list) and len(imgs) > 0:
        p["image"] = imgs[0]
    else:
        # fallback to single 'image' if present, else an empty placeholder
        p["image"] = p.get("image", "https://via.placeholder.com/1200x800?text=No+Image")
        p["images"] = [p["image"]]

# ===== Path data =====
DATA_DIR = "data"
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "w") as f:
        json.dump([], f, indent=2)

# ===== Helpers =====
def format_rupiah(n):
    return f"Rp {n:,.0f}".replace(",", ".")

def get_product(pid):
    prod = next((p for p in products if p["id"] == pid), None)
    if not prod:
        return None
    # guarantee images + image are present (they already are from initialization)
    if "images" not in prod or not isinstance(prod["images"], list):
        prod["images"] = [prod.get("image", "https://via.placeholder.com/1200x800?text=No+Image")]
    if "image" not in prod:
        prod["image"] = prod["images"][0]
    return prod

def cart_list():
    return session.get("cart", [])

def save_cart(cart):
    session["cart"] = cart

def cart_aggregate(cart):
    by_id = {}
    for item in cart:
        pid = item["id"]
        by_id[pid] = by_id.get(pid, 0) + 1
    items, total = [], 0
    for pid, qty in by_id.items():
        prod = get_product(pid)
        if not prod:
            continue
        subtotal = prod["price"] * qty
        items.append({"product": prod, "qty": qty, "subtotal": subtotal})
        total += subtotal
    return items, total

def load_orders():
    with open(ORDERS_FILE, "r") as f:
        return json.load(f)

def save_orders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def next_order_id():
    today = datetime.datetime.now().strftime("%Y%m%d")
    orders = load_orders()
    seq = sum(1 for o in orders if o.get("id", "").startswith(f"ORD-{today}-")) + 1
    return f"ORD-{today}-{seq:04d}"

# ===== Routes Produk & Cart =====
@app.route("/")
def home():
    return render_template("index.html", products=products, format_rupiah=format_rupiah)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    return render_template("product_detail.html", product=product, products=products, format_rupiah=format_rupiah)

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product = get_product(product_id)
    if product:
        cart = cart_list()
        cart.append({"id": product["id"]})
        save_cart(cart)
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart = cart_list()
    items, total = cart_aggregate(cart)
    return render_template("cart.html", items=items, total=total, format_rupiah=format_rupiah)

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = cart_list()
    for i, item in enumerate(cart):
        if item["id"] == product_id:
            cart.pop(i)
            break
    save_cart(cart)
    return redirect(url_for("cart"))

@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("cart"))

# ===== Checkout & Orders =====
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = cart_list()
    items, subtotal = cart_aggregate(cart)
    if not items:
        return redirect(url_for("cart"))

    ongkir = 20000
    diskon = 0
    total_bayar = subtotal + ongkir - diskon

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not all([name, email, phone, address]):
            error = "Semua field wajib diisi."
            return render_template("checkout.html", items=items, subtotal=subtotal,
                                   ongkir=ongkir, diskon=diskon, total=total_bayar,
                                   error=error, format_rupiah=format_rupiah)

        oid = next_order_id()
        order = {
            "id": oid,
            "customer": {"name": name, "email": email, "phone": phone, "address": address},
            "items": [
                {"id": it["product"]["id"], "name": it["product"]["name"],
                 "price": it["product"]["price"], "qty": it["qty"], "subtotal": it["subtotal"]}
                for it in items
            ],
            "subtotal": subtotal,
            "ongkir": ongkir,
            "diskon": diskon,
            "total": total_bayar,
            "created_at": datetime.datetime.now().isoformat(timespec="seconds")
        }
        orders = load_orders()
        orders.append(order)
        save_orders(orders)
        session.pop("cart", None)
        return redirect(url_for("order_success", order_id=oid))

    return render_template("checkout.html", items=items, subtotal=subtotal,
                           ongkir=ongkir, diskon=diskon, total=total_bayar,
                           format_rupiah=format_rupiah)

@app.route("/order_success/<order_id>")
def order_success(order_id):
    orders = load_orders()
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return "Order tidak ditemukan", 404
    return render_template("order_success.html", order=order, format_rupiah=format_rupiah)

@app.route("/orders")
def orders():
    orders = load_orders()
    orders.sort(key=lambda o: o.get("created_at", ""), reverse=True)
    return render_template("orders.html", orders=orders, format_rupiah=format_rupiah)

@app.route("/delete_order/<order_id>")
def delete_order(order_id):
    orders = load_orders()
    orders = [o for o in orders if o["id"] != order_id]
    save_orders(orders)
    return redirect(url_for("orders"))

# ===== Resi =====
@app.route("/order_receipt/<order_id>")
def order_receipt(order_id):
    orders = load_orders()
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return "Order tidak ditemukan", 404
    return render_template("receipt.html", order=order, format_rupiah=format_rupiah)

@app.route("/download_receipt/<order_id>")
def download_receipt(order_id):
    orders = load_orders()
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return "Order tidak ditemukan", 404

    filename = f"resi_{order_id}.pdf"
    filepath = os.path.join(DATA_DIR, filename)

    # ==== FORMAT PDF RAPIH DENGAN TABEL ====
    c = canvas.Canvas(filepath, pagesize=(595, 842))  # A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(220, 810, "RESI PEMBELIAN")
    c.setLineWidth(1)
    c.line(50, 800, 550, 800)

    c.setFont("Helvetica", 12)
    c.drawString(60, 770, f"Order ID : {order['id']}")
    c.drawString(60, 755, f"Tanggal  : {order['created_at']}")
    c.drawString(60, 740, f"Nama     : {order['customer']['name']}")
    c.drawString(60, 725, f"Email    : {order['customer']['email']}")
    c.drawString(60, 710, f"Telepon  : {order['customer']['phone']}")
    c.drawString(60, 695, f"Alamat   : {order['customer']['address']}")

    y = 660
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, "Produk")
    c.drawString(300, y, "Qty")
    c.drawString(360, y, "Harga")
    c.drawString(460, y, "Subtotal")
    c.line(50, y-5, 550, y-5)

    c.setFont("Helvetica", 11)
    for item in order["items"]:
        y -= 20
        c.drawString(60, y, item["name"])
        c.drawString(300, y, str(item["qty"]))
        c.drawString(360, y, format_rupiah(item["price"]))
        c.drawString(460, y, format_rupiah(item["subtotal"]))

    y -= 30
    c.line(50, y+10, 550, y+10)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(360, y, "Subtotal:")
    c.drawString(460, y, format_rupiah(order["subtotal"]))

    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(360, y, "Ongkir:")
    c.drawString(460, y, format_rupiah(order["ongkir"]))

    y -= 20
    c.drawString(360, y, "Diskon:")
    c.drawString(460, y, f"-{format_rupiah(order['diskon'])}")

    y -= 25
    c.setFont("Helvetica-Bold", 13)
    c.drawString(360, y, "Total Bayar:")
    c.drawString(460, y, format_rupiah(order["total"]))
    c.line(350, y-5, 550, y-5)

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(60, 60, "Terima kasih telah berbelanja bersama kami")

    c.save()
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
