import base64

def encrypt(key, clear):
	enc = []
	for i in range(len(clear)):
		key_c = key[i % len(key)]
		enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
		enc.append(enc_c)
	return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decrypt(key, encrypted):
	dec = []
	encrypted = base64.urlsafe_b64decode(encrypted).decode()
	for i in range(len(encrypted)):
		key_c = key[i % len(key)]
		dec_c = chr((256 + ord(encrypted[i]) - ord(key_c)) % 256)
		dec.append(dec_c)
	return "".join(dec)
