CYTOGENETIC_BAND_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "taxon_id": {"type": "number"},
            "chr": {"type": "string"},
            "source": {"type": "string"},
            "type": {"type": "string"},
            "start": {"type": "number"},
            "end": {"type": "number"},
            "location": {"type": "string"},
            "color": {"type": "string"}
        }
    },
    "minItems": 0
}