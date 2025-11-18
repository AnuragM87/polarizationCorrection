import numpy as np

POL = {
    "H": np.array([1, 0], dtype=complex),
    "V": np.array([0, 1], dtype=complex),
    "D": np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex),
    "A": np.array([1/np.sqrt(2), -1/np.sqrt(2)], dtype=complex),
    "R": np.array([1/np.sqrt(2), -1j/np.sqrt(2)], dtype=complex),
    "L": np.array([1/np.sqrt(2),  1j/np.sqrt(2)], dtype=complex),
}

# def get_polarization_vector(code: str):
#     code = code.upper().strip()
#     if code in POL:
#         return POL[code]

#     # Custom vector: "0.5+0.5j, 0.5-0.5j"
#     if "," in code:
#         a, b = code.split(",")
#         v = np.array([complex(a), complex(b)], dtype=complex)
#         return v / np.linalg.norm(v)

#     raise ValueError("Invalid polarization code")

def get_polarization_vector(pol):
    pol = pol.strip()

    # Predefined states
    base = {
        "H": np.array([1, 0], dtype=complex),
        "V": np.array([0, 1], dtype=complex),
        "D": np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex),
        "A": np.array([1/np.sqrt(2), -1/np.sqrt(2)], dtype=complex),
        "R": np.array([1/np.sqrt(2), -1j/np.sqrt(2)], dtype=complex),
        "L": np.array([1/np.sqrt(2),  1j/np.sqrt(2)], dtype=complex),
    }

    if pol.upper() in base:
        return base[pol.upper()]

    # ---- FIX: allow input like "0.5+0.5j, 0.5-0.5j" ----
    if "," in pol:
        try:
            a, b = pol.split(",")
            vec = np.array([complex(a.strip()), complex(b.strip())], dtype=complex)
            # normalize to unit Jones vector
            norm = np.linalg.norm(vec)
            if norm == 0:
                raise ValueError("Zero vector")
            return vec / norm
        except Exception:
            raise ValueError("Invalid custom Jones vector format. Use: a+bi, c+di")

    raise ValueError(f"Unknown polarization state: {pol}")

