import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

QG_all = []
skip_index = [-1]
for i in range(50):
    if i in skip_index:
        continue
    else:
        QG = np.zeros((19999, 2))
        Q = np.loadtxt(f'../{i}/GQ/Q/{i}.Q', skiprows=1, delimiter=',')
        G = np.loadtxt(f'../{i}/GQ/G/{i}.G', skiprows=1, delimiter=',')
        
        # Add this check:
        if Q.shape[0] != 19999:
            print(f"Warning: Q file for traj {i} has {Q.shape[0]} lines (expected 19999)")
        else:
            print(f"traj {i}: Q OK")
        if G.shape[0] != 19999:
            print(f"Warning: G file for traj {i} has {G.shape[0]} lines (expected 19999)")
        else:
            print(f"traj {i}: G OK")
        
        fQ = Q[:,-1]
        fG = G[:,-1]

        QG[:,0] = fQ
        QG[:,1] = fG
        QG_all.append(QG)
        
QG_all = np.asarray(QG_all)
np.save('QG.npy',QG_all)

# Plot Free energy landscape on Q order parameter to see if the simulations reached the folded state.
raw_data_all = np.concatenate(QG_all, axis=0)
# Check if the simulations reached the folded state by plot Free energy landscape on Q order parameter.
x = raw_data_all[:, 0]
# Compute histogram
hist, bin_edges = np.histogram(x, bins=75, density=True)

# Avoid log(0) by masking or replacing zero probabilities
hist = np.where(hist == 0, np.nan, hist)  # or use a small epsilon instead

# Convert to free energy
F = -np.log(hist)
F -= np.nanmin(F)  # Optional: shift minimum to zero for better visualization

# Bin centers for plotting
bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

# Plot
plt.figure(figsize=(8, 5))
plt.plot(bin_centers, F, lw=2)
plt.xlabel('Reaction Coordinate (Q)')
plt.ylabel('Free Energy (kT)')
plt.title('New model')
plt.grid(True)
plt.tight_layout()
plt.savefig('Q_free_energy.png', dpi=300)
plt.show()


# Check the distribution of G
y = raw_data_all[:, 1]
# Compute histogram
hist, bin_edges = np.histogram(y, bins=75, density=True)

# Avoid log(0) by masking or replacing zero probabilities
hist = np.where(hist == 0, np.nan, hist)  # or use a small epsilon instead

# Convert to free energy
F = -np.log(hist)
F -= np.nanmin(F)  # Optional: shift minimum to zero for better visualization

# Bin centers for plotting
bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

# Plot
plt.figure(figsize=(8, 5))
plt.plot(bin_centers, F, lw=2)
plt.xlabel('Reaction Coordinate (G)')
plt.ylabel('Free Energy (kT)')
plt.title('New model')
plt.grid(True)
plt.tight_layout()
plt.savefig('G_free_energy.png', dpi=300)
plt.show()
