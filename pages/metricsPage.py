import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

import EMAqueries

st.title("Metrics 📈")
st.markdown("This page displays charts based on data from your GraphDB.")

# Add your logic to fetch and display charts here

st.header("Accuracy Metrics")

# Patients with Disability Score above a certain threshold
st.subheader("% Patients with Disability Score above a certain threshold")

st.markdown(
    """
    Percentage of patients with Disability score higher than a certain threshold.
    """
)

number = st.number_input(
    "Insert a number", value=10, placeholder="10"
)
resultThreshold, resultTotal = EMAqueries.recordsDisabilityScoreAboveTreshold(number)

percentage = (int(resultThreshold.iloc[0]["aboveValue"])/int(resultTotal.iloc[0]["numTotal"]))*100
percentage = round(percentage, 2)
if resultTotal.iloc[0]["numTotal"] == "0":
    st.error('No Disability Score found in the database.', icon="🚨")
else:
    st.write(f"Percentage of patients with Disability score above {number}: {percentage}%")


# Patients with Disability Score above a certain threshold
st.subheader("% Changes in Ambulatory State")

st.markdown(
    """
    Percentage of changes in ambulatory states between measurements in a certain amount of time.
    """
)

duration = st.number_input(
    "Insert a maximum duration period (in days)", value=100, placeholder="100"
)
result = EMAqueries.percentagesChangesAmbulatoryState(duration)
print(result)
if result.iloc[0]["totalPairs"] == "0":
    st.error('No Ambulatory states found in the database.', icon="🚨")
else:
    st.write(f"Percentage of patients with changes in ambulatory states in less than {duration} days: {round(float(result.iloc[0]["percentageUnderXDays"]), 2)}%")


# Duplicate Patient IDs
st.subheader("% Duplicate Patient IDs")

st.markdown(
    """
    Percentage of duplicate Patient IDs in the database.
    """
)

result = EMAqueries.duplicatedIDinSameContext()
print(result)
if result.iloc[0]["totalUniqueIDs"] == "0":
    st.error('No Patient IDs found in the database.', icon="🚨")
else:
    st.write(f"Percentage of duplicate Patient IDs: {round(float(result.iloc[0]["duplicatePercentage"]), 2)}%")
    st.info('In case you have duplicated data in your database, it should be flagged 🚩', icon="ℹ️")


st.header("Precision Metric")


# Length of decimals
st.subheader("Length of decimals")

st.markdown(
    """
    This chart shows the length of decimals in the database.
    """
)

result = EMAqueries.numberDecimals()
if result.empty:
    st.error('No decimals found in the database.', icon="🚨")
else:
    tab1, tab2 = st.tabs(["Chart", "Dataframe"])
    result["count"] = pd.to_numeric(result["count"], errors='coerce', downcast='integer')
    tab1.bar_chart(result, x="decimals", y="count", height=250)
    tab2.dataframe(result, height=250, use_container_width=True)


st.header("Completeness Metrics")

# CDE properties with missing values
st.subheader("CDE properties with missing values")

st.markdown(
    """
    This chart shows the number of values missing for each Common Data Element.
    """
)

result = EMAqueries.propertiesWithNoValues()

combined_results = pd.DataFrame()

for CDEProperty in result:
    if CDEProperty[0].empty:
        st.error(f'No {CDEProperty[2]} found in the database.', icon="🚨")
    else:
        percentageMissingValues =(1 - (int(CDEProperty[1].iloc[0]["countTresh"]) / int(CDEProperty[0].iloc[0]["countTotal"]))) * 100
        percentageMissingValues = round(percentageMissingValues, 2)
        combined_results = pd.concat(
            [combined_results, pd.DataFrame([{"CDE Property": CDEProperty[2], "% Missing Values": percentageMissingValues}])],
            ignore_index=True
        )

# Create a chart from the combined DataFrame
if not combined_results.empty:
    tab1, tab2 = st.tabs(["Chart", "Dataframe"])
    tab1.bar_chart(combined_results, x="CDE Property", y="% Missing Values", height=250)
    tab2.dataframe(combined_results, height=250, use_container_width=True)



# Patients with multiple disability checks
st.subheader("% Patients with multiple disability checks")

st.markdown(
    """
    Percentage of patients with multiple disability checks.
    """
)

resultMultiple, resultOne, resultTotal  = EMAqueries.patientsMultipleDisabilities()

isResult = False

if resultMultiple.empty and resultOne.empty:
    st.error('No Patients with Disability scores found in the database.', icon="🚨")
elif resultMultiple.empty:
    isResult = True
    oneCheck = int(resultOne.iloc[0]["totalID"]) / int(resultTotal.iloc[0]["totalID"])
    noDisability = 1 - oneCheck
    resultsDataset= pd.DataFrame([{"Label": ['No Disability', 'One Check'], 'Values': [noDisability, oneCheck] }])    
    labelDis = ['No Disability', 'One Check']
    valuesDis = [noDisability, oneCheck]
