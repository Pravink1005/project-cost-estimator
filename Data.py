import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic project data
num_samples = 500

labor_cost = np.random.randint(3000, 25000, num_samples)   # Random labor costs
material_cost = np.random.randint(5000, 40000, num_samples)  # Random material costs
equipment_cost = np.random.randint(2000, 15000, num_samples)  # Equipment costs
miscellaneous_cost = np.random.randint(500, 5000, num_samples)  # Miscellaneous costs
duration = np.random.randint(3, 24, num_samples)  # Project duration (months)

# Calculate total cost with a realistic overhead of 10% to 20%
overhead_percentage = np.random.uniform(1.1, 1.2, num_samples)
total_cost = (labor_cost + material_cost + equipment_cost + miscellaneous_cost) * overhead_percentage

# Create a DataFrame
df = pd.DataFrame({
    "Labor Cost": labor_cost,
    "Material Cost": material_cost,
    "Equipment Cost": equipment_cost,
    "Miscellaneous Cost": miscellaneous_cost,
    "Duration": duration,
    "Total Cost": total_cost.round(2)  # Round to 2 decimal places
})

# Save dataset to CSV
df.to_csv("data/real_project_cost_data.csv", index=False)

print("✅ Realistic Project Cost Dataset Created Successfully!")
