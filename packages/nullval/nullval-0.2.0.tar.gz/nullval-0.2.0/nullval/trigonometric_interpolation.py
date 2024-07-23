import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import sys
import math
import matplotlib.pyplot as plt
"""
def trigonometric_interpolation(x, y, x_new):
    """
    Performs trigonometric interpolation for the given data points.

    Parameters:
    x (array-like): x-coordinates of the data points.
    y (array-like): y-coordinates of the data points.
    x_new (array-like): New x-coordinates for which to compute interpolated y values.

    Returns:
    np.ndarray: Interpolated y-values corresponding to x_new.
    """
    N = len(x)
    if N % 2 == 0:
        k = np.arange(-N//2, N//2)  # Use a symmetric range of k values for even N
    else:
        k = np.arange(-(N-1)//2, (N+1)//2)  # Use a symmetric range of k values for odd N 
    
    Y_k = np.fft.fftshift(np.fft.fft(y)) / N
    y_new = np.zeros_like(x_new, dtype=np.complex128)

    for i, k_val in enumerate(k):
        y_new += Y_k[i] * np.exp(2j * np.pi * k_val * x_new / (x[-1] - x[0])) # Scale x_new by the range of original x

    return y_new.real




def plot_trigonometric_interpolation(x_points, y_points, x_new, y_new):
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
        go.Scatter(x=x_points, y=y_points, mode='markers', name='Data Points', marker=dict(color='black')),
        row=1, col=1
    )

    # Line plot of interpolated values
    fig.add_trace(
        go.Scatter(x=x_new, y=y_new, mode='lines', name='Trigonometric Interpolation', line=dict(color='red')),
        row=1, col=1
    )

    # Update layout
    fig.update_layout(
        title='Trigonometric Interpolation',
        xaxis_title='x',
        yaxis_title='y',
        showlegend=True,
        legend=dict(x=0.7, y=1.1),
        template='plotly_white'
    )

    # Show plot
    fig.show()




'''
# Example usage:
x_points = np.linspace(0, 2 * np.pi, 10)
y_points = np.sin(x_points)

# Generate new x values for plotting
x_new = np.linspace(min(x_points), max(x_points), 1000)
# Compute interpolated y values
y_new = trigonometric_interpolation(x_points, y_points, x_new)

# Plot using plot_trigonometric_interpolation function
plot_trigonometric_interpolation(x_points, y_points, x_new, y_new)


def trigonometric_interpolation(x, y, x_new):
    """
    Performs trigonometric interpolation for the given data points.

    Parameters:
    x (array-like): x-coordinates of the data points.
    y (array-like): y-coordinates of the data points.
    x_new (array-like): New x-coordinates for which to compute interpolated y values.

    Returns:
    np.ndarray: Interpolated y-values corresponding to x_new.
    """
    N = len(x)
    if N % 2 == 0:
        k = np.arange(-N//2, N//2)
    else:
        k = np.arange(-(N-1)//2, (N+1)//2)
    
    Y_k = np.fft.fftshift(np.fft.fft(y)) / N
    y_new = np.zeros_like(x_new, dtype=np.complex128)

    for i, k_val in enumerate(k):
        y_new += Y_k[i] * np.exp(2j * np.pi * k_val * x_new / N)
    
    return y_new.real
'''





def e_complex_pow(power):
    return complex(np.cos(power), np.sin(power))

def get_complex_representation(points):
    N = len(points)
    xs = np.array([(2*np.pi * i) / N for i in range(N)])
    ys = np.array(points, dtype=np.complex_)

    w = e_complex_pow(2*np.pi / N)
    
    # Fourier-Matrix
    F_N = np.array([ [w ** (j * k) for j in range(N)] for k in range(-(N-1)//2, (N-1)//2 + 1) ])

    Ck_s = (1 / N) * (np.conj(F_N) @ ys)  # Fourier-Coefficients    
    return Ck_s


def get_sin_cos_representation(points):
    Ck_s = get_complex_representation(points)
    Ck_zero_idx = (len(Ck_s)-1) // 2
    
    Ak_s = [2 * Ck_s[Ck_zero_idx]] + [Ck_s[Ck_zero_idx + n] + Ck_s[Ck_zero_idx - n] for n in range(1, Ck_zero_idx+1)]  # cosine coefficients
    Bk_s = [0] + [complex(0, Ck_s[Ck_zero_idx + n] - Ck_s[Ck_zero_idx - n]) for n in range(1, Ck_zero_idx+1)]  # sine coefficients

    for n in range(len(Ak_s)):
        if Ak_s[n].imag < 1e-3:
            Ak_s[n] = Ak_s[n].real
        
        if Bk_s[n].imag < 1e-3:
            Bk_s[n] = Bk_s[n].real

    return np.array(Ak_s), np.array(Bk_s)


def eval_sin_cos_representation(t, A, B):
    return A[0]/2 + sum(A[n] * np.cos(n * t) + B[n] * np.sin(n * t) for n in range(1, len(A)))


def plot_sin_cos_representation(A, B, y_points, start=-10, end=10):
    Xs = np.linspace(start, end, 5000)
    Ys = [eval_sin_cos_representation(t, A, B) for t in Xs]

    N = len(points)
    x_points = np.array([(2*np.pi * i) / N for i in range(N)])

    plt.figure(figsize=(14,7))
    plt.plot(Xs, Ys)
    plt.scatter(x_points, y_points, c='black')
    plt.show()

'''
if __name__ == '__main__':
    points = list(map(float, float(sys.argv[1:])))
    A, B = get_sin_cos_representation(points)

    plot_sin_cos_representation(A, B, points, start=-4*np.pi, end=4*np.pi)

'''
"""