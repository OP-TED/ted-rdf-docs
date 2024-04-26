# CPVs and Notices

## Introduction

In this post, we'll explore how Linked Data can be queried from different datasets related to eProcurement.

The [Publc Procurement Data Space](https://single-market-economy.ec.europa.eu/single-market/public-procurement/digital-procurement/public-procurement-data-space-ppds_en) gathers data from various actors, For example while notices of public procurement in the European Union above certain thresholds have to be published on TED (Tenders Electronic Daily), public procurement notices of lower-value are distributed across national or regional levels in diverse formats. [Linked Data](https://en.wikipedia.org/wiki/Linked_data) technology is well-suited to bridge the gap. It allows the Publications Office, any agency and Member States to independently publish data using [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework) (Resource Description Framework) and then establish links between them.

Our goal is to enhance transparency, integrity, and accountability in public spending through data discovery, querying, and analysis.

### CPV codes

CPV stands for Common Procurement Vocabulary. This classification system, developed by the European Union, specifically targets public procurement.

Primary Purpose of CPVs:

- Standardize how contracting authorities describe the subject of procurement contracts.
- Enable precise categorization of goods, services, or works involved in a contract using CPV codes.
- Facilitate efficient communication and understanding across diverse procurement processes.

### Notices

Notices play a crucial role in public procurement. They serve as formal announcements related to contracts, events, or other relevant matters.

### The data

We publish Linked Data versions of CPVs and Notices, adhering to these principles:

- Unique URIs (Uniform Resource Identifiers): Each CPV code and Notice has a distinct URI, making it easy to reference and retrieve specific information.
- HTTP URIs: Each identifier is also a URL, allowing you to directly access the data using, for example, a web browser.
- Include links to other URIs. So we can connect the data together.

Additionally, the Publications Office offers an endpoint, https://publications.europa.eu/webapi/rdf/sparql, that allows querying its contents using [SPARQL](https://en.wikipedia.org/wiki/SPARQL), a powerful language for querying RDF data. The endpoint can be queried from several applications.

This document provides some examples of how you can leverage SPARQL to unlock valuable insights from the eProcurement-related data.

## Example of integration

Let's explore how CPVs and Notices work together through queries:

### Querying CPVs

CPV codes are described using the SKOS (Simple Knowledge Organization System) vocabulary, a standard for classifying information.

Interesting SKOS Properties for CPVs:

- `skos:prefLabel`: Describes the label (name) of each concept.
- `skos:broader`: Indicates that one concept is broader (more general) than another (e.g., "Building construction work" is broader than "Construction work for schools").
- `skos:narrower`: Indicates that one concept is narrower (more specific) than another (e.g., "Construction work for schools" is narrower than "Building construction work").

These relationships help organize CPV codes into a hierarchical structure.

Let's say we have the CPV code '45216000' and want to find the label in French:

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?Identifier ?label 
WHERE {
        ?Identifier skos:notation "45216000" ;
            skos:prefLabel ?label .
        FILTER(LANG(?label) = 'fr')
}
```

[Result](https://api.triplydb.com/s/nAZDkuaun):

| Identifier                               | label                                                                                                                               |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| <http://data.europa.eu/cpv/cpv/45216000> | Travaux de construction de bâtiments destinés aux institutions d'ordre public ou aux services de secours et de bâtiments militaires |

The query retrieved two things:

1. The Identifier (URI) of the CPV code. Note that opening this UTL in a web browser can lead you to more information about the CPV code
2. The label of the CPV code in French.

We can delve deeper using another query to find the broader category of the CPV code with another query:

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?broaderLabel ?label
WHERE {
        ?Identifier skos:notation "45216000" ;
            skos:prefLabel ?label ;
            skos:broader  [ skos:prefLabel ?broaderLabel ] .
        FILTER(LANG(?label) = 'en')
        FILTER(LANG(?broaderLabel) = 'en')
}
```

[Result](https://api.triplydb.com/s/Wt5GJtAZ0):

| broaderLabel               | label                                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Building construction work | Construction work for buildings relating to law and order or emergency services and for military buildings<br> |

Now we know that the CPV concept "Construction work for buildings relating to law and order or emergency services and for military buildings" belongs to the broader category of "Building construction work."

### Querying Notices: Exploring Daily Publications

The Notices are described using the [eProcurement Ontology](https://docs.ted.europa.eu/EPO/latest/index.html), actively developed by the Publications Office.

Notices are published daily. Let's say we want to find out how many notices were published on a specific date, say "2023-09-11":

```sparql
PREFIX epo: <http://data.europa.eu/a4g/ontology#>

SELECT (COUNT(?Notice) AS ?NoticeCount) 
WHERE {
    ?Notice a epo:Notice ;
            epo:hasPublicationDate "20230911" .
}
```

[Result](https://api.triplydb.com/s/yvlfJCoq6):

| NoticeCount |
| ----------- |
| 1187        |

This query reveals that 1,187 notices were published on September 11th, 2023.

We might want to see the titles (procedure titles) associated with some of these notices. Let's limit the results to 10 titles in English:

```sparql
PREFIX epo: <http://data.europa.eu/a4g/ontology#>

SELECT ?title
WHERE {
    ?notice epo:hasPublicationDate "20230911" ;
            epo:refersToProcedure [ epo:hasTitle ?title ] .
    FILTER(LANG(?title) = 'en')
} LIMIT 10
```

[Result](https://api.triplydb.com/s/lrwVTJ_M8):

| title                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Construction All Risk (CAR) Insurance Hollandse Kust West beta                                                                                       |
| SPD1/2023/025 - FRAMEWORK CONTRACT FOR THE PROVISION OF REDUCED ENVIRONMENT IMPACT CLEANING SERVICES TO MALTA LIBRARIES                              |
| Disability Data Advocacy Consultancy                                                                                                                 |
| Catering Services to The Ascension Catholic Academy Trust for St Ignatius Catholic Primary School and Our Lady of the Rosary Catholic Primary School |
| Provision of services for fire safety, personal assistance and surveillance patrols at the site of the European Parliament in Luxembourg             |
| Framework agreement for flowers                                                                                                                      |
| Commercial brokerage services                                                                                                                        |
| Multi-Disciplinary Design team to prepare integrated Urban Realm Design for Killarney Town Centre                                                    |
| HVAC System - Upgrade Biosafety Level 3 (BSL-3) Laboratory Ecuador                                                                                   |
| Slide printers for the Department of Pathology, Olavs Hospital Trust.                                                                                |

### Mixing datasets together

The true power of Linked Data lies in its ability to combine datasets. Let's explore how we can combine information from CPVs and Notices:

Scenario: Imagine we want to understand the distribution of CPVs used in notices published on a specific date (e.g., September 11th, 2023).

The following query retrieves and groups data, revealing the distribution of CPVs for the notices published on that date:

```sparql
PREFIX epo: <http://data.europa.eu/a4g/ontology#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX euvoc: <http://publications.europa.eu/ontology/euvoc#>
PREFIX at: <http://publications.europa.eu/resource/authority/concept-status/>

SELECT   (count(?notice) as ?noticeCount) ?classificationLabel
WHERE {
    # The following segment returns notices published at a certain date, 
    # that refer to a procedure -> that have a purpose -> that is classified with a CPV 
    ?notice a epo:Notice ;
            epo:hasPublicationDate "20230911";
            epo:refersToProcedure [ 
                a epo:Procedure ;
                epo:hasPurpose [
                    a epo:Purpose ;
                    epo:hasMainClassification ?Identifier ;                    
                ] 
            ] .
    # For such CPV, return the labels in english
    ?Identifier a skos:Concept ;
			    skos:prefLabel ?classificationLabel ;
			    euvoc:status at:CURRENT .
    FILTER(LANG(?classificationLabel) = 'en')
}
GROUP BY ?classificationLabel
ORDER BY DESC(?noticeCount)
LIMIT 10
```

[Result](https://api.triplydb.com/s/BTqhK6CXz):

| noticeCount | classificationLabel                                                 |
| ----------- | ------------------------------------------------------------------- |
| 26          | Adult and other education services                                  |
| 23          | Electricity                                                         |
| 21          | Medical equipments                                                  |
| 18          | Road transport services                                             |
| 18          | Construction work                                                   |
| 16          | Pharmaceutical products                                             |
| 14          | Medical consumables                                                 |
| 14          | IT services: consulting, software development, Internet and support |
| 13          | Engineering services                                                |
| 12          | Architectural, construction, engineering and inspection services    |

Explanation of the Query:

- Filtering Notices: The query retrieves notices published on "2023-09-11."
- Connecting Notices to Procedures: Notices refer to a procedure using the epo:refersToProcedure property.
- Procedures and Purposes: It checks if the procedures have a purpose defined using the epo:hasPurpose property.
- Purpose and Main Classification: It verifies if the purpose has a "main classification" linked using the epo:hasMainClassification property. This classification is most likely a CPV code.
- CPV Label Retrieval: For the retrieved CPVs (identified by URIs in ?Identifier), the query gets the preferred labels (skos:prefLabel) in English using the FILTER clause.
- Grouping and Ordering: The results are grouped by the CPV labels (?classificationLabel), ordered by the number of notices in descending order (DESC(?noticeCount)), and limited to the top 10 entries.

## Importing your data

You can use the [SPARQL endpoint](https://publications.europa.eu/webapi/rdf/sparql) to access and analyze data without the need of downloading all the notices. SPARQL queries act like precise search tools, retrieving only the specific information you require and then be imported within any application you are familiar with, such as Excel or Python. Look into the [examples] for more information.

## Conclusion

This example demonstrates how Linked Data allows us to combine information from different datasets (CPVs and Notices) using SPARQL queries. This empowers us to gain valuable insights that wouldn't be possible with isolated datasets.

Linked Data fosters transparency, efficiency, and cross-border collaboration in public procurement!
