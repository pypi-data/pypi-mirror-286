# mst_package

A package containing utility functions for matrix operations including transpose, 1D windowing, and 2D convolution.

## Installation

You can install the package using pip:

```bash
pip install mst_package
```

## Usage

### Importing the Functions

```python
from mst_package import transpose2d, window1d, convolution2d
```

### Functions

#### 1. `transpose2d`

Transpose a 2D matrix.

**Arguments:**

- `input_matrix` (List[List[float]]): A 2D list representing the matrix to be transposed.

**Returns:**

- `List[List[float]]`: The transposed 2D list.

**Example:**

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

transposed_matrix = transpose2d(matrix)
print(transposed_matrix)
# Output: [[1, 4], [2, 5], [3, 6]]
```

#### 2. `window1d`

Generate a 1D sliding window view of the input array.

**Arguments:**

- `input_array` (Union[List, np.ndarray]): The input array.
- `size` (int): The size of each window.
- `shift` (int, optional): The shift between consecutive windows. Defaults to 1.
- `stride` (int, optional): The stride within each window. Defaults to 1.

**Returns:**

- `List[Union[List, np.ndarray]]`: A list of windows.

**Example:**

```python
array = [1, 2, 3, 4, 5]
windows = window1d(array, size=3, shift=1)
print(windows)
# Output: [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
```

#### 3. `convolution2d`

Perform a 2D convolution on the input matrix using the given kernel.

**Arguments:**

- `input_matrix` (np.ndarray): The input matrix.
- `kernel` (np.ndarray): The convolution kernel.
- `stride` (int, optional): The stride of the convolution. Defaults to 1.

**Returns:**

- `np.ndarray`: The result of the convolution.

**Example:**

```python
import numpy as np

input_matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

kernel = np.array([
    [1, 0],
    [0, -1]
])

convolution_result = convolution2d(input_matrix, kernel)
print(convolution_result)
# Output: [[ -4.  -4.]
#          [-4. -4.]]
```
