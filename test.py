import hashlib

def generate_hmac_sha512(message, secret_key):
    hmac_hash = hashlib.sha512(message.encode() + secret_key.encode()).hexdigest()
    return hmac_hash

def calculate_plinko_payout(clientseed, nonce, secret_key):
    message = f"{clientseed},{nonce}"
    print("Message for hashing:", message)
    hmac_sha512 = generate_hmac_sha512(message, secret_key)
    
    rights = 0
    lefts = 0

    print("HMAC SHA-512 hash:", hmac_sha512)

    for i, char in enumerate(hmac_sha512[:16], start=1):  # Consider only the first 16 characters
        decimal_value = int(char, 16)  # Convert hexadecimal to decimal
        if 8 <= decimal_value <= 15:
            rights += 1
            direction = "right"
        elif 0 <= decimal_value <= 7:
            lefts += 1
            direction = "left"
        
        print(f"Step {i}: Character '{char}', Decimal value: {decimal_value}, Ball goes {direction}")

    total_rows = 16  # Total rows fixed at 16

    payout = ((rights - lefts + total_rows) / 2) + 1
    return payout

clientseed = "hihihihiihiaisiseieieiideideindeonisfsafgsdgasgag"
nonce = "2612"
secret_key = "b03a9a066926916af8bf01a3fa0c862b4215da3a79b441e9cedd32cfef46686a881a0c006d9fc55888edf0e19b2df47679adb033d64bf4a9d9dec1548d24d418"

print("Calculating Plinko Payout...")
payout = calculate_plinko_payout(clientseed, nonce, secret_key)
print("\nPlinko Payout:", payout)
