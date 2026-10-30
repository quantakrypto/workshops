import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def hash160(b): return hashlib.new('ripemd160',hashlib.sha256(b).digest()).hexdigest()

def classify(script, observed_public_keys):
    try: bytes.fromhex(script)
    except ValueError: return {'type':'unknown','exposure':'unknown','reason':'Script inválido.'}
    if len(script)==68 and script.startswith('5120'):
        return {'type':'P2TR','exposure':'exposed','reason':'La clave pública de salida está en el script.'}
    if len(script) in (70,134) and script[:2] in ('21','41') and script.endswith('ac'):
        return {'type':'P2PK','exposure':'exposed','reason':'La clave pública está en el script.'}
    target=None; typ='unknown'
    if len(script)==44 and script.startswith('0014'): target=script[4:];typ='P2WPKH'
    if len(script)==50 and script.startswith('76a914') and script.endswith('88ac'):target=script[6:-4];typ='P2PKH'
    if target:
        found=any(hash160(bytes.fromhex(k))==target for k in observed_public_keys)
        return {'type':typ,'exposure':'exposed' if found else 'not-observed','reason':'Una clave revelada coincide con esta huella.' if found else 'Solo se ve una huella en esta salida; sin coincidencia en la historia suministrada. No demuestra ausencia global de exposición.'}
    return {'type':'unknown','exposure':'unknown','reason':'Requiere revisar scripts, rutas de gasto e historia. No clasificamos como seguro.'}

def scanner(options=None):
    pk=ec.generate_private_key(ec.SECP256K1()).public_key().public_bytes(serialization.Encoding.X962,serialization.PublicFormat.CompressedPoint).hex()
    other=ec.generate_private_key(ec.SECP256K1()).public_key().public_bytes(serialization.Encoding.X962,serialization.PublicFormat.CompressedPoint).hex()
    cases=[('Clave pública en salida Taproot','5120'+pk[2:],100000),('Huella sin exposición observada','0014'+hash160(bytes.fromhex(other)),60000),('Huella de una clave ya revelada','0014'+hash160(bytes.fromhex(pk)),39500),('Script no analizado','0020'+hashlib.sha256(b'test script').hexdigest(),21000)]
    rows=[{'label':label,'txid':hashlib.sha256(label.encode()).hexdigest(),'vout':0,'sats':amount,'scriptPubKey':script,**classify(script,[pk])} for label,script,amount in cases]
    return {'demo':'scanner','network':'synthetic-fixtures','rows':rows,'observed_public_key':pk,'total_sats':sum(x['sats'] for x in rows),'limit':'UTXO = salida todavía no gastada. Datos sintéticos, sin consulta a una blockchain. No observar exposición no demuestra seguridad; no calcula una fecha de ataque.'}
