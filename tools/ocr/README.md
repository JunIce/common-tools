# OCR Tool

Offline OCR service using PaddleOCR for text recognition.

## Features

- Offline text recognition - no internet required after model download
- Chinese text recognition support
- Easy-to-use REST API
- Health check endpoint

## Usage

### OCR Recognition

```
POST /ocr
```

Upload an image file to extract text. Supported formats: PNG, JPG, JPEG, BMP, TIFF

```bash
curl -X POST -F "file=@image.jpg" http://localhost:8001/ocr
```

Response:
```json
{
  "filename": "image.jpg",
  "text": ["recognized text 1", "recognized text 2"],
  "count": 2,
  "status": "success"
}
```

## API Documentation

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
