# ============================================================
#   QUESTION 2: Encoding's Role in Securing HTTP Payloads
#               and Preventing Injection Attacks
#   Run: python3 question2_encoding_security.py
# ============================================================

import urllib.parse
import html
import base64
import hashlib
import hmac
import re

# ─────────────────────────────────────────────────────────────
# HELPER: Pretty section printer
# ─────────────────────────────────────────────────────────────
def section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def subsection(title):
    print(f"\n  ── {title} ──")

# ============================================================
# PART 1: HOW ENCODING SECURES HTTP PAYLOADS IN TRANSMISSION
# ============================================================
section("PART 1: ENCODING IN HTTP TRANSMISSION")

# ── 1A: URL Encoding ────────────────────────────────────────
subsection("1A. URL Encoding — Securing Query Parameters")

user_inputs = [
    "john@example.com",
    "hello world & goodbye",
    "price=100<200",
    "path/to/../secret"
]

print(f"\n  {'Raw Input':<30} {'URL Encoded'}")
print(f"  {'-'*30} {'-'*35}")
for raw in user_inputs:
    encoded = urllib.parse.quote(raw, safe='')
    print(f"  {raw:<30} {encoded}")

# Build a safe URL with encoded parameters
params = {
    "username" : "john@example.com",
    "search"   : "hello world & more",
    "redirect" : "https://safe.com/page?id=1"
}
safe_url = "https://example.com/api?" + urllib.parse.urlencode(params)
print(f"\n  Safe URL built:\n  {safe_url}")

# ── 1B: Base64 in HTTP Auth Header ──────────────────────────
subsection("1B. Base64 Encoding — HTTP Basic Authentication")

username = "admin"
password = "SuperSecret123"
credentials = f"{username}:{password}"

# Encode credentials
b64_encoded = base64.b64encode(credentials.encode()).decode()
http_header  = f"Authorization: Basic {b64_encoded}"

print(f"\n  Username      : {username}")
print(f"  Password      : {password}")
print(f"  Combined      : {credentials}")
print(f"  Base64        : {b64_encoded}")
print(f"  HTTP Header   : {http_header}")

# Decode it back (showing it is NOT encryption)
decoded_back = base64.b64decode(b64_encoded).decode()
print(f"\n  ⚠  Decoded back: {decoded_back}")
print(f"  ⚠  Base64 is NOT encryption — always use HTTPS!")

# ── 1C: Hex for Data Integrity ───────────────────────────────
subsection("1C. Hex Encoding — Data Integrity with SHA-256")

payload = "Transfer $500 to account 12345"
secret_key = b"mysecretkey"

# Create HMAC-SHA256 signature
signature = hmac.new(secret_key,
                     payload.encode(),
                     hashlib.sha256).hexdigest()

print(f"\n  Payload   : {payload}")
print(f"  Signature : {signature}")
print(f"  (Hex SHA-256 — server uses this to verify payload was not tampered)")

# Verify integrity
def verify_payload(payload, received_sig, key):
    expected = hmac.new(key, payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, received_sig)

is_valid = verify_payload(payload, signature, secret_key)
print(f"  Integrity check passed: {is_valid} ✓")

# Tampered payload
tampered = "Transfer $9999 to account 99999"
is_tampered = verify_payload(tampered, signature, secret_key)
print(f"  Tampered payload valid: {is_tampered} ✗ — BLOCKED")


# ============================================================
# PART 2: PREVENTING XSS (CROSS-SITE SCRIPTING) ATTACKS
# ============================================================
section("PART 2: XSS ATTACK PREVENTION")

# Simulate XSS attack payloads an attacker might submit
xss_attacks = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('hacked')>",
    "<a href='javascript:steal()'>Click me</a>",
    "Normal safe text",
    "<b onmouseover=alert('xss')>hover me</b>"
]

subsection("Without Encoding — VULNERABLE")
print(f"\n  {'Attack Input':<45} {'Server Response (DANGEROUS)'}")
print(f"  {'-'*45} {'-'*30}")
for attack in xss_attacks:
    # Vulnerable — directly embedding user input in HTML
    response = f"<h2>{attack}</h2>"
    print(f"  {attack:<45} {response[:40]}")

subsection("With HTML Escaping — PROTECTED")
print(f"\n  {'Attack Input':<45} {'Server Response (SAFE)'}")
print(f"  {'-'*45} {'-'*30}")
for attack in xss_attacks:
    # Protected — HTML escape before rendering
    safe = html.escape(attack)
    response = f"<h2>{safe}</h2>"
    print(f"  {attack:<45} {safe[:40]}")

