import subprocess
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, f_oneway
import numpy as np
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
simulation_output_file_accuracy = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_safety_t1.txt"
simulation_output_file_accuracy2 = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_safety_t2.txt"
simulation_output_file_accuracy3 = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_safety_t3.txt"

def simulate_data(accs, covs, num_scenarios=3, num_repeats=100):
    data = []
    np.random.seed(42)  # ثابت برای بازتولیدپذیری
    
    for scenario in range(num_scenarios):
        accuracy = accs[scenario]
        coverage = covs[scenario]
        for i in range(num_repeats):
            safety = 0.5 * accuracy[i] + 0.5 * coverage[i]  # شاخص Safety
            data.append({
                'Scenario': f'Scenario {scenario + 1}',
                'Accuracy': accuracy[i],
                'Coverage': coverage[i],
                'Safety': safety
            })

    return pd.DataFrame(data)

# Accuracy storage
accuracy1=[]
covearage1=[]
accuracy2 = []
covearage2=[]
accuracy3 = []
covearage3=[]

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
            section_idx = columns.index("section")

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
        max_section = max([int(line.strip().split()[section_idx]) for line in lines[1:]])
        coveragerate=max_section/ total_sections
        accuracy1.append(accuracy)
        covearage1.append(coveragerate)
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
            section_idx = columns.index("section")
            
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
        max_section = max([int(line.strip().split()[section_idx]) for line in lines[1:]])
        # Calculate 1 - accuracy
        inverted_accuracy = 1 - accuracy
        accuracy2.append(inverted_accuracy)
        coveragerate=max_section/ total_sections
        covearage2.append(coveragerate)
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
            section_idx = columns.index("section")

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
        max_section = max([int(line.strip().split()[section_idx]) for line in lines[1:]])
        coveragerate=max_section/ total_sections
        accuracy3.append(accuracy)
        covearage3.append(coveragerate)
        print(f"Run {run + 1}: Accuracy = {accuracy:.2f}")
    # تبدیل داده‌ها به DataFrame برای رسم

    acc = [accuracy1, accuracy2, accuracy3]
    cov = [covearage1, covearage2, covearage3]
    num_scenarios = 3
    num_repeats = 100  #

    data = simulate_data(acc, cov, num_scenarios, num_repeats)

    # محاسبه میانگین، انحراف معیار، و خطای استاندارد
    summary_stats = data.groupby('Scenario').agg(
        Mean_Safety=('Safety', 'mean'),
        Std_Safety=('Safety', 'std'),
        Std_Error=('Safety', lambda x: x.std() / np.sqrt(len(x)))
    ).reset_index()

    print("\nSummary Statistics:")
    print(summary_stats)

    # آزمون‌های آماری
    scenario_1 = data[data['Scenario'] == 'Scenario 1']['Safety']
    scenario_2 = data[data['Scenario'] == 'Scenario 2']['Safety']
    scenario_3 = data[data['Scenario'] == 'Scenario 3']['Safety']

    # تی‌تست بین سناریوها
    t_stat_12, p_value_12 = ttest_ind(scenario_1, scenario_2)
    t_stat_13, p_value_13 = ttest_ind(scenario_1, scenario_3)

    # آزمون ANOVA برای همه سناریوها
    anova_stat, anova_p_value = f_oneway(scenario_1, scenario_2, scenario_3)

    print("\nT-Test Results:")
    print(f"Scenario 1 vs Scenario 2: T-statistic = {t_stat_12:.2f}, P-value = {p_value_12:.4f}")
    print(f"Scenario 1 vs Scenario 3: T-statistic = {t_stat_13:.2f}, P-value = {p_value_13:.4f}")

    print("\nANOVA Test Results:")
    print(f"F-statistic = {anova_stat:.2f}, P-value = {anova_p_value:.4f}")

        # رسم نمودار جعبه‌ای برای مقایسه شاخص Safety
    plt.figure(figsize=(8, 6))
    data.boxplot(column='Safety', by='Scenario', grid=False, patch_artist=True, 
            boxprops=dict(facecolor='lightblue', color='blue'),
            medianprops=dict(color='red'))
    plt.title('Safety Index Comparison by Scenario')
    plt.suptitle('')  # حذف عنوان پیش‌فرض
    plt.xlabel('Scenario')
    plt.ylabel('Safety')
    plt.tight_layout()
    plt.savefig(r"plots\plot_safety.png", dpi=300, format="png", bbox_inches="tight")
    plt.show()
            
except subprocess.CalledProcessError as e:
    print("Error during execution:", e)
    print(e.output)