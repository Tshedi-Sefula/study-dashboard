# save_oas.py
import json
import os
from main import app  

def save_openapi_spec():
    # Get the OpenAPI schema
    openapi_schema = app.openapi()
    
    # Save to file
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    print("OpenAPI spec saved to openapi.json")

if __name__ == "__main__":
    save_openapi_spec()