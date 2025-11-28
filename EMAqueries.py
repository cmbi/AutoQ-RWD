# SPARQL Queries file

from graphDBConfig import run_sparql_query

def recordsDisabilityScoreAboveTreshold(treshold):
    queryThreshold = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (count(?val) as ?aboveValue)
            WHERE {
                ?attr a obo:NCIT_C21007.
                ?output sio:SIO_000628 ?attr.
                ?output sio:SIO_000300 ?val.
                FILTER(?val > %s)
            }
    """ % (treshold)
    queryTotal = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT 
        (COUNT(?valTotal) AS ?numTotal)
        WHERE {
        ?attr a obo:NCIT_C21007.
        ?output sio:SIO_000628 ?attr.
        ?output sio:SIO_000300 ?valTotal.
        }
    """
    resultThreshold = run_sparql_query(queryThreshold)
    resultTotal = run_sparql_query(queryTotal)

    return resultThreshold, resultTotal

def percentagesChangesAmbulatoryState(duration):
    query = """
        PREFIX ofn: <http://www.ontotext.com/sparql/functions/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        PREFIX sio: <http://semanticscience.org/resource/>


        select 
            (SUM(IF(?duration <= %s, 1, 0)) AS ?pairsUnderXDays)
        (COUNT(*) AS ?totalPairs)
            ((SUM(IF(?duration <= %s, 1, 0)) * 100 / 
        COUNT(*)) AS ?percentageUnderXDays)
        where {
        Select distinct ?timeline ?enddate1 ?startdate2 ?duration
            WHERE {
                ?event1 a obo:NCIT_C25499.
                ?elem1 sio:SIO_000068 ?event1;
                    sio:SIO_000681 ?end1;
                    sio:SIO_000068 ?timeline.
                ?end1 sio:SIO_000300 ?enddate1.

                ?event2 a obo:NCIT_C25499.
                ?elem2 sio:SIO_000068 ?event2;
                    sio:SIO_000680 ?start2;
                    sio:SIO_000068 ?timeline.
                ?start2 sio:SIO_000300 ?startdate2.

                FILTER(?event1 != ?event2)
                FILTER (?enddate1 <= ?startdate2)
                BIND (ofn:daysBetween(?startdate2, ?enddate1) as ?duration)
                FILTER NOT EXISTS {
                    ?event3 a obo:NCIT_C25499.
                    ?elem3 sio:SIO_000068 ?event3;
                        sio:SIO_000680 ?start3;
                        sio:SIO_000681 ?end3;
                        sio:SIO_000068 ?timeline.
                    ?end3 sio:SIO_000300 ?enddate3.
                    ?start3 sio:SIO_000300 ?startdate3.
                    FILTER(?enddate1 < ?startdate3 && ?enddate3 < ?startdate2)
                }    
            }
        }
    """ % (duration, duration)
    result = run_sparql_query(query)
    return result


