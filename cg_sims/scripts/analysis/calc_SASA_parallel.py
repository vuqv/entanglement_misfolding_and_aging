import os
import mdtraj as md
import numpy as np
import parmed as pmd
from multiprocessing import Pool

n_trajs = 50
n_frames = 20_000
p = pmd.load_file('../template/setup/top.psf')
n_residues = p.topology.getNumResidues()

os.makedirs('SASA', exist_ok=True)

def process_traj(i):
    print(f"Processing trajectory: {i}")
    dcd_file = f'../{i}/aa_{i}.dcd'
    psf_file = f'../{i}/aa_{i}.psf'

    if not (os.path.exists(dcd_file) and os.path.exists(psf_file)):
        raise FileNotFoundError(f"Missing files for traj {i}: {dcd_file} or {psf_file}")

    traj = md.load(dcd_file, top=psf_file)
    if traj.n_frames != n_frames:
        raise ValueError(
            f"Trajectory {i} has {traj.n_frames} frames, expected {n_frames}. "
            "Stopping execution."
        )
    sasa = md.shrake_rupley(traj[::10], mode='residue')
    np.save(f'SASA/sasa_{i}.npy', sasa)
    return sasa

if __name__ == '__main__':
    with Pool(processes=8) as pool:
        all_sasa = pool.map(process_traj, range(n_trajs))
    all_sasa = np.array(all_sasa, dtype=np.float32)
    np.save('SASA/SASA.npy', all_sasa)
    print("Finished. SASA.npy and individual SASA files saved.")
