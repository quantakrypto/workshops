# LABITCONF 2026 · QuantaKrypto

Primero exploramos computación cuántica y riesgos para sistemas descentralizados; después probamos una demo.

| Demo | Qué hacés | Qué comprobás |
| --- | --- | --- |
| [Mensaje híbrido](hybrid-dm/README.md) | Creás claves X25519 + ML-KEM y cifrás tu mensaje | Que Ana puede abrirlo y que una alteración se rechaza |
| [Recibo firmado](lightning-receipt/README.md) | Firmás un importe ficticio con ML-DSA | Que cambiar el importe invalida la firma |
| [Exposición de UTXOs](utxo-scanner/README.md) | Comparás cuatro salidas sintéticas | Qué cambia cuando conocemos una clave pública revelada |

No necesitás ejecutar las tres. Abrí el README de la que elegiste y seguí sus pasos. La instalación requiere computadora; el navegador del taller puede usarse desde el teléfono.

[Instalación y problemas frecuentes](INSTALL.md).

Estos ejercicios reproducen las operaciones del taller por consola. No incluyen las diapositivas ni despliegan el sitio web. El mensaje es un prototipo de cifrado, no un cliente Nostr interoperable. El recibo no prueba un pago real. El escáner no determina que una wallet sea segura.
