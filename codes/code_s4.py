import subprocess
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the constants
constants = {
    "total_sections": 10,
    "max_retries": 3,
    "max_distance": 150,

    "p_gas_presence":0.78,
    "p_structure_stable":  0.8,
    "p_structure_checkable": 1,
    
    "p_explore_success": 0.95,
    "p_gas_detect": 0.88,
    "p_structure_safe": 0.86,
    "p_send_success": 0.98,
    "p_send_success_lead": 0.86,
 
    "min_energy_lead": 10,
    "min_energy_gas_detector": 10,
    "min_energy_safe_detector": 10,
    "min_energy_leader": 10,
    "max_speed_lead": 120,
    "max_speed_gas_detector": 120,
    "max_speed_safe_detector": 120,
    "max_speed_leader": 120
}


param_str = ",".join([f"{key}={value}" for key, value in constants.items()])

model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"
simulation_output_file = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_output4.txt"


prism_command = [
    r"cd", r"prism-4.8.1\bin", "&&", 
    r"prism.bat", model_file, properties_file, "-const", param_str, 
    "-simpath", "300", simulation_output_file
]

# Execute the command
try:
    result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
    section_safe_to_check = set()
    structure_ok_flag_false = set()
    gas_detected_flag_true = set()
    section_safe_true = set()

    # Read the file and process
    with open(simulation_output_file, 'r') as file:
        lines = file.readlines()
        
        columns = lines[0].strip().split()
        
        current_section_idx = columns.index("current_section")
        section_safe_to_check_ind = columns.index("structure_safe_flag")
        structure_ok_flag_idx = columns.index("structure_ok_flag")
        gas_detected_flag_idx = columns.index("gas_detected_flag")
        section_safe_idx = columns.index("section_safe")
        
        for line in lines[1:]:
            fields = line.strip().split()
            
            current_section = fields[current_section_idx]
            section_safe_to_check_flag = fields[section_safe_to_check_ind] == "true"
            structure_ok_flag = fields[structure_ok_flag_idx] == "false"
            gas_detected_flag = fields[gas_detected_flag_idx] == "true"
            section_safe = fields[section_safe_idx] == "true"
            
            if structure_ok_flag:
                structure_ok_flag_false.add((current_section, structure_ok_flag))
            
            if gas_detected_flag:
                gas_detected_flag_true.add((current_section, gas_detected_flag))
            
            if section_safe:
                section_safe_true.add((current_section, section_safe))

            if section_safe_to_check_flag:
                section_safe_to_check.add((current_section, section_safe_to_check_flag))
    print("\nTuples with  section_safe_to_check:\n")
    for item in sorted( section_safe_to_check):
        print(item)    

    print("\nTuples with gas_detected_flag=True:\n")
    for item in sorted(gas_detected_flag_true):
        print(item)

    print("\nTuples with structure_ok_flag=False:\n")
    for item in sorted(structure_ok_flag_false):
        print(item)


    print("\nTuples with section_safe=True:\n")
    for item in sorted(section_safe_true):
        print(item)

    df = pd.read_csv(simulation_output_file, sep="\s+", header=None)


    columns = ["action", "step", "section_index", "gas_present", "structure_stable", 
            "can_check_section", "m", "z", "section", "structure_safe_flag", 
            "distance_to_leader", "lead_retry_count", "current_speed_lead", 
            "current_energy_lead", "send_data", "section_gas_check", 
            "gas_detected_flag", "send_gas_data", "x", 
            "distance_gas_detector_to_leader", "current_speed_gas_detector", 
            "current_energy_gas_detector", "section_safety_check", 
            "structure_ok_flag", "send_structure_data", 
            "distance_safety_assessment_to_leader", "y", 
            "current_speed_safe_detector", "current_energy_safe_detector", 
            "current_section", "section_safe_to_check", "section_safe", 
            "leader_retry_count", "sending_flag", "connection_success", 
            "k", "current_speed_leader", "current_energy_leader", "wait"]

    df.columns = columns 

   
    selected_columns = ["current_section","can_check_section","gas_present", "structure_stable", 
                        "structure_safe_flag", "gas_detected_flag","structure_ok_flag", "send_data","send_gas_data", "send_structure_data",
                        "section_safe"]

    df_selected = df[selected_columns]


    output_file = r"C:\Aterm9\Karshensi_Project\all\tables\selected_data_table4.txt"
    df_selected.to_csv(output_file, index=False, sep='\t')

    print("Selected data has been saved as a formatted table.")
    
    # Prepare a DataFrame to represent the heatmap
    sections = sorted(set([item[0] for item in section_safe_to_check] +
                        [item[0] for item in gas_detected_flag_true] +
                        [item[0] for item in structure_ok_flag_false] +
                        [item[0] for item in section_safe_true]))

    # Create a dictionary to hold flag values for each section
    data_dict = {
        "section_safe_to_check": section_safe_to_check,
        "gas_detected_flag_true": gas_detected_flag_true,
        "structure_ok_flag_false": structure_ok_flag_false,
        "section_safe_true": section_safe_true
    }

    # Initialize a DataFrame with the section names as the index
    df_heatmap = pd.DataFrame(index=sections, columns=data_dict.keys(), dtype=int).fillna(0)

    # Populate the DataFrame with 1s for the conditions that are true for each section
    for condition_name, condition_set in data_dict.items():
        for section, value in condition_set:
            df_heatmap.at[section, condition_name] = 1  # Set 1 where the flag is True

    plt.figure(figsize=(10, 6))
    sns.heatmap(df_heatmap, annot=True, cmap='coolwarm', cbar=False, linewidths=0.5, fmt="g")
    plt.title('scenario where the mining environment can be monitored')
    plt.ylabel('Section')
    plt.xlabel('Condition')
    s3_output_file = "plots\plot_s4_result.png" 
    plt.savefig(s3_output_file, format='png')
    plt.show()

except subprocess.CalledProcessError as e:
    print("Error during execution:", e)
    print(e.output)  
