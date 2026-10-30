import json
from crypto_demo import receipt, canonical, oqs
def main():
    print('QuantaKrypto · recibo ficticio · no se mueve dinero')
    amount=int(input('1. Importe ficticio en sats (1–1000000): '))
    if not 1<=amount<=1000000: raise ValueError('Importe fuera de rango')
    result=receipt({'amount':amount})
    print('2. Recibo y firma:',json.dumps(result,ensure_ascii=False,indent=2))
    while True:
        value=input('3. Importe a verificar; Enter usa el original; salir termina: ').strip()
        if value=='salir': break
        sats=amount if not value else int(value)
        modified={**result['receipt'],'amount_msat':sats*1000}
        with oqs.Signature('ML-DSA-65') as verifier:
            valid=verifier.verify(b'qk-workshop/receipt/v1\0'+canonical(modified),bytes.fromhex(result['signature_hex']),bytes.fromhex(result['public_key_hex']))
        print('Firma válida:',valid)
if __name__=='__main__': main()
