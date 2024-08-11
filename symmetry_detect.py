import numpy as np
from scipy.spatial import ConvexHull

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

def check_reflection_symmetry(XY):
    x, y = XY[:, 0], XY[:, 1]
    mid_x = (np.min(x) + np.max(x)) / 2
    reflected_XY = np.copy(XY)
    reflected_XY[:, 0] = 2 * mid_x - x
    return np.allclose(XY, reflected_XY, atol=1e-5)

def check_rotational_symmetry(XY, angle_step=5):
    def rotate(XY, angle):
        theta = np.radians(angle)
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta), np.cos(theta)]])
        return np.dot(XY, rotation_matrix.T)

    angles = np.arange(0, 360, angle_step)
    for angle in angles:
        rotated_XY = rotate(XY, angle)
        if np.allclose(XY, rotated_XY, atol=1e-5):
            return angle
    return None

def main_symmetry(input_csv):
    paths_XYs = read_csv(input_csv)
    for i, path in enumerate(paths_XYs):
        for j, XY in enumerate(path):
            if check_reflection_symmetry(XY):
                print(f"Path {i+1}, Polyline {j+1}: Reflection symmetry detected")
            rotation_angle = check_rotational_symmetry(XY)
            if rotation_angle is not None:
                print(f"Path {i+1}, Polyline {j+1}: Rotational symmetry detected with angle {rotation_angle}")

if __name__ == "__main__":
    main_symmetry('examples/frag0.csv')
