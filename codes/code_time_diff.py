import subprocess
import matplotlib.pyplot as plt
import sys


model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"
cost_file_path = r"consts\consts7.txt"
simulation_output_file= r"C:\Aterm9\Karshensi_Project\all\tables\simulation_output7.txt"
##prism.bat "C:\Aterm9\Karshensi_Project\all\first_model.prism" "C:\Aterm9\Karshensi_Project\all\properties.props" -const total_sections=10,max_retries=3,max_distance=150,recovery_position=33,p_explore_success=0.7,p_gas_detect=0.88,p_structure_safe=0.86,p_gas_presence=0.78,p_structure_stable=0.96,p_structure_checkable=0.89,p_send_success=0.78,p_send_success_lead=0.86,p_send_success_gas_detector=0.86,min_energy_lead=10,min_energy_gas_detector=10,min_energy_safe_detector=10,min_energy_leader=10,max_speed_lead=120,max_speed_gas_detector=120,max_speed_safe_detector=120,max_speed_leader=120 -simpath 250 "C:\Aterm9\Karshensi_Project\all\simulation_output.txt"




def parse_cost_line(line):
    param_dict = {}
    for param in line.strip().split(","):
        key_value = param.split("=")
        if len(key_value) == 2:
            key, value = key_value
            param_dict[key.strip()] = float(value.strip()) if "." in value else int(value.strip())  
    return param_dict


def run_prism_with_cost_group(cost_group, counterGroup, result_data, maxs, mins, avgs):
    param_str = ",".join([f"{key}={value}" for key, value in cost_group.items()])

    prism_command = [
        r"cd", r"prism-4.8.1\bin", "&&",
        r"prism.bat", model_file, properties_file, "-const", param_str,
        "-simpath", "600", simulation_output_file
    ]

    try:
        max_value = 0  # تغییر نام متغیر
        min_value = sys.maxsize  # تغییر نام متغیر
        sum_value = 0
        for run in range(20): 
            subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)

            with open(simulation_output_file, 'r') as file:
                lines = file.readlines()
                total_section = cost_group["total_sections"]
                # استفاده از max_value به جای max
                max_step = max([int(line.strip().split()[1]) for line in lines[1:]])
                print(max_step)
                if max_step > max_value:
                    max_value = max_step
                if max_step < min_value:
                    min_value = max_step
                sum_value += max_step
            if run == 19:
                maxs.append(max_value)
                mins.append(min_value)
                avgs.append(sum_value /20)   
                result_data['group'].append(total_section)     
            print(f"here {total_section} and step: {max_step}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running PRISM with cost group {counterGroup}:\n", e.stderr)

result_data = {
    'group': [],
    'property_5': []
}


counterGroup = 1
mins=[]
maxs=[]
avgs=[]
with open(cost_file_path, 'r') as cost_file:
    for line in cost_file:
        if line.strip():  
            cost_group = parse_cost_line(line)
            run_prism_with_cost_group(cost_group, counterGroup, result_data,maxs,mins,avgs)
        counterGroup += 1 

import matplotlib.pyplot as plt

# دریافت مقادیر گروه‌ها و داده‌های مرتبط
groups = result_data['group']

# رسم نمودار
plt.figure(figsize=(10, 6))
plt.plot(groups, mins, label="Min Values", marker='o', linestyle='-', linewidth=2)
plt.plot(groups, maxs, label="Max Values", marker='o', linestyle='-', linewidth=2)
plt.plot(groups, avgs, label="Average Values", marker='o', linestyle='-', linewidth=2)

# تنظیمات نمودار
plt.title("Min, Max, and Average Values for Different Groups", fontsize=14)
plt.xlabel("total sections", fontsize=12)
plt.ylabel("time to cover", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)

plt.tight_layout()
plt.savefig(r"plots\acc_box.png", dpi=300, format="png", bbox_inches="tight")
# نمایش نمودار
plt.show()

