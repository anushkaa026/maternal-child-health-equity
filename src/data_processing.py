"""
Data cleaning and processing utilities
"""

import pandas as pd
import numpy as np
import re


def clean_currency(amount_str):
    """
    Convert currency strings like '$1,234,567' to float
    
    Args:
        amount_str: String with dollar sign and commas
        
    Returns:
        float or np.nan if invalid
    """
    if pd.isna(amount_str):
        return np.nan
    
    # Remove dollar signs, commas, and spaces
    cleaned = str(amount_str).replace('$', '').replace(',', '').strip()
    
    try:
        return float(cleaned)
    except ValueError:
        return np.nan


def load_grant_data(filepath):
    """
    Load and do initial cleaning of MCHB grant data
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with cleaned data
    """
    df = pd.read_csv(filepath, encoding='utf-8-sig')  # Handle BOM if present
    
    # Clean column names - remove extra spaces
    df.columns = df.columns.str.strip()
    
    # Convert award amounts to numeric
    if 'Awardee Amount' in df.columns:
        df['Awardee Amount'] = df['Awardee Amount'].apply(clean_currency)
    
    return df


def categorize_program(program_name):
    """
    Categorize programs into broader groups for analysis
    
    Args:
        program_name: String name of the program
        
    Returns:
        String category name
    """
    if pd.isna(program_name):
        return 'Unknown'
    
    program_lower = program_name.lower()
    
    # Mental health programs
    if 'mental health' in program_lower or 'pediatric mental' in program_lower:
        return 'Mental Health'
    
    # Maternal health
    elif 'maternal' in program_lower or 'healthy start' in program_lower:
        return 'Maternal Health'
    
    # Home visiting
    elif 'home' in program_lower and 'visit' in program_lower:
        return 'Home Visiting'
    
    # Children with special needs
    elif 'cshcn' in program_lower or 'special' in program_lower:
        return 'Special Healthcare Needs'
    
    # Training and education
    elif 'training' in program_lower or 'leadership' in program_lower or 'education' in program_lower:
        return 'Training & Education'
    
    # Emergency services
    elif 'emsc' in program_lower or 'emergency' in program_lower:
        return 'Emergency Services'
    
    # Screening programs
    elif 'screening' in program_lower or 'newborn' in program_lower:
        return 'Screening Programs'
    
    else:
        return 'Other'


def get_state_summary(df, state_col='State', amount_col='Awardee Amount'):
    """
    Get summary statistics by state
    
    Args:
        df: DataFrame with grant data
        state_col: Name of state column
        amount_col: Name of amount column
        
    Returns:
        DataFrame with state-level summaries
    """
    summary = df.groupby(state_col).agg({
        amount_col: ['sum', 'mean', 'count'],
        'Grant Number': 'count'
    }).reset_index()
    
    # Flatten column names
    summary.columns = [state_col, 'total_funding', 'avg_grant_size', 
                       'num_grants', 'grant_count_check']
    
    # Drop duplicate count column
    summary = summary.drop('grant_count_check', axis=1)
    
    return summary.sort_values('total_funding', ascending=False)


def identify_outliers(series, method='iqr', threshold=1.5):
    """
    Identify outliers in a numeric series
    
    Args:
        series: Pandas Series
        method: 'iqr' or 'zscore'
        threshold: IQR multiplier or z-score cutoff
        
    Returns:
        Boolean mask of outliers
    """
    if method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        return (series < lower_bound) | (series > upper_bound)
    
    elif method == 'zscore':
        z_scores = np.abs((series - series.mean()) / series.std())
        return z_scores > threshold
    
    else:
        raise ValueError("Method must be 'iqr' or 'zscore'")


def validate_data_quality(df):
    """
    Print data quality report
    
    Args:
        df: DataFrame to validate
    """
    print("=" * 50)
    print("DATA QUALITY REPORT")
    print("=" * 50)
    
    print(f"\nTotal records: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")
    
    print("\n--- Missing Values ---")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Missing': missing,
        'Percent': missing_pct
    })
    print(missing_df[missing_df['Missing'] > 0].sort_values('Missing', ascending=False))
    
    print("\n--- Duplicates ---")
    duplicates = df.duplicated().sum()
    print(f"Duplicate rows: {duplicates}")
    
    if 'Awardee Amount' in df.columns:
        print("\n--- Grant Amounts ---")
        print(f"Min: ${df['Awardee Amount'].min():,.2f}")
        print(f"Max: ${df['Awardee Amount'].max():,.2f}")
        print(f"Mean: ${df['Awardee Amount'].mean():,.2f}")
        print(f"Median: ${df['Awardee Amount'].median():,.2f}")
    
    print("\n" + "=" * 50)
