import pandas as pd

def update_config_item_name_with_correct_logic(config_csv_path, matrix_csv_path, output_csv_path):
    # Load the configuration CSV
    config_df = pd.read_csv(config_csv_path)
    
    # Load the matrix CSV
    matrix_df = pd.read_csv(matrix_csv_path, index_col=0)
    
    # Iterate through each configuration item
    for index, row in config_df.iterrows():
        # Attempt to update based on Exporter_name_app
        exporter_app = row['Exporter_name_app']
        if pd.notna(exporter_app) and exporter_app in matrix_df.columns:
            # Find the first 'Y' in the column and get the corresponding server type
            server_type = matrix_df[matrix_df[exporter_app] == 'Y'].index[0]
            config_df.at[index, 'Configuration Item Name'] = server_type
            continue  # Move to the next row once updated
        
        # If not updated, fallback to Exporter_name_os
        exporter_os = row['Exporter_name_os']
        if pd.notna(exporter_os):
            # Use the value with "exporter_" removed as the "Configuration Item Name"
            os_name = exporter_os.replace('exporter_', '')
            config_df.at[index, 'Configuration Item Name'] = os_name.capitalize()
            continue
        
        # Further fallback to "blackbox"
        if row.get('blackbox', 'FALSE') == 'TRUE':
            config_df.at[index, 'Configuration Item Name'] = 'blackbox'
    
    # Save the updated configuration
    config_df.to_csv(output_csv_path, index=False)

# Running the updated function with the correct file paths
config_csv_path = '/path/to/your/config.csv'  # Update this path
matrix_csv_path = '/path/to/your/Exporter Matrix.csv'  # Update this path
output_csv_path = '/path/to/your/final_updated_config.csv'  # Update this path

update_config_item_name_with_correct_logic(config_csv_path, matrix_csv_path, output_csv_path)
