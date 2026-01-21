"""
Visualization utilities for health equity analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def plot_funding_by_state(df, state_col='State', amount_col='Awardee Amount', 
                          top_n=20, save_path=None):
    """
    Bar chart of funding by state
    
    Args:
        df: DataFrame with grant data
        state_col: Name of state column
        amount_col: Name of amount column
        top_n: Number of top states to show
        save_path: Optional path to save figure
    """
    # Aggregate by state
    state_totals = df.groupby(state_col)[amount_col].sum().sort_values(ascending=False)
    
    # Take top N
    top_states = state_totals.head(top_n)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(range(len(top_states)), top_states.values)
    ax.set_yticks(range(len(top_states)))
    ax.set_yticklabels(top_states.index)
    ax.invert_yaxis()
    
    # Color bars
    colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(top_states)))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax.set_xlabel('Total Funding ($)', fontsize=12, fontweight='bold')
    ax.set_title(f'Top {top_n} States by MCHB Grant Funding', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Format x-axis as currency
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def plot_program_distribution(df, program_col='Program Name', save_path=None):
    """
    Pie chart showing distribution of grants by program type
    
    Args:
        df: DataFrame with grant data
        program_col: Name of program column
        save_path: Optional path to save figure
    """
    program_counts = df[program_col].value_counts()
    
    # Keep top 10, group rest as 'Other'
    top_programs = program_counts.head(10)
    other_count = program_counts[10:].sum()
    
    if other_count > 0:
        top_programs['Other Programs'] = other_count
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    colors = sns.color_palette('Set3', len(top_programs))
    
    wedges, texts, autotexts = ax.pie(top_programs.values, 
                                       labels=top_programs.index,
                                       autopct='%1.1f%%',
                                       colors=colors,
                                       startangle=90)
    
    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Distribution of Grants by Program Type', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def plot_funding_vs_outcome(funding_series, outcome_series, 
                           funding_label='Funding', outcome_label='Outcome',
                           save_path=None):
    """
    Scatter plot with regression line showing funding vs health outcome
    
    Args:
        funding_series: Series with funding amounts
        outcome_series: Series with health metric
        funding_label: Label for x-axis
        outcome_label: Label for y-axis
        save_path: Optional path to save
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Remove NaN values
    valid_mask = ~(funding_series.isna() | outcome_series.isna())
    x = funding_series[valid_mask]
    y = outcome_series[valid_mask]
    
    # Scatter plot
    ax.scatter(x, y, alpha=0.6, s=100)
    
    # Add regression line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), "r", alpha=0.8, label=f'Trend line')
    
    # Calculate correlation
    corr = np.corrcoef(x, y)[0, 1]
    
    ax.set_xlabel(funding_label, fontsize=12, fontweight='bold')
    ax.set_ylabel(outcome_label, fontsize=12, fontweight='bold')
    ax.set_title(f'{outcome_label} vs {funding_label}\n(Correlation: {corr:.3f})', 
                fontsize=14, fontweight='bold')
    
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()
    
    return corr


def create_choropleth_map(state_data, value_col, title, save_path=None):
    """
    Create interactive choropleth map of US states
    
    Args:
        state_data: DataFrame with state-level data
        value_col: Column name to visualize
        title: Map title
        save_path: Optional path to save HTML
    """
    fig = px.choropleth(state_data,
                        locations='state',
                        locationmode='USA-states',
                        color=value_col,
                        scope='usa',
                        title=title,
                        color_continuous_scale='YlOrRd',
                        labels={value_col: value_col.replace('_', ' ').title()})
    
    fig.update_layout(
        title_font_size=16,
        title_x=0.5,
        geo=dict(bgcolor='rgba(0,0,0,0)')
    )
    
    if save_path:
        fig.write_html(save_path)
        print(f"Saved interactive map to {save_path}")
    
    fig.show()
    
    return fig


def plot_correlation_matrix(df, columns, save_path=None):
    """
    Heatmap of correlations between variables
    
    Args:
        df: DataFrame
        columns: List of column names to include
        save_path: Optional path to save
    """
    # Calculate correlation matrix
    corr_matrix = df[columns].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    sns.heatmap(corr_matrix, 
                annot=True, 
                fmt='.2f',
                cmap='coolwarm',
                center=0,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": 0.8},
                ax=ax)
    
    ax.set_title('Correlation Matrix: Funding and Health Outcomes', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def plot_distributions_comparison(df, column, groupby, save_path=None):
    """
    Box plot comparing distributions across groups
    
    Args:
        df: DataFrame
        column: Column to plot distribution of
        groupby: Column to group by
        save_path: Optional path to save
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create box plot
    df.boxplot(column=column, by=groupby, ax=ax)
    
    ax.set_xlabel(groupby.replace('_', ' ').title(), fontsize=12, fontweight='bold')
    ax.set_ylabel(column.replace('_', ' ').title(), fontsize=12, fontweight='bold')
    ax.set_title(f'Distribution of {column.replace("_", " ").title()} by {groupby.replace("_", " ").title()}',
                fontsize=14, fontweight='bold')
    
    plt.suptitle('')  # Remove default title
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def create_summary_dashboard(state_data, save_path=None):
    """
    Create multi-panel summary dashboard
    
    Args:
        state_data: DataFrame with state-level metrics
        save_path: Optional path to save
    """
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Panel 1: Top states by funding
    ax1 = fig.add_subplot(gs[0, 0])
    top_states = state_data.nlargest(15, 'total_funding')
    ax1.barh(range(len(top_states)), top_states['total_funding'].values)
    ax1.set_yticks(range(len(top_states)))
    ax1.set_yticklabels(top_states['state'].values)
    ax1.invert_yaxis()
    ax1.set_title('Top 15 States by Funding', fontweight='bold')
    ax1.set_xlabel('Total Funding ($M)')
    
    # Panel 2: Funding vs infant mortality
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.scatter(state_data['total_funding'], 
               state_data['infant_mortality_rate'],
               alpha=0.6)
    ax2.set_xlabel('Total Funding')
    ax2.set_ylabel('Infant Mortality Rate')
    ax2.set_title('Funding vs Infant Mortality', fontweight='bold')
    
    # Panel 3: Distribution of grant sizes
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.hist(state_data['avg_grant_size'], bins=30, edgecolor='black')
    ax3.set_xlabel('Average Grant Size')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Distribution of Avg Grant Sizes', fontweight='bold')
    
    # Panel 4: Number of grants vs outcomes
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.scatter(state_data['num_grants'],
               state_data['prenatal_care_pct'],
               alpha=0.6)
    ax4.set_xlabel('Number of Grants')
    ax4.set_ylabel('Prenatal Care %')
    ax4.set_title('Grant Count vs Prenatal Care Access', fontweight='bold')
    
    # Panel 5: Regional comparison
    ax5 = fig.add_subplot(gs[2, :])
    metrics = ['infant_mortality_rate', 'prenatal_care_pct', 'low_birthweight_pct']
    state_data[metrics].boxplot(ax=ax5)
    ax5.set_title('Health Outcome Distributions', fontweight='bold')
    ax5.set_ylabel('Value')
    
    fig.suptitle('Maternal & Child Health Equity Dashboard', 
                fontsize=16, fontweight='bold', y=0.995)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved dashboard to {save_path}")
    
    plt.show()
