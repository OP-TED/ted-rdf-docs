# Contributing to the Query Library

The queries in this directory are displayed in the **Query Library** tab of the [TED Open Data Service](https://data.ted.europa.eu/). The live application reads queries from the `main` branch. Changes should be made on feature branches and submitted as pull requests to `develop`. They will be published with the next release when `develop` is merged to `main`.

## How queries are loaded

The TED Open Data Service loads queries from this directory at runtime:

1. It reads `index.yaml` to get the list of queries with their categories, titles, and descriptions
2. When a user selects a query, it fetches the corresponding `.sparql` file
3. The query is displayed in a read-only editor with syntax highlighting
4. The user can click "Try this query" to copy it into the main editor and run it

## Adding a new query

1. Create a `.sparql` file in this directory with your query
2. Add an entry to `index.yaml` with the category, title, description, and filename:

```yaml
- category: Notices
  title: Your query title
  description: A clear description of what the query does and what results it returns.
  sparql: your-query-filename.sparql
```

3. Create a branch from `develop` and open a pull request targeting `develop`
4. Your query will be published with the next release (when `develop` is merged to `main`)

## Writing guidelines

### Comments

Every query should include comments that explain:
- What the query does (brief summary at the top)
- What each major section of the WHERE clause is doing
- Any non-obvious joins or filters

```sparql
# Retrieves the amount awarded per tender for notices published on a specific date.
# Returns: publication number, tender identifier, awarded amount, and currency.

PREFIX epo: <http://data.europa.eu/a4g/ontology#>
...

WHERE {
  # Filter by publication date
  FILTER (?publicationDate = "2024-11-04"^^xsd:date)

  GRAPH ?g {
    # Get the notice and its publication details
    ?notice a epo:Notice ;
            epo:hasPublicationDate ?publicationDate ;
            epo:hasNoticePublicationNumber ?publicationNumber .

    # Link notice to procedure explicitly for performance
    ?notice epo:refersToProcedure ?procedure .

    # Get the tender and its awarded amount
    ?tender epo:isSubmittedForLot ?lot ;
            epo:hasFinancialOfferValue ?offerValue .
    ...
  }
}
```

### Explicit joins

Always include explicit links between entities, even when the named graph boundary makes the query work without them. For example, always link notices to procedures:

```sparql
# Good: explicit join
?notice epo:refersToProcedure ?procedure .
?procedure a epo:Procedure .

# Avoid: relying on named graph boundary alone
?procedure a epo:Procedure .
```

Explicit joins improve query performance and make the query logic clear to readers.

### Prefixes

Use the standard prefixes consistently:

```sparql
PREFIX epo: <http://data.europa.eu/a4g/ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX adms: <http://www.w3.org/ns/adms#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
```

Only include prefixes that are actually used in the query.

### Parameterisation

Use date filters like `FILTER (?publicationDate = "2024-11-04"^^xsd:date)` with a recent date so users can see results immediately. Users will change the date to suit their needs.

For queries that filter by a specific identifier (e.g. publication number or procedure ID), use `VALUES` with a real example value and add a comment explaining what to change:

```sparql
# Change the publication number below to look up a different notice
VALUES ?publicationNumber { "00676595-2024" }
```

## Fixing an existing query

If you find a bug or want to improve an existing query:

1. Edit the `.sparql` file
2. If the title or description need updating, edit `index.yaml` too
3. Test the query on the [TED Open Data Service](https://data.ted.europa.eu/) before submitting
4. Create a branch from `develop` and open a pull request targeting `develop` with a description of what you changed and why
5. Your fix will be published with the next release

## Categories

Queries are organised into categories in `index.yaml`. The current categories are:

- **Notices** — queries about procurement notices and their metadata
- **Tenders** — queries about tender submissions and awarded amounts
- **Procedures** — queries about procurement procedures and their details
- **Organisations** — queries about buyers, winners, and other organisations
- **Advanced queries** — queries for power users (RDF retrieval, named graphs, etc.)

New categories can be added by simply using a new category name in `index.yaml`.
