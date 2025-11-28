import streamlit as st


# Nested pages
# https://github.com/blackary/st_pages/


# st.navigation(["main.py", "pages/metricsPage.py"], position="hidden")

st.title("AutoQ-RWD Data Quality Report 📊")
st.markdown(
    """
    This webpage shows the quality metrics of your [CARE-SM model](https://github.com/CARE-SM/CARE-Semantic-Model?tab=readme-ov-file).
    These metrics are based on the ones in EMA and will help you to understand the quality of your data.
    The data is stored in a [SPARQL](https://www.w3.org/TR/rdf-sparql-query/) endpoint.
    The metrics are based queried on your [GraphDB](https://graphdb.ontotext.com/) database.
    """
)

st.subheader(":rainbow[Let's start!]")

url = st.text_input("Provide your URL👇 (Ex: http://localhost:7200/repositories/NameOfRepository)")

if st.button("Get Metrics 📈"):
    if url:
        st.session_state["url"] = url
        st.switch_page("pages/metricsPage.py")
    else:
        st.error("Please provide a URL before continuing.")