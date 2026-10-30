import json
from crypto_demo import scanner, classify
def main():
    data=scanner()
    print('QuantaKrypto · UTXOs sintéticos · no se consulta una blockchain')
    print(json.dumps(data,ensure_ascii=False,indent=2))
    while True:
        value=input('Elegí salida 1–4; salir termina: ').strip()
        if value=='salir': break
        index=int(value)-1
        if index not in range(4): print('Elegí 1–4'); continue
        script=data['rows'][index]['scriptPubKey']
        print('Sin historia:',classify(script,[]))
        print('Con clave revelada:',classify(script,[data['observed_public_key']]))
if __name__=='__main__': main()
