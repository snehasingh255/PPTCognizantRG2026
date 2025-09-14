import qrcode

url = "https://www.cognizantppt.com"  
qr_img = qrcode.make(url)
qr_img.save("cognizantppt_qr.png")

print("✅ QR code saved as cognizantppt_qr.png")
