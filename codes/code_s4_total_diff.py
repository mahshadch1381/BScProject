import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# مقداردهی اولیه ثابت‌های مشترک
constants_template = {
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

# مقادیر مختلف برای total_sections
total_sections_values = [6, 8, 10, 12]

# مسیر فایل‌ها
model_file = r"..\..\first_model.prism"
properties_file = r"..\..\properties.props"
simulation_output_file_template = r"C:\Aterm9\Karshensi_Project\all\tables\simulation_output4_total_sections_{}.txt"

# داده‌های خروجی برای رسم نمودار
results = []

# اجرای شبیه‌سازی برای هر مقدار از total_sections
for total_sections in total_sections_values:
    # تنظیم ثابت‌ها برای این مقدار
    constants = constants_template.copy()
    constants["total_sections"] = total_sections
    param_str = ",".join([f"{key}={value}" for key, value in constants.items()])
    simulation_output_file = simulation_output_file_template.format(total_sections)

    # فرمان PRISM
    prism_command = [
        r"cd", r"prism-4.8.1\bin", "&&",
        r"prism.bat", model_file, properties_file, "-const", param_str,
        "-simpath", "600", simulation_output_file
    ]

    try:
        # اجرای شبیه‌سازی
        result = subprocess.run(' '.join(prism_command), shell=True, capture_output=True, text=True, check=True)
        section_safe_to_check = set()
        structure_ok_flag_false = set()
        gas_detected_flag_true = set()
        section_safe_true = set()

        # پردازش فایل خروجی
        with open(simulation_output_file, 'r') as file:
            lines = file.readlines()

            columns = lines[0].strip().split()

            current_section_idx = columns.index("current_section")
            section_safe_to_check_ind = columns.index("structure_safe_flag")
        
            send_data_idx = columns.index("send_data")
            section_safe_idx = columns.index("section_safe")
            section_idx = columns.index("section")

            todt_values = []  # برای ذخیره ToTD

            for line in lines[1:]:
                fields = line.strip().split()
                current_section = fields[current_section_idx]
                section_safe_to_check_flag = fields[section_safe_to_check_ind] == "true"
    
                send_data_flag = fields[send_data_idx ] == "true"
                section_safe = fields[section_safe_idx] == "true"

                # ذخیره اولین زمان شناسایی هدف (ToTD)
            
                if send_data_flag:
                     todt_values.append(int(fields[1]))    

                if section_safe:
                    section_safe_true.add((current_section, section_safe))

                if section_safe_to_check_flag:
                    section_safe_to_check.add((current_section, section_safe_to_check_flag))

        # محاسبه مقادیر مورد نظر
        max_step = max([int(line.strip().split()[1]) for line in lines[1:]])
        avg_todt = sum(todt_values) / len(todt_values) if todt_values else 0
        max_section = max([int(line.strip().split()[section_idx]) for line in lines[1:]])

        results.append({
            "total_sections": total_sections,
            "section_safe_to_check": len(section_safe_to_check),
            "gas_detected_flag": len(gas_detected_flag_true),
            "max_step": max_step,
            "avg_todt": avg_todt,
            "max_section": max_section
        })

    except subprocess.CalledProcessError as e:
        print(f"Error during execution for total_sections={total_sections}: {e}")

# تبدیل نتایج به DataFrame
results_df = pd.DataFrame(results)

# رسم نمودار Coverage Time (CT)
plt.figure(figsize=(8, 5))
plt.bar(results_df["total_sections"], results_df["max_step"], color="blue")
plt.xlabel("Total Sections")
plt.ylabel("Coverage Time (Steps)")
plt.title("Coverage Time (CT)")

plot_file ="plots\plot_s4_total_diff_ct.png"
plt.savefig(plot_file, format='png')
plt.show()


# رسم نمودار Number of Targets Found (NoTF)
plt.figure(figsize=(8, 5))
plt.bar(results_df["total_sections"], results_df["section_safe_to_check"], color="green")
plt.xlabel("Total Sections")
plt.ylabel("Number of Targets Found")
plt.title("Number of Targets Found (NoTF)")

plot_file ="plots\plot_s4_total_diff_Notf.png"
plt.savefig(plot_file, format='png')
plt.show()

# رسم نمودار Coverage Ratio (CR)
plt.figure(figsize=(8, 5))
coverage_ratio = results_df["max_section"] / results_df["total_sections"]
plt.bar(results_df["total_sections"], coverage_ratio, color="purple")
plt.xlabel("Total Sections")
plt.ylabel("Coverage Ratio")
plt.title("Coverage Ratio (CR)")
plt.ylim(0, 1.2)

plot_file = "plots\plot_s4_total_diff_CR.png"
plt.savefig(plot_file, format='png')
plt.show()

# رسم نمودار Time of Target Discovery (ToTD)
plt.figure(figsize=(10, 6))
plt.plot(results_df["total_sections"], results_df["avg_todt"], marker="o", color="orange", label="Average ToTD")
plt.xlabel("Total Sections")
plt.ylabel("Average Time of Target Discovery (Steps)")
plt.title("Time of Target Discovery (ToTD)")
plt.legend()
plt.grid()
plot_file = "plots\plot_s4_total_diff_ToTD.png"
plt.savefig(plot_file, format='png')
plt.show()
