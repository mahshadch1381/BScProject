import subprocess
import matplotlib.pyplot as plt

model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"
cost_file_path = r"consts\consts2.txt"

def plot_grouped_results(grouped_data, output_file):
    plt.figure(figsize=(10, 6))

    # Iterate over each total_sections group and plot its data
    for total_sections, data in grouped_data.items():
        plt.plot(
            data['p_explore_success'], 
            data['property_5'], 
            marker='o', 
            label=f'total_sections={total_sections}'
        )

    plt.xlabel('p-explore-success')
    plt.ylabel('Max reward for :F "area_checked" {"all_robots_ready"}')
    plt.title('Probability of Success vs Max Reward (Grouped by total_sections)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()

def extract_cost_line(line):
    param_dict = {}
    for param in line.strip().split(","):
        key_value = param.split("=")
        if len(key_value) == 2:
            key, value = key_value
            param_dict[key.strip()] = float(value.strip()) if "." in value else int(value.strip())
    return param_dict

def connect_to_prism_cli_and_run(cost_group, result_data):
    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])
    prism_command = [
        r"cd", r"prism-4.8.1\bin", "&&",
        r"prism.bat", model_file, properties_file, "-const", param_str
    ]
    try:
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        output = result.stdout
        propertyNumber = 1
        for line in output.splitlines():
            if "Result" in line:
                if propertyNumber == 5:
                    property_5 = float(line.split(":")[1].strip())
                    total_sections = cost_group["total_sections"]
                    p_explore_success = cost_group["p_explore_success"]
                    print(f"Result for cost group {total_sections} , property { propertyNumber} : {line}")
                    if total_sections not in result_data:
                        result_data[total_sections] = {"p_explore_success": [], "property_5": []}

                    result_data[total_sections]["p_explore_success"].append(p_explore_success)
                    result_data[total_sections]["property_5"].append(property_5)
                    break  # Only process property_5
                propertyNumber += 1    
                
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {cost_group}:", e.stderr)

# Main script
result_data = {}
with open(cost_file_path, 'r') as cost_file:
    for line in cost_file:
        if line.strip():
            cost_group = extract_cost_line(line)
            connect_to_prism_cli_and_run(cost_group, result_data)

# Plotting the grouped results
plot_grouped_results(result_data, "plots/grouped_plot_results_explore.png")
