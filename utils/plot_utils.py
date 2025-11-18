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

def polarization_ellipse_animation(E, filename="ellipse.gif"):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    Ex, Ey = E[0], E[1]

    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("Ex")
    ax.set_ylabel("Ey")

    line, = ax.plot([], [], lw=2)

    t = np.linspace(0, 2*np.pi, 300)

    def animate(i):
        phi = t[i]
        x = np.real(Ex * np.exp(1j * phi))
        y = np.real(Ey * np.exp(1j * phi))
        line.set_data([0, x], [0, y])
        return line,

    anim = FuncAnimation(fig, animate, frames=len(t), interval=20)
    anim.save(filename, writer="pillow")
    plt.close()
    return filename