def duplicatedIDinSameContext():
    query = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        select

        (COUNT(DISTINCT ?totalID) AS ?totalUniqueIDs)
        (COUNT(DISTINCT ?id) AS ?dupUniqueIDs)
        ((COUNT(DISTINCT ?id) * 100.0) / COUNT(DISTINCT ?totalID) AS ?duplicatePercentage)
        where {
            ?context a obo:NCIT_C62143.
            ?context sio:SIO_000068 ?time.
            ?time sio:SIO_000332 ?ind.
            ?ind sio:SIO_000671 ?totalID.
            OPTIONAL {
                SELECT ?context ?id
                WHERE {
                    ?context a obo:NCIT_C62143.
                    ?context sio:SIO_000068 ?time.
                    ?time sio:SIO_000332 ?ind.
                    ?ind sio:SIO_000671 ?id.
                }
                GROUP BY ?context ?id
                HAVING (COUNT(?id) > 1) 
            }
        }
    """
    result = run_sparql_query(query)
    return result

def numberDecimals():
    query = """
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT ?decimals (COUNT(*) as ?count)
        WHERE {
        ?subject ?predicate ?value .
        FILTER(datatype(?value) = xsd:float)
            BIND(STR(?value) AS ?valStr)
            BIND(STRLEN(STRAFTER(?valStr, ".")) AS ?decimals)
        }
        group by ?decimals
    """
    result = run_sparql_query(query)
    return result

def propertiesWithNoValues():

    # Make a query for each property
    sexQueryTotal = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT ?type (COUNT(?type) as ?countTotal)
        WHERE {
            ?out a ?type ;
            sio:SIO_000628 ?att .
            FILTER( ?type = obo:NCIT_C160908)
        }
        GROUP BY ?onttype ?type
    """
    sexQueryThreshold = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT ?type (COUNT(?nullVar) as ?countTresh)
        WHERE {
            ?out a ?type ;
            sio:SIO_000628 ?att .
            ?att a ?onttype .

            FILTER( ?type = obo:NCIT_C160908)
            OPTIONAL{
            FILTER (
                    (?onttype IN (
                        obo:NCIT_C20197,    # Male
                        obo:NCIT_C16576,    # Female
                        obo:NCIT_C124294,   # Unknown
                        obo:NCIT_C17998     # Undifferentiated
                    ))
                    )
            BIND(?att AS ?nullVar)
            }
        }
        GROUP BY ?type
    """
    birthDateQueryTotal = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        SELECT (COUNT(?att) AS ?countTotal)
        WHERE {
        ?att a ?type .
        ?out sio:SIO_000628 ?att .
        FILTER(?type = obo:NCIT_C68615)
        }
        GROUP BY ?type
        HAVING (COUNT(?att) > 0)
    """
    birthDateQueryThreshold = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        select (COUNT(?val) AS ?countTresh)
        where {
            ?att a ?type.
            ?out sio:SIO_000628 ?att .
    		?out sio:SIO_000300 ?val.

            FILTER(?type = obo:NCIT_C68615)
            FILTER( str(?val) !='')
        }
    """
    idQueryTotal = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>        

        SELECT (COUNT(?type) AS ?countTotal)
        WHERE {
            ?variable a ?type ;
                        sio:SIO_000020 ?role .
            ?ind a sio:SIO_000498 ;
                sio:SIO_000228 ?role .
            FILTER(?type = sio:SIO_000115)
        }
        GROUP BY ?type
        HAVING (COUNT(?type) > 0)
    """
    idQueryThreshold = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>        

        SELECT (COUNT(?value) AS ?countTresh)
        WHERE {
            ?variable a ?type ;
                        sio:SIO_000020 ?role .
            ?ind a sio:SIO_000498 ;
                sio:SIO_000228 ?role .
            ?variable sio:SIO_000300 ?value .
            FILTER(?type = sio:SIO_000115)
            Filter(str(?value) != '')
        }
    """
    disabilityQueryTotal = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>        

        SELECT (COUNT(?type) AS ?countTotal)
        WHERE {
            ?att a ?type .
            ?out sio:SIO_000628 ?att.
            FILTER(?type = obo:NCIT_C21007)
        }
        GROUP BY ?type
        HAVING (COUNT(?type) > 0)
    """

    disabilityQueryThreshold = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (COUNT(?value) AS ?countTresh)
        WHERE {
            ?att a ?type .
            ?out sio:SIO_000628 ?att.
            ?out sio:SIO_000300 ?value.
            FILTER(?type = obo:NCIT_C21007)
            Filter(str(?value) != '')
        }
    """

    diagnosisQueryTotal = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (COUNT(?type) as ?countTotal)
        WHERE {
            ?out a ?type ;
            sio:SIO_000628 ?att .
            FILTER( ?type = obo:NCIT_C154625)
        }
        GROUP BY ?onttype ?type
    """

    diagnosisQueryThreshold = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT ?type (COUNT(?nullVar) as ?countTresh)
        WHERE {
            ?out a ?type ;
            sio:SIO_000628 ?att .

            FILTER( ?type = obo:NCIT_C154625)
            OPTIONAL{
            ?att a ?onttype .
            FILTER (
                    (?onttype IN (
						sio:SIO_000614
                    ))
                    )
            BIND(?att AS ?nullVar)
            }
        }
        GROUP BY ?type
    """
    consentQueryTotal = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (COUNT(?nullVar) as ?countTotal)
        WHERE {
            ?out a ?type ;
            sio:SIO_000628 ?att .
            FILTER( ?type = obo:NCIT_C25460)
        } GROUP BY ?onttype ?type
    """

    consentQueryThreshold = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT ?type (COUNT(?nullVar) as ?countTresh)
        WHERE {
            ?out a ?type ;
            sio:SIO_000628 ?att .

            FILTER( ?type = obo:NCIT_C25460)
            OPTIONAL{
            ?att a ?onttype .
            FILTER (
                    (?onttype IN (
                obo:DUO_0000001, # Attribute
                obo:OBIB_0000488                    ))
                    )
            BIND(?att AS ?nullVar)
            }
        }
        GROUP BY ?type
    """
    # Genetic
    geneticQueryTotal = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>        

        SELECT (COUNT(?type) AS ?countTotal)
        WHERE {
            ?variable a ?type .
            ?variable sio:SIO_000229 ?out .
            FILTER(?type = obo:NCIT_C15709)
        }
        GROUP BY ?type
        HAVING (COUNT(?type) > 0)
    """
    geneticQueryThreshold = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (COUNT(?value) AS ?countTresh)
        WHERE {
            ?variable a ?type .
            ?variable sio:SIO_000229 ?out .
    		?out sio:SIO_000671 ?value.
            FILTER(?type = obo:NCIT_C15709)
            Filter(str(?value) != '')
        }
    """
    # Don't know how to do biobank

    sexResult = [run_sparql_query(sexQueryTotal), run_sparql_query(sexQueryThreshold), "Sex"]
    birthDateResult =[run_sparql_query(birthDateQueryTotal), run_sparql_query(birthDateQueryThreshold), "BirthDate"]
    idResult = [run_sparql_query(idQueryTotal), run_sparql_query(idQueryThreshold), "ID"]
    disabilityResult = [run_sparql_query(disabilityQueryTotal), run_sparql_query(disabilityQueryThreshold), "Disability"]
    diagnosisResult = [run_sparql_query(diagnosisQueryTotal), run_sparql_query(diagnosisQueryThreshold), "Diagnosis"]
    consentResult = [run_sparql_query(consentQueryTotal), run_sparql_query(consentQueryThreshold), "Consent"]
    geneticResult = [run_sparql_query(geneticQueryTotal), run_sparql_query(geneticQueryThreshold), "Genetic"]

    # Add the results to a list
    result = [sexResult, birthDateResult, idResult, disabilityResult, diagnosisResult, consentResult, geneticResult]

    return result
    
def patientsMultipleDisabilities():
    # Multiple Disabilities
    queryMultiple = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        select (count(?idval) as ?totalID)
        where {
        SELECT ?idval
        (count(?idval) as ?countThreshold)
        WHERE {
            #Search Disability value
            ?attr a obo:NCIT_C21007.
            ?output sio:SIO_000628 ?attr;
            sio:SIO_000300 ?val.
            # Search individual related to the Disability Val
            ?id a sio:SIO_000115;
                sio:SIO_000300 ?idval;
                sio:SIO_000020 ?role.
            ?role sio:SIO_000356 ?proc.
            ?proc sio:SIO_000229 ?output.

        }group by ?idval
        having(count(?val)>1)   
        }
    """
    # One disability
    queryOne = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        select (count(?idval) as ?totalID)
        where {
        SELECT ?idval
        (count(?idval) as ?countThreshold)
        WHERE {
            #Search Disability value
            ?attr a obo:NCIT_C21007.
            ?output sio:SIO_000628 ?attr;
            sio:SIO_000300 ?val.
            # Search individual related to the Disability Val
            ?id a sio:SIO_000115;
                sio:SIO_000300 ?idval;
                sio:SIO_000020 ?role.
            ?role sio:SIO_000356 ?proc.
            ?proc sio:SIO_000229 ?output.

        }group by ?idval
        having(count(?val)=1)   
        }
    """
    # 0 Disabilties
    queryTotal = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        select (count(?idval) as ?totalID)
        where {
        SELECT distinct ?idval
        WHERE {
            ?id a sio:SIO_000115;
            sio:SIO_000300 ?idval;
            sio:SIO_000020 ?role.
            ?role sio:SIO_000356 ?proc.
            ?proc sio:SIO_000229 ?output.
            
        } group by ?idval
                }
    """

    resultMultiple = run_sparql_query(queryMultiple)
    resultOne = run_sparql_query(queryOne)
    resultTotal = run_sparql_query(queryTotal)

    return resultMultiple, resultOne, resultTotal

