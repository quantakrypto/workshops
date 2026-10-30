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

def receipt(options=None):
    options=options or {}
    preimage=bytes.fromhex(options['seed']) if options.get('seed') else os.urandom(32)
    data={'schema':'qk-lightning-test-receipt-v1','test_only':True,'amount_msat':options.get('amount',2100)*1000,'payment_hash':hashlib.sha256(preimage).hexdigest(),'status':'simulated-settled','recipient':'Ana de prueba','network':'simulated','created_at':'2026-10-31T17:10:00-03:00'}
    payload=b'qk-workshop/receipt/v1\0'+canonical(data)
    with oqs.Signature('ML-DSA-65') as signer, oqs.Signature('ML-DSA-65') as verifier:
        pk=signer.generate_keypair(); signature=signer.sign(payload)
        changed={**data,'amount_msat':data['amount_msat']+1000}
        with oqs.Signature('ML-DSA-65') as other:
            wrong_pk=other.generate_keypair()
        return {'demo':'receipt','library':'liboqs '+oqs.oqs_version(),'algorithm':'ML-DSA-65','receipt':data,'public_key_bytes':len(pk),'signature_bytes':len(signature),'valid':verifier.verify(payload,signature,pk),'tamper_rejected':not verifier.verify(b'qk-workshop/receipt/v1\0'+canonical(changed),signature,pk),'wrong_key_rejected':not verifier.verify(payload,signature,wrong_pk),'public_key_hex':pk.hex(),'signature_hex':signature.hex(),'canonical_payload':payload.decode(),'limit':'Firma una declaración de pago simulado. No prueba una liquidación real ni cambia las firmas de Lightning o Bitcoin. El verificador necesita confiar en la clave del emisor.'}
