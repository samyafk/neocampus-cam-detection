import numpy as np

def transform_point(point, H):
    point_homog = np.array([point[0], point[1], 1], dtype=np.float32).reshape(-1, 1)
    transformed_point = np.dot(H, point_homog)
    transformed_point /= transformed_point[2]  # Normaliser les coordonnées homogènes
    return transformed_point[0], transformed_point[1]