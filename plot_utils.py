import numpy as np
import matplotlib.pyplot as plt

def plot_poincare(input_stokes, output_stokes, filename="poincare_plot.png"):
    """
    Plot input and output polarization on the Poincaré sphere.
    """
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Draw sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x, y, z, alpha=0.1)

    # Input polarization
    ax.scatter(
        input_stokes[1], input_stokes[2], input_stokes[3],
        s=80, label="Input", depthshade=True
    )

    # Output polarization
    ax.scatter(
        output_stokes[1], output_stokes[2], output_stokes[3],
        s=80, label="Output", depthshade=True
    )

    ax.set_xlabel("S1")
    ax.set_ylabel("S2")
    ax.set_zlabel("S3")
    ax.legend()

    plt.savefig(filename, dpi=300)
    plt.close()
    return filename
