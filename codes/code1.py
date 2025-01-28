import subprocess
import matplotlib.pyplot as plt


model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"
cost_file_path = r"consts\consts1.txt"
##prism.bat "C:\Aterm9\Karshensi_Project\all\first_model.prism" "C:\Aterm9\Karshensi_Project\all\properties.props" -const total_sections=10,max_retries=3,max_distance=150,recovery_position=33,p_explore_success=0.7,p_gas_detect=0.88,p_structure_safe=0.86,p_gas_presence=0.78,p_structure_stable=0.96,p_structure_checkable=0.89,p_send_success=0.78,p_send_success_lead=0.86,p_send_success_gas_detector=0.86,min_energy_lead=10,min_energy_gas_detector=10,min_energy_safe_detector=10,min_energy_leader=10,max_speed_lead=120,max_speed_gas_detector=120,max_speed_safe_detector=120,max_speed_leader=120 -simpath 250 "C:\Aterm9\Karshensi_Project\all\simulation_output.txt"




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
        r"cd", r"prism-4.8.1\bin", "&&", 
        r"prism.bat", model_file, properties_file, "-const", param_str
    ]

    try:
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        
        output = result.stdout
        propertyNumber = 1
        total_section = cost_group["total_sections"]
        for line in output.splitlines():
            if "Result" in line:
                print(f"Result for cost group {counterGroup} , property { propertyNumber} : {line}")
                if propertyNumber == 5:
                    property_5 = float(line.split(":")[1].strip())
                    result_data['group'].append(total_section)
                    result_data['property_5'].append(property_5)
                elif propertyNumber == 7:
                    property_7 = float(line.split(":")[1].strip())
                    result_data['property_7'].append(property_7)
                elif propertyNumber == 10:
                    numerical_value = line.split(":")[1].split()[0].strip()
                    property_10 = float(numerical_value)
                    result_data['property_10'].append(1-property_10)    
         
             
                propertyNumber += 1
    
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {counterGroup}:\n", e.stderr)

result_data = {
    'group': [],
    'property_5': [],
    'property_7': [],
    'property_10': []
}


counterGroup = 1
with open(cost_file_path, 'r') as cost_file:
    for line in cost_file:
        if line.strip():  
            cost_group = parse_cost_line(line)
            run_prism_with_cost_group(cost_group, counterGroup, result_data)
        counterGroup += 1 


plt.figure(figsize=(10, 6))

# Plot Property 5
plt.subplot(121)
plt.plot(result_data['group'], result_data['property_5'], marker='o', color='b', label='Max reward when "all robots ready" seen')
plt.xlabel('Total Sections')
plt.ylabel('Max reward for :F "area_checked" {"all_robots_ready"}')
plt.title('total sections vs max reward')
plt.grid(True)
plt.legend()

# Table for Property 5
plt.subplot(122)
plt.axis('off')
columns = ["Total Sections", "all robots ready max rewards"]
data = list(zip(result_data['group'], result_data['property_5']))
plt.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
plt.title("Property 5 Values")

plt.tight_layout()
plt.savefig("plots/plot_results1.png", format='png', dpi=300)
plt.close()

# Plot and save Reliability plot and table
plt.figure(figsize=(10, 6))

# Plot Reliability
plt.subplot(121)
plt.plot(result_data['group'], result_data['property_10'], marker='o', color='r', label='Reliability')
plt.xlabel('Total Sections')
plt.ylabel('Reliability')
plt.title('Reliability')
plt.grid(True)
plt.legend()

# Table for Reliability
plt.subplot(122)
plt.axis('off')
columns = ["Total Sections", "Reliability"]
data = list(zip(result_data['group'], result_data['property_10']))
plt.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
plt.title("Reliability Values")

plt.tight_layout()
plt.savefig("plots/plot_reliability_results.png", format='png', dpi=300)
plt.close()
