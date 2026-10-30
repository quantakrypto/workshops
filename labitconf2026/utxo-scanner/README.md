# Exposición de UTXOs

## Qué instalar

Python 3.12 y las dependencias de requirements.txt. No necesitás liboqs, Bitcoin Core ni una wallet.

Seguí la [guía de instalación](../INSTALL.md), que incluye macOS, notas para Linux/Windows y solución de problemas.

## Ejecutarlo

Desde la raíz del repositorio:

```sh
cd labitconf2026/utxo-scanner
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Los comandos anteriores son para macOS. La guía compartida explica los cambios para otros sistemas.

## Qué vas a hacer

Se crean cuatro salidas sintéticas. Elegís una y comparás la clasificación sin historia con la clasificación que incluye una clave pública revelada.

## Cómo comprobarlo

La salida 1 muestra una clave visible. La 2 queda no observada. La 3 cambia de no observada a expuesta al incluir la clave revelada. La 4 permanece desconocida. Escribí salir para terminar.

También podés ejecutar las pruebas automatizadas:

```sh
python -m unittest discover -p 'test_*.py'
```

## Qué contiene esta carpeta

main.py es el recorrido interactivo; crypto_demo.py contiene las operaciones; requirements.txt fija las dependencias; test_demo.py comprueba los resultados y los casos negativos.

## Límites

No consulta una blockchain ni audita una wallet. No observar exposición no demuestra seguridad. Las salidas y claves son ejemplos sintéticos; no hay fondos.
