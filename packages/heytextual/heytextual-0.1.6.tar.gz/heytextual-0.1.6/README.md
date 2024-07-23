# HeyTextual Python SDK

Este repositorio contiene el SDK de Python para la API de HeyTextual.

## Installación

```bash
pip install heytextual
```

## Uso

Puedes encontrar más información en la API reference de nuestro website.

Ejemplo:
```python
import heytextual

client = heytextual.Client(api_key="your_api_key")

data = client.extract("/path/to/file", "AUTO")
print(data)

documents = client.documents(limit=20, start_date="2024-07-07", end_date="2024-07-20")
print(documents)

document = client.document(document_id="DOCUMENTID")
print(document)

templates = client.templates(limit=20, start_date="2024-07-07", end_date="2024-07-20")
print(templates)
```
