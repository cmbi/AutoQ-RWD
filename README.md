# AutoQ-RWD

This project is called **Auto**mated data **Q**uality Metrics Assesment in **R**eal **W**orld **D**ata.

It aims to apply metrics derived from the European Medicine Agency (EMA) Quality Metrics and other sources for the Common Data Elements present in a model. In this use case, the model used to retrieve the metrics is the [CARE-SM](https://github.com/CARE-SM/CARE-Semantic-Model) semantic model.

To learn how to map your own data model to CARE-SM and how to implement the semantic model in an RDF graph, follow the instructions in the official [CARE-SM documentation](https://care-sm.readthedocs.io/en/latest/introduction.html).

Once your data is aligned with CARE-SM and available in a graph database, AutoQ-RWD can automatically compute the EMA-derived data quality metrics.


## ✨ Features

- Automatic computation of EMA‑based data quality metrics  
- SPARQL‑driven assessment using semantic (RDF) data  
- Fully compatible with CARE‑SM and CDE‑aligned rare‑disease registries  
- Simple Streamlit‑based interface (no HTML/JS required)  
- Real‑time visualisation using Plotly and Streamlit components  
- Easily extendable with new metrics and queries  


## 📦 Pre-requisites

- Python 3.5 or later
- Streamlit
- CARE-SM model in a read-access repository
- Install all required libraries from `requirements.txt`

**It is strongly recommended creating a dedicated virtual environment:**

```
python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## ▶️  Run

To start the AutoQ‑RWD web application, run the following command:

```
streamlit run main.py
```

🎉Congratulations! AutoQ-RWD is now running at: [http://localhost:8501](http://localhost:8501)

On the main page of the application:

1. Enter the URL of your **CARE‑SM SPARQL endpoint**.  
2. AutoQ‑RWD will automatically execute the predefined SPARQL queries on your dataset.  
3. The dashboard will display your **EMA‑derived data‑quality metrics** as interactive tables and visualisations.
