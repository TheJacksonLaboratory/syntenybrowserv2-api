SCHEMA_ONT_TERMS_SIMPLE = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "count": {"type": "number"}
        }
    },
    "minItems": 1
}


SCHEMA_ONT_TERMS = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "namespace": {"type": "string"},
            "def": {"type": "string"},
            "descendants": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "count": {"type": "number"}
                    }
                },
                "minItems": 0
            }
        }
    },
    "minItems": 1
}


SCHEMA_ONT_METADATA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "namespace": {"type": "string"},
            "def": {"type": "string"},
            "descendants": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "count": {"type": "number"}
                    }
                },
                "minItems": 0
            }
        }
    },
    "minItems": 1
}


SCHEMA_ONT_ASSOCIATIONS = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "taxon_id": {"type": "number"},
            "symbol": {"type": "string"},
            "chr": {"type": "string"},
            "start": {"type": "number"},
            "end": {"type": "number"},
            "strand": {"type": "string"},
            "type": {"type": "string"},
            "term_id": {"type": "string"},
            "term_name": {"type": "string"}
        }
    },
    "minItems": 1
}