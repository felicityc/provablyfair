import hmac
import hashlib
import csv
import math

def generate_hmac_sha512(message, secret_key):
    hmac_hash = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha512)
    return hmac_hash.hexdigest()

def generate_hmac_sha256(data, secret_key):
    return hashlib.sha256(data.encode()).hexdigest()

def calculate_result(clientseed, nonce, secret_key):
    message = f"{clientseed},{nonce}"
    hmac_sha512 = generate_hmac_sha512(message, secret_key)
    result = int(hmac_sha512[:13], 16)
    final_result = result / (2**52)
    answer = math.floor(98 / (1 - final_result)) / 100
    return min(answer, 1000000)

def validate_secret_key(secret_key_unhashed, secret_key_hashed):
    return generate_hmac_sha256(secret_key_unhashed, 'example_secret_key') == secret_key_hashed

clientseed = input("Enter clientseed: ")
start_nonce = int(input("Enter start nonce: "))
end_nonce = int(input("Enter end nonce: "))
hashed_secret_key = input("Enter the hashed server seed: ").strip()
secret_key_unhashed = input("Enter the unhashed server seed: ").strip()

if validate_secret_key(secret_key_unhashed, hashed_secret_key):
    answers = []

    for nonce in range(start_nonce, end_nonce + 1):
        result = calculate_result(clientseed, nonce, hashed_secret_key)
        answers.append((nonce, result))

    print("Results:")
    for nonce, result in answers:
        print(f"Nonce: {nonce}, Result: {result} *smiles*")

    print("Writing to results.csv...")
    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Nonce','','Result'])
        for nonce, result in answers:
            writer.writerow([nonce,'',result])
    print("Results written to results.csv *smiles*")
else:
    print("Warning: Hashed secret key does not match the provided unhashed secret key.")
