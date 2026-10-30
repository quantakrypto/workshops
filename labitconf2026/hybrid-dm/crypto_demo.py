"""Offline workshop prototypes. No payments, relay connections, or persistent keys."""
import json, os, sys, hashlib
from contextlib import redirect_stdout
with redirect_stdout(sys.stderr):
    import oqs
from cryptography.hazmat.primitives.asymmetric import x25519, ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

def public(key):
    return key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)

def rejected(fn):
    try: fn(); return False
    except InvalidTag: return True

def private(key):
    return key.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption())

def dm_keys(options=None):
    options=options or {}
    sender=x25519.X25519PrivateKey.from_private_bytes(bytes.fromhex(options['seed'])) if options.get('seed') else x25519.X25519PrivateKey.generate()
    receiver=x25519.X25519PrivateKey.generate()
    with oqs.KeyEncapsulation('ML-KEM-768') as recipient:
        kem_public=recipient.generate_keypair()
        return {'test_only':True,'sender_private_hex':private(sender).hex(),'sender_public_hex':public(sender).hex(),
                'recipient_private_hex':private(receiver).hex(),'recipient_public_hex':public(receiver).hex(),
                'kem_public_hex':kem_public.hex(),'kem_private_hex':recipient.export_secret_key().hex(),
                'library':'liboqs '+oqs.oqs_version()}

def validate_dm_keys(keys):
    if not isinstance(keys,dict) or keys.get('test_only') is not True: raise ValueError('Test keys required')
    lengths={'sender_private_hex':32,'sender_public_hex':32,'recipient_private_hex':32,'recipient_public_hex':32,'kem_public_hex':1184,'kem_private_hex':2400}
    for name,length in lengths.items():
        value=keys.get(name)
        if not isinstance(value,str) or len(value)!=length*2 or any(c not in '0123456789abcdef' for c in value):
            raise ValueError('Invalid key encoding')
    for owner in ['sender','recipient']:
        key=x25519.X25519PrivateKey.from_private_bytes(bytes.fromhex(keys[owner+'_private_hex']))
        if public(key).hex()!=keys[owner+'_public_hex']: raise ValueError('Public/private mismatch')

def dm(options=None):
    options=options or {}
    keys=options.get('keys') or dm_keys(options)
    validate_dm_keys(keys)
    sender=x25519.X25519PrivateKey.from_private_bytes(bytes.fromhex(keys['sender_private_hex']))
    receiver=x25519.X25519PrivateKey.from_private_bytes(bytes.fromhex(keys['recipient_private_hex']))
    with oqs.KeyEncapsulation('ML-KEM-768',secret_key=bytes.fromhex(keys['kem_private_hex'])) as recipient, oqs.KeyEncapsulation('ML-KEM-768') as encapsulator:
        kem_public=bytes.fromhex(keys['kem_public_hex'])
        kem_cipher, secret_a=encapsulator.encap_secret(kem_public)
        secret_b=recipient.decap_secret(kem_cipher)
        if secret_a!=secret_b: raise ValueError('ML-KEM public/private mismatch')
        context=canonical({'version':'qk-workshop-experimental-v1','sender_x25519':public(sender).hex(),'recipient_x25519':public(receiver).hex(),'kem_public':kem_public.hex(),'kem_ciphertext':kem_cipher.hex()})
        def derive(k,z):
            return HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(context).digest(),info=b'qk-workshop/dm/aes256gcm/v1').derive(k+z)
        key_a=derive(sender.exchange(receiver.public_key()),secret_a)
        key_b=derive(receiver.exchange(sender.public_key()),secret_b)
        message=options.get('message','Hola Ana. Mensaje de prueba del taller QuantaKrypto.')
        nonce=os.urandom(12); ciphertext=AESGCM(key_a).encrypt(nonce,message.encode(),context)
        opened=AESGCM(key_b).decrypt(nonce,ciphertext,context).decode()
        altered=bytearray(ciphertext); altered[0]^=1
        wrong=x25519.X25519PrivateKey.generate()
        wrong_key=derive(wrong.exchange(sender.public_key()),secret_b)
        return {'demo':'dm','library':'liboqs '+oqs.oqs_version(),'algorithms':['X25519','ML-KEM-768','HKDF-SHA256','AES-256-GCM'],'message':message,'recovered':opened,'shared_secrets_match':secret_a==secret_b and key_a==key_b,'tamper_rejected':rejected(lambda:AESGCM(key_b).decrypt(nonce,bytes(altered),context)),'wrong_recipient_rejected':rejected(lambda:AESGCM(wrong_key).decrypt(nonce,ciphertext,context)),'kem_public_bytes':len(kem_public),'kem_ciphertext_bytes':len(kem_cipher),'ciphertext_hex':ciphertext.hex(),'x25519_public_hex':public(sender).hex(),'recipient_x25519_public_hex':public(receiver).hex(),'kem_public_hex':kem_public.hex(),'kem_ciphertext_hex':kem_cipher.hex(),'nonce_hex':nonce.hex(),'limit':'Prototipo del cifrado de un DM. No es NIP-44/NIP-59 ni conecta Nostr WoT. Falta autenticar el vínculo entre identidades Nostr y estas claves.'}

def dm_open(options=None):
    keys=options['keys']
    validate_dm_keys(keys)
    try:
        envelope=options['envelope']
        cipher=bytes.fromhex(options['ciphertext'])
        nonce=bytes.fromhex(envelope['nonce_hex'])
        kem_cipher=bytes.fromhex(envelope['kem_ciphertext_hex'])
        if len(nonce)!=12 or len(kem_cipher)!=1088 or not 16<=len(cipher)<=2016: raise ValueError('Invalid envelope')
        receiver=x25519.X25519PrivateKey.from_private_bytes(bytes.fromhex(keys['recipient_private_hex']))
        sender=x25519.X25519PublicKey.from_public_bytes(bytes.fromhex(envelope['x25519_public_hex']))
        context=canonical({'version':'qk-workshop-experimental-v1','sender_x25519':envelope['x25519_public_hex'],'recipient_x25519':envelope['recipient_x25519_public_hex'],'kem_public':envelope['kem_public_hex'],'kem_ciphertext':envelope['kem_ciphertext_hex']})
        with oqs.KeyEncapsulation('ML-KEM-768',secret_key=bytes.fromhex(keys['kem_private_hex'])) as recipient:
            secret=recipient.decap_secret(kem_cipher)
        key=HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(context).digest(),info=b'qk-workshop/dm/aes256gcm/v1').derive(receiver.exchange(sender)+secret)
        return {'valid':True,'recovered':AESGCM(key).decrypt(nonce,cipher,context).decode()}
    except (ValueError,KeyError,TypeError,InvalidTag):
        return {'valid':False,'recovered':None}
