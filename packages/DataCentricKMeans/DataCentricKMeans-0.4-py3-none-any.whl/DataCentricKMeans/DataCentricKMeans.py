import subprocess
import os
import platform

class KMeansResult:
    def __init__(self, loop_counter, num_dists, assignments, centroids, sse):
        self.loop_counter = loop_counter
        self.num_dists = num_dists
        self.assignments = assignments
        self.centroids = centroids
        self.sse = sse

    def to_dict(self):
        return {
            "loop_counter": self.loop_counter,
            "num_dists": self.num_dists,
            "assignments": self.assignments,
            "centroids": self.centroids,
            "sse": self.sse
        }

def run_lloyd_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
    return run_cpp_program("lloyd_kmeans", num_iterations, threshold, num_clusters, seed, file_paths)

def run_geokmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
    return run_cpp_program("geokmeans", num_iterations, threshold, num_clusters, seed, file_paths)

def run_elkan_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
    return run_cpp_program("elkan", num_iterations, threshold, num_clusters, seed, file_paths)

def run_hamerly_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
    return run_cpp_program("hamerly", num_iterations, threshold, num_clusters, seed, file_paths)

def run_annulus_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
    return run_cpp_program("annulus", num_iterations, threshold, num_clusters, seed, file_paths)

def run_exponion_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
    return run_cpp_program("exponion", num_iterations, threshold, num_clusters, seed, file_paths)

def run_cpp_program(algorithm, num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
    # Check: num_iterations must be >= 1
    if not isinstance(num_iterations, int) or num_iterations < 1:
        raise ValueError("Number of iterations must be >= 1.")
    
    # Check: threshold must be >= 0
    if not isinstance(threshold, float) or threshold < 0:
        raise ValueError("Threshold must be >= 0.")
    
    # Check: num_clusters must be >= 2 and less than the number of samples
    if not isinstance(num_clusters, int) or num_clusters < 2:
        raise ValueError("Number of clusters must be >= 2.")
    
    # Check: seed must be a positive integer, use default if not provided
    if seed is None:
        seed = 42  # Default seed value
    elif not isinstance(seed, int) or seed <= 0:
        raise ValueError("Seed must be a positive integer.")
    
    # Check: file_paths must be a list of strings
    if not isinstance(file_paths, list) or not all(isinstance(path, str) for path in file_paths):
        raise ValueError("File paths must be a list of strings.")
    
    # Check: Each file in file_paths must exist
    for path in file_paths:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found: {path}")

    # Select the correct C++ executable based on the operating system
    if platform.system() == "Darwin":
        executable = 'DataCentricKMeans_universal.out'
    elif platform.system() == "Linux":
        executable = 'DataCentricKMeans_linux.out'
    elif platform.system() == "Windows":
        executable = 'DataCentricKMeans_windows.exe'
    else:
        raise RuntimeError("Unsupported operating system")

    executable_path = os.path.join(os.path.dirname(__file__), executable)

    # Join file paths into a single string separated by commas
    file_paths_str = ",".join(file_paths)
    
    # Create the command to run the C++ program
    command = [
        executable_path,
        algorithm,
        str(num_iterations),
        str(threshold),
        str(num_clusters),
        str(seed),
        file_paths_str
    ]
    
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        # Process the output files
        outputs = []
        for path in file_paths:
            output_path = os.path.splitext(path)[0] + f"-solution-{algorithm}.txt"
            outputs.append(read_output_file(output_path))
        return outputs
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error occurred while running the program: {e.stderr}")

def read_output_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    result_data = {
        'loop_counter': None,
        'num_dists': None,
        'assignments': [],
        'centroids': [],
        'sse': None
    }
    
    centroid_section = False
    
    for line in lines:
        if line.startswith("Loop Counter:"):
            result_data['loop_counter'] = int(line.split(":")[1].strip())
        elif line.startswith("Number of Distances:"):
            result_data['num_dists'] = int(line.split(":")[1].strip())
        elif line.startswith("Assignments:"):
            assignments = lines[lines.index(line) + 1].strip().split()
            result_data['assignments'] = [int(a) for a in assignments]
        elif line.startswith("Centroids:"):
            centroid_section = True
        elif line.startswith("SSE:"):
            result_data['sse'] = float(line.split(":")[1].strip())
        elif centroid_section:
            if line.strip():  # Skip empty lines in centroids section
                centroids = [float(value) for value in line.split()]
                result_data['centroids'].append(centroids)
    
    return KMeansResult(**result_data)
