import hmac
import hashlib
import csv

def generate_hmac_sha512(message, secret_key):
    hmac_hash = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha512)
    return hmac_hash.hexdigest()

def calculate_result(clientseed, nonce, secret_key):
    message = f"{clientseed},{nonce}"
    hmac_sha512 = generate_hmac_sha512(message, secret_key)
    result = int(hmac_sha512[:5], 16)
    while result >= 1000000:
        hmac_sha512 = hmac_sha512[5:]  # Remove first 5 characters
        result = int(hmac_sha512[:5], 16)
    return result % 10000 / 100

clientseed = input("Enter clientseed: ")
start_nonce = int(input("Enter start nonce: "))
end_nonce = int(input("Enter end nonce: "))
secret_key = input("Enter the revealed server seed: ")

results = []

for nonce in range(start_nonce, end_nonce + 1):
    result = calculate_result(clientseed, nonce, secret_key)
    results.append((nonce, result))

print("Results:")
for nonce, result in results:
    print(f"Nonce: {nonce}, Result: {result} *smiles*")

# Writing to results.csv
print("Writing to results.csv...")
with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Nonce','','Result'])
    for nonce, result in results:
        writer.writerow([nonce,'',result])
print("Results written to results.csv *smiles*")
