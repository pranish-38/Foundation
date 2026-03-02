import base64
import urllib.parse

# -------- Base64 Encoding --------
text = "Hello World"

# Encode to Base64
base64_encoded = base64.b64encode(text.encode()).decode()
print("Base64 Encoded:", base64_encoded)

# Decode Base64
base64_decoded = base64.b64decode(base64_encoded).decode()
print("Base64 Decoded:", base64_decoded)


# -------- Hex Encoding --------
hex_encoded = text.encode().hex()
print("\nHex Encoded:", hex_encoded)

hex_decoded = bytes.fromhex(hex_encoded).decode()
print("Hex Decoded:", hex_decoded)


# -------- URL Encoding --------
url_encoded = urllib.parse.quote("hello world@2026")
print("\nURL Encoded:", url_encoded)

url_decoded = urllib.parse.unquote(url_encoded)
print("URL Decoded:", url_decoded)