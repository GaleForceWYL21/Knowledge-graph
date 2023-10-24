from owlready2 import *
import rdflib

# load OWL file
onto = get_ontology("file://onto.owl").load()

g = default_world.as_rdflib_graph()


# Function for executing queries
def execute_query(g, query):
    print("\nExecuting query:")
    print(query)
    results = g.query(query)
    if results:
        for row in results:
            print(row)
    else:
        print("No results found.")


input_unit = "CITS3200"
# SPARQL query1: A prerequisite of a prerequisite is a prerequisite
# Assume using CITS3200 as input unit,
# check if result show the prerequisite of prerequisite is a prerequisite of CITS3200
query1 = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX onto: <http://www.CITS3005.Knowledge.graph.q3.org/onto.owl#>

SELECT ?initialPrerequisite (GROUP_CONCAT(DISTINCT ?prerequisite; separator=", ") AS ?prerequisites)
WHERE {{
  onto:{input_unit} onto:prerequisite_require ?initialPrerequisite.
  OPTIONAL {{
    ?initialPrerequisite onto:prerequisite_require* ?prerequisite.
  }}
}}
GROUP BY ?initialPrerequisite
"""

# Execute the SPARQL query
results = list(g.query(query1))
print(f"\n\nFor unit {input_unit}, A prerequisite of a prerequisite is a prerequisite:\n")
# print results
if not results or all(not row[1] for row in results):
    print(f"{input_unit} has no prerequisites.")
else:
    prerequisites_set = set()
    for row in results:
        if row[1]:
            prerequisites_set.add(row[1])  # Add the prerequisite to the set, which will automatically remove duplicates

    if prerequisites_set:
        print(f"Prerequisites for {input_unit}:")
        for prerequisite in prerequisites_set:
            # Split the prerequisite string at each comma and iterate through the resulting list
            for item in prerequisite.split(','):
                print(item.strip())
    else:
        print(f"No additional prerequisites for {input_unit}")

# SPARQL query2 :An outcome of a core unit is an outcome of a major
# Assume using: An outcome of core units (CITS2005,CITS1401....) are an outcome of a major MJD-CMPSC.
input_major = "MJD-CMPSC"
query2 = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX onto: <http://www.CITS3005.Knowledge.graph.q3.org/onto.owl#>

SELECT ?unit ?outcomeText
WHERE {{
  {{
    ?unit onto:is_core_unit_of onto:{input_major}.
    ?unit onto:has_outcome ?outcome.
    ?outcome onto:text ?outcomeText.
  }}
  UNION
  {{
    onto:{input_major} onto:has_outcome ?majorOutcome.
    ?majorOutcome onto:text ?outcomeText.
    BIND(onto:{input_major} AS ?unit)
  }}
}}
"""

# Execute the SPARQL query
results = g.query(query2)
print(f"\n\nFor major {input_major}, an outcome of a core unit is an outcome of a major:\n")
if not results:
    print("No result found")
# print results
num = 0
for row in results:
    unit = str(row[0]).split('#')[1] if row[0] else None

    outcome_text = str(row[1]) if len(row) > 1 else None

    if unit and outcome_text:
        num += 1
        print(f"No.{num}, Code: {unit}, Outcome: {outcome_text}")

# SPARQL query3: A required text of a core unit is a required text for a major
# Assume using: Required text of core units (CITS2005,CITS1401....) is a required text for a major MJD-CMPSC.
input_major_q3 = "MJD-CMPSC"
query3 = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX onto: <http://www.CITS3005.Knowledge.graph.q3.org/onto.owl#>

SELECT ?unit ?description
WHERE {{
  {{
    ?unit onto:is_core_unit_of onto:{input_major_q3}.
    ?unit onto:description ?description. 
  }}
  UNION
  {{ 
    onto:{input_major_q3} onto:description ?description. 
    BIND(onto:{input_major_q3} AS ?unit)
  }}
}}
"""
# Execute the SPARQL query
results = g.query(query3)
print(f"\n\nFor major {input_major_q3}, A required text of a core unit is a required text for a major:\n")
if not results:
    print("No result found")
# print results
num = 0
for row in results:
    unit = str(row[0]).split('#')[1] if row[0] else None

    outcome_text = str(row[1]) if len(row) > 1 else None

    if unit and outcome_text:
        num += 1
        print(f"No.{num}, Code: {unit}\nDescription: {outcome_text}\n")
