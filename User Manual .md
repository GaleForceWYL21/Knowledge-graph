## File explanation

`create12.py`:Create knowledge graph and constraints for Question1 & 2

`002.py`:Queries for Question 1

`create01.py`:Create  ontology schema fro question 3

`001.py`:Queries for Question 3



## For question 1 & 2

#### **1.Schema**:

The schema of the knowledge graph defines how data is organized and represented. In my code `create12.py` provided, two main classes - `Unit` and `Major`, along with their associated properties, are defined.

**Unit**:

- `code`: Represents the unit code of the unit.
- `title`: Represents the name of the unit.
- `level`: Represents the level of the unit.
- `description`: Provides a description of the unit.
- `credit`: Represents the credit of the unit.
- `outcomes`: The expected outcomes text of the unit.
- `assessment`:  The assessment methods of the unit.
- `prerequisites`: The prerequisites of the unit.
- `contact_hours`: The total number of the contact hours of the unit.

**Major**:

- `code`: Represents the code of the major.
- `title`: Represents the title of the major.
- `description`: Provides a description of the major.
- `core_units`: Lists the core units within the major.

These classes and properties are organized and associated within the knowledge graph through an RDF graph.

`knowledge_graph.ttl` should be the generated knowledge graph file.



**Notice**:The `bridging` unit is not included in the core unit. Because I personally think that bridging unit is a broad basic university course and should not be a core unit for a specific major.



**visualization picture of the schema**

![截屏2023-10-21 上午6.26.15](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午6.26.15.png)

![截屏2023-10-21 上午6.32.11](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午6.32.11.png)

#### **2.Constraints**:

SHACL (Shapes Constraint Language) is used to define and validate constraints within the knowledge graph. In the project clarification, the following constraints are defined:

- **Prerequisite Level Constraint**: Every prerequisite for a level X unit should have a level less than X
- **Self Prerequisite Constraint**: No unit should be its own prerequisite
- **Major Core Unit Contact Time Constraint**: No major should require more than 40 contact hours per week

These constraints ensure the consistency and correctness of the data, and help in identifying and correcting errors. The implement code are shown from line 90 to 147 in `create12.py`（as it's too long to show in here）



**Notice**: They way I defind `No major should require more than 40 contact hours per week` is to calculate  the average of total contact hours  of the major:
$$
total~contact~hours = sum(contact~hours*credit/6)
$$

$$
average = total~contact~hours/(total~number~of~core~unit)
$$

Assume each student are enroll in 4 unit, which means the require contact hours should be `required_contact_hours = 40/10 = 10`

if `average <= 10` means this major satisfied the constraints.



### 3. **Example Queries**

All the queries implementation are  in `002.py`, run this file to see the result.

**Find all units with more than 6 outcomes:**

![截屏2023-10-21 上午7.05.20](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午7.05.20.png)

![截屏2023-10-21 上午7.05.42](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午7.05.42.png)



**Find all level 3 units that do not have an exam, and where none of their prerequisites have an exam:**

![截屏2023-10-22 下午4.24.40](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-22 下午4.24.40.png)

![截屏2023-10-22 下午4.23.52](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-22 下午4.23.52.png)



**Find all units that appear in more than 3 majors:**

![截屏2023-10-21 上午7.08.14](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午7.08.14.png)

![截屏2023-10-21 上午7.08.31](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午7.08.31.png)





**Basic search functionality: Given a query string (eg "environmental policy"), find the units that contain this string in the description or outcomes:**

change `query_string` to search other string.

![截屏2023-10-21 上午7.10.36](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午7.10.36.png)

![截屏2023-10-21 上午7.10.51](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午7.10.51.png)



### 4.Instructions

All code are shown in `create12.py`

**Add, update or remove data:**

 `old_title`,  `new_title`, `remove_unit` are examples on how to add, update or remove data.

![截屏2023-10-21 上午7.18.37](/Users/legendfrozen/Desktop/截屏2023-10-21 上午7.18.37.png)

Or you can change the data value in the JSON file to implement it.



**Add, update or remove constrain rules:**

Modify value in `shach_graph` to Add, update or remove constrain rules.

（Only a portion of the code is shown here）

![截屏2023-10-21 上午7.22.11](/Users/legendfrozen/Desktop/截屏2023-10-21 上午7.22.11.png)



**Validation:**

![截屏2023-10-21 上午7.25.56](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午7.25.56.png)

Validate result will show in the terminal.





# For question 3

### **1.Schema**:

The ontology schema for question 3 is in `create01.py`.

The ontology schema consists of the following classes and properties:

**Classes**:

- `Major`: Represents major fields of study.
- `Unit`: Represents individual units.
- `Outcome`: Represents expected outcomes from units or majors.
- `Assessment`: Represents assessments within units.

**Properties**:

- **Data Properties**:
  - `title`: The title of a Major or Unit.
  - `description`: The description of a Major or Unit.
  - `level`: The level of a Unit.
  - `credit`: The credit value of a Unit.
  - `text`: The text description of an Outcome or Assessment.
- **Object Properties**:
  - `prerequisite_require`: The prerequisite units required for a Unit.
  - `has_outcome`: The outcomes associated with a Unit or Major.
  - `has_assessment`: The assessments associated with a Unit.
  - `has_contact`: The contacts associated with a Unit (not utilized in the provided code).
  - `is_core_unit_of`: The core units associated with a Major.

`onto.owl` should be the generated knowledge graph. 

**Notice**:The `bridging` unit is not included in the core unit. 





**visualization picture of the schema**

**For units:**

![截屏2023-10-21 上午8.04.04](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.04.04.png)

![截屏2023-10-21 上午8.04.44](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.04.44.png)

![截屏2023-10-21 上午8.05.01](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.05.01.png)



**For majors:**

![截屏2023-10-21 上午8.06.01](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.06.01.png)

![截屏2023-10-21 上午8.08.00](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.08.00.png)





### 2.Example Queries

All queries are in file `001.py`, run this file and see the result in terminal.

**A prerequisite of a prerequisite is a prerequisite.**

change `input_unit` to see other units value.

![截屏2023-10-21 上午8.13.05](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.13.05.png)

![截屏2023-10-21 上午8.13.38](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.13.38.png)





**An outcome of a core unit is an outcome of a major**

change  `input_major` to other value could see outcomes of other majors.

![截屏2023-10-21 上午8.19.08](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.19.08.png)

![截屏2023-10-21 上午8.19.37](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.19.37.png)





**A required text of a core unit is a required text for a major**



Assume ***required text*** is the description of each unit and major.

Change `input_major_q3` to see other require text of major

![截屏2023-10-21 上午8.27.10](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.27.10.png)

![截屏2023-10-21 上午8.28.13](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.28.13.png)





### 3.Instructions



**Add data**: By using the code in blue, you can add the new data into the instance.

![截屏2023-10-21 上午8.49.22](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.49.22.png)





**Update and delete** : Here's the examples on how to update and delete.

![截屏2023-10-21 上午8.50.58](/Users/legendfrozen/Library/Application Support/typora-user-images/截屏2023-10-21 上午8.50.58.png)