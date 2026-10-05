import pandas as pd
import numpy as np
import os

def main():
    print("Starting data ingestion and transformation pipeline...")

    # 1. Safely handle file paths (works whether you run from root or /src)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, '..', 'data', 'supply_chain_dataset1.csv')
    output_path = os.path.join(base_dir, '..', 'data', 'processed_inventory_data.csv')

    # 2. Load the Kaggle dataset
    try:
        df = pd.read_csv(input_path)
        print(f"Successfully loaded {len(df)} rows.")
    except FileNotFoundError:
        print(f"ERROR: Could not find dataset at {input_path}")
        return

    # 3. Standardize column names (strips spaces, makes everything lowercase)
    # This prevents KeyErrors if Kaggle uses "Inventory Level" instead of "Inventory_Level"
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Check for the correct 'category' and 'inventory' columns based on the clean names
    category_col = 'category' if 'category' in df.columns else 'product_category' if 'product_category' in df.columns else df.columns[0]
    inventory_col = 'inventory_level' if 'inventory_level' in df.columns else 'inventory' if 'inventory' in df.columns else 'quantity'

    # 4. Engineer the Storage_Cost_Per_SqFt column based on Product Category
    cost_mapping = {
        'electronics': 0.25, 
        'furniture': 0.85, 
        'apparel': 0.15,
        'heavy machinery': 1.10
    }
    
    # Apply mapping. If the exact category isn't found, default to $0.40
    df['storage_cost_per_sqft'] = df[category_col].astype(str).str.lower().map(cost_mapping).fillna(0.40)

    # 5. Simulate 'Unit_Square_Footage' for each item
    np.random.seed(42) # Keeps random numbers consistent across runs
    df['unit_square_footage'] = np.where(
        df[category_col].astype(str).str.lower().str.contains('furniture'), 
        np.random.uniform(5.0, 15.0, len(df)),
        np.where(
            df[category_col].astype(str).str.lower().str.contains('electronics'), 
            np.random.uniform(0.5, 2.0, len(df)), 
            1.0
        )
    )

    # 6. Simulate 'Months_Stagnant' 
    # (Since we haven't built the advanced SQL window functions yet, we simulate it to test the math)
    df['months_stagnant'] = np.random.randint(0, 12, size=len(df))

    # 7. Calculate the Total_Holding_Cost for the Dead Stock
    df['total_holding_cost'] = (
        df[inventory_col] * 
        df['unit_square_footage'] * 
        df['storage_cost_per_sqft'] * 
        df['months_stagnant']
    )

    # 8. Export the processed data for Power BI / Dashboarding
    df.to_csv(output_path, index=False)
    
    # 9. Review the new financial metrics
    print("\n--- Pipeline Complete. Data Snippet ---")
    print(df[[category_col, inventory_col, 'months_stagnant', 'total_holding_cost']].head())
    print(f"\nProcessed data saved successfully to: {output_path}")

if __name__ == "__main__":
    main()