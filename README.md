# Common Tools

A FastAPI-based microservice providing common utility tools.

## Tools

- **OCR**: Offline OCR service using PaddleOCR for text recognition. [See details](./tools/ocr/README.md)
- **Printer**: Printer tools
  - **Zebra**: Send ZPL templates to Zebra printers. [See details](./tools/printer/zebra/README.md)

## Requirements

- Python 3.8+
- PaddlePaddle
- PaddleOCR
- FastAPI
- Uvicorn
- Pillow

## Installation

```bash
pip install -r requirements.txt
```

Or using uv:

```bash
uv pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The service will start on `http://localhost:8001`

## API Endpoints

### Root

```
GET /
```

### Health Check

```
GET /health
```

See [OCR Tool](./tools/ocr/README.md) for OCR API details.

## API Documentation

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Project Structure

```
├── main.py                 # Application entry point
├── tools/
│   ├── ocr/               # OCR tool
│   │   ├── ocr.py        # OCR engine
│   │   └── routes.py     # OCR API routes
│   └── printer/          # Printer tool
│       └── zebra/       # Zebra printer tool
├── models/                # Model files
└── temp/                 # Temporary files
```
