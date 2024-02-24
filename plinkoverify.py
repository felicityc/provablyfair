import os
import hashlib
import hmac
import csv

def generate_hmac_sha512(message, secret_key):
    hmac_hash = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha512)
    return hmac_hash.hexdigest()

def calculate_plinko_payout(clientseed, nonce, secret_key, num_rows):
    message = f"{clientseed},{nonce}"
    hmac_sha512 = generate_hmac_sha512(message, secret_key)
    
    rights = 0
    lefts = 0

    for char in hmac_sha512[:num_rows]:  # Consider only the specified number of characters
        decimal_value = int(char, 16)  # Convert hexadecimal to decimal
        if 8 <= decimal_value <= 15:
            rights += 1
        elif 0 <= decimal_value <= 7:
            lefts += 1

    total_rows = num_rows  # Total rows specified by the user

    payout = ((rights - lefts + total_rows) / 2) + 1
    return payout

clientseed = input("Enter clientseed: ")
start_nonce = int(input("Enter start nonce: "))
end_nonce = int(input("Enter end nonce: "))
secret_key = input("Enter the revealed server seed: ")
num_rows = int(input("Enter the number of rows: "))

# Generate a unique filename for the CSV file
base_filename = 'plinkoresults.csv'
filename = base_filename
counter = 1
while os.path.exists(filename):
    filename = f"{base_filename.split('.')[0]}_{counter}.csv"
    counter += 1

print("Calculating results.")
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Nonce', 'Result'])  # Updated the header
    for nonce in range(start_nonce, end_nonce + 1):
        payout = calculate_plinko_payout(clientseed, nonce, secret_key, num_rows)
        writer.writerow([nonce, payout])
        print(f"Nonce: {nonce}, Payout: {payout}")

print(f"Results written to {filename} *smiles*")
