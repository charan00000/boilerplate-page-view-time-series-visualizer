import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import numpy as np
register_matplotlib_converters()

np.float = float    
np.int = int   #module 'numpy' has no attribute 'int'
np.object = object    #module 'numpy' has no attribute 'object'
np.bool = bool    #module 'numpy' has no attribute 'bool'

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col=0, parse_dates=True)

# Clean data
df = df[(df['value']>=df['value'].quantile(.025)) & 
        (df['value']<=df['value'].quantile(.975))]


def draw_line_plot():
    fig, ax = plt.subplots(layout='constrained')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.plot(df.index, 'value', data=df)
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Months'] = df_bar.index.month
    df_bar['Years'] = df_bar.index.year
    df_bar = df_bar.groupby(['Years', 'Months'], as_index=False).mean()
    df_bar = df_bar.rename(columns={'value': 'Average Page Views'})
    months={1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 
            6:'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 
            11: 'November', 12: 'December'}
    df_bar['Months'].replace(months, inplace=True)

    # Draw bar plot
    fig = sns.catplot(x='Years', y='Average Page Views', data=df_bar, 
                      hue='Months', kind='bar', 
                      hue_order=['January', 'February', 'March', 'April', 'May',
                                 'June', 'July', 'August', 'September',
                                 'October', 'November', 'December'
    ])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]
    # Draw box plots (using Seaborn)
    df_box.rename(columns={'value': 'Page Views'}, inplace=True)
    fig, (ax1, ax2) = plt.subplots(1,2, layout='constrained', figsize=(10,5))
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    sns.catplot(data=df_box, x='Year', y='Page Views', kind='box', ax=ax1)
    sns.catplot(data=df_box, x='Month', y='Page Views', kind='box', ax=ax2, 
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 
                       'Sep', 'Oct', 'Nov', 'Dec'])
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