elif resultOne.empty:
    isResult = True
    multipleChecks = int(resultMultiple.iloc[0]["totalID"]) / int(resultTotal.iloc[0]["totalID"])
    noDisability = 1 - multipleChecks
    labelDis = ['No Disability', 'Multiple Checks']
    valuesDis = [noDisability, multipleChecks]
else:
    isResult = True
    multipleChecks = int(resultMultiple.iloc[0]["totalID"]) / int(resultTotal.iloc[0]["totalID"])
    oneCheck = int(resultOne.iloc[0]["totalID"]) / int(resultTotal.iloc[0]["totalID"])
    noDisability = 1 - (multipleChecks + oneCheck)
    labelDis = ['No Disability', 'Multiple Checks', 'One Check']
    valuesDis = [noDisability, multipleChecks, oneCheck]

if isResult:

    fig = go.Figure(data=[go.Pie(
        labels=labelDis,
        values=valuesDis,
        textinfo='percent',
        insidetextorientation='radial',
        hoverinfo='label+percent+value',
        hole=0.3
    )])
    # Customize hover template
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>" +
                    "Percentage: %{percent:.1%}",
        textfont_size=14
    )
    fig.update_layout(
    uniformtext_minsize=12,
    uniformtext_mode='hide',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    )
    )
    st.plotly_chart(fig, use_container_width=True)

st.header("Format coherence (conformance)")


# HPO terms in the Phenotype
st.subheader("% HPO terms in the Phenotype property")

st.markdown(
    """
    Percentage HPO terms in the Phenotype property
    """
)

resultHPO, resultOther = EMAqueries.phenotypeHPOQuery()

if resultHPO.iloc[0]["countTotal"] == "0" and resultOther.iloc[0]["countTotal"] == "0":
    st.error('No ontology from Phenotype found in the database.', icon="🚨")
else:

    st.write(f"Percentage of HPO terms in the Phenotype property: {round((int(resultHPO.iloc[0]["countTotal"])/(int(resultHPO.iloc[0]["countTotal"])+int(resultOther.iloc[0]["countTotal"])))*100, 2)}%")


# NCIT terms in Sex
st.subheader("% NCIT terms in the Sex property")

st.markdown(
    """
    Percentage NCIT terms in the Sex property
    """
)

resultNCIT, resultOther = EMAqueries.sexNCITQuery()

if resultNCIT.iloc[0]["countTotal"] == "0" and resultOther.iloc[0]["countTotal"] == "0":
    st.error('No ontology from Sex found in the database.', icon="🚨")
else:

    st.write(f"Percentage of NCIT terms in the Phenotype property: {round((int(resultNCIT.iloc[0]["countTotal"])/(int(resultNCIT.iloc[0]["countTotal"])+int(resultOther.iloc[0]["countTotal"])))*100, 2)}%")


st.header("Relational coherence (conformance)")

# Correct Age

st.subheader("Correct Age")
st.markdown(
    """
    Check if the age is correct based on the date of birth and the date of the measurement.
    """
)

result = EMAqueries.checkAge()

if result.empty:
    st.error('No Age attribute found in the database.', icon="🚨")
else:
    countPeople = 0
    countPeopleCorrectAge = 0
    for rowNumber in range(result.shape[0]):
        countPeople += 1
        startDate = datetime.strptime(result.iloc[rowNumber]['startdate'], "%Y-%m-%d")
        birthDate = datetime.strptime(result.iloc[rowNumber]['BirthDate'], "%Y-%m-%d")
        ageValue = int(float(result.iloc[rowNumber]['ageValue']))
        deltaDays = startDate - birthDate
        yearsDiff= int(deltaDays.days / 365.25)
        if ageValue == int(yearsDiff):
            countPeopleCorrectAge += 1
    st.write(f"Percentage of correct Age values: {round((countPeopleCorrectAge/countPeople)*100, 2)}%")



# % ORDO terms in the Diagnosis property
st.subheader("% ORDO terms in the Diagnosis property")

st.markdown(
    """
    Percentage ORDO terms in the Diagnosis property
    """
)

resultORDO, resultOther = EMAqueries.checkDiagnosisOntologies()

if resultORDO.iloc[0]["countTotal"] == "0" and resultOther.iloc[0]["countTotal"] == "0":
    st.error('No ontology from Diagnosis found in the database.', icon="🚨")
else:

    st.write(f"Percentage of ORDO terms in the Diagnosis property: {round((int(resultORDO.iloc[0]["countTotal"])/(int(resultORDO.iloc[0]["countTotal"])+int(resultOther.iloc[0]["countTotal"])))*100, 2)}%")


# st.header("Currency (Is your data up to date?)")

# Avg time between event ID
st.subheader("Avg time between event ID")

st.markdown(
    """
    Average time between event ID for the same patient.
    """
)

result = EMAqueries.avgTimeEventId()

if result.empty:
    st.error('No Event time attribute found in the database.', icon="🚨")
else:
    st.write(f"Average days between events: {round(float(result.iloc[0]["averageGapInDays"]), 2)} days")



if st.button("Back to Main Page"):
    st.switch_page("main.py")