def phenotypeHPOQuery():

    # Make a query for HPO in Phenotype
    queryHPO = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (count(?val) as ?countTotal)
        WHERE {
            ?spec a obo:NCIT_C16977.
            ?spec sio:SIO_000628 ?atr.
            ?atr a ?val.
            FILTER(regex(str(?val), "HP:"))
        }
    """

    queryOther = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (count(?val) as ?countTotal)
        WHERE {
            ?spec a obo:NCIT_C16977.
            ?spec sio:SIO_000628 ?atr.
            ?atr a ?val.
            FILTER(! regex(str(?val), "HP"))
            FILTER(! regex(str(?val), "SIO_000614"))

        }
    """
    resultHPO = run_sparql_query(queryHPO)
    resultOther = run_sparql_query(queryOther)
    return resultHPO, resultOther

def sexNCITQuery():

    # Make a query for NCIT (Sex)
    queryNCIT = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (count(?val) as ?countTotal)
        WHERE {
            ?spec a obo:NCIT_C160908.
            ?spec sio:SIO_000628 ?atr.
            ?atr a ?val.
            FILTER(regex(str(?val), "NCIT"))
        }
    """

    queryOther = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (count(?val) as ?countTotal)
        WHERE {
            ?spec a obo:NCIT_C160908.
            ?spec sio:SIO_000628 ?atr.
            ?atr a ?val.
            FILTER(! regex(str(?val), "NCIT"))
            FILTER(! regex(str(?val), "SIO_000614"))
        }
    """

    resultNCIT = run_sparql_query(queryNCIT)
    resultOther = run_sparql_query(queryOther)
    return resultNCIT, resultOther

