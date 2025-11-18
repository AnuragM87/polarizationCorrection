# import numpy as np

# def apply_qwp_pdf(E_in, theta_deg):
#     """
#     Quarter-wave plate matrix from the PDF:
#     U_Q(theta) = [[cos^2θ + i sin^2θ, sinθ cosθ (1 - i)],
#                   [sinθ cosθ (1 - i), sin^2θ + i cos^2θ]]
#     """
#     th = np.deg2rad(theta_deg)
#     c = np.cos(th)
#     s = np.sin(th)

#     M = np.array([
#         [c*c + 1j*s*s,  s*c*(1 - 1j)],
#         [s*c*(1 - 1j),  s*s + 1j*c*c]
#     ], dtype=complex)

#     return M @ E_in
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
