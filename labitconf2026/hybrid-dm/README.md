# Mensaje híbrido

## Qué instalar

Python 3.12, Git, liboqs 0.16.0 y las dependencias de requirements.txt.

Seguí la [guía de instalación](../INSTALL.md), que incluye macOS, notas para Linux/Windows y solución de problemas.

## Ejecutarlo

Desde la raíz del repositorio:

```sh
cd labitconf2026/hybrid-dm
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export OQS_INSTALL_PATH="$(brew --prefix liboqs)"
python main.py
```

Los comandos anteriores son para macOS. La guía compartida explica los cambios para otros sistemas.

## Qué vas a hacer

Se generan claves X25519 y ML-KEM-768 de prueba. Escribís hasta 500 caracteres y se crea un sobre con HKDF-SHA256 y AES-256-GCM.

## Cómo comprobarlo

Enter en la comprobación usa el cifrado original: valid debe ser true y el texto recuperado debe coincidir. Pegá una copia y cambiá un carácter hexadecimal: valid debe ser false. Escribí salir para terminar.

También podés ejecutar las pruebas automatizadas:

```sh
python -m unittest discover -p 'test_*.py'
```

## Qué contiene esta carpeta

main.py es el recorrido interactivo; crypto_demo.py contiene las operaciones; requirements.txt fija las dependencias; test_demo.py comprueba los resultados y los casos negativos.

## Límites

Las claves privadas se muestran exclusivamente para aprender. No hay autenticación de identidades Nostr ni NIP-44/NIP-59, red de relays o integración con extensiones. ML-KEM crea sus claves de forma independiente; el prototipo híbrido no es un protocolo de producción.
