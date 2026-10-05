import pandas as pd
import numpy as np
import os

def main():
    print("Starting data ingestion and transformation pipeline...")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, '..', 'data', 'supply_chain_dataset1.csv')
    output_path = os.path.join(base_dir, '..', 'data', 'processed_inventory_data.csv')

    try:
        df = pd.read_csv(input_path)
        print(f"Successfully loaded {len(df)} rows.")
    except FileNotFoundError:
        print(f"ERROR: Could not find dataset at {input_path}")
        return

    # Defensive cleaning: lowercasing and stripping hidden spaces
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # FIX 1: Convert date object to actual datetime format based on EDA
    df['date'] = pd.to_datetime(df['date'])

    # FIX 2: Synthesize the missing 'category' column based on the 50 unique SKUs
    np.random.seed(42)
    categories = ['electronics', 'furniture', 'apparel', 'heavy machinery']
    unique_skus = df['sku_id'].unique()
    sku_to_category = {sku: np.random.choice(categories) for sku in unique_skus}
    
    df['product_category'] = df['sku_id'].map(sku_to_category)

    # Engineer the Storage_Cost_Per_SqFt column based on our synthetic category
    cost_mapping = {
        'electronics': 0.25, 
        'furniture': 0.85, 
        'apparel': 0.15,
        'heavy machinery': 1.10
    }
    df['storage_cost_per_sqft'] = df['product_category'].map(cost_mapping)

    # Simulate 'Unit_Square_Footage'
    df['unit_square_footage'] = np.where(
        df['product_category'] == 'furniture', 
        np.random.uniform(5.0, 15.0, len(df)),
        np.where(
            df['product_category'] == 'electronics', 
            np.random.uniform(0.5, 2.0, len(df)), 
            1.0
        )
    )

    # Simulate 'Months_Stagnant' 
    df['months_stagnant'] = np.random.randint(0, 12, size=len(df))

    # Calculate Total_Holding_Cost 
    df['total_holding_cost'] = (
        df['inventory_level'] * 
        df['unit_square_footage'] * 
        df['storage_cost_per_sqft'] * 
        df['months_stagnant']
    )

    df.to_csv(output_path, index=False)
    
    print("\n--- Pipeline Complete. Data Snippet ---")
    print(df[['date', 'sku_id', 'product_category', 'total_holding_cost']].head())

if __name__ == "__main__":
    main()