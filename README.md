# CS506 Final Project

The project aims to optimize the allocation of classrooms to teachers by considering each teacher’s required classroom size at specific time periods and the distances between classrooms. The objective is to reassign classrooms to minimize the average walking time for all teachers. The optimization will be performed using the PuLP library in Python.

Group members:
- Junhui Huang (hjh604@bu.edu)
- Mingyuan Sun (mingyuan@bu.edu)



## Goals
- Develop a classroom allocation model that minimizes the average walking time for all teachers.
- Implement the model using the PuLP optimization library.
- Demonstrate the effectiveness of the model through comparative analysis with current planning.



## Data collection

- Classroom size requirements: Extract detailed scheduling needs from the school’s website.
- Distances between classrooms: Create a model using building address and room number to estimate the walk distance.
- Class schedules: Arranged by the school and could be fetched from portal



## Modeling the data

- Formulate the problem as a linear optimization model.
- Define variables representing classroom assignments to professors.
- Set constraints based on classroom capacities and availability.
- Use PuLP to model and solve the optimization problem to minimize average walking time.



## Visualization

- Create scatter plots showing the positions of classrooms and walking paths.
- Use heatmaps to display the frequency of classroom usage.
- Generate bar charts comparing average walking times before and after optimization.



## Testing

- Perform k-fold cross-validation to assess the model’s performance across different data subsets.
- Test the model on various what-if scenarios, such as changes in classroom availability.
- Assess the reduction in average walking time achieved by the model.
