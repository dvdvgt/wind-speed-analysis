import numpy as np
from tueplots.constants.color.rgb import tue_red

def ridgeline_plot(X, Y, ax, y_labels, overlap=0.5, range_threshold=None, linewidth=1, alpha=1, fill=False, fill_color=tue_red):
    """
    Create a ridgeline plot using Matplotlib.

    Parameters:
    - X: Matrix containing evaluation points as rows.
    - Y: Matrix containing corresponding values of the density.
    - ax: Matplotlib axis where the plot will be drawn.
    - y_label: Label for the y-axis.
    - fill: Whether to fill the areas between the lines.
    - fill-color: Color to fill between
    - fade: 1 is fully opaque while 0 is fully transparent
    - range_threshold: limit x-axis to only those values where y-axis is above the threshold
    - overlap: Overlap factor controlling the spacing between groups.
    """
    for i, (x, y) in enumerate(zip(X, Y)):
        offset = i * (1 - overlap)
        if range_threshold:
            x = x[y > range_threshold]
            y = y[y > range_threshold]
        if fill:
            ax.fill_between(x, np.ones_like(x) * offset, offset + y, alpha=alpha, label=y_labels[i],  zorder=len(Y) - i + 1, color=fill_color)
        ax.plot(x, y + offset, c="k", zorder=len(Y) - i + 1, alpha=alpha, linewidth=linewidth)

    for loc in ["top", "bottom", "left", "right"]:
        ax.spines[loc].set_visible(False)
    ax.set_yticks([i * ( 1 - overlap) for i in range(len(X))])
    ax.set_yticklabels([y_labels[i] for i in range(X.shape[0])])