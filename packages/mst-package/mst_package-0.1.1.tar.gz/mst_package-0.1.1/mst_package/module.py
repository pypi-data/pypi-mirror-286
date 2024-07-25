from typing import List, Union
import numpy as np

def transpose2d(input_matrix: List[List[float]]) -> List[List[float]]:
    """
    Transpose a 2D matrix.

    Args:
        input_matrix (List[List[float]]): A 2D list representing the matrix to be transposed.

    Returns:
        List[List[float]]: The transposed 2D list.
    """
    if input_matrix == []:
        return input_matrix
    
    cols = len(input_matrix[0])
    rows = len(input_matrix)
    transpose_list = [[input_matrix[row][col] for row in range(rows)] for col in range(cols)]
    return transpose_list

def window1d(input_array: Union[List, np.ndarray], size: int, shift: int = 1, stride: int = 1) -> List[Union[List, np.ndarray]]:
    """
    Generate a 1D sliding window view of the input array.

    Args:
        input_array (Union[List, np.ndarray]): The input array.
        size (int): The size of each window.
        shift (int, optional): The shift between consecutive windows. Defaults to 1.
        stride (int, optional): The stride within each window. Defaults to 1.

    Returns:
        List[Union[List, np.ndarray]]: A list of windows.
    """
    input_array = list(input_array)
    if input_array == []:
        return input_array

    array_length = len(input_array)
    window_array = []

    for i in range(0, array_length, shift):
        row_array = input_array[i:i + size:stride]
        if len(row_array) == size:
            window_array.append(row_array)

    return window_array

def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Perform a 2D convolution on the input matrix using the given kernel.

    Args:
        input_matrix (np.ndarray): The input matrix.
        kernel (np.ndarray): The convolution kernel.
        stride (int, optional): The stride of the convolution. Defaults to 1.

    Returns:
        np.ndarray: The result of the convolution.
    """
    h, w = kernel.shape
    out_height = (input_matrix.shape[0] - h) // stride + 1
    out_width = (input_matrix.shape[1] - w) // stride + 1
    Y = np.zeros((out_height, out_width))
    for i in range(0, out_height):
        for j in range(0, out_width):
            Y[i, j] = (input_matrix[i*stride:i*stride + h, j*stride:j*stride + w] * kernel).sum()
    
    return Y