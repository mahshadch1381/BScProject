import subprocess
import matplotlib.pyplot as plt

model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"
cost_file_path = r"consts\consts2.txt"

def plot_results(result_data, output_file):
    plt.figure(figsize=(10, 6))

    # Plot Property 5
    plt.subplot(121)
    plt.plot(result_data['group'], result_data['property_5'], marker='o', color='b', label='Max reward when "all robots ready" seen')
    plt.xlabel('p-explore-success')
    plt.ylabel('Max reward for :F "area_checked" {"all_robots_ready"}')
    plt.title('Success lead vs MaxReward "all robots ready"')
    plt.grid(True)
    plt.legend()

    # Table for Property 5
    plt.subplot(122)
    plt.axis('off')
    columns = ["p-explore-success", "max reward when all robots ready seen"]
    data = list(zip(result_data['group'], result_data['property_5']))
    plt.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
    plt.title("p-explore-success VS Max Reward all_robots_ready")
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


def connect_to_prism_cli_and_run(cost_group, counterGroup, result_data):
    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])
    prism_command = [
        r"cd", r"prism-4.8.1\bin", "&&",
        r"prism.bat", model_file, properties_file, "-const", param_str
    ]
    try:
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        output = result.stdout
        propertyNumber = 1
        p_explore_success = cost_group["p_explore_success"]
        for line in output.splitlines():
            if "Result" in line:
                print(f"Result for cost group {counterGroup} , property {propertyNumber} : {line}")
                if propertyNumber == 5:
                    property_5 = float(line.split(":")[1].strip())
                    result_data['group'].append(p_explore_success)
                    result_data['property_5'].append(property_5)
                elif propertyNumber == 7:
                    property_7 = float(line.split(":")[1].strip())
                    result_data['property_7'].append(property_7)

                propertyNumber += 1
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {counterGroup}:\n", e.stderr)




def plot_comparison(data1, data2, group_label, property_label, title, output_file):
    """
    Plots comparison between two sets of data with a graph and table.

    Parameters:
    - data1: Dictionary with 'group' and 'property' values for dataset 1.
    - data2: Dictionary with 'group' and 'property' values for dataset 2.
    - group_label: Label for the x-axis (e.g., "p-explore-success").
    - property_label: Label for the y-axis (e.g., "Max Reward").
    - title: Title of the plot and table (e.g., "Comparison of Max Rewards").
    - output_file: Path for saving the output plot image.
    """
    plt.figure(figsize=(16, 8))

    # Plot Comparison
    plt.subplot(121)
    plt.plot(data1['group'], data1['property'], marker='o', color='b', label='Max reward when "all robots ready" seen')
    plt.plot(data2['group'], data2['property'], marker='x', color='r', label='Max reward when "section not checkale" seen')
    plt.xlabel(group_label)
    plt.ylabel(property_label)
    plt.title(f"{title} (Graph)")
    plt.grid(True)
    plt.legend()

    # Table for Comparison
    plt.subplot(122)
    plt.axis('off')
    columns = [group_label, "MaxRewardAllRobotsReady", "MaxRewardNotCheckable", "Difference"]
    table_data = [( data1['group'][i],  # p_gas_detect 
            data1['property'][i],  # Reward for Property 5
            data2['property'][i],  # Reward for Property 7
            data2['property'][i] - data1['property'][i]  # Difference
            )  for i in range(len(data1['group']))
    ]
    table = plt.table(
        cellText=table_data,
        colLabels=columns,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)  # Adjust font size
    table.scale(1.2, 1.4)  # Adjust table scaling
    plt.title(f"{title} (Table)")
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()


# Main script
result_data = {'group': [],'property_5': [],'property_7': []}
counterGroup = 1
with open(cost_file_path, 'r') as cost_file:
    for line in cost_file:
        if line.strip():
            cost_group = extract_cost_line(line)
            connect_to_prism_cli_and_run(cost_group, counterGroup, result_data)
        counterGroup += 1

# Plotting the individual results
plot_results(result_data, "plots/plot_results2.png")

# Plotting the comparison
data1 = {'group': result_data['group'], 'property': result_data['property_5']}
data2 = {'group': result_data['group'], 'property': result_data['property_7']}
plot_comparison(data1, data2, "p-explore-success", "Max Reward", "Comparison of max reward in different conditions", "plots/plot_comparison_result2.png")
