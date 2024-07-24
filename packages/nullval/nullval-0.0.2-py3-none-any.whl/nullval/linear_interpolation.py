import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import plotly.graph_objs as go
from plotly.subplots import make_subplots

"""
Linear Interpolation:

Use Case: When the data changes smoothly between points and a simple approximation is sufficient.
Advantages: Fast computation, simple to implement.
Limitations: May not capture complex non-linear relationships.

"""


def li_int(x_points, y_points, x_new):
    """
    Perform linear interpolation on a set of data points.

    Parameters:
    x_points (array-like): Known x-values of the data points.
    y_points (array-like): Known y-values of the data points.
    x_new (array-like): New x-values at which to interpolate the y-values.

    Returns:
    array-like: Interpolated y-values at x_new points.
    """
    # Input validation
    if len(x_points) != len(y_points):
        raise ValueError("x_points and y_points must have the same length")
    if not (np.all(np.diff(x_points) > 0) or np.all(np.diff(x_points) < 0)):
        raise ValueError(
            "x_points must be strictly monotonic (either increasing or decreasing)"
        )

    # Perform linear interpolation
    interpolator = interp1d(x_points, y_points, kind="linear")
    y_new = interpolator(x_new)

    return y_new


def plot_li_int(x_points, y_points, x_new, y_new):
    """
    Plot the original data points and the interpolated values using Plotly.

    Parameters:
    x_points (array-like): Known x-values of the data points.
    y_points (array-like): Known y-values of the data points.
    x_new (array-like): New x-values at which y-values were interpolated.
    y_new (array-like): Interpolated y-values at x_new points.
    """
    fig = make_subplots(rows=1, cols=1)

    # Scatter plot of original data points
    fig.add_trace(
        go.Scatter(
            x=x_points,
            y=y_points,
            mode="markers",
            name="Data Points",
            marker=dict(color="black"),
        ),
        row=1,
        col=1,
    )

    # Line plot of interpolated values
    fig.add_trace(
        go.Scatter(
            x=x_new,
            y=y_new,
            mode="lines",
            name="Linear Interpolation",
            line=dict(color="red", dash="dash"),
        ),
        row=1,
        col=1,
    )

    # Update layout
    fig.update_layout(
        title="Linear Interpolation",
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
        legend=dict(x=0.7, y=1.1),
        template="plotly_white",
    )

    # Show plot
    fig.show()
