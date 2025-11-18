import numpy as np
import re

POL = {
    "H": np.array([1, 0], dtype=complex),
    "V": np.array([0, 1], dtype=complex),
    "D": np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex),
    "A": np.array([1/np.sqrt(2), -1/np.sqrt(2)], dtype=complex),
    "R": np.array([1/np.sqrt(2), -1j/np.sqrt(2)], dtype=complex),
    "L": np.array([1/np.sqrt(2),  1j/np.sqrt(2)], dtype=complex),
}

def clean_complex_string(s: str):
    """
    Remove brackets, parentheses, accidental spaces.
    Ensures values like '(0.5+0.5j, 0.5-0.5j)' parse correctly.
    """
    s = s.replace("(", "").replace(")", "")
    s = s.replace("[", "").replace("]", "")
    return s.strip()

def get_polarization_vector(pol):
    pol = pol.strip()

    # Predefined states
    if pol.upper() in POL:
        return POL[pol.upper()]

    # ---------- FIX: allow general complex Jones input ----------
    if "," in pol:
        try:
            cleaned = clean_complex_string(pol)
            a, b = cleaned.split(",")

            a = a.strip()
            b = b.strip()

            # Convert to complex numbers
            vec = np.array([complex(a), complex(b)], dtype=complex)

            # Normalize
            norm = np.linalg.norm(vec)
            if norm == 0:
                raise ValueError("Zero vector given.")
            return vec / norm

        except Exception as e:
            raise ValueError(f"Invalid custom Jones vector. Error: {e}")

    raise ValueError(f"Unknown polarization state: {pol}")
