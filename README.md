# CS506 Final Project

#### Project Title

Optimizing Classroom Allocation to Minimize Professors’ Walking Cost at Boston University

#### Group members

- Junhui Huang (hjh604@bu.edu)
- Mingyuan Sun (mingyuan@bu.edu)

#### Midterm Report
[Video](https://www.youtube.com/watch?v=cfRX62oWjNg)

#### Description

The project aims to optimize the allocation of classrooms to professors by considering each professor’s required classroom size at specific time periods and the cost associated with walking between classrooms. The objective is to reassign classrooms to minimize the total walking cost for all professors. The optimization will be performed using the PuLP library in Python.



## Goals
- Develop a classroom allocation model that minimizes the total walking cost for all professors.
- Incorporate additional factors such as accessibility requirements and classroom features.
- Implement the model using the PuLP optimization library.
- Demonstrate the effectiveness of the model through comparative analysis with current planning at Boston University.



## Data collection
we are planing to use info on https://www.bu.edu/classrooms/find-a-classroom/
- Classroom Size Requirements
  - Extract detailed scheduling needs from Boston University’s website, including class sizes and time slots.
- Distances Between Classrooms
  - Create a model using building addresses and room numbers to estimate the walking cost between classrooms, possibly using campus maps or GIS data.
- Class Schedules
  - Obtain fixed class schedules arranged by the university from the student portal
- Classroom Equipment Requirements
  - Identify any special needs for classroom equipment for certain professors, such as lecture capture device and wireless microphone.
- Classroom Features
  - Gather information on classrooms with special equipment or facilities, such as
    - Lecture Capture
    - Audio Equipment
    - Chalkboard
    - Projector



## Modeling

The classroom assignment challenge is formulated as a linear optimization model. The objective is to allocate classrooms to professors in a way that **minimizes the total walking cost** over the entire schedule.



**Decision Variables**:

- Define a binary variable `x[i, j, k]`, which represents whether professor i is assigned to classroom j at time slot k. This variable helps determine classroom assignments while aiming to minimize walking costs.
- Introduce another helper binary variable `y[i, j, k, m]` to represent whether professor i transitions from classroom j at time k to classroom m at time k+1. 

**Constraints**:

- **Transition Constraints**: For each professor, if they are in classroom j at time k and then move to classroom m at time k+1, the variable y[i,j,k,m] must be 1 according to the classroom assignments.
- **One Classroom per Course**: Each professor can only be assigned to one classroom at a time.
- **One Course per Classroom**: To prevent classroom conflicts, each classroom can host only one course at any given time. 
- **Classroom Capacity Constraint**: Each classroom’s capacity must meet or exceed the demand of the assigned course. 

**Solution Approach**:

- The optimization problem is modeled with PuLP and solved using CBC for the midterm with a small datasets. We decide to run the full datasets with Cplex since it has a better optimization strategy.



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
