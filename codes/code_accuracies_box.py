import subprocess
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the constants
constants1 = {
    "total_sections": 8,
     "max_retries": 3,
    "max_distance": 150,
    "p_gas_presence": 1,
    "p_structure_stable": 0.96,
    "p_structure_checkable": 0.89,
    "p_explore_success": 0.95,
    "p_gas_detect": 0.97,
    "p_structure_safe": 0.95,
    "p_send_success": 0.78,
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
constants2 = {
   "total_sections": 10,
    "max_retries": 3,
    "max_distance": 150,
    "p_gas_presence":0.78,
    "p_structure_stable": 1,
    "p_structure_checkable": 0.89,
    "p_explore_success": 0.95,
    "p_gas_detect": 0.97,
    "p_structure_safe": 0.95,
    "p_send_success": 0.78,
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
constants3 = {
    "total_sections": 10,
    "max_retries": 3,
    "max_distance": 150,
    "p_gas_presence":0.78,
    "p_structure_stable": 0.96,
    "p_structure_checkable": 1,
    "p_explore_success": 0.95,
    "p_gas_detect": 0.97,
    "p_structure_safe": 0.95,
    "p_send_success": 0.78,
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


model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"
simulation_output_file_accuracy = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_output_t1.txt"
simulation_output_file_accuracy2 = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_output_t2.txt"
simulation_output_file_accuracy3 = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_output_t3.txt"

# Accuracy storage
accuracies = []
inverted_accuracies = []
accuracies3 = []

try:
    param_str = ",".join([f"{key}={value}" for key, value in constants1.items()])
    for run in range(100):  # Run the command 15 times
        prism_command = [
            r"cd", r"prism-4.8.1\bin", "&&",
            r"prism.bat", model_file, properties_file, "-const", param_str,
            "-simpath", "300", simulation_output_file_accuracy
        ]

        subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)

        gas_detected_flag_true = set()

        with open(simulation_output_file_accuracy, 'r') as file:
            lines = file.readlines()

            columns = lines[0].strip().split()
            current_section_idx = columns.index("current_section")
            gas_detected_flag_idx = columns.index("gas_detected_flag")

            for line in lines[1:]:
                fields = line.strip().split()
                current_section = fields[current_section_idx]
                gas_detected_flag = fields[gas_detected_flag_idx] == "true"

                if gas_detected_flag:
                    gas_detected_flag_true.add(current_section)

        # Calculate accuracy
        detected_count = len(gas_detected_flag_true)
        total_sections = constants1["total_sections"]
        accuracy = detected_count / total_sections
        accuracies.append(accuracy)
        print(f"Run {run + 1}: Accuracy = {accuracy:.2f}")
    #--------------------------------------------------------------------
    param_str = ",".join([f"{key}={value}" for key, value in constants2.items()])
    for run in range(100):  # Run the command 15 times
        prism_command = [
            r"cd", r"prism-4.8.1\bin", "&&",
            r"prism.bat", model_file, properties_file, "-const", param_str,
            "-simpath", "300", simulation_output_file_accuracy2
        ]

        subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)

        structure_ok_flag_false = set()

        with open(simulation_output_file_accuracy2, 'r') as file:
            lines = file.readlines()

            columns = lines[0].strip().split()
            current_section_idx = columns.index("current_section")
            structure_ok_flag_idx = columns.index("structure_ok_flag")

            for line in lines[1:]:
                fields = line.strip().split()
                current_section = fields[current_section_idx]
                structure_ok_flag = fields[structure_ok_flag_idx] == "false"

                if structure_ok_flag:
                    structure_ok_flag_false.add(current_section)

        # Calculate accuracy for structure_ok_flag = false
        false_flag_count = len(structure_ok_flag_false)
        total_sections = constants2["total_sections"]
        accuracy = false_flag_count / total_sections

        # Calculate 1 - accuracy
        inverted_accuracy = 1 - accuracy
        inverted_accuracies.append(inverted_accuracy)
        print(f"Run {run + 1}: Accuracy = {inverted_accuracy:.2f}")
    #--------------------------------------------------------------------
    param_str = ",".join([f"{key}={value}" for key, value in constants3.items()])        
    for run in range(100):  # Run the command 15 times
        prism_command = [
            r"cd", r"prism-4.8.1\bin", "&&",
            r"prism.bat", model_file, properties_file, "-const", param_str,
            "-simpath", "300", simulation_output_file_accuracy3
        ]

        subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)

        structure_checkable_true = set()

        with open(simulation_output_file_accuracy3, 'r') as file:
            lines = file.readlines()

            columns = lines[0].strip().split()
            current_section_idx = columns.index("current_section")
            structure_checkable_idx = columns.index("section_safe_to_check")

            for line in lines[1:]:
                fields = line.strip().split()
                current_section = fields[current_section_idx]
                structure_checkable = fields[structure_checkable_idx] == "true"

                if structure_checkable:
                    structure_checkable_true.add(current_section)

        # Calculate accuracy for p_structure_checkable = true
        true_flag_count = len(structure_checkable_true)
        total_sections = constants3["total_sections"]
        accuracy = true_flag_count / total_sections

        # Store accuracy
        accuracies3.append(accuracy)
        print(f"Run {run + 1}: Accuracy = {accuracy:.2f}")
    # تبدیل داده‌ها به DataFrame برای رسم
    data = {
        "Accuracy": accuracies + inverted_accuracies + accuracies3,
        "Sections": (["gas_presence"] * len(accuracies)) + (["structure_stable"] * len(inverted_accuracies)) + (["structure_checkable"] * len(accuracies3))
    }

    df = pd.DataFrame(data)

    # رسم نمودار باکس پلات
    plt.figure(figsize=(8, 6))
    sns.boxplot(x="Accuracy", y="Sections", data=df, orient="h", palette="Set2")

    # تنظیمات نمودار
    plt.xlabel("Accuracy")
    plt.ylabel("Sections (n)")
    plt.title("Boxplot of Accuracies for Different Section Sizes")
    plt.xlim(0, 1)  
    plt.grid(True, linestyle='--', alpha=0.7)
    output_file="plots/plot_accuracies_box.png" 
    plt.savefig(output_file, format='png', dpi=300)
    plt.show()
         
except subprocess.CalledProcessError as e:
    print("Error during execution:", e)
    print(e.output)