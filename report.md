### 1.Design

**For Question 3**, considering the implementation of complex queries, continuing to use the simple knowledge graph from Question 1 will not effectively handle complex queries. Therefore, I decided to create a more refined ontology model, by abstracting common properties (such as `outcomes`, `description`) from `Unit` and `Major`, and linking them through relationships (such as `has_outcome`, `has_assessment`), providing a clear representation for the associations between data. This design aids in solving complex queries, like `"A prerequisite of a prerequisite is a prerequisite"` type nested queries, while also making the structure of the knowledge graph clearer and more reasonable.



**For Question 1**, after analyzing the query information, I opted to embed all the data directly into the knowledge graph without much abstraction and connection. This design is simple and direct, making it easier to implement.



**For the definition of core units**, I excluded `bridging` units, for two reasons. Firstly, I believe bridging units belong to a general course, which appears in dozens of majors, thus they shouldn't be considered as a core unit of any particular major. Secondly, bridging units and core units are constituted by two key-value pairs in the JSON file. Storing two key-value pairs in one variable would make the code more complex and prone to errors, so I chose not to include bridging units as part of core units.



**For the design of `No major should require more than 40 contact hours per week`,** I designed it as a major's *total average contact hours*, with the formula: 
$$
sum((total~contact~hour)*credit/6)/(number~of~units)
$$
For example, a major has 2 units a and b. 

`a(total contact hours =10, credit =6)`, 

`b(total contact hours=20, credit =12)`

 Using this formula the *total average contact hours* can be calculated as 10. The reason for this design is that initially, I hoped to use the example given by the teacher on Microsoft Teams,` (credit*40)/24`. But I found that this example does not apply to all cases. There might be some units with credit = 6 but contact hours >10. However, even if this course is selected, it doesn't mean the *total contact hours* exceed 40. It's more reasonable to have an average contact hours per unit, so I thought of using the total average contact hours as the measure for `No major should require more than 40 contact hours per week`.





### 2.tools used

**In the project**, I used `Pycharm` code editor, which helped me a lot with code debugging and format modification. Besides, I also used `Protégé` as a knowledge graph visualization tool, which allowed me to easily check whether the generated knowledge graph meets my requirements in all aspects, and I could quickly locate specified instances based on keywords. I would highly recommend both of these software for others to use in the future.





### 3.estimate of time

**For Question 1 and Question 2**, since they can be seen as the same task, I spent about 3 hours in total, from reading the project requirements, to identifying and importing data to writing code and checking for correctness. I spent 2 hours thinking, writing, and debugging the corresponding constraints and queries. 

**For Question 3**, it troubled me a lot. Initially, I saw it as the same knowledge graph as Question 1, but due to the overly simplistic design of the previous knowledge graph, I was unable to complete the task. Additionally, I wasn't sure whether it was allowed to have two knowledge graphs, so this process took me about 3-5 hours until I clarified with classmates that the project rules allowed for the creation of two knowledge graphs. I spent another 5 hours completing all coding for Question 3, among which 3 queries troubled me a lot, spending much time writing incorrect queries. 

**For report and user manual**, It took me 3 hours to write these, and while writing these contents, I reviewed and checked my code again.