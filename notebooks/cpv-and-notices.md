# CPVs and Notices

## Introduction

In this post, we'll explore how Linked Data can be queried from different datasets related to eProcurement.

The [The Public Procurement Data Space](https://single-market-economy.ec.europa.eu/single-market/public-procurement/digital-procurement/public-procurement-data-space-ppds_en) gathers data from various actors, For example while notices of public procurement in the European Union above certain thresholds have to be published on TED (Tenders Electronic Daily), public procurement notices of lower-value are distributed across national or regional levels in diverse formats. [Linked Data](https://en.wikipedia.org/wiki/Linked_data) technology is well-suited to bridge the gap. It allows the Publications Office, any agency and Member States to independently publish data using [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework) (Resource Description Framework) and then establish links between them.

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

This document provides some examples of how you can leverage SPARQL to unlock valuable insights from the eProcurement dataspace.

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

- [Run the query online](https://publications.europa.eu/webapi/rdf/sparql?default-graph-uri=&query=PREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0A%0D%0ASELECT+%3FIdentifier+%3Flabel+%0D%0AWHERE+%7B%0D%0A++++++++%3FIdentifier+skos%3Anotation+%2245216000%22+%3B%0D%0A++++++++++++skos%3AprefLabel+%3Flabel+.%0D%0A++++++++FILTER%28LANG%28%3Flabel%29+%3D+%27fr%27%29%0D%0A%7D&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+):

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

- [Run the query online](https://publications.europa.eu/webapi/rdf/sparql?default-graph-uri=&query=PREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0A%0D%0ASELECT+%3FbroaderLabel+%3Flabel%0D%0AWHERE+%7B%0D%0A++++++++%3FIdentifier+skos%3Anotation+%2245216000%22+%3B%0D%0A++++++++++++skos%3AprefLabel+%3Flabel+%3B%0D%0A++++++++++++skos%3Abroader++%5B+skos%3AprefLabel+%3FbroaderLabel+%5D+.%0D%0A++++++++FILTER%28LANG%28%3Flabel%29+%3D+%27en%27%29%0D%0A++++++++FILTER%28LANG%28%3FbroaderLabel%29+%3D+%27en%27%29%0D%0A%7D&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)

| broaderLabel               | label                                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Building construction work | Construction work for buildings relating to law and order or emergency services and for military buildings<br> |

Now we know that the CPV concept "Construction work for buildings relating to law and order or emergency services and for military buildings" belongs to the broader category of "Building construction work."

### Querying Notices: Exploring Daily Publications

The Notices are described using the [eProcurement Ontology](https://docs.ted.europa.eu/EPO/latest/index.html), actively developed by the Publications Office.

Notices are published daily. Let's say we want to find out how many notices were published on a specific date, say "2024-11-04":

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX epo: <http://data.europa.eu/a4g/ontology#>

SELECT (COUNT(?Notice) AS ?NoticeCount) 
WHERE {
    ?Notice a epo:Notice ;
            epo:hasPublicationDate "2024-11-04"^^xsd:date .
}
```

- [Run the query online](https://publications.europa.eu/webapi/rdf/sparql?default-graph-uri=&query=PREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+epo%3A+%3Chttp%3A%2F%2Fdata.europa.eu%2Fa4g%2Fontology%23%3E%0D%0A%0D%0ASELECT+%28COUNT%28%3FNotice%29+AS+%3FNoticeCount%29+%0D%0AWHERE+%7B%0D%0A++++%3FNotice+a+epo%3ANotice+%3B%0D%0A++++++++++++epo%3AhasPublicationDate+%222024-11-04%22%5E%5Exsd%3Adate+.%0D%0A%7D&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+):

| NoticeCount |
| ----------- |
| 2063        |

This query reveals that 2063 notices were published on November 4th, 2024.

We might want to see the titles (procedure titles) associated with some of these notices. Let's limit the results to 10 titles in English:

```sparql
PREFIX epo: <http://data.europa.eu/a4g/ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?title
WHERE {
    ?notice epo:hasPublicationDate "2024-11-04"^^xsd:date ;
            epo:refersToProcedure ?procedureURI .
	?procedureURI dcterms:title ?title .
  	FILTER(LANG(?title) = 'en')
}  LIMIT 10
```

- [Run the query online](https://publications.europa.eu/webapi/rdf/sparql?default-graph-uri=&query=PREFIX+epo%3A+%3Chttp%3A%2F%2Fdata.europa.eu%2Fa4g%2Fontology%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+dcterms%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0D%0A%0D%0ASELECT+%3Ftitle%0D%0AWHERE+%7B%0D%0A++++%3Fnotice+epo%3AhasPublicationDate+%222024-11-04%22%5E%5Exsd%3Adate+%3B%0D%0A++++++++++++epo%3ArefersToProcedure+%3FprocedureURI+.%0D%0A%09%3FprocedureURI+dcterms%3Atitle+%3Ftitle+.%0D%0A++%09FILTER%28LANG%28%3Ftitle%29+%3D+%27en%27%29%0D%0A%7D++LIMIT+10&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)

| **Title**                                                                                                                                           |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| "Request for Tenders for IT support and maintenance services 2025/2026"@en                                                                          |
| "UCDOPP5443 General Building Fabric Maintenance and Operation Services to University College Dublin"@en                                             |
| "SPD8/2024/087 - Framework Contract For The Management Of Gypsum-Based Construction Materials For Recycling From Sites Managed And Operated By WSM Ltd"@en |
| "2024/1394 Parallel framework agreements for external sun screening in Oslo."@en                                                                    |
| "Helium recovery system"@en                                                                                                                         |
| "Donegal County Council, Co designed Local Community Peace Action Plan, Cultural Connections Peace Programme, Glenties Municipal District"@en       |
| "Competition for playground equipment"@en                                                                                                           |
| "Service contract for winter maintenance"@en                                                                                                        |
| "Service CFT for the provision of a proof of concept SMART on FHIR Risk Assessment Application RH"@en                                               |
| "Framework agreement, Lifting and transport of rotary converters, transformers and other materials."@en                                             |

### Mixing datasets together

The true power of Linked Data lies in its ability to combine datasets. Let's explore how we can combine information from CPVs and Notices:

Scenario: Imagine we want to understand the distribution of CPVs used in notices published on a specific date (e.g., September 11th, 2023).

The following query retrieves and groups data, revealing the distribution of CPVs for the notices published on that date:

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX epo: <http://data.europa.eu/a4g/ontology#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX euvoc: <http://publications.europa.eu/ontology/euvoc#>
PREFIX at: <http://publications.europa.eu/resource/authority/concept-status/>

SELECT   (count(?notice) as ?noticeCount) ?classificationLabel
WHERE {
    # The following segment returns notices published at a certain date, 
    # that refer to a procedure -> that have a purpose -> that is classified with a CPV 
    ?notice a epo:Notice ;
            epo:hasPublicationDate "2024-11-04"^^xsd:date;
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

- [Run the query online](https://publications.europa.eu/webapi/rdf/sparql?default-graph-uri=&query=PREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+epo%3A+%3Chttp%3A%2F%2Fdata.europa.eu%2Fa4g%2Fontology%23%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0APREFIX+euvoc%3A+%3Chttp%3A%2F%2Fpublications.europa.eu%2Fontology%2Feuvoc%23%3E%0D%0APREFIX+at%3A+%3Chttp%3A%2F%2Fpublications.europa.eu%2Fresource%2Fauthority%2Fconcept-status%2F%3E%0D%0A%0D%0ASELECT+++%28count%28%3Fnotice%29+as+%3FnoticeCount%29+%3FclassificationLabel%0D%0AWHERE+%7B%0D%0A++++%23+The+following+segment+returns+notices+published+at+a+certain+date%2C+%0D%0A++++%23+that+refer+to+a+procedure+-%3E+that+have+a+purpose+-%3E+that+is+classified+with+a+CPV+%0D%0A++++%3Fnotice+a+epo%3ANotice+%3B%0D%0A++++++++++++epo%3AhasPublicationDate+%222024-11-04%22%5E%5Exsd%3Adate%3B%0D%0A++++++++++++epo%3ArefersToProcedure+%5B+%0D%0A++++++++++++++++a+epo%3AProcedure+%3B%0D%0A++++++++++++++++epo%3AhasPurpose+%5B%0D%0A++++++++++++++++++++a+epo%3APurpose+%3B%0D%0A++++++++++++++++++++epo%3AhasMainClassification+%3FIdentifier+%3B++++++++++++++++++++%0D%0A++++++++++++++++%5D+%0D%0A++++++++++++%5D+.%0D%0A++++%23+For+such+CPV%2C+return+the+labels+in+english%0D%0A++++%3FIdentifier+a+skos%3AConcept+%3B%0D%0A%09%09%09++++skos%3AprefLabel+%3FclassificationLabel+%3B%0D%0A%09%09%09++++euvoc%3Astatus+at%3ACURRENT+.%0D%0A++++FILTER%28LANG%28%3FclassificationLabel%29+%3D+%27en%27%29%0D%0A%7D%0D%0AGROUP+BY+%3FclassificationLabel%0D%0AORDER+BY+DESC%28%3FnoticeCount%29%0D%0ALIMIT+10&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)


| **noticeCount** | **classificationLabel**                                                                             |
|------------------|----------------------------------------------------------------------------------------------------|
| 730              | "Various office equipment and supplies"@en                                                        |
| 730              | "Sport-related services"@en                                                                       |
| 71               | "Construction work"@en                                                                            |
| 71               | "Planting and maintenance services of green areas"@en                                             |
| 68               | "Miscellaneous repair and maintenance services"@en                                                |
| 68               | "Non-scheduled passenger transport"@en                                                            |
| 66               | "Miscellaneous medical devices and products"@en                                                   |
| 66               | "Detection and analysis apparatus"@en                                                             |
| 65               | "Repair and maintenance services of motor vehicles and associated equipment"@en                   |
| 50               | "IT services: consulting, software development, Internet and support"@en                          |

Explanation of the Query:

- Filtering Notices: The query retrieves notices published on "2024-11-04."
- Connecting Notices to Procedures: Notices refer to a procedure using the epo:refersToProcedure property.
- Procedures and Purposes: It checks if the procedures have a purpose defined using the epo:hasPurpose property.
- Purpose and Main Classification: It verifies if the purpose has a "main classification" linked using the epo:hasMainClassification property. This classification is most likely a CPV code.
- CPV Label Retrieval: For the retrieved CPVs (identified by URIs in ?Identifier), the query gets the preferred labels (skos:prefLabel) in English using the FILTER clause.
- Grouping and Ordering: The results are grouped by the CPV labels (?classificationLabel), ordered by the number of notices in descending order (DESC(?noticeCount)), and limited to the top 10 entries.

## Importing your data

You can use the [SPARQL endpoint](https://data.ted.europa.eu/) to access and analyze data without the need of downloading all the notices. SPARQL queries act like precise search tools, retrieving only the specific information you require and then be imported within any application you are familiar with, such as Excel or Python. 

## Conclusion

This example demonstrates how Linked Data allows us to combine information from different datasets (CPVs and Notices) using SPARQL queries. This empowers us to gain valuable insights that wouldn't be possible with isolated datasets.

Linked Data fosters transparency, efficiency, and cross-border collaboration in public procurement!
