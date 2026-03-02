import base64
import urllib.parse

# -------- 1. Base64 Encoding Example --------
payload = "Hello HTTP World"
encoded_base64 = base64.b64encode(payload.encode()).decode()
decoded_base64 = base64.b64decode(encoded_base64).decode()

print("Base64 Encoded:", encoded_base64)
print("Base64 Decoded:", decoded_base64)


# -------- 2. URL Encoding Example --------
user_input = "admin' OR 1=1 --"  # Potential SQL injection
encoded_url = urllib.parse.quote(user_input)
decoded_url = urllib.parse.unquote(encoded_url)

print("\nOriginal Input:", user_input)
print("URL Encoded Input:", encoded_url)
print("URL Decoded Input:", decoded_url)


# -------- 3. XSS Example --------
xss_payload = "<script>alert(1)</script>"
encoded_xss = urllib.parse.quote(xss_payload)
decoded_xss = urllib.parse.unquote(encoded_xss)

print("\nOriginal XSS Payload:", xss_payload)
print("Encoded XSS Payload:", encoded_xss)
print("Decoded XSS Payload:", decoded_xss)