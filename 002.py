import rdflib
from rdflib import Namespace

# define the namespace
UWA = Namespace('http://www.CITS3005.Knowledge.graph.q1.org/')

# read the knowledge graph
g = rdflib.Graph()
g.parse('knowledge_graph.ttl', format='turtle')

# SPARQL query1: Find all units with more than 6 outcomes
query1 = '''
SELECT ?unit WHERE {
    ?unit a uwa:Unit ;
          uwa:outcome ?outcome .
} GROUP BY ?unit HAVING (COUNT(?outcome) > 6)
'''

# SPARQL query2: Find all level 3 units that have no exam and none of their prerequisites have an exam
query2 = '''
SELECT ?unit WHERE {
    ?unit a uwa:Unit ;
          uwa:level "3" .

    FILTER NOT EXISTS { 
        ?unit uwa:assessment ?assessment .
        FILTER REGEX(?assessment, "exam", "i")
    }

    FILTER NOT EXISTS {
        ?unit uwa:prerequisite ?prerequisiteCode.
        ?prerequisite a uwa:Unit ;
                      uwa:code ?prerequisiteCode ;
                      uwa:assessment ?prerequisiteAssessment .
        FILTER REGEX(?prerequisiteAssessment, "exam", "i")
    }
}
'''

# SPARQL query3: Find all units that appear in more than 3 majors
query3 = '''
SELECT ?unit WHERE {
    ?major uwa:core_unit ?unit .
} GROUP BY ?unit HAVING (COUNT(?major) > 3)
'''

# Execute the queries and print the results
for query, description in zip([query1, query2, query3],
                              ["Units with more than 6 outcomes:",
                               "Level 3 units without an exam and none of their prerequisites have an exam:",
                               "Units that appear in more than 3 majors:"]):
    num = 0
    print(description)
    for row in g.query(query, initNs={'uwa': UWA}):
        num += 1
        print(f" No.{num}- {row[0]}")

# Basic search: find units that contain the query string in the description
query_string = "environmental policy"
basic_search_query = f'''
SELECT DISTINCT ?unit WHERE {{
    ?unit a uwa:Unit ;
          uwa:description ?description ;
          uwa:outcome ?outcome .
    FILTER (regex(?description, "{query_string}", "i") || regex(?outcome, "{query_string}", "i"))
}}
'''

print(f'\nUnits containing the string "{query_string}" in the description or outcomes:')
for row in g.query(basic_search_query, initNs={'uwa': UWA}):
    print(f" - {row[0]}")
