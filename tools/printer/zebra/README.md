# Zebra Printer Tool

Send ZPL (Zebra Programming Language) templates to Zebra printers.

## Usage

### Print ZPL

```
POST /print/zebra
```

Send ZPL template to a Zebra printer.

Request body:
```json
{
  "host": "192.168.1.100",
  "port": 9100,
  "zpl": "^XA^FO50,50^A0N,50,50^FDSample Label^FS^XZ"
}
```

- `host`: Printer IP address or hostname (default: "localhost")
- `port`: Printer port (default: 9100)
- `zpl`: ZPL template string

Response:
```json
{
  "status": "success",
  "message": "Label sent successfully",
  "printer": "192.168.1.100:9100"
}
```

## Example

```bash
curl -X POST http://localhost:8001/print/zebra \
  -H "Content-Type: application/json" \
  -d '{
    "host": "192.168.1.100",
    "port": 9100,
    "zpl": "^XA^FO50,50^A0N,50,50^FDSample^FS^XZ"
  }'
```
