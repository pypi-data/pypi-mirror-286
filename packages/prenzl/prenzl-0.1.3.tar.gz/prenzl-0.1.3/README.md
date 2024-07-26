# Prenzl AI agent observbility tool for agents and advanced RAG
This is the python sdk of Prenzl AI - an agent and advanced RAG observability tool.

### Installation
```
pip install prenzl
```

### Using Prenzl AI Observability
```
from prenzl import prenzl_observe

api_key = "YOUR_API_KEY"

# To work on local host
base_url = "http://localhost:3000/api"

# Initialize the observer
prenzl = Prenzl(api_key,base_url)

# Write observed data into DB
data = "Here goes your data you want to log in a JSON file."
result = prenzl.prenzl_observe(data)
```

The PyPI website for Prenzl AI can be found here: https://pypi.org/project/prenzl/
