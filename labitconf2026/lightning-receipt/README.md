# Recibo Lightning firmado

## Qué instalar

Python 3.12, Git, liboqs 0.16.0 y las dependencias de requirements.txt.

Seguí la [guía de instalación](../INSTALL.md), que incluye macOS, notas para Linux/Windows y solución de problemas.

## Ejecutarlo

Desde la raíz del repositorio:

```sh
cd labitconf2026/lightning-receipt
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export OQS_INSTALL_PATH="$(brew --prefix liboqs)"
python main.py
```

Los comandos anteriores son para macOS. La guía compartida explica los cambios para otros sistemas.

## Qué vas a hacer

Elegís entre 1 y 1.000.000 sats ficticios. ML-DSA-65 firma un JSON canónico con separación de dominio. Se muestran el recibo, la clave pública y la firma.

## Cómo comprobarlo

Verificá el importe original: Firma válida debe ser True. Sumale un sat: debe ser False. Escribí salir para terminar.

También podés ejecutar las pruebas automatizadas:

```sh
python -m unittest discover -p 'test_*.py'
```

## Qué contiene esta carpeta

main.py es el recorrido interactivo; crypto_demo.py contiene las operaciones; requirements.txt fija las dependencias; test_demo.py comprueba los resultados y los casos negativos.

## Límites

No se realiza un pago. La firma solo prueba que una clave firmó esa declaración, no que el dinero se liquidó. No modifica las firmas de Bitcoin ni Lightning. La clave del emisor requiere una fuente confiable.
