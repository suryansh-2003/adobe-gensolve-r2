import numpy as np
import matplotlib.pyplot as plt
import svgwrite
import cairosvg

def plot(paths_XYs):
    colours = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta']
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for i, XYs in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    plt.show()

def polylines2svg(paths_XYs, svg_path):
    W, H = 0, 0
    for path_XYs in paths_XYs:
        for XY in path_XYs:
            W = max(W, np.max(XY[:, 0]))
            H = max(H, np.max(XY[:, 1]))

    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)
    
    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')
    group = dwg.g()
    
    for path in paths_XYs:
        path_data = []
        c = 'black'
        for XY in path:
            path_data.append(("M", (XY[0, 0], XY[0, 1])))
            for j in range(1, len(XY)):
                path_data.append(("L", (XY[j, 0], XY[j, 1])))
        if not np.allclose(path[0], path[-1]):
            path_data.append(("Z", None))
        group.add(dwg.path(d=path_data, fill=c, stroke='none', stroke_width=2))
    
    dwg.add(group)
    dwg.save()
    
    png_path = svg_path.replace('.svg', '.png')
    fact = max(1, 1024 // min(W, H))
    cairosvg.svg2png(url=svg_path, write_to=png_path, parent_width=W, parent_height=H, output_width=fact*W, output_height=fact*H, background_color='white')
    return png_path

# Example usage
if __name__ == "__main__":
    # Example data for testing
    example_paths_XYs = [
        [np.array([[0, 0], [1, 1], [1, 0], [0, 0]])],  # Simple triangle
        [np.array([[2, 2], [3, 2], [3, 3], [2, 3], [2, 2]])]  # Simple square
    ]
    plot(example_paths_XYs)
    svg_path = 'example_shapes.svg'
    png_path = polylines2svg(example_paths_XYs, svg_path)
    print(f'SVG saved to {svg_path}')
    print(f'PNG saved to {png_path}')