def checkAge():

    query = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT distinct ?indIDVal ?BirthDate ?ageValue ?startdate
        WHERE {
            #Find personId
            ?ID a sio:SIO_000115;
            sio:SIO_000300 ?indIDVal;
            sio:SIO_000020 ?role.
            ?role sio:SIO_000356 ?proc.
            ?proc sio:SIO_000229 ?out.
            
            #Retrieve Birth date
            ?attr a obo:NCIT_C68615.
            ?out sio:SIO_000628 ?attr.
            ?out sio:SIO_000300 ?BirthDate.

            # Context model
            ?indID a sio:SIO_000115;
                sio:SIO_000300 ?indIDVal.
            ?ind sio:SIO_000671 ?indID.
            ?timeline sio:SIO_000332 ?ind.
            
            ?elem sio:SIO_000068 ?timeline;
            sio:SIO_000687 ?age;
            sio:SIO_000680 ?start.
            ?age a obo:NCIT_C25150;
            sio:SIO_000300 ?ageValue.
            ?start sio:SIO_000300 ?startdate.
        }
        order by ?indIDVal
    """

    result = run_sparql_query(query)
    return result

def checkDiagnosisOntologies():

    # Make a query for all ontolgies in Diagnosis
    queryORDO = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (count(?val) as ?countTotal)
        WHERE {
            ?spec a obo:NCIT_C154625.
            ?spec sio:SIO_000628 ?atr.
            ?atr a ?val.
            FILTER(regex(str(?val), "ORDO"))
        }
    """

    queryOther = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT (count(?val) as ?countTotal)
        WHERE {
            ?spec a obo:NCIT_C154625.
            ?spec sio:SIO_000628 ?atr.
            ?atr a ?val.
            FILTER(! regex(str(?val), "ORDO"))
            FILTER(! regex(str(?val), "SIO_000614"))
        }
    """
    resultORDO = run_sparql_query(queryORDO)
    resultOther = run_sparql_query(queryOther)
    return resultORDO, resultOther

def avgTimeEventId():

    query = """
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX ofn: <http://www.ontotext.com/sparql/functions/>  # if daysBetween function available
        PREFIX obo: <http://purl.obolibrary.org/obo/>


        SELECT (AVG(?duration) AS ?averageGapInDays)
        WHERE {
            SELECT distinct ?timeline ?enddate1 ?startdate2 ?duration
            WHERE {
            
            ?event1 a obo:NCIT_C25499.
            ?elem1 sio:SIO_000068 ?event1;
                sio:SIO_000681 ?end1;
                sio:SIO_000068 ?timeline.
            ?end1 sio:SIO_000300 ?enddate1.
            
            ?event2 a obo:NCIT_C25499.
            ?elem2 sio:SIO_000068 ?event2;
                sio:SIO_000680 ?start2;
                sio:SIO_000068 ?timeline.
            ?start2 sio:SIO_000300 ?startdate2.

            FILTER(?event1 != ?event2)
            FILTER (?enddate1 <= ?startdate2)
            BIND (ofn:daysBetween(?startdate2, ?enddate1) as ?duration)
            # Only consecutive events: No intermediate event between date1 and date2
                FILTER NOT EXISTS {
                ?event3 a obo:NCIT_C25499.
                ?elem3 sio:SIO_000068 ?event3;
                    sio:SIO_000680 ?start3;
                    sio:SIO_000681 ?end3;
                    sio:SIO_000068 ?timeline.
                ?end3 sio:SIO_000300 ?enddate3.
                ?start3 sio:SIO_000300 ?startdate3.
                FILTER(?enddate1 < ?startdate3 && ?enddate3 < ?startdate2)
                }
            }
        }
    """
    result = run_sparql_query(query)
    return result