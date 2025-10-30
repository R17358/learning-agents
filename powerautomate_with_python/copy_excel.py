import pandas as pd

# Step 1: Read data from the source Excel file
input_file = r"C:\Users\Admin\Desktop\my_wbs.xlsx"      
output_file = r"C:\Users\Admin\Desktop\output.xlsx"      

# Read all sheets 
data = pd.read_excel(input_file, sheet_name=None)  # Read all sheets as a dict

# Step 2: Write data to a new Excel file
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for sheet_name, df in data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Data successfully copied from {input_file} to {output_file}")
