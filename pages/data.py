import flet as ft  # type: ignore
import numpy as np
import pandas as pd # type: ignore
import matplotlib # type: ignore
import matplotlib.pyplot as plt # type: ignore
from flet.matplotlib_chart import MatplotlibChart # type: ignore
import warnings
from components import navbar, appbar

warnings.filterwarnings("ignore", category=DeprecationWarning)

matplotlib.use("svg")

def DataScreen(page):
    data = page.dataframe
    intervalos = getattr(page, 'current_intervals', 10)
    page.current_intervals = intervalos
    
    # Create initial figure
    def create_histogram(num_bins):
        fig, ax = plt.subplots()
        ax.hist(data, bins=num_bins)
        return fig
    
    # Calculate descriptive statistics
    def calculate_stats(data_array):
        stats = {
            "Mean": np.mean(data_array),
            "Median": np.median(data_array),
            "Std Dev": np.std(data_array),
            "Min": np.min(data_array),
            "Max": np.max(data_array),
            "Q1 (25%)": np.percentile(data_array, 25),
            "Q3 (75%)": np.percentile(data_array, 75),
            "Count": len(data_array)
        }
        return stats
    
    # Format stats into a string for display
    def format_stats(stats_dict):
        result = ""
        for key, value in stats_dict.items():
            # Format numbers to 4 decimal places
            if isinstance(value, (int, float)):
                value = f"{value:.4f}"
            result += f"{key}: {value}\n"
        return result
    
    fig = create_histogram(intervalos)
    chart = MatplotlibChart(fig, expand=True)
    
    # Initial stats calculation
    initial_stats = calculate_stats(data)
    stats_text = ft.Text(
        value=format_stats(initial_stats),
        size=14,
        selectable=True
    )
    
    # Text field for intervals
    intervals_input = ft.TextField(
        label="Numero de intervalos", 
        value=str(intervalos),
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    # Function to update the chart
    def update_chart(e):
        try:
            new_intervals = int(intervals_input.value)
            if new_intervals < 1:
                new_intervals = 1
                
            # Guardar el valor actualizado
            page.current_intervals = new_intervals
            
            new_fig = create_histogram(new_intervals)
            chart.figure = new_fig
            # Update stats
            current_stats = calculate_stats(data)
            stats_text.value = format_stats(current_stats)
            page.update()
        except ValueError:
            # Handle invalid input
            pass
    
    apply_button = ft.ElevatedButton("Aplicar", on_click=update_chart)
    
    return ft.View(
        "/data",
        [
            appbar.appBar(page, "Data"),
            ft.Row(
                [
                    ft.Column(
                        [
                            intervals_input,
                            apply_button,
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Estadísticas descriptivas:", weight=ft.FontWeight.BOLD),
                                    stats_text
                                ]),
                                margin=ft.margin.only(top=20),
                                padding=10,
                                border=ft.border.all(1, ft.colors.GREY_400),
                                border_radius=5
                            )
                        ],
                        expand=1
                    ),
                    ft.Column(
                        [
                            chart
                        ],
                        expand=2
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            ),
            navbar.NavigationBar(page)
        ]
    )