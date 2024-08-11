import numpy as np
import csv
from scipy.spatial import distance_matrix

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def complete_curve(XY):
    if not np.allclose(XY[0], XY[-1]):
        # Interpolate missing points
        start_point = XY[0]
        end_point = XY[-1]
        # Simple linear interpolation to complete the curve
        num_points = 10
        interpolated_points = np.linspace(start_point, end_point, num_points + 2)[1:-1]
        return np.vstack([XY, interpolated_points, end_point])
    return XY

def save_paths(paths_XYs, output_csv):
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        for i, path in enumerate(paths_XYs):
            for j, XY in enumerate(path):
                for k, point in enumerate(XY):
                    writer.writerow([i, j, k, point[0], point[1]])

def main_completion(input_csv, output_csv):
    paths_XYs = read_csv(input_csv)
    completed_paths = [complete_curve(XY) for path in paths_XYs for XY in path]
    save_paths(completed_paths, output_csv)

if __name__ == "__main__":
    main_completion('examples/occlusion1.csv', 'completed_output.csv')
