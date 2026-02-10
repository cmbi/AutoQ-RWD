# AutoQ-RWD

This project is called **Auto**mated data **Q**uality Metrics Assesment in **R**eal **W**orld **D**ata.

It tries to apply metrics derived from the European Medicine Agency (EMA) Quality Metrics and other sources for the Common Data Elements present in a model. In this use case, the model used to retrieve the metrics is the [CARE-SM](https://github.com/CARE-SM/CARE-Semantic-Model) semantic model. These metrics can also be applied to many other data models.

## Pre-requisites

- Python 3.5 or later.
- Streamlit.
- CARE-SM model in a read-access repository.
- Install libraries found in `requirements.txt`. You can use them with a Python environment running the following code:

```
python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```


## Run

To run the website you need to run:

```
streamlit run main.py
```

Congratulations! You can enter to the website in [http://localhost:8501](http://localhost:8501).

After you add your CARE-SM repository URL in the first page of the website, the code will do SPARQL queries in your dataset and the page will show your metrics!
