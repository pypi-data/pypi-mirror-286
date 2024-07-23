# splines interpolation

# source code for the original functions
# -->  https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter17.03-Cubic-Spline-Interpolation.html

import numpy as np
from scipy.interpolate import CubicSpline
import plotly.graph_objs as go

##########################################################################################
"""Cubic Spline Interpolation:

Use Case: When smoothness of the interpolated function is crucial and you have enough data points.
Advantages: Provides smooth interpolation, avoids oscillations.
Limitations: More complex than linear or polynomial interpolation, can be computationally intensive."""


####### Compute functions ###################################################
def compute_cubic_spline_multi(x, y, x_new_sets):
    """
    Computes cubic spline interpolation for multiple sets of new x-coordinates.

    Parameters:
    x (array-like): x-coordinates of the data points.
    y (array-like): y-coordinates of the data points.
    x_new_sets (array-like or list of array-like): Multiple sets of new x-coordinates for the spline curves.

    Returns:
    list of np.ndarray: Corresponding y-coordinates for the spline curves.
    """
    if len(x) != len(y):
        raise ValueError("The input arrays x and y must have the same length.")
    if len(x) < 2:
        raise ValueError(
            "At least two data points are required for spline interpolation."
        )

    # Create a cubic spline interpolation
    cs = CubicSpline(x, y, bc_type="natural")

    y_new_sets = []
    for x_new in x_new_sets:
        y_new_sets.append(cs(x_new))

    return y_new_sets


###################    plot functions      ##################################################################


def plot_cubic_spline_multi(x, y, x_new_sets, y_new_sets):
    """
    Plots the original data points and multiple cubic spline interpolations using Plotly.

    Parameters:
    x (array-like): x-coordinates of the original data points.
    y (array-like): y-coordinates of the original data points.
    x_new_sets (list of array-like): Multiple sets of new x-coordinates for the spline curves.
    y_new_sets (list of np.ndarray): Corresponding y-coordinates for the spline curves.
    """
    fig = go.Figure()

    # Add the original data points
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name="Data points",
            marker=dict(color="blue", size=8),
        )
    )

    # Add the spline interpolations
    for i, (x_new, y_new) in enumerate(zip(x_new_sets, y_new_sets)):
        fig.add_trace(
            go.Scatter(
                x=x_new,
                y=y_new,
                mode="lines",
                name=f"Cubic spline interpolation {i + 1}",
                line=dict(width=2),
            )
        )

    # Update the layout
    fig.update_layout(
        title="Cubic Spline Interpolation",
        xaxis_title="x",
        yaxis_title="y",
        legend=dict(x=0, y=1),
        plot_bgcolor="black",
    )

    # Show the plot
    fig.show()


"""
 = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 1, 4, 1, 0, 1])

 # Define multiple sets of new x-coordinates
x_new_sets = [
        np.linspace(0, 5, 100),
    ]

    # Compute the cubic spline interpolation for each set of new x-coordinates
y_new_sets = compute_cubic_spline_multi(x, y, x_new_sets)

    # Plot the results
plot_cubic_spline_multi(x, y, x_new_sets, y_new_sets)

"""
