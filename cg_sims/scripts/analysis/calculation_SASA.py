import os
import mdtraj as md
import numpy as np
import parmed as pmd

n_trajs = 50
n_frames = 20_000
p = pmd.load_file('../template/setup/top.psf')
n_residues = p.topology.getNumResidues()

# allocate with NaNs so missing trajectories stay obvious
all_sasa = np.full((n_trajs, n_frames, n_residues), np.nan, dtype=np.float32)


for i in range(n_trajs):
    print(f"Calculating SASA for trajectory {i}")

    dcd_file = f'../{i}/aa_{i}.dcd'
    psf_file = f'../{i}/aa_{i}.psf'

    if not (os.path.exists(dcd_file) and os.path.exists(psf_file)):
        raise FileNotFoundError(f"Missing files for traj {i}: {dcd_file} or {psf_file}")

    # load trajectory
    traj = md.load(dcd_file, top=psf_file)

    # enforce frame count check
    if traj.n_frames != n_frames:
        raise ValueError(
            f"Trajectory {i} has {traj.n_frames} frames, expected {n_frames}. "
            "Stopping execution."
        )
    
    # calculate SASA per residue (frames × residues)
    sasa = md.shrake_rupley(traj, mode='residue')

    # write to array
    all_sasa[i] = sasa

# save to disk
np.save('SASA.npy', all_sasa)
print("Finished. SASA.npy saved.")