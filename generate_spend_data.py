import pandas as pd
import numpy as np
from datetime import timedelta, date

def generate_marketing_spend(start_date, end_date):
    # Configuration of Channel Characteristics
    # Search: High Cost, High Intent. Facebook: Medium Cost. Email: Low Cost.
    channel_configs = {
        'Search': {'base_cpc': 2.50, 'cpc_volatility': 0.50, 'ctr': 0.12},
        'Facebook': {'base_cpc': 1.20, 'cpc_volatility': 0.30, 'ctr': 0.02},
        'Display': {'base_cpc': 0.40, 'cpc_volatility': 0.10, 'ctr': 0.005},
        'Email': {'base_cpc': 0.05, 'cpc_volatility': 0.01, 'ctr': 0.05}
    }
    
    dates = pd.date_range(start_date, end_date)
    data = []

    for d in dates:
        # Seasonality Factor: Increase spend in Q4 (Oct-Dec)
        seasonality = 1.5 if d.month in [10, 11, 12] else 1.0
        
        for channel, config in channel_configs.items():
            # 1. Generate Daily Spend using Normal Distribution to simulate variance
            # Mean spend increases with seasonality
            base_daily_spend = 500 * seasonality 
            daily_spend = np.random.normal(base_daily_spend, 50) 
            # Ensure non-negative spend
            daily_spend = max(0, daily_spend)
            
            # 2. Derive Impressions and Clicks from Spend
            # Logic: Spend / CPC = Clicks. Clicks / CTR = Impressions.
            # We add noise to CPC to ensure it's not a flat line
            current_cpc = config['base_cpc'] + np.random.normal(0, config['cpc_volatility'])
            current_cpc = max(0.01, current_cpc) # Prevent negative cost
            
            clicks = int(daily_spend / current_cpc)
            impressions = int(clicks / config['ctr'])
            
            data.append([d, channel, round(daily_spend, 2), impressions, clicks])

    df = pd.DataFrame(data, columns=['date', 'utm_source', 'cost', 'impressions', 'clicks'])
    return df

if __name__ == "__main__":
    print("Generating simulated marketing spend data...")
    # Generate data from Jan 1 2021 to Dec 31 2025
    df_spend = generate_marketing_spend(date(2021, 1, 1), date(2025, 12, 31))
    output_file = 'marketing_spend_simulated.csv'
    df_spend.to_csv(output_file, index=False)
    print(f"Data generation complete. Saved to {output_file}")
