# import numpy as np

# # Predefined states
# POL_MAP = {
#     "H": np.array([1, 0], dtype=complex),
#     "V": np.array([0, 1], dtype=complex),
#     "D": np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex),
#     "A": np.array([1/np.sqrt(2), -1/np.sqrt(2)], dtype=complex),
#     "R": np.array([1/np.sqrt(2), -1j/np.sqrt(2)], dtype=complex),
#     "L": np.array([1/np.sqrt(2), 1j/np.sqrt(2)], dtype=complex)
# }

# def get_polarization_vector(code):
#     return POL_MAP.get(code.upper(), None)

# def jones_to_stokes(E):
#     Ex, Ey = E
#     S0 = np.abs(Ex)**2 + np.abs(Ey)**2
#     S1 = np.abs(Ex)**2 - np.abs(Ey)**2
#     S2 = 2 * np.real(Ex * np.conj(Ey))
#     S3 = 2 * np.imag(Ex * np.conj(Ey))
#     return np.array([S0, S1, S2, S3]) / S0

# def hwp_matrix(theta_deg):
#     theta = np.deg2rad(theta_deg)
#     return np.array([
#         [np.cos(2*theta), np.sin(2*theta)],
#         [np.sin(2*theta), -np.cos(2*theta)]
#     ], dtype=complex)

# def apply_hwp(E_in, theta_deg):
#     H = hwp_matrix(theta_deg)
#     return H @ E_in
import numpy as np

def hwp_matrix(theta_deg):
    th = np.deg2rad(theta_deg)
    c2 = np.cos(2*th)
    s2 = np.sin(2*th)
    return np.array([[c2, s2],
                     [s2, -c2]], dtype=complex)

def apply_hwp(E, theta_deg):
    return hwp_matrix(theta_deg) @ E
