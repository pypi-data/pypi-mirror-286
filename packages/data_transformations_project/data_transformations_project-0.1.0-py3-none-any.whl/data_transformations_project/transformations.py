import numpy as np
from typing import Union, List


def transpose2d(input_matrix: list[list[float]]) -> list[list[float]]:
    """
    Transpose a 2D matrix (list of lists).

    Parameters:
    input_matrix (list[list[float]]): The input 2D matrix.
    Returns:
    list[list[float]]: The transposed matrix.
    """
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
    """
    input_array = np.asarray(input_array)
    num_windows = (len(input_array) - size) // shift + 1
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
    """
    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1

    output_matrix = np.zeros((output_height, output_width))

    for i in range(output_height):
        for j in range(output_width):
            region = input_matrix[
                i * stride : i * stride + kernel_height,
                j * stride : j * stride + kernel_width,
            ]
            output_matrix[i, j] = np.sum(region * kernel)

    return output_matrix
