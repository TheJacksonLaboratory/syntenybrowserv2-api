QTLS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "chr": {"type": "string"},
            "taxon_id": {"type": "number"},
            "symbol": {"type": "string"},
            "type": {"type": "string"},
            "start": {"type": "number"},
            "end": {"type": "number"}
        }
    },
    "minItems": 1
}