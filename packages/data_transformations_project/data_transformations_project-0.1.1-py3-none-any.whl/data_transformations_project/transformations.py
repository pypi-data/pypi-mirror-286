import numpy as np
from typing import Union, List


def transpose2d(input_matrix: list[list[float]]) -> list[list[float]]:
    """
    Transpose a 2D matrix (list of lists).

    Parameters:
    input_matrix (list[list[float]]): The input 2D matrix.

    Returns:
    list[list[float]]: The transposed matrix.

    Raises:
    ValueError: If the input is not a 2D list or if rows have different lengths.
    """
    if not all(isinstance(row, list) for row in input_matrix):
        raise ValueError("Input must be a 2D list.")

    row_length = len(input_matrix[0])
    if not all(len(row) == row_length for row in input_matrix):
        raise ValueError("All rows in the input matrix must have the same length.")

    return [list(row) for row in zip(*input_matrix)]


def window1d(
    input_array: Union[list, np.ndarray], size: int, shift: int = 1, stride: int = 1
) -> List[np.ndarray]:
    """
    Generate time series windows from a 1D array.

    Parameters:
    input_array (Union[list, np.ndarray]): The input 1D array.
    size (int): The size of each window.
    shift (int): The shift between consecutive windows.
    stride (int): The stride within each window.

    Returns:
    List[np.ndarray]: A list of 1D windows.

    Raises:
    ValueError: If input_array is not a list or numpy array, or if size, shift, or stride are invalid.
    """
    if not isinstance(input_array, (list, np.ndarray)):
        raise ValueError("Input array must be a list or numpy array.")

    if size <= 0 or shift <= 0 or stride <= 0:
        raise ValueError("Size, shift, and stride must be positive integers.")

    input_array = np.asarray(input_array)
    num_windows = (len(input_array) - size) // shift + 1

    if num_windows <= 0:
        raise ValueError("Window size and shift are too large for the input array.")

    windows = [
        input_array[i * shift : i * shift + size : stride] for i in range(num_windows)
    ]
    return windows


def convolution2d(
    input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1
) -> np.ndarray:
    """
    Perform a 2D cross-correlation operation on an input matrix with a given kernel.

    Parameters:
    input_matrix (np.ndarray): 2D Numpy array of real numbers representing the input matrix.
    kernel (np.ndarray): 2D Numpy array of real numbers representing the kernel.
    stride (int): The stride (step size) between applications of the kernel. Default is 1.

    Returns:
    np.ndarray: The result of the 2D cross-correlation operation as a 2D Numpy array of real numbers.

    Raises:
    ValueError: If input_matrix or kernel are not 2D numpy arrays, or if stride is invalid.
    """
    if not (isinstance(input_matrix, np.ndarray) and input_matrix.ndim == 2):
        raise ValueError("Input matrix must be a 2D numpy array.")

    if not (isinstance(kernel, np.ndarray) and kernel.ndim == 2):
        raise ValueError("Kernel must be a 2D numpy array.")

    if stride <= 0:
        raise ValueError("Stride must be a positive integer.")

    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1

    if output_height <= 0 or output_width <= 0:
        raise ValueError("Kernel size and stride are too large for the input matrix.")

    output_matrix = np.zeros((output_height, output_width))

    for i in range(output_height):
        for j in range(output_width):
            region = input_matrix[
                i * stride : i * stride + kernel_height,
                j * stride : j * stride + kernel_width,
            ]
            output_matrix[i, j] = np.sum(region * kernel)

    return output_matrix
