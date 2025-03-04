import os

import h5py
import matplotlib.pyplot as plt
import tomopy


def load_data(proj_file, flat_file, dark_file, angles_file, recon_init, recon_end):
    """
    Loads projection, flat, dark, and angles data from HDF files.
    Slices the projection, flat, and dark data between recon_init and recon_end.
    Converts the rotation angles to radians.
    """
    with h5py.File(proj_file, "r") as f_proj:
        proj = f_proj["entry"]["data"]["data"][:, recon_init:recon_end, :]
        print("proj", proj.shape, proj.dtype)
    with h5py.File(flat_file, "r") as f_flat:
        flats = f_flat["entry"]["data"]["data"][:, recon_init:recon_end, :]
        print("flats", flats.shape, flats.dtype)
    with h5py.File(dark_file, "r") as f_dark:
        darks = f_dark["entry"]["data"]["data"][:, recon_init:recon_end, :]
        print("darks", darks.shape, darks.dtype)
    with h5py.File(angles_file, "r") as f_angles:
        theta = f_angles["entry"]["data"]["rotation_angle"][:]
        theta = theta * 3.141592653589793 / 180  # convert to radians
        print("theta", theta.shape, theta.dtype)
    return proj, flats, darks, theta


def recon_data(proj, flats, darks, theta):
    """
    Normalizes the projection data, finds the rotation center,
    applies logarithmic normalization, reconstructs the tomographic image,
    and applies a circular mask.
    """
    proj_norm = tomopy.normalize(proj, flats, darks)
    print("proj_norm", proj_norm.shape, proj_norm.dtype)

    # Find rotation center from normalized projections
    rot_center = tomopy.find_center_vo(proj_norm)
    print("rot_center", rot_center)

    # Apply log normalization
    proj_log = tomopy.minus_log(proj_norm)
    print("proj_norm_ml", proj_log.shape, proj_log.dtype)

    # Reconstruct using the gridrec algorithm
    recon = tomopy.recon(proj_log, theta, center=rot_center, algorithm="gridrec")
    print("recon", recon.shape)

    # Apply a circular mask to the reconstruction
    recon_masked = tomopy.circ_mask(recon, axis=0, ratio=0.95)

    return recon_masked, proj_norm, rot_center


def save_data(recon, rot_center, output_dir="recon"):
    """
    Saves the reconstructed volume as a stack of TIFF files and writes the
    rotation center to a text file in the specified output directory.
    """
    import dxchange

    os.makedirs(output_dir, exist_ok=True)

    # Save the reconstruction; files will be written with a prefix in the output directory.
    dxchange.write_tiff_stack(recon, fname=os.path.join(output_dir, "recon"), axis=0)
    print("Reconstruction data saved with shape:", recon.shape)

    # Save the rotation center to a text file.
    center_file = os.path.join(output_dir, "center.txt")
    with open(center_file, "w") as file:
        file.write(str(rot_center))
    print("Rotation center saved:", center_file)


def save_images(proj, recon, output_dir="."):
    """
    Saves representative images of the projection and reconstruction data as PNG files.
    """
    os.makedirs(output_dir, exist_ok=True)
    proj_img_path = os.path.join(output_dir, "proj.png")
    recon_img_path = os.path.join(output_dir, "recon.png")

    # Save a sinogram (first column of projection data)
    plt.imsave(proj_img_path, proj[:, 0, :], cmap="gray")
    # Save the middle slice of the reconstruction
    mid_slice = recon[recon.shape[0] // 2, :, :]
    plt.imsave(recon_img_path, mid_slice, cmap="gray")

    print(f"Projection image saved as {proj_img_path}")
    print(f"Reconstruction image saved as {recon_img_path}")


def show_images(proj, recon):
    """
    Displays images of the projection data and reconstruction.
    """
    # Plot the middle slice of the projection data.
    fig, ax = plt.subplots(figsize=(10, 15))
    mid_proj = proj[proj.shape[0] // 2, :, :]
    ax.imshow(mid_proj, cmap="gray")
    ax.set_title("Middle Slice of Projection")
    plt.show()

    # Display the sinogram.
    plt.imshow(proj[:, 0, :], cmap="gray")
    plt.title("Sinogram")
    plt.show()

    # Plot cross sections of the reconstruction along Z, Y, and X axes.
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(recon[recon.shape[0] // 2, :, :], cmap="gray")
    axes[0].set_title("Cross Section along Z-axis")
    axes[1].imshow(recon[:, recon.shape[1] // 2, :], cmap="gray")
    axes[1].set_title("Cross Section along Y-axis")
    axes[2].imshow(recon[:, :, recon.shape[2] // 2], cmap="gray")
    axes[2].set_title("Cross Section along X-axis")
    plt.tight_layout()
    plt.show()
