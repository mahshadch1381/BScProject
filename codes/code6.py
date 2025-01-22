import subprocess
import matplotlib.pyplot as plt


model_file = r"C:\Aterm9\Karshensi_Project\all\first_model.prism"
properties_file = r"C:\Aterm9\Karshensi_Project\all\properties.props"
##prism.bat "C:\Aterm9\Karshensi_Project\all\first_model.prism" "C:\Aterm9\Karshensi_Project\all\properties.props" -const total_sections=10,max_retries=3,max_distance=150,recovery_position=33,p_explore_success=0.7,p_gas_detect=0.88,p_structure_safe=0.86,p_gas_presence=0.78,p_structure_stable=0.96,p_structure_checkable=0.89,p_send_success=0.78,p_send_success_lead=0.86,p_send_success_gas_detector=0.86,min_energy_lead=10,min_energy_gas_detector=10,min_energy_safe_detector=10,min_energy_leader=10,max_speed_lead=120,max_speed_gas_detector=120,max_speed_safe_detector=120,max_speed_leader=120 -simpath 250 "C:\Aterm9\Karshensi_Project\all\simulation_output.txt"

cost_file_path = r"C:\Aterm9\Karshensi_Project\all\consts\consts6.txt"

def parse_cost_line(line):
    param_dict = {}
    for param in line.strip().split(","):
        key_value = param.split("=")
        if len(key_value) == 2:
            key, value = key_value
            param_dict[key.strip()] = float(value.strip()) if "." in value else int(value.strip())
    return param_dict

def run_prism_with_cost_group(cost_group, counterGroup, result_data):
    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])

    prism_command = [
        r"cd", r"C:\Program Files\prism-4.8.1\bin", "&&",
        r"prism.bat", model_file, properties_file, "-const", param_str
    ]

    try:
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        output = result.stdout

        total_section = cost_group["total_sections"]
        result_data[0].append(total_section)  # Add total_sections to the result_data

        propertyNumber = 1
        for line in output.splitlines():
            if "Result" in line:
                print(f"Result for cost group {counterGroup}, property {propertyNumber}: {line}")
                value_str = line.split(":")[1].strip()

                if propertyNumber == 10:
                    # Parse and round numerical values to 5 decimal places
                    numerical_value = float(value_str.split()[0].strip())
                    rounded_value = round(numerical_value, 5)
                    result_data[propertyNumber].append(rounded_value)
                else:
                    if value_str.lower() == "true" or value_str.lower() == "false":
                        result_data[propertyNumber].append(value_str)  # Append boolean values as is
                    else:
                        # Parse and round other numerical values
                        numerical_value = float(value_str)
                        rounded_value = round(numerical_value, 5)
                        result_data[propertyNumber].append(rounded_value)

                propertyNumber += 1

    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {counterGroup}:\n", e.stderr)


# Initialize result_data with keys 0 to 10
result_data = {i: [] for i in range(11)}

counterGroup = 1
with open(cost_file_path, 'r') as cost_file:
    for line in cost_file:
        if line.strip():  # Skip empty lines
            cost_group = parse_cost_line(line)
            run_prism_with_cost_group(cost_group, counterGroup, result_data)
        counterGroup += 1

columns = ["Total Sections"] + [f"Property {i}" for i in range(1, 11)]
table_data = list(zip(*[result_data[key] for key in range(11)]))

plt.figure(figsize=(12, 6))
plt.axis("off")
plt.title("Result Table for Properties", fontsize=14)

# Add table
table = plt.table(
    cellText=table_data,
    colLabels=columns,
    loc="center",
    cellLoc="center",
)

# Increase font size for the table cells
table.auto_set_font_size(False)
table.set_fontsize(9)  # Adjust this value to make the font size bigger
table.scale(1.2, 1.2)  # Scale the table to make it larger

# Add explanations below the table
explanation_text = """
Property 1:From any state, if unsafe area is detected, system in next step will reach unsafe state.
Property 2:From any state, if safe area is detected, system in next step will reach safe state.
Property 3:From any state, if low energy is detected, robot will eventually recover.
Property 4:From any state, proper distance is maintained.
Property 5:Maximum expected REWARD to reach area_checked state and it has the conditions for the robots to return to the initial state.
Property 6:Minimum expected REWARD to reach area_checked state and it has the conditions for the robots to return to the initial state. 
Property 7:Maximum expected REWARD to reach area_checked state and it has the conditions for the section can not be checked.
Property 8:Safty condition,all section should be checked(with probability of 1).
Property 9:Finaly all robots should be at initialize situation.
Property 10:failure condition,when has failure in connection or low energ for robots.
"""

plt.text(
    0.01, -0.15, explanation_text, fontsize=7, ha="left", va="top", transform=plt.gca().transAxes
)

# Save the table as an image
output_file = "plots/result_properties_table_with_explanations.png"
plt.savefig(output_file, dpi=300, format="png", bbox_inches="tight")
plt.show()
