#!/usr/bin/env python3
import argparse
from tomography_flow.tomo_flow.recon import load_data, recon_data, save_data, save_images

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run tomographic reconstruction using tomopy, dxchange, and Globus Compute SDK."
    )
    parser.add_argument("--proj-file", type=str, required=True,
                        help="Path to the projection HDF file.")
    parser.add_argument("--angles-file", type=str, required=True,
                        help="Path to the angles file (NXS format).")
    parser.add_argument("--dark-file", type=str, required=True,
                        help="Path to the dark HDF file.")
    parser.add_argument("--flat-file", type=str, required=True,
                        help="Path to the flat HDF file.")
    parser.add_argument("--recon-init", type=int, default=1000,
                        help="Starting slice for reconstruction (default: 1000).")
    parser.add_argument("--recon-end", type=int, default=1512,
                        help="Ending slice for reconstruction (default: 1512).")
    # Although rot_center is now computed automatically, you can optionally pass one
    parser.add_argument("--rot-center", type=float, default=None,
                        help="Rotation center for reconstruction (default: None).")
    return parser.parse_args()

def main():
    args = parse_args()

    # Load data using the provided reconstruction slice limits.
    proj, flats, darks, theta = load_data(
        args.proj_file,
        args.flat_file,
        args.dark_file,
        args.angles_file,
        args.recon_init,
        args.recon_end
    )

    # Perform the reconstruction.
    # This function returns the reconstructed volume, the normalized projection data, and the calculated rotation center.
    recon, proj_norm, rot_center = recon_data(proj, flats, darks, theta)

    # Save the reconstructed data (TIFF stack and rotation center value) to an output directory.
    save_data(recon, rot_center, output_dir='recon_output')

    # Save representative images (sinogram and middle slice) of the normalized projection and reconstruction.
    save_images(proj_norm, recon, output_dir='recon_output')

    print("Processing complete. Check the 'recon_output' directory for results.")

if __name__ == '__main__':
    main()
