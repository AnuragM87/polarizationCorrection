import numpy as np

def qwp_matrix(theta_deg):
    th = np.deg2rad(theta_deg)
    c = np.cos(th)
    s = np.sin(th)
    c2 = c*c
    s2 = s*s
    off = s*c*(1 - 1j)

    return np.array([
        [c2 + 1j*s2, off],
        [off,        s2 + 1j*c2]
    ], dtype=complex)

def apply_qwp(E, theta_deg):
    return qwp_matrix(theta_deg) @ E
