# Instalación

Necesitás una computadora, una terminal y Python 3.12. La configuración comprobada es macOS con liboqs 0.16.0 y Python 3.12. Las demos de mensajes y recibos usan liboqs; el escáner no.

## macOS

Instalá [Homebrew](https://brew.sh) si no lo tenés. Luego:

```sh
brew install python@3.12 git
# Solo mensaje híbrido y recibo:
brew install liboqs
export OQS_INSTALL_PATH="$(brew --prefix liboqs)"
```

Entrá a la carpeta de una demo y ejecutá:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -p 'test_*.py'
python main.py
```

La primera instalación descarga dependencias; después las demos funcionan sin red. Abrir otra terminal requiere volver a activar .venv y definir OQS_INSTALL_PATH para las dos demos postcuánticas.

## Linux y Windows

Usá Python 3.12 y Git. Para mensajes o recibos instalá liboqs 0.16.0 como biblioteca compartida siguiendo las instrucciones oficiales de [liboqs](https://github.com/open-quantum-safe/liboqs) y [liboqs-python](https://github.com/open-quantum-safe/liboqs-python). Necesitarás un compilador C y CMake si construís la biblioteca desde sus fuentes. OQS_INSTALL_PATH debe apuntar a su prefijo de instalación. No se verificó este paquete en Linux o Windows.

En Linux, los pasos del entorno virtual son los mismos que en macOS. En PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
# Solo las demos que usan liboqs; reemplazá la ruta:
$env:OQS_INSTALL_PATH = "C:\ruta\a\liboqs"
.venv\Scripts\python.exe -m unittest discover -p "test_*.py"
.venv\Scripts\python.exe main.py
```

## Si algo falla

- **No module named oqs**: instalá requirements.txt usando el Python del entorno de esa demo.
- **No se encuentra liboqs**: comprobá OQS_INSTALL_PATH y que instalaste una biblioteca compartida compatible con tu arquitectura.
- **No module named cryptography**: ejecutá de nuevo la instalación de requirements.txt dentro del entorno.
- **Git no está disponible**: es necesario para descargar el wrapper fijado a un commit.
- **No se ve el mismo resultado hexadecimal**: las claves y nonces se generan de nuevo; es lo esperado. Compará el resultado de las verificaciones, no claves entre ejecuciones.

## Qué instalamos

Python ejecuta el código; cryptography implementa X25519, HKDF, AES-GCM y las claves de los ejemplos de UTXOs; liboqs implementa ML-KEM y ML-DSA; liboqs-python conecta Python con esa biblioteca. Las dependencias Python están fijadas en cada requirements.txt. El código utiliza bibliotecas externas, no implementaciones criptográficas propias.
