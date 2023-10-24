import json
import rdflib
from rdflib import Namespace, Literal, URIRef
from rdflib.namespace import RDF
from pyshacl import validate

# load JSON data
with open('units.json') as f:
    units_data = json.load(f)

with open('majors.json') as f:
    majors_data = json.load(f)

# create a graph
g = rdflib.Graph()

# define the namespace
UWA = Namespace('http://www.CITS3005.Knowledge.graph.q1.org/')
g.bind('uwa', UWA)

# process units data
for code, unit in units_data.items():
    unit_ref = URIRef(f'http://www.CITS3005.Knowledge.graph.q1.org/{code}')

    # add basic properties
    g.add((unit_ref, RDF.type, UWA.Unit))
    g.add((unit_ref, UWA.code, Literal(unit['code'])))
    g.add((unit_ref, UWA.title, Literal(unit['title'])))
    g.add((unit_ref, UWA.level, Literal(unit['level'])))
    g.add((unit_ref, UWA.description, Literal(unit['description'])))
    g.add((unit_ref, UWA.credit, Literal(unit['credit'])))

    # add outcomes
    if unit.get('outcomes'):
        for outcome in unit['outcomes']:
            g.add((unit_ref, UWA.outcome, Literal(outcome)))

    # add assessment
    if unit.get('assessment'):
        for assessment in unit['assessment']:
            g.add((unit_ref, UWA.assessment, Literal(assessment)))

    # add prerequisites
    if unit.get('prerequisites_cnf'):
        for prereq_group in unit.get('prerequisites_cnf', []):
            for prereq in prereq_group:
                g.add((unit_ref, UWA.prerequisite, Literal(prereq)))

    # add contact hours
    total_hours = sum([int(hours) for hours in unit['contact'].values()]) if unit.get('contact') else 0
    g.add((unit_ref, UWA.contact_hours, Literal(total_hours)))

# add majors
for code, major in majors_data.items():
    major_ref = URIRef(f'http://www.CITS3005.Knowledge.graph.q1.org/{code}')

    # add basic properties
    g.add((major_ref, RDF.type, UWA.Major))
    g.add((major_ref, UWA.code, Literal(major['code'])))
    g.add((major_ref, UWA.title, Literal(major['title'])))
    g.add((major_ref, UWA.description, Literal(major['description'])))

    # add units
    for unit_code in major['units']:
        unit_ref = URIRef(f'http://www.CITS3005.Knowledge.graph.q1.org/{unit_code}')
        g.add((major_ref, UWA.core_unit, unit_ref))

# # Use if in need
# # Update data function
# old_title = 'Data Science'
# new_title = 'Data Science and Artificial Intelligence'
# old_triple = (unit_ref, UWA.title, Literal(old_title))
# if old_triple in g:
#     g.remove(old_triple)
# g.add((unit_ref, UWA.title, Literal(new_title)))# also an example of adding data
#
# # Delete data function
# remove_unit = 'CITS1401'
# rm_unit_ref = URIRef(f'http://www.CITS3005.Knowledge.graph.q1.org/{remove_unit}')
# for triple in g.triples((rm_unit_ref, None, None)):
#     g.remove(triple)


# save the graph
with open('knowledge_graph.ttl', 'w') as f:
    f.write(g.serialize(format='turtle'))

# Implement SHACL constraints
shacl_graph = '''
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix uwa: <http://www.CITS3005.Knowledge.graph.q1.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Constraint 1: The level of each prerequisite should be less than the level of the unit it belongs to
uwa:PrerequisiteLevelShape
    a sh:NodeShape ;
    sh:targetClass uwa:Unit ;
    sh:property [
        sh:path uwa:prerequisite ;
        sh:property [
            sh:path uwa:level ;
            sh:lessThan uwa:level ;
        ] ;
    ] .


# Constraint 2: A unit cannot be its own prerequisite
uwa:SelfPrerequisiteShape
    a sh:NodeShape ;
    sh:targetClass uwa:Unit ;
    sh:property [
        sh:path uwa:prerequisite ;
        sh:class uwa:Unit ;
        sh:nodeKind sh:IRI ;
        sh:not [
            sh:hasValue $this ;
        ] ;
    ] .


# Constraint 3: The total contact time of core units in a major should not exceed the average contact time of all units

uwa:MajorShape
    a sh:NodeShape ;
    sh:targetClass uwa:Major ;
    sh:property [
        sh:path uwa:unit ;
        sh:sparql [
            sh:select """
                SELECT $this (AVG(?avgContactTime) as ?averageContactTime)
                WHERE {
                    $this uwa:unit ?unit .
                    ?unit uwa:contact_hours ?contact_hours ;
                          uwa:credit ?credit .
                    
                    # Calculate the adjusted contact time per unit
                    BIND ((?contact_hours * ?credit / 6) as ?adjustedContactTime)
                    
                    # Calculate the average contact time per unit
                    BIND (?adjustedContactTime / COUNT(?unit) as ?avgContactTime)
                }
                GROUP BY $this
                HAVING (AVG(?avgContactTime) > 10)
            """ ;
        ] ;
    ] .
'''

# Use the pySHACL library to validate the RDF graph
r = validate(g, shacl_text=shacl_graph, shacl_graph_format='turtle')
conforms, results_graph, results_text = r
# print results
print(f'SHACL validation conforms: {conforms}')
if not conforms:
    print(results_text)
