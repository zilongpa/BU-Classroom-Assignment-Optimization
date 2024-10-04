# CS506 Final Project

#### Project Title

Optimizing Classroom Allocation to Minimize Professors’ Walking Cost at Boston University

#### Group members

- Junhui Huang (hjh604@bu.edu)
- Mingyuan Sun (mingyuan@bu.edu)

#### Description

The project aims to optimize the allocation of classrooms to professors by considering each professor’s required classroom size at specific time periods and the cost associated with walking between classrooms. The objective is to reassign classrooms to minimize the total walking cost for all professors. The optimization will be performed using the PuLP library in Python.



## Goals
- Develop a classroom allocation model that minimizes the total walking cost for all professors.
- Incorporate additional factors such as accessibility requirements and classroom features.
- Implement the model using the PuLP optimization library.
- Demonstrate the effectiveness of the model through comparative analysis with current planning at Boston University.



## Data collection

- Classroom Size Requirements:
  - Extract detailed scheduling needs from Boston University’s website, including class sizes and time slots.
- Distances Between Classrooms:
  - Create a model using building addresses and room numbers to estimate the walking cost between classrooms, possibly using campus maps or GIS data.
- Class Schedules:
  - Obtain fixed class schedules arranged by the university from the student portal
- Classroom Equipment Requirements:
  - Identify any special needs for classroom equipment for certain professors, such as lecture capture device and wireless microphone.
- Classroom Features
  - Gather information on classrooms with special equipment or facilities, such as
    - Lecture Capture
    - Audio Equipment
    - Chalkboard
    - Projector



## Modeling

- Formulate the problem as a linear optimization model.
- Define decision variables representing classroom assignments to professors to minimize the total walking cost for all professors.
- Set constraints based on classroom capacities and equipment availability.
- Use PuLP to model and solve the optimization problem to minimize average walking time.



## Visualization

- Create scatter plots or campus maps showing the locations of classrooms and the walking paths between them.
- Use heatmaps to display the frequency of classroom usage ( and highlight heavily trafficked areas if possible).
- Generate bar charts comparing total walking costs before and after optimization.
- Visualize the distribution of classrooms with special features and accessibility options.



## Testing

- Test the model on various what-if scenarios, such as changes in classroom availability.
- Assess the reduction in total walking cost achieved by the model.
- Evaluate the model’s ability to meet accessibility and feature requirements.
- Perform comparative analysis with the current classroom allocation to demonstrate improvements
