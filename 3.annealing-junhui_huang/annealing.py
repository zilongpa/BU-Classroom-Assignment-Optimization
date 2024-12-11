import pickle
import numpy as np
import time
import argparse


def evaluate_cost(solution, professor_courses, walking_cost, classroom_capacities):
    total_cost = 0
    for i, courses in professor_courses.items():
        for k in range(len(courses) - 1):
            current_classroom = solution[i][k]
            next_classroom = solution[i][k + 1]

            if current_classroom == next_classroom:
                total_cost -= 10  # Award for staying in the same room
            else:
                total_cost += walking_cost[current_classroom][next_classroom]

    for i, courses in professor_courses.items():
        for k, (_, _, demand) in enumerate(courses):
            classroom = solution[i][k]
            if demand > classroom_capacities[classroom]:
                total_cost += 1e6  # Penalty for putting too many students in a classroom

    return total_cost


def save_best_solution(solution, cost, filename):
    with open(filename, 'wb') as f:
        pickle.dump((solution, cost), f)


def simulated_annealing(professor_courses, num_classrooms, classroom_capacities, walking_cost, max_runtime, output_file, temperature=1000.0, cooling_rate=0.99):
    # Optimal values for temperature and cooling_rate determined to be 1000 and 0.99 through hyperparameter tuning.
    start_time = time.time()
    np.random.seed(42)
    solution = {i: np.random.randint(0, num_classrooms, len(
        courses)) for i, courses in professor_courses.items()}
    best_solution = solution
    best_cost = evaluate_cost(
        solution, professor_courses, walking_cost, classroom_capacities)

    iteration = 0
    while True:
        new_solution = {i: sol.copy() for i, sol in solution.items()}
        professor = np.random.choice(list(professor_courses.keys()))
        course = np.random.randint(0, len(professor_courses[professor]))
        new_solution[professor][course] = np.random.randint(0, num_classrooms)

        new_cost = evaluate_cost(
            new_solution, professor_courses, walking_cost, classroom_capacities)

        if new_cost < best_cost or np.random.rand() < np.exp((best_cost - new_cost) / temperature):
            solution = new_solution
            best_cost = new_cost
            best_solution = solution

        save_best_solution(best_solution, best_cost, output_file)
        temperature *= cooling_rate

        if iteration % 1000 == 0:
            print(f"Iteration {iteration}, Best Cost: {best_cost}")
        iteration += 1

        elapsed_time = time.time() - start_time
        if elapsed_time > max_runtime:
            print("Reached maximum runtime. Exiting loop.")
            break

    return best_solution, best_cost


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Simulated Annealing for Classroom Scheduling')
    parser.add_argument('--max_runtime', type=int, default=11 *
                        60 * 60 + 30 * 60, help='Maximum runtime in seconds')
    parser.add_argument('--days_of_week', nargs='+', default=[
                        "monday", "tuesday", "wednesday", "thursday", "friday"], help='Days of the week to process')
    args = parser.parse_args()

    max_runtime = args.max_runtime
    days_of_week = args.days_of_week

    for dayofweek in days_of_week:
        with open(f"2.preprocess-mingyuan_sun/{dayofweek}.pkl", "rb") as f:
            data = pickle.load(f)

        print("Number of available classrooms:", len(
            data["capacities"]))
        print(f"Number of professors on {dayofweek}:", len(
            data[f"{dayofweek}_professor_schedule"]))

        num_professors = len(data[f"{dayofweek}_professor_schedule"])
        num_classrooms = len(data["capacities"])
        classroom_capacities = np.asarray(data["capacities"])
        professor_courses = data[f"{dayofweek}_professor_schedule"]
        walking_cost = np.asarray(data["walking_cost"].tolist())

        best_solution, best_cost = simulated_annealing(
            professor_courses, num_classrooms, classroom_capacities, walking_cost, max_runtime, f'4.solutions/best_solution_{dayofweek}.pkl')

        print(f"Best Cost for {dayofweek}: {best_cost}")
        print(f"Best Solution for {dayofweek}: {best_solution}")
