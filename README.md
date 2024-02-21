# AI based management system development for production logistics optimization in the company
## Summary

| Company name                            | [TALLINNA TEHNIKAÜLIKOOL](https://taltech.ee/)                                                                                                                                                          |
|:----------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Development Team Lead Name              | [Tõnis, Raamets](https://taltech.ee/kontaktid/tonis-raamets)                                                                                                                                            |
| Development Team Lead e-mail            | [tonis.raamets@taltech.ee](tonis.raamets@taltech.ee)                                                                                                                                                    |
| Objectives of the Demonstration Project | Organizing and visualizing the company's daily based production logistics through the smart AI based management system, which help to increase production capacity and production processes efficiency. |

# Kirjeldus:

The title of the project is "AI based management system development for production 
logistics optimization in the company". The challenge of the project was to organize 
and visualize the company's daily production logistics using a smart AI-based 
management system that would help increase production capacity and the efficiency 
of production processes. The aim of the project was to validate artificial intelligence 
technology that would enable optimization of production logistics planning, 
management and monitoring in real time. The project's activities included the 
development, testing and implementation of an AI-based control system in the 
company's production units. The results of the project showed that the AI-based 
management system was able to reduce production logistics costs, improve the quality 
and accuracy of production processes, and increase customer satisfaction.

## Objectives of the Demonstration Project

*Organizing and visualizing the company's daily based production logistics through the smart AI 
based management system, which help to increase production capacity and production 
processes efficiency.*

## Activities and results of demonstration project

*Challenge addressed (i.e. whether and how the initial challenge was changed during the project, for which investment the demonstration project was
provided)*

- The aim of the demonstration project was to address the challenge of improving 
production logistics in the context of growing production volumes and new, more 
efficient production lines. This challenge was crucial for the company as it affected the 
efficiency, quality and profitability of the production process. The demonstration project 
implemented a new automated transportation system with artificial intelligence 
functionality that connected the raw material warehouse, production lines, and finished 
goods warehouse, as well as the introduction of a smart transportation task 
management system that minimized the need for intermediate storage areas on the 
factory floor. In this way, the demo project ensured a smooth and fast material and 
information flow throughout the entire production cycle, which resulted in incre

*Data sources (which data was used for the technological solution)*

- The technological solution uses data from the digital twin(Dimusa), the optimal route 
algorithm and the work orders to provide the initial system input for ordering the work 
orders. We exclude the part of the system that deals with task execution and history 
collection because it is another system that ultimately helps with refining the work 
order sequencing. 
To find the best system, we need to set the evaluation criteria. 
• Number of delays; 
• Total time of delays; 
• Amount of empty travel; 
• Empty travel time. 
Their importance may vary for the observer, but the most important are the first 2 and 
their value should be 0, and the rest should be as close to 0 as possible.

*Description and justifictaion of used AI technology*

- The AI technology used for finding the optimal path is implemented as a multi-level 
(hierarchical) algorithm. It uses the information from the nodes and additional general 
information such as the distances between the nodes to determine the loading and 
unloading points, i.e. the nodes that must be passed through. On the lower level, the 
algorithm determines the detailed optimal path from start to finish using the results 
from the upper level and general information (distances between nodes, allowed 
directions of movement) as input. The lower level algorithm can be implemented as 
subtasks. For the specific task, many shortest path algorithms are suitable because the 
data volumes are small (genetic, ant colony, particle swarm, etc. algorithms). 
Considering also the possible increase in data volumes, combinatorial algorithms 
(Dijkstra and Bellmann-FORD) are reasonable choices. The experiments conducted 
confirmed that evolutionary algorithms are significantly slower even for very small data 
volumes. For the problem under consideration, Dijkstra's algorithm proved to be the 
fastest and was also the final choice. The solution is planned to work in real time 
(decisions are made based on real-time information from sensors). 

*Results of testing and validating technological solution*

- The results of testing and validation of the development of the transport order 
management system based on artificial intelligence show that the system is capable of 
providing the user with a convenient and efficient solution for organizing production 
logistics. The system allows the user to enter, monitor and manage transport orders 
using an intuitive and informative user interface (Dimusa). The system uses artificial 
intelligence algorithms to optimize the execution of transport orders, taking into 
account various production logistics requirements and constraints, such as the 
availability of transport means, the schedule of production processes, customer 
expectations and environmental impacts. The system provides the user with an 
overview of the optimized transport order plan, allowing the user to make changes or 
confirm the plan. The system communicates with means of transport (people, robots) 
and transmits to them the plan of approved transport orders, monitoring their 
execution in real time and notifying the user of possible problems or deviations. The 
system collects and stores data on the execution of transport orders and prepares 
reports and statistics based on them, which help the user to evaluate the efficiency of 
production logistics and find opportunities for improvement. 

*Technical architecture (presented graphically, where can also be seen how the technical solution integrates with the existing system)*

![Alt text](pic/tehnical_architecture.png?raw=true "Title")


*Potential areas of use of technical solution*

- An AI based management system development for production logistics optimization in 
the company can have various potential areas of use. For example, it can help to 
improve the efficiency and accuracy of inventory management, reduce the costs and 
risks of transportation and distribution, enhance the quality and reliability of customer 
service, and support the decision making and planning of production processes. By using 
AI techniques such as machine learning, natural language processing, computer vision, 
and optimization algorithms, the system can learn from data, analyze complex 
situations, generate insights and recommendations, and automate tasks. The system 
can also adapt to changing conditions and demands and provide feedback and 
evaluation to improve its performance over time.

*Lessons learned (i.e. assessment whether the technological solution actually solved the initial challenge)*

- The management system based on artificial intelligence allows CHEMI-PHARM to 
optimize its production logistics processes and reduce costs. Such a system can use, for 
example, data analysis, machine learning and optimization algorithms to find the best 
solutions for production logistics transport plans, to ensure the need for materials at 
workplaces, to transport finished products from production lines and to visualize 
transport tasks. 
A positive user experience when implementing such a system depends on how the 
system interacts with users and how much they can influence the system's decisions. 
Ideally, the system should be intuitive, transparent and flexible, so that users can trust 
and follow the system's recommendations, as well as make changes or exceptions if 
necessary. Such a complete system ultimately improves user satisfaction, efficiency and 
motivation. 

### Description of User Interface



- Separate and additional features for GUI were developed for user interaction. GUI 
include tables, forms and graphs from where client can setup system; create, request, 
validate, manage tasks and all other required inputs that is needed to fill system 
requirements (beacons, anchor, anchor connections, storages, actions, missions) and 
visualize previously mentioned. Everything mentioned was developed and validated by 
users in Taltech and client in CHEMI-PHARM. While handling tasks history is written by 
every command action and stored in database for future use. All GUI actions can be 
done as API requests, therefore it can be integrated to any work process that can use 
API and any measured result can see by any system (ERP) that can manage API access.