# Show character-by-character what escaping does
subsection("What HTML Escaping Does to Each Character")
dangerous_chars = {
    '<' : '&lt;',
    '>' : '&gt;',
    '"' : '&quot;',
    "'" : '&#x27;',
    '&' : '&amp;',
}
print(f"\n  {'Dangerous Char':<20} {'Safe Escaped'}")
print(f"  {'-'*20} {'-'*15}")
for char, escaped in dangerous_chars.items():
    print(f"  {repr(char):<20} {escaped}")


# ============================================================
# PART 3: PREVENTING SQL INJECTION ATTACKS
# ============================================================
section("PART 3: SQL INJECTION PREVENTION")

# SQL injection payloads
sql_attacks = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "admin'--",
    "' UNION SELECT username, password FROM users--",
    "normaluser"
]

subsection("Without Protection — VULNERABLE SQL Queries")
print()
for attack in sql_attacks:
    # Dangerous: building SQL with raw user input
    vulnerable_query = f"SELECT * FROM users WHERE username = '{attack}'"
    danger = "⚠ DANGEROUS" if any(c in attack for c in ["'", "--", "DROP", "UNION"]) else "✓ Safe"
    print(f"  Input   : {attack}")
    print(f"  Query   : {vulnerable_query}")
    print(f"  Status  : {danger}\n")

subsection("With Encoding + Sanitisation — PROTECTED")

def sanitise_sql_input(user_input):
    """Sanitise input to prevent SQL injection"""
    # Step 1: URL decode first (catch encoded attacks)
    decoded = urllib.parse.unquote(user_input)
    # Step 2: Remove dangerous SQL characters
    sanitised = decoded.replace("'", "''")   # escape single quotes
    sanitised = sanitised.replace(";", "")    # remove semicolons
    sanitised = sanitised.replace("--", "")   # remove SQL comments
    # Step 3: Strip dangerous keywords
    sql_keywords = ["DROP", "DELETE", "INSERT", "UPDATE", "UNION", "SELECT"]
    for kw in sql_keywords:
        sanitised = re.sub(kw, "", sanitised, flags=re.IGNORECASE)
    return sanitised

print()
for attack in sql_attacks:
    safe_input = sanitise_sql_input(attack)
    # Parameterised query style (? placeholder — never string concatenation)
    safe_query = f"SELECT * FROM users WHERE username = ?"
    print(f"  Raw input       : {attack}")
    print(f"  Sanitised input : {safe_input}")
    print(f"  Safe query      : {safe_query}  with param=({repr(safe_input)})")
    print(f"  Status          : ✓ PROTECTED\n")


# ============================================================
# PART 4: ATTACKER OBFUSCATION USING ENCODING
# ============================================================
section("PART 4: ATTACKER ENCODING OBFUSCATION")

malicious = "<script>alert('XSS')</script>"

subsection("How Attackers Use Encoding to Bypass Filters")
print(f"\n  Original payload : {malicious}")

# Technique 1: Single URL encoding
single = urllib.parse.quote(malicious, safe='')
print(f"\n  Technique 1 — Single URL Encode:")
print(f"  {single}")

# Technique 2: Double URL encoding (bypasses basic WAFs)
double = urllib.parse.quote(single, safe='')
print(f"\n  Technique 2 — Double URL Encode (bypasses naive filters):")
print(f"  {double}")

# Technique 3: Base64 obfuscation
b64_payload = base64.b64encode(malicious.encode()).decode()
print(f"\n  Technique 3 — Base64 Obfuscation:")
print(f"  Encoded  : {b64_payload}")
print(f"  In HTML  : <script>eval(atob('{b64_payload}'))</script>")
print(f"  (Hides the script from keyword-based filters)")

# Technique 4: Hex encoding
hex_payload = malicious.encode().hex()
print(f"\n  Technique 4 — Hex Encoding:")
print(f"  {hex_payload}")

subsection("Defence — Recursive Decoding Before Validation")

def decode_fully(payload, max_depth=10):
    """Recursively URL-decode until no more changes occur"""
    previous = None
    depth = 0
    while previous != payload and depth < max_depth:
        previous = payload
        payload = urllib.parse.unquote(payload)
        depth += 1
    return payload

def is_safe(payload):
    """Check if payload contains dangerous patterns after full decode"""
    decoded = decode_fully(payload)
    escaped = html.escape(decoded)
    dangerous = ["<script", "onerror", "javascript:", "DROP TABLE",
                 "UNION SELECT", "eval(", "alert("]
    for pattern in dangerous:
        if pattern.lower() in decoded.lower():
            return False, decoded
    return True, escaped

