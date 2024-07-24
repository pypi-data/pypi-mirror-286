import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

"""Polynomial Interpolation (e.g., Lagrange, Newton):

Use Case: When higher accuracy is needed and the underlying function is well approximated by a polynomial over the interpolation range.
Advantages: Can provide high accuracy with sufficient data points.
Limitations: Can be sensitive to outliers and can oscillate between points (Runge's phenomenon).
"""

###### find the ideal degree depending on the value of the polynomial ??????????????????################

### plot the value of the data and find the best degree based on the dataset


def polynomial_interpolation(x, y, degree, x_new):
    """
    Performs polynomial interpolation of given degree for the given data points and x_new,
    and calculates the error rate.

    Parameters:
    x (array-like): x-coordinates of the data points.
    y (array-like): y-coordinates of the data points.
    degree (int): Degree of the polynomial to fit.
    x_new (array-like): New x-coordinates for which to compute interpolated y values.

    Returns:
    tuple: Interpolated y-values corresponding to x_new, Mean Squared Error (MSE).
    """
    # Fit polynomial to data
    coefficients = np.polyfit(x, y, degree)
    polynomial = np.poly1d(coefficients)

    # Compute interpolated y-values for new x-coordinates
    y_new = polynomial(x_new)

    # Calculate mean squared error (MSE)
    y_pred = polynomial(x)
    mse = np.mean((y - y_pred) ** 2)

    return y_new


"""
coefficients = np.polyfit(x, y, degree)
    polynomial = np.poly1d(coefficients)
    y_new = polynomial(x_new)
"""

########################## plot the polynomial ################################################


def plot_polynomial_interpolation(x, y, degree, x_new):
    """
    Performs polynomial interpolation, computes interpolated y values, and plots the results using Plotly.

    Parameters:
    x (array-like): x-coordinates of the data points.
    y (array-like): y-coordinates of the data points.
    degree (int): Degree of the polynomial to fit.
    x_new (array-like): New x-coordinates for which to compute interpolated y values.
    """
    # Perform polynomial interpolation and compute y values
    y_new = polynomial_interpolation(x, y, degree, x_new)

    # Plotting using Plotly
    fig = make_subplots(rows=1, cols=1)

    # Scatter plot of original data points
    fig.add_trace(
        go.Scatter(x=x, y=y, mode="markers", name="Data Points"), row=1, col=1
    )

    # Line plot of interpolated data
    fig.add_trace(
        go.Scatter(
            x=x_new,
            y=y_new,
            mode="lines",
            name=f"Polynomial Interpolation (Degree {degree})",
        ),
        row=1,
        col=1,
    )

    # Update layout
    fig.update_layout(
        title=f"Polynomial Interpolation (Degree {degree})",
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
        legend=dict(x=0.7, y=1.1),
        template="plotly_white",
    )

    # Show plot
    fig.show()


"""
# Example usage:
x = np.array([1.0, 2.0, 3.0, 4.0])
y = np.array([1.0, 4.0, 9.0, 16.0])
degree = 2  # Degree of the polynomial to fit
x_new = np.linspace(min(x), max(x), 100)  # New x-values for interpolation

# Plot polynomial interpolation and compute interpolated y values
plot_polynomial_interpolation(x, y, degree, x_new)


"""
