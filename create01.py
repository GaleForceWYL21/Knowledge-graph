from owlready2 import *
import json
import re


# definition of a function to clean text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = text.replace('"', "'")
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()


# create a new ontology
onto = get_ontology("http://www.CITS3005.Knowledge.graph.q3.org/onto.owl")

# define classes and properties
with onto:
    class Major(Thing):
        pass


    class Unit(Thing):
        pass


    class Outcome(Thing):
        pass


    class Assessment(Thing):
        pass


    class Contact(Thing):
        pass


    # 数据属性
    class title(DataProperty):
        domain = [Major, Unit]
        range = [str]


    class description(DataProperty):
        domain = [Major, Unit]
        range = [str]


    class level(DataProperty):
        domain = [Unit]
        range = [int]


    class credit(DataProperty):
        domain = [Unit]
        range = [int]


    class text(DataProperty):
        domain = [Outcome, Assessment]
        range = [str]


    # object properties
    class prerequisite_require(ObjectProperty):
        domain = [Unit]
        range = [Unit]


    class has_outcome(ObjectProperty):
        domain = [Unit, Major]
        range = [Outcome]


    class has_assessment(ObjectProperty):
        domain = [Unit]
        range = [Assessment]


    class has_conatct(ObjectProperty):
        domain = [Unit]
        range = [Contact]


    class is_core_unit_of(ObjectProperty):
        domain = [Unit]
        range = [Major]

# load JSON data
with open('units.json') as f:
    units_data = json.load(f)

with open('majors.json') as f:
    majors_data = json.load(f)

# add units with onto:
with onto:
    for code, data in units_data.items():
        unit = Unit(namespace=onto, name=code)
        unit.title.append(clean_text(data['title']))
        unit.level.append(int(data['level']))
        unit.description.append(clean_text(data['description']))
        unit.credit.append(int(data['credit']))

        # add outcomes
        if data.get('outcomes'):
            outcome_text = str(data['outcomes'])
            clean_text(outcome_text)
            outcome = Outcome(namespace=onto, name=f"{code}_outcome")
            outcome.text.append(outcome_text.strip().replace('[', '').replace(']', ''))
            unit.has_outcome.append(outcome)

        # add assessments
        for assessment_text in data['assessment']:
            clean_text(assessment_text)
            assessment = Assessment(namespace=onto, name=f"{code}_assessment")
            assessment.text.append(assessment_text.strip())
            unit.has_assessment.append(assessment)

        # add contacts
        if data.get('contacts'):
            for contact_text in data['contacts']:
                clean_text(contact_text)
                contact = Contact(namespace=onto, name=f"{code}_contact")
                contact.text.append(contact_text.strip())
                unit.has_conatct.append(contact)

        # add prerequisites
        prereq_groups = data.get('prerequisites_cnf')
        if prereq_groups:
            for prereq_group in prereq_groups:
                for prereq_code in prereq_group:
                    prereq_unit = Unit(namespace=onto, name=prereq_code)
                    unit.prerequisite_require.append(prereq_unit)

# add majors
with onto:
    for code, data in majors_data.items():
        major = Major(namespace=onto, name=code)
        major.title.append(clean_text(data['title']))
        major.description.append(clean_text(data['description']))

        # add outcomes
        if data.get('outcomes'):
            outcome_text = str(data['outcomes'])
            clean_text(outcome_text)
            outcome = Outcome(namespace=onto, name=f"{code}_outcome")
            outcome.text.append(outcome_text.strip().replace('[', '').replace(']', ''))
            major.has_outcome.append(outcome)

        # add core units
        for unit_code in data['units']:
            core_unit = Unit(namespace=onto, name=unit_code)
            core_unit.is_core_unit_of.append(major)

# # Use in need
# # update the data
# with onto:
#     unit = onto.Unit["example_unit_code"]  # get the Unit instance
#     unit.title[0] = "New Title"  # update the title
# # delete the data
# with onto:
#     unit = onto.Unit["example_unit_code"]
#     destroy_entity(unit)  # detele the unit instance

# save the ontology
onto.save(file="onto.owl", format="ntriples")
