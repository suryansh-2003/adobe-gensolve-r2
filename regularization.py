import numpy as np
from scipy.optimize import least_squares
import svgwrite
import cairosvg

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

def fit_circle(XY):
    def circle_residuals(params, x, y):
        xc, yc, r = params
        return (np.sqrt((x - xc)**2 + (y - yc)**2) - r).ravel()

    x, y = XY[:, 0], XY[:, 1]
    x_m, y_m = np.mean(x), np.mean(y)
    r_initial = np.mean(np.sqrt((x - x_m)**2 + (y - y_m)**2))
    
    result = least_squares(circle_residuals, (x_m, y_m, r_initial), args=(x, y))
    xc, yc, r = result.x
    
    return np.array([(xc, yc), r])

def fit_ellipse(XY):
    def ellipse_residuals(params, x, y):
        x0, y0, a, b, angle = params
        x_ = x - x0
        y_ = y - y0
        term1 = (x_ * np.cos(angle) + y_ * np.sin(angle))**2 / a**2
        term2 = (x_ * np.sin(angle) - y_ * np.cos(angle))**2 / b**2
        return (term1 + term2 - 1).ravel()

    x, y = XY[:, 0], XY[:, 1]
    x_m, y_m = np.mean(x), np.mean(y)
    a_initial = (np.max(x) - np.min(x)) / 2
    b_initial = (np.max(y) - np.min(y)) / 2
    angle_initial = 0.0
    
    result = least_squares(ellipse_residuals, (x_m, y_m, a_initial, b_initial, angle_initial), args=(x, y))
    x0, y0, a, b, angle = result.x
    
    return np.array([(x0, y0), a, b, angle])

def regularize_curve(XY):
    if len(XY) < 2:
        return XY
    if is_straight_line(XY):
        return np.array([XY[0], XY[-1]])
    if is_circle(XY):
        return fit_circle(XY)
    if is_ellipse(XY):
        return fit_ellipse(XY)
    return XY

def is_straight_line(XY):
    diffs = np.diff(XY, axis=0)
    slopes = np.arctan2(diffs[:, 1], diffs[:, 0])
    return np.allclose(slopes, slopes[0], atol=1e-5)

def is_circle(XY):
    try:
        _ = fit_circle(XY)
        return True
    except:
        return False

def is_ellipse(XY):
    try:
        _ = fit_ellipse(XY)
        return True
    except:
        return False

def save_paths(paths_XYs, output_csv):
    with open(output_csv, 'w') as f:
        for i, path in enumerate(paths_XYs):
            for j, XY in enumerate(path):
                np.savetxt(f, np.hstack([np.full((XY.shape[0], 1), i), XY]), delimiter=',', fmt='%f')

def main_regularize(input_csv, output_csv):
    paths_XYs = read_csv(input_csv)
    regularized_paths = [regularize_curve(XY) for path in paths_XYs for XY in path]
    save_paths(regularized_paths, output_csv)

if __name__ == "__main__":
    main_regularize('examples/isolated.csv', 'regularized_output.csv')
