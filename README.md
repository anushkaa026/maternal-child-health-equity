# Maternal & Child Health Equity Analysis

**Analyzing the relationship between federal health program funding and community health outcomes**

## Overview

This project examines Maternal and Child Health Bureau (MCHB) grant allocations across the United States, with a particular focus on mental health programs and their correlation with regional health outcomes. Using data from the Health Resources and Services Administration (HRSA) with CDC public health data, I explored funding patterns, equity issues, and potential impacts on maternal and child health metrics.

**Why this matters:** Mental health support during pregnancy and early childhood can significantly impact long-term health outcomes, yet access to these programs varies widely by geography and demographics.

## Key Questions

1. How are mental health-focused grants distributed geographically?
2. What's the relationship between program funding levels and local health outcomes?
3. Can we identify underserved regions that might benefit from increased funding?
4. Do specific program types correlate with better maternal/child health metrics?

## Dataset

- **Source:** HRSA Maternal and Child Health Bureau Grant Data (FY 2021)
- **Records:** ~5,000 grants across all U.S. states and territories
- **Scope:** Multiple program types including Healthy Start, Pediatric Mental Health Care Access, Home Visiting programs, and more
- **External Data:** CDC health outcome metrics (infant mortality, prenatal care access, etc.)

## Technical Approach

### Data Processing
- Cleaned and standardized grant amounts (removed currency formatting)
- Geocoded and aggregated data by state and county
- Merged with CDC health outcome data via API calls
- Handled missing values and outliers

### Analysis Methods
- **Exploratory Data Analysis:** Distribution of funding across states, program types, and grantee classes
- **Statistical Testing:** ANOVA and t-tests to compare health outcomes across funding levels
- **Regression Modeling:** Multiple regression to predict health outcomes from funding and demographic variables
- **Clustering:** K-means to identify states with similar funding patterns
- **Geospatial Analysis:** Choropleth maps showing funding and outcome distributions

### Technologies Used
- **Python 3.11**
- **Data Manipulation:** pandas, numpy
- **Visualization:** matplotlib, seaborn, plotly, folium
- **Statistics:** scipy, statsmodels
- **Machine Learning:** scikit-learn
- **APIs:** CDC WONDER API, requests library

## Project Structure

```
maternal-child-health-equity/
├── data/
│   ├── raw/                    # Original MCHB grant data
│   ├── processed/              # Cleaned and transformed data
│   └── external/               # CDC API data
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_predictive_modeling.ipynb
├── src/
│   ├── data_processing.py      # Data cleaning functions
│   ├── api_fetcher.py          # CDC API interaction
│   └── visualization.py        # Plotting utilities
├── reports/
│   └── figures/                # Generated visualizations
├── requirements.txt
└── README.md
```

## Key Findings

*Will be updated as analysis progresses*

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anushkaa026/maternal-child-health-equity.git
   cd maternal-child-health-equity
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the notebooks:**
   Open Jupyter and run notebooks in order (01 through 05)

## Usage

Each notebook is designed to be run sequentially. The workflow is:

1. **Exploration** - Get familiar with the data structure and distributions
2. **Cleaning** - Handle missing values, standardize formats, validate data
3. **Feature Engineering** - Create meaningful variables for analysis
4. **Statistical Analysis** - Test hypotheses about funding and outcomes
5. **Modeling** - Build predictive models and evaluate performance

## Future Enhancements

- Time-series analysis across multiple fiscal years
- Natural language processing on program descriptions
- Interactive dashboard with Plotly Dash
- Causal inference methods (propensity score matching)
- Integration with social determinants of health data

## Contact

**Anushka Anand**
- GitHub: [@anushkaa026](https://github.com/anushkaa026)
- LinkedIn: [Add your LinkedIn]

## License

This project is available under the MIT License.

## Acknowledgments

- Data provided by HRSA Maternal and Child Health Bureau
- CDC WONDER database for health outcome metrics
- Inspiration from public health equity research
