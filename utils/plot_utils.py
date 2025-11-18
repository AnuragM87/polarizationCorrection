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

    # fewer frames -> faster generation while keeping smoothness
    t = np.linspace(0, 2*np.pi, 100)

    def animate(i):
        phi = t[i]
        x = np.real(Ex * np.exp(1j * phi))
        y = np.real(Ey * np.exp(1j * phi))
        line.set_data([0, x], [0, y])
        return line,

    anim = FuncAnimation(fig, animate, frames=len(t), interval=30)
    anim.save(filename, writer="pillow")
    plt.close()
    return filename


def polarization_ellipse_html(E, width=400, height=400):
        """
        Return an HTML string that renders a fast client-side animation
        of the polarization ellipse using an HTML5 canvas and JavaScript.
        """
        Ex, Ey = E[0], E[1]

        ex_re = float(np.real(Ex))
        ex_im = float(np.imag(Ex))
        ey_re = float(np.real(Ey))
        ey_im = float(np.imag(Ey))

        # Create HTML with embedded JS that computes the real field components
        html = f"""
        <div>
            <canvas id="polCanvas" width="{width}" height="{height}" style="border:1px solid #ddd"></canvas>
        </div>
        <script>
        (function() {{
            const ex_re = {ex_re};
            const ex_im = {ex_im};
            const ey_re = {ey_re};
            const ey_im = {ey_im};

            const canvas = document.getElementById('polCanvas');
            const ctx = canvas.getContext('2d');
            const W = canvas.width;
            const H = canvas.height;
            const cx = W/2;
            const cy = H/2;
            const margin = 20;
            const maxR = Math.max(Math.hypot(ex_re, ex_im), Math.hypot(ey_re, ey_im), 1e-6);
            const scale = (Math.min(W, H) / 2 - margin) / (1.0 * maxR);

            const N = 200;
            const pts = new Array(N);
            for (let i=0;i<N;i++){{
                const phi = 2*Math.PI * i / N;
                const x = ex_re * Math.cos(phi) - ex_im * Math.sin(phi);
                const y = ey_re * Math.cos(phi) - ey_im * Math.sin(phi);
                pts[i] = [x, y];
            }}

            function draw(){{
                ctx.clearRect(0,0,W,H);

                // axes
                ctx.strokeStyle = '#ddd';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(0, cy);
                ctx.lineTo(W, cy);
                ctx.moveTo(cx, 0);
                ctx.lineTo(cx, H);
                ctx.stroke();

                // ellipse trace
                ctx.strokeStyle = '#0074D9';
                ctx.lineWidth = 2;
                ctx.beginPath();
                for (let i=0;i<N;i++){{
                    const x = cx + pts[i][0] * scale;
                    const y = cy - pts[i][1] * scale;
                    if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
                }}
                ctx.closePath();
                ctx.stroke();

                // rotating point (advance by time)
                const t = Date.now() / 60.0;
                const phi = (t % (2*Math.PI));
                const rx = ex_re * Math.cos(phi) - ex_im * Math.sin(phi);
                const ry = ey_re * Math.cos(phi) - ey_im * Math.sin(phi);
                const px = cx + rx * scale;
                const py = cy - ry * scale;

                // radial vector
                ctx.strokeStyle = '#FF4136';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                ctx.lineTo(px, py);
                ctx.stroke();

                // rotating dot
                ctx.fillStyle = '#FF4136';
                ctx.beginPath();
                ctx.arc(px, py, 5, 0, 2*Math.PI);
                ctx.fill();

                requestAnimationFrame(draw);
            }}

            draw();
        }})();
        </script>
        """

        return html

