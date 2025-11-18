import numpy as np
import matplotlib.pyplot as plt

def plot_poincare(S_in, S_out, filename="poincare.png"):
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection="3d")

    u = np.linspace(0, 2*np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    ax.plot_surface(x, y, z, alpha=0.1)
    ax.scatter(S_in[1], S_in[2], S_in[3], s=80, label="Input")
    ax.scatter(S_out[1], S_out[2], S_out[3], s=80, label="Output")
    ax.legend()
    plt.savefig(filename)
    plt.close()
    return filename
