import numpy as np

def hwp_matrix(theta_deg):
    th = np.deg2rad(theta_deg)
    c2 = np.cos(2*th)
    s2 = np.sin(2*th)
    return np.array([[c2, s2],
                     [s2, -c2]], dtype=complex)

def apply_hwp(E, theta_deg):
    return hwp_matrix(theta_deg) @ E
