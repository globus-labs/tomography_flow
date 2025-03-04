#!/usr/bin/env python3
import argparse

from recon import load_data, recon_data, save_data, save_images, show_images


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run tomographic reconstruction using tomopy, dxchange, and Globus Compute SDK."
    )
    parser.add_argument(
        "--proj-file", type=str, required=True, help="Path to the projection HDF file."
    )
    parser.add_argument(
        "--angles-file",
        type=str,
        required=True,
        help="Path to the angles file (NXS format).",
    )
    parser.add_argument(
        "--dark-file", type=str, required=True, help="Path to the dark HDF file."
    )
    parser.add_argument(
        "--flat-file", type=str, required=True, help="Path to the flat HDF file."
    )
    parser.add_argument(
        "--recon-init",
        type=int,
        default=1000,
        help="Starting slice for reconstruction (default: 1000).",
    )
    parser.add_argument(
        "--recon-end",
        type=int,
        default=1512,
        help="Ending slice for reconstruction (default: 1512).",
    )
    parser.add_argument(
        "--rot-center",
        type=float,
        default=None,
        help="Rotation center for reconstruction (default: None).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="recon_output",
        help="Output directory for saving results.",
    )
    parser.add_argument(
        "--show-images", action="store_true", help="Display images after processing."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Load the data with specified slice limits.
    proj, flats, darks, theta = load_data(
        args.proj_file,
        args.flat_file,
        args.dark_file,
        args.angles_file,
        args.recon_init,
        args.recon_end,
    )

    # Perform the reconstruction.
    recon, proj_norm, rot_center = recon_data(proj, flats, darks, theta)

    # Save the reconstructed volume and write out the rotation center.
    save_data(recon, rot_center, output_dir=args.output_dir)

    # Save representative images (sinogram and middle slice).
    save_images(proj_norm, recon, output_dir=args.output_dir)

    # Optionally display the images.
    if args.show_images:
        show_images(proj_norm, recon)

    print(f"Processing complete. Check the '{args.output_dir}' directory for results.")


if __name__ == "__main__":
    main()
