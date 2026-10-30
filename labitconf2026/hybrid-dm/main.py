import json
from crypto_demo import dm_keys, dm, dm_open
def main():
    print('QuantaKrypto · mensaje híbrido · solo prueba')
    keys=dm_keys()
    print('1. Claves temporales:',json.dumps(keys,indent=2))
    message=input('2. Mensaje para Ana: ').strip()
    if not message or len(message)>500:
        raise ValueError('Escribí entre 1 y 500 caracteres.')
    envelope=dm({'keys':keys,'message':message})
    print('3. Sobre público:',json.dumps(envelope,ensure_ascii=False,indent=2))
    while True:
        received=input('4. Pegá un cifrado; Enter usa el original; salir termina: ').strip()
        if received=='salir': break
        result=dm_open({'keys':keys,'envelope':envelope,'ciphertext':received or envelope['ciphertext_hex']})
        print(json.dumps(result,ensure_ascii=False,indent=2))
        print('Coincide con el original:', result['valid'] and result['recovered']==message)
if __name__=='__main__': main()
