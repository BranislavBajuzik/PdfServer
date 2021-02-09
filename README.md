# PdfServer

Simple Flask server that processes PDF files and provides them as PNG images.

# How to run

## Docker
```shell
cd docker
docker-compose up -d
```

### Cleanup
```shell
docker-compose down
docker volume rm docker_pdf_storage
```

## Local
_Tested on Ubuntu 18.4_

### Setup
[Optional] Setup virtualenv

```shell
sudo apt install poppler-utils  # Most distros have ths pre-installed
pip install -r requirements.txt
```

### Database and RabbitMQ
```shell
cd docker/local
docker-compose up
```

### Dramatiq worker
```shell
cd pdf_worker
dramatiq worker
```

### Server
```shell
cd pdf_server
python main.py
```

# API
Examples in runnable [REST file](test/hand.rest)

- `/documents`
  - Returns:
    ```json
    {
        "id": <document_id>
    }
    ```
  - Requires `document` form-data field
  - cURL example:
    ```shell
    curl -X POST --location "http://localhost:5000/documents" \
    -H "Authorization: Bearer 12345" \
    -H "Content-Type: multipart/form-data; boundary=WebAppBoundary" \
    -F "document=@test/sample.pdf;filename=document.pdf;type=*/*"
    ```
- `/documents/<int:document_id>`
  - Returns:
    ```json
    {
        "status": <"processing"|"done">,
        "n_pages": <n_pages>
    }
    ```
- `/documents/<int:document_id>/pages/<int:number>`
  - Returns: Rendered PNG

Errors have this JSON body:
```json
{
    "error": "message"
}
```
