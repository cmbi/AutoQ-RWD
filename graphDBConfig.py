import requests
import pandas as pd
import streamlit as st

# 2. --- Helper Function: Run SPARQL Query ---
def run_sparql_query(query: str) -> pd.DataFrame:
    headers = {
        "Accept": "application/sparql-results+json",
    }
    url = st.session_state["url"]
    print(url)
    response = requests.post(url, data={"query": query}, headers=headers)
    response.raise_for_status()
    results = response.json()

    columns = results['head']['vars']
    rows = [
        [binding.get(col, {}).get('value', None) for col in columns]
        for binding in results['results']['bindings']
    ]
    df = pd.DataFrame(rows, columns=columns)
    return df