# CS506 Final Project

![](assets\图片_20241210194403.png)

> This is a 3D visualization of the campus created using Blender. Unfortunately, I was unable to complete it due to time constraints.

#### Project Title

Optimizing Classroom Allocation to Minimize Professors’ Walking Cost at Boston University

#### Group members

- Junhui Huang (hjh604@bu.edu)
- Mingyuan Sun (mingyuan@bu.edu)

#### Midterm Report
[Video](https://www.youtube.com/watch?v=cfRX62oWjNg)

#### Description

The project aims to optimize the allocation of classrooms to professors by considering each professor’s required classroom size at specific time periods and the cost associated with walking between classrooms. The objective is to reassign classrooms to minimize the total walking cost for all professors. The optimization will be performed using the simulated annealing in Python.



## Goals
- Develop a classroom allocation model that minimizes the total walking cost for all professors.
- Take room capacity limits into account, and, if possible, consider additional factors such as media device requirements.
- Implement the model using the simulated annealing.
- Demonstrate the effectiveness of the model through comparative analysis with current planning at Boston University.



# Data Processing Report

### Overview

This report provides a detailed description of the data processing steps completed so far in our project. The data has been gathered from two primary sources: BU’s public student information system and BU’s classroom resources website. The main focus of this processing phase was to clean, reformat, and integrate data from these disparate sources to facilitate modeling and analysis.

### Data Collection

1. **Course Information**  
   - **Collected by**: Junhui Huang  
   - **Source**: [BU Public Student Information System](https://public.mybustudent.bu.edu/psp/BUPRD/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_Main)  
   - **Description**: All available course information for the Spring semester was scraped, covering details such as course names, schedules, locations, and instructor IDs.

2. **Classroom Information**  
   - **Collected by**: Mingyuan Sun  
   - **Source**: [BU Classroom Resource Finder](https://www.bu.edu/classrooms/find-a-classroom/)  
   - **Description**: Classroom details including room capacities, locations, and equipment were gathered from BU’s classroom finder website.

3. **Building Coordinates and Distance Matrix**  
   - **Collected by**: Junhui Huang  
   - **Description**: Geographical coordinates of all academic buildings were collected, and a matrix representing distances between each building was generated to calculate walking times between classrooms.

### Data Cleaning and Integration

- **Data Cleaning**  
  - **Responsibility**: Mingyuan Sun  
  - **Process**: Irrelevant fields were removed, and rows with missing or unreliable data were discarded to ensure data quality.
  - **Reformatting**: The data from both sources were reformatted to achieve consistency, enabling integration between course and classroom datasets.

- **Data Transformation**  
  - Fields were transformed and mapped across datasets, establishing links between course schedules and classroom details to support advanced scheduling models.

### Data Extraction for Modeling

From the cleaned and integrated dataset, the following data elements were extracted for use in modeling:

1. **Classroom Capacities**  
   - **Format**: Integer array  
   - **Description**: An array listing the seating capacity of each classroom, useful for determining space constraints in scheduling.

2. **Professor Schedule**  
   - **Format**: Dictionary with keys as `professor_id` and values as tuples `(start_time, end_time, capacity_required)`  
   - **Description**: Each professor’s weekly schedule, recorded in five-minute intervals, with a total of 2016 time slots per week. This structure also records each professor’s required classroom capacity.

3. **Walking Cost**  
   
   - **Format**: 2D Float Array `[i][j]`  

   - **Description**: A matrix representing the walking distance (cost) between classrooms `i` and `j`, facilitating calculations for optimal scheduling based on proximity.
   
   - **Visualizations**
   
     - ![](1.acquisition-junhui_huang\distribution_of_walking_distances.png)![](1.acquisition-junhui_huang\boxplot_of_walking_distances.png)
   
     - Most of the buildings are reachable within 2200 meters, with an average distance of 1200 meters. The outliers on the right represent building pairs that require walking between the main campus and the medical campus. To maintain relevance to computer science activities, we will exclude medical campus buildings to avoid scenarios like scheduling a computer science class in an operating room.
   
     - ![](1.acquisition-junhui_huang\top_10_distances.png)
   
     - We also provide a heat map of walking distances, which requires zooming in to view the values within the cells.
   
     - ![](1.acquisition-junhui_huang\heatmap_of_walking_distances.png)
   
     - We also provide a [map displaying the distribution of building locations](1.acquisition-junhui_huang\map.html), along with another [map illustrating the paths from all other buildings to the LAW building](1.acquisition-junhui_huang\path_to_law_map.html). Below are the corresponding screenshots:
   
     - ![image-20241210232204164](assets/image-20241210232204164.png)
   
       ![image-20241210232258400](assets/image-20241210232258400.png)



### Data Packaging

To streamline future data access, all processed datasets were serialized using Python’s `pickle` library. This approach allows for quick loading and ensures data consistency across multiple sessions and models.




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



#### A map showing the distribution of building locations.

[Here](https://github.com/zilongpa/CS506-Final-Project/blob/master/map.html)



## Evaluation

- Test the model on various what-if scenarios, such as changes in classroom availability.
- Assess the reduction in total walking cost achieved by the model.
- Evaluate the model’s ability to meet accessibility and feature requirements.
- Perform comparative analysis with the current classroom allocation to demonstrate improvements
