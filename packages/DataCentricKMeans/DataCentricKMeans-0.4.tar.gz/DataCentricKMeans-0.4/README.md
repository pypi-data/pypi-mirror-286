    #Authors:
        - Vasfi Tataroglu (vtatarog@iu.edu)
        - Parichit Sharma (parishar@iu.edu)
        - Hasan Kurban (hasan.kurban@qatar.tamu.edu)
        - Mehmet M. Dalkilic (dalkilic@iu.edu)


# `DataCentricKMeans` Package Documentation

## Installation
First, you can install the package from PyPI:
```bash
pip install DataCentricKMeans
```

## Usage
This package allows you to run various KMeans algorithms using the provided functions. All functions take similar parameters and return similarly structured results.

### `run_geokmeans` Function

**Function Definition:**
```python
def run_geokmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[])
```

**Parameters:**

1. `num_iterations` (int): 
   - Description: Maximum number of iterations for the algorithm.
   - Condition: Must be 1 or greater.

2. `threshold` (float): 
   - Description: Convergence threshold for the algorithm.
   - Condition: Must be 0 or greater.

3. `num_clusters` (int): 
   - Description: The number of clusters.
   - Condition: Must be 2 or greater and less than the number of samples in the data.

4. `seed` (int, optional): 
   - Description: The seed value for the random number generator. If not provided, the default value of 42 is used.
   - Condition: Must be a positive integer.

5. `file_paths` (list of str): 
   - Description: The file paths of the data files to be processed.
   - Condition: The file paths must be valid and the files must exist.

**Example Usage:**

```python
import DataCentricKMeans

results = DataCentricKMeans.run_geokmeans(
    100,
    0.0001,
    12,
    17,
    [
        "./Breastcancer.csv",
        "./CreditRisk.csv",
        "./census.csv",
        "./birch.csv"
    ]
)

# Accessing results
print(results[0].loop_counter)
print(results[0].to_dict())
```

**Outputs:**
The `run_geokmeans` function returns a list of `KMeansResult` objects, one for each data file. Each `KMeansResult` object contains the following information:

- `loop_counter` (int): The number of iterations the algorithm ran.
- `num_dists` (int): The number of distances computed.
- `assignments` (list of int): The cluster assignment for each data point.
- `centroids` (list of list of float): The coordinates of each cluster's centroid.
- `sse` (float): The sum of squared errors (SSE).

**Accessing the Results:**
You can access the results either as class attributes or as dictionary keys:
```python
result = results[0]
print(result.loop_counter)  # Number of iterations
print(result.to_dict())     # All results as a dictionary
```

### `run_lloyd_kmeans` Function

**Function Definition:**
```python
def run_lloyd_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[])
```

The `run_lloyd_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

**Example Usage:**

```python
import DataCentricKMeans

results = DataCentricKMeans.run_lloyd_kmeans(
    100,
    0.0001,
    12,
    17,
    [
        "./Breastcancer.csv",
        "./CreditRisk.csv",
        "./census.csv",
        "./birch.csv"
    ]
)

# Accessing results
print(results[0].loop_counter)
print(results[0].to_dict())
```

### `run_elkan_kmeans` Function

**Function Definition:**
```python
def run_elkan_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[])
```

The `run_elkan_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

**Example Usage:**

```python
import DataCentricKMeans

results = DataCentricKMeans.run_elkan_kmeans(
    100,
    0.0001,
    12,
    17,
    [
        "./Breastcancer.csv",
        "./CreditRisk.csv",
        "./census.csv",
        "./birch.csv"
    ]
)

# Accessing results
print(results[0].loop_counter)
print(results[0].to_dict())
```

### `run_hamerly_kmeans` Function

**Function Definition:**
```python
def run_hamerly_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[])
```

The `run_hamerly_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

**Example Usage:**

```python
import DataCentricKMeans

results = DataCentricKMeans.run_hamerly_kmeans(
    100,
    0.0001,
    12,
    17,
    [
        "./Breastcancer.csv",
        "./CreditRisk.csv",
        "./census.csv",
        "./birch.csv"
    ]
)

# Accessing results
print(results[0].loop_counter)
print(results[0].to_dict())
```

### `run_annulus_kmeans` Function

**Function Definition:**
```python
def run_annulus_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[])
```

The `run_annulus_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

**Example Usage:**

```python
import DataCentricKMeans

results = DataCentricKMeans.run_annulus_kmeans(
    100,
    0.0001,
    12,
    17,
    [
        "./Breastcancer.csv",
        "./CreditRisk.csv",
        "./census.csv",
        "./birch.csv"
    ]
)

# Accessing results
print(results[0].loop_counter)
print(results[0].to_dict())
```

### `run_exponion_kmeans` Function

**Function Definition:**
```python
def run_exponion_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[])
```

The `run_exponion_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

**Example Usage:**

```python
import DataCentricKMeans

results = DataCentricKMeans.run_exponion_kmeans(
    100,
    0.0001,
    12,
    17,
    [
        "./Breastcancer.csv",
        "./CreditRisk.csv",
        "./census.csv",
        "./birch.csv"
    ]
)

# Accessing results
print(results[0].loop_counter)
print(results[0].to_dict())
```

### Detailed Output Description
Each `KMeansResult` object contains the following attributes:

- **`loop_counter`**: Indicates the number of iterations the algorithm ran.
- **`num_dists`**: The total number of distances computed.
- **`assignments`**: A list indicating the cluster assignment for each data point.
- **`centroids`**: A list of lists, where each inner list contains the coordinates of a cluster centroid.
- **`ballkm_centroids`**: Ball KMeans centroid information in string format.
- **`timeout`**: A boolean indicating if the algorithm timed out.
- **`sse`**: The sum of squared errors (SSE).

### Example of Processing Results
```python
# Get results for the first data file
result = results[0]

# Print the number of iterations
print(f"Loop Counter: {result.loop_counter}")

# Print the SSE value
print(f"SSE: {result.sse}")

# Print all results as a dictionary
print(result.to_dict())

# Print centroid information
for centroid in result.centroids:
    print(centroid)
```

### Summary
The `DataCentricKMeans` package provides easy-to-use functions for running various KMeans algorithms and accessing their results in Python. The examples and descriptions above illustrate how to use these functions and handle their outputs.
