import base64
import urllib.parse
import hashlib

# -----------------------------
# 1️⃣ Base64 Authentication Header
# -----------------------------
username = "myuser"
password = "mypassword"

credentials = f"{username}:{password}"
base64_credentials = base64.b64encode(credentials.encode()).decode()

print("Authorization Header:")
print("Authorization: Basic", base64_credentials)


# -----------------------------
# 2️⃣ URL Encoding Query Parameters
# -----------------------------
params = {
    "search": "John Doe",
    "role": "admin & manager"
}

encoded_params = urllib.parse.urlencode(params)

print("\nEncoded Query Parameters:")
print(encoded_params)


# -----------------------------
# 3️⃣ Hex Signature (Simulating OAuth Signing)
# -----------------------------
secret_key = "mysecretkey"

# Combine data to simulate signing string
signing_string = credentials + encoded_params + secret_key

signature = hashlib.sha256(signing_string.encode()).hexdigest()

print("\nGenerated Hex Signature:")
print(signature)


# -----------------------------
# 4️⃣ Simulated REST API Request
# -----------------------------
api_url = "https://api.example.com/users"

full_request = f"""
POST {api_url}?{encoded_params}

Headers:
Authorization: Basic {base64_credentials}
X-Signature: {signature}
"""

print("\nSimulated REST API Request:")
print(full_request)