print()
test_payloads = [single, double, malicious, "hello world", b64_payload]
for payload in test_payloads:
    safe, result = is_safe(payload)
    status = "✓ SAFE" if safe else "✗ BLOCKED"
    print(f"  Input   : {payload[:50]}")
    print(f"  Decoded : {result[:50]}")
    print(f"  Status  : {status}\n")


# ============================================================
# PART 5: COMPLETE SECURE HTTP FORM SUBMISSION PIPELINE
# ============================================================
section("PART 5: COMPLETE SECURE FORM SUBMISSION PIPELINE")

subsection("Simulating a Full Secure Login Form")

def secure_form_handler(form_data):
    """
    Complete encoding security pipeline for HTTP form submission.
    Demonstrates all encoding protections working together.
    """
    print(f"\n  {'─'*55}")
    print(f"  STEP 1: Raw form data received from HTTP request")
    print(f"  {'─'*55}")
    for key, value in form_data.items():
        print(f"  {key:<15}: {value}")

    print(f"\n  {'─'*55}")
    print(f"  STEP 2: URL Decode (normalise encoded input)")
    print(f"  {'─'*55}")
    url_decoded = {}
    for key, value in form_data.items():
        decoded = decode_fully(value)
        url_decoded[key] = decoded
        print(f"  {key:<15}: {decoded}")

    print(f"\n  {'─'*55}")
    print(f"  STEP 3: Validate — check for dangerous patterns")
    print(f"  {'─'*55}")
    blocked = False
    for key, value in url_decoded.items():
        safe, _ = is_safe(value)
        status = "✓ OK" if safe else "✗ BLOCKED"
        print(f"  {key:<15}: {status}  ({value[:35]})")
        if not safe:
            blocked = True

    if blocked:
        print(f"\n  ⛔ REQUEST REJECTED — malicious input detected")
        return None

    print(f"\n  {'─'*55}")
    print(f"  STEP 4: HTML Escape (safe for display)")
    print(f"  {'─'*55}")
    html_escaped = {}
    for key, value in url_decoded.items():
        escaped = html.escape(value)
        html_escaped[key] = escaped
        print(f"  {key:<15}: {escaped}")

    print(f"\n  {'─'*55}")
    print(f"  STEP 5: Generate integrity hash (Hex SHA-256)")
    print(f"  {'─'*55}")
    payload_str = str(html_escaped)
    integrity_hash = hashlib.sha256(payload_str.encode()).hexdigest()
    print(f"  SHA-256: {integrity_hash}")

    print(f"\n  ✅ REQUEST ACCEPTED — data is secure and ready to store")
    return html_escaped

# Test 1: Safe user input
print("\n  TEST 1: Normal user submitting login form")
safe_form = {
    "username" : "john_doe",
    "email"    : "john@example.com",
    "password" : "MyPassword123",
    "message"  : "Hello, I love your website!"
}
secure_form_handler(safe_form)

# Test 2: Attacker input
print("\n\n  TEST 2: Attacker submitting malicious input")
attack_form = {
    "username" : "' OR '1'='1",
    "email"    : "hacker@evil.com",
    "password" : "anything",
    "message"  : "<script>alert('XSS')</script>"
}
secure_form_handler(attack_form)

# Test 3: Double-encoded attack
print("\n\n  TEST 3: Attacker using double-encoded bypass")
encoded_attack = urllib.parse.quote(urllib.parse.quote("<script>steal()</script>"))
bypass_form = {
    "username" : "admin",
    "email"    : "test@test.com",
    "password" : "pass",
    "message"  : encoded_attack
}
secure_form_handler(bypass_form)


rules = [
    ("Rule 1", "URL encode all data in HTTP query strings and form submissions"),
    ("Rule 2", "Decode input FULLY before validating — never validate encoded data"),
    ("Rule 3", "HTML escape ALL output before displaying to users"),
    ("Rule 4", "Use parameterised SQL queries — never concatenate raw input"),
    ("Rule 5", "Base64 is NOT encryption — always pair with HTTPS/TLS"),
    ("Rule 6", "Apply recursive decoding to catch double-encoded attacks"),
    ("Rule 7", "Use SHA-256 hex signatures to verify payload integrity"),
    ("Rule 8", "Implement CSP headers as a last line of defence"),
]

print()
for rule, description in rules:
    print(f"  [{rule}] {description}")

print("\n" + "=" * 60)
print("=" * 60)