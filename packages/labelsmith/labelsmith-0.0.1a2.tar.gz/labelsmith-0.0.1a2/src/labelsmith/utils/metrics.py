# labelsmith/src/labelsmith/utils/metrics.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpld3
from mpld3 import plugins
import numpy as np
from typing import Dict, List, Union, Tuple, Optional
from pathlib import Path
import json
import appdirs
import os
import tempfile
import webbrowser

class ShyftMetrics:
    def __init__(self, data_file: Union[str, Path]):
        self.data_file = Path(data_file)
        self.df = self._load_data()
        self.app_name = "Labelsmith"
        self.app_author = "kosmolebryce"

    def _load_data(self) -> pd.DataFrame:
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(data['data'], orient='index')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Duration (hrs)'] = df['Duration (hrs)'].astype(float)
        df['Hourly rate'] = df['Hourly rate'].astype(float)
        df['Gross pay'] = df['Gross pay'].astype(float)
        df['Tasks completed'] = df['Tasks completed'].fillna(0).astype(int)
        return df.sort_values('Date')

    def get_data_dir(self) -> Path:
        data_dir = Path(appdirs.user_data_dir(self.app_name, self.app_author))
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    def productivity_earnings_trend(self, window: int = 7) -> pd.DataFrame:
        trend = self.df.groupby('Date').agg({
            'Tasks completed': 'sum',
            'Gross pay': 'sum'
        }).reset_index()
        trend = trend.sort_values('Date')
        trend['Rolling Tasks'] = trend['Tasks completed'].rolling(window=window, min_periods=1).mean()
        trend['Rolling Earnings'] = trend['Gross pay'].rolling(window=window, min_periods=1).mean()
        return trend

    def plot_interactive_trend(self, save_path: Optional[Union[str, Path]] = None, 
                           window: int = 7, 
                           start_date: Optional[str] = None, 
                           end_date: Optional[str] = None,
                           figsize: Tuple[int, int] = (700, 400),
                           auto_open: bool = True):
        trend = self.productivity_earnings_trend(window)
        
        if start_date:
            trend = trend[trend['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            trend = trend[trend['Date'] <= pd.to_datetime(end_date)]

        fig, ax = plt.subplots(figsize=(figsize[0]/100, figsize[1]/100))
        
        scatter = ax.scatter(trend['Date'], trend['Tasks completed'], 
                            c=trend['Gross pay'], cmap='viridis', 
                            s=50, alpha=0.7)
        
        line, = ax.plot(trend['Date'], trend['Rolling Tasks'], alpha=0.7, color='red', linewidth=2)

        ax.set_title(f'{window}-Day Rolling Average: Tasks and Earnings', fontsize=14, pad=20)
        ax.set_xlabel('Date', fontsize=12, labelpad=10)
        ax.set_ylabel('Tasks Completed', fontsize=12, labelpad=10)
        
        cbar = plt.colorbar(scatter, label='Daily Gross Pay')
        cbar.ax.tick_params(labelsize=10)
        cbar.ax.set_ylabel('Daily Gross Pay', fontsize=12, labelpad=10)

        # Improve x-axis labeling
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)

        # Adjust y-axis to fit all data points and use integer ticks
        max_tasks = trend['Tasks completed'].max()
        ax.set_ylim(0, max_tasks * 1.1)
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.setp(ax.get_yticklabels(), fontsize=10)

        # Set very subtle grid lines
        ax.grid(True, linestyle='--', color='#E0E0E0', alpha=0.1)
        
        # Add legend with slight transparency for better visibility
        legend = ax.legend([line, scatter], ['Rolling Average', 'Daily Tasks'], 
                        loc='upper left', fontsize=10, framealpha=0.9)
        legend.get_frame().set_facecolor('#F8F8F8')  # Light background for better contrast

        plt.tight_layout(pad=2.0)

        tooltip = plugins.PointHTMLTooltip(
            scatter,
            labels=[f"Date: {d:%Y-%m-%d}<br>Daily Tasks: {int(t)}<br>Rolling Avg: {r:.1f}<br>Earnings: ${e:.2f}" 
                    for d, t, r, e in zip(trend['Date'], trend['Tasks completed'], trend['Rolling Tasks'], trend['Gross pay'])],
            voffset=10,
            hoffset=10
        )
        plugins.connect(fig, tooltip)

        if not save_path:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
                save_path = tmp.name

        if isinstance(save_path, str):
            save_path = self.get_data_dir() / save_path

        html = mpld3.fig_to_html(fig)
        
        # Modify the HTML to set a fixed size
        html = html.replace('<div id="', f'<div style="width: {figsize[0]}px; height: {figsize[1]}px;" id="')
        
        with open(save_path, 'w') as f:
            f.write(html)
        
        print(f"Interactive plot saved to: {save_path}")
        
        if auto_open:
            webbrowser.open('file://' + os.path.realpath(save_path))

        plt.close(fig)  # Close the figure to free up memory
        
        return save_path

        if not save_path:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
                save_path = tmp.name

        if isinstance(save_path, str):
            save_path = self.get_data_dir() / save_path

        html = mpld3.fig_to_html(fig)
        
        # Modify the HTML to set a fixed size
        html = html.replace('<div id="', f'<div style="width: {figsize[0]}px; height: {figsize[1]}px;" id="')
        
        with open(save_path, 'w') as f:
            f.write(html)
        
        print(f"Interactive plot saved to: {save_path}")
        
        if auto_open:
            webbrowser.open('file://' + os.path.realpath(save_path))

        plt.close(fig)  # Close the figure to free up memory
        
        return save_path
        
    def calculate_efficiency_metrics(self) -> Dict[str, float]:
        daily_metrics = self.df.groupby('Date').agg({
            'Tasks completed': 'sum',
            'Duration (hrs)': 'sum',
            'Gross pay': 'sum'
        })
        
        daily_metrics['Tasks per Hour'] = daily_metrics['Tasks completed'] / daily_metrics['Duration (hrs)']
        daily_metrics['Earnings per Hour'] = daily_metrics['Gross pay'] / daily_metrics['Duration (hrs)']
        
        return {
            'Avg Tasks per Hour': daily_metrics['Tasks per Hour'].mean(),
            'Avg Earnings per Hour': daily_metrics['Earnings per Hour'].mean(),
            'Best Day (Tasks)': daily_metrics['Tasks completed'].max(),
            'Best Day (Earnings)': daily_metrics['Gross pay'].max()
        }

    def generate_report(self) -> Dict[str, Union[float, int]]:
        efficiency_metrics = self.calculate_efficiency_metrics()
        return {
            'Total Hours Worked': self.total_hours_worked(),
            'Total Tasks Completed': self.total_tasks_completed(),
            'Total Gross Pay': self.total_gross_pay(),
            'Average Hourly Rate': self.average_hourly_rate(),
            'Overall Tasks Per Hour': self.tasks_per_hour(),
            'Overall Earnings Per Task': self.earnings_per_task(),
            'Average Daily Tasks per Hour': efficiency_metrics['Avg Tasks per Hour'],
            'Average Daily Earnings per Hour': efficiency_metrics['Avg Earnings per Hour'],
            'Best Day (Tasks)': efficiency_metrics['Best Day (Tasks)'],
            'Best Day (Earnings)': efficiency_metrics['Best Day (Earnings)']
        }