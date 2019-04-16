"""
JWT Utilities for Controller
"""

AUTHORIZATIONS = {
    'Access': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'Refresh': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
