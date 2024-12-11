import matplotlib.pyplot as plt

def parse_cost_file(filepath):
    day_costs = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(':')
                day = parts[0].replace(" cost", "").strip()  # "Monday"
                cost_value = float(parts[1].strip())
                day_costs[day] = cost_value
    return day_costs

original_cost_file = '../4.solutions/weekly_walking_cost_original.txt'
new_cost_file = '../4.solutions/weekly_walking_cost_solution.txt'

original_costs = parse_cost_file(original_cost_file)
new_costs = parse_cost_file(new_cost_file)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
original_values = [original_costs[d] for d in days]
new_values = [new_costs[d] for d in days]

x = range(len(days))

plt.figure(figsize=(10,6))
bar_width = 0.35

plt.bar([i - bar_width/2 for i in x], original_values, width=bar_width, label='Original Cost')
plt.bar([i + bar_width/2 for i in x], new_values, width=bar_width, label='Optimized Cost', color='orange')

plt.xticks(x, days)
plt.ylabel('Cost')
plt.title('Comparison of Walking Costs Before and After Optimization')
plt.legend()

plt.tight_layout()
plt.savefig("../assets/cost_comparison.png")

