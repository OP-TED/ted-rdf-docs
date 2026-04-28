# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "altair==5.4.1",
#     "marimo",
#     "sparqlwrapper==2.0.0",
#     "pandas",
#     "pyarrow",
# ]
# ///

import marimo

__generated_with = "0.13.10"
app = marimo.App(width="full")


@app.cell
def _():
    import altair as alt
    import pandas as pd
    import marimo as mo
    from textwrap import dedent
    from SPARQLWrapper import SPARQLWrapper, JSON
    return JSON, SPARQLWrapper, alt, dedent, mo, pd


@app.cell
def _():
    sparql_endpoint = "https://publications.europa.eu/webapi/rdf/sparql"
    return (sparql_endpoint,)


@app.cell
def _(dedent):
    sparql_query = dedent("""\
        PREFIX epo: <http://data.europa.eu/a4g/ontology#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?year (COUNT(DISTINCT ?publicationNumber) AS ?numberOfNotices)
        WHERE {
          FILTER (?publicationDate >= "2024-01-01"^^xsd:date &&
                  ?publicationDate <= "2026-03-31"^^xsd:date)

          GRAPH ?g {
            ?notice a epo:Notice ;
                    epo:hasPublicationDate ?publicationDate ;
                    epo:hasNoticePublicationNumber ?publicationNumber .

            BIND(YEAR(?publicationDate) AS ?year)
          }
        }
        GROUP BY ?year
        ORDER BY ?year
    """)
    return (sparql_query,)


@app.cell
def _(JSON, SPARQLWrapper, pd, sparql_endpoint, sparql_query):
    sparql = SPARQLWrapper(sparql_endpoint, agent="Sparql Wrapper")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    df = pd.DataFrame(result["results"]["bindings"]).applymap(lambda x: x["value"])
    df["year"] = df["year"].astype(int)
    df["numberOfNotices"] = df["numberOfNotices"].astype(int)
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(alt, df):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("numberOfNotices:Q", title="Number of Notices"),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("numberOfNotices:Q", title="Notices", format=","),
            ],
        )
        .properties(width="container", height=400, title="Notices Published Per Year")
    )
    chart
    return


if __name__ == "__main__":
    app.run()
