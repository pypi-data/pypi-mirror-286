import numpy as np
import plotly.graph_objs as go
import plotly.io as pio


def lagrange_interpolation(x_points, y_points, x_new):
    """
    Perform Lagrange interpolation on a set of data points.

    Parameters:
    x_points (array-like): Known x-values of the data points.
    y_points (array-like): Known y-values of the data points.
    x_new (array-like): New x-values at which to interpolate the y-values.

    Returns:
    array-like: Interpolated y-values at x_new points.
    """
    if len(x_points) != len(y_points):
        raise ValueError("x_points and y_points must have the same length")

    def lagrange_basis(j, x_point):
        basis = [
            (x_point - x_points[m]) / (x_points[j] - x_points[m])
            for m in range(len(x_points))
            if m != j
        ]
        return np.prod(basis)

    y_new = np.array(
        [
            sum(y_points[j] * lagrange_basis(j, xi) for j in range(len(x_points)))
            for xi in x_new
        ]
    )
    return y_new


def plot_lagrange_interpolation(x_points, y_points, x_new, y_new):
    """
    Plot the Lagrange interpolation results using Plotly.

    Parameters:
    x_points (array-like): Known x-values of the data points.
    y_points (array-like): Known y-values of the data points.
    x_new (array-like): New x-values at which the y-values were interpolated.
    y_new (array-like): Interpolated y-values at x_new points.
    """
    data_points = go.Scatter(x=x_points, y=y_points, mode="markers", name="Data points")
    lagrange_curve = go.Scatter(
        x=x_new, y=y_new, mode="lines", name="Lagrange interpolation"
    )

    layout = go.Layout(
        title="Lagrange Interpolation", xaxis=dict(title="x"), yaxis=dict(title="y")
    )

    fig = go.Figure(data=[data_points, lagrange_curve], layout=layout)
    pio.show(fig)


"""
 Example usage
x = np.array([0, 1, 2, 3])
y = np.array([1, 2, 0, 3])
x_new = np.linspace(0, 3, 100)
y_new = lagrange_interpolation(x, y, x_new)

# Plot the results
plot_lagrange_interpolation(x, y, x_new, y_new)
"""
