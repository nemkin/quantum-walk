import numpy as np

# Generate a random matrix
n = 4  # Size of the matrix
random_matrix = np.random.rand(n, n) + 1j * np.random.rand(n, n)  # Complex random matrix

# QR decomposition
Q, R = np.linalg.qr(random_matrix)

# Normalize Q to make it unitary
Q_unitary = Q / np.sqrt(np.sum(np.abs(Q)**2, axis=0, keepdims=True))

# Check if Q_unitary is indeed unitary
identity_matrix = np.eye(n)
unitary_check = np.allclose(np.dot(Q_unitary.conj().T, Q_unitary), identity_matrix)

print("Original Matrix:")
print(random_matrix)
print("\nQ (Orthogonal Matrix):")
print(Q)
print("\nQ Unitary (Unitary Matrix):")
print(Q_unitary)
print("\nIs Q Unitary:", unitary_check)
