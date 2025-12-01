"""
Simple script to visualize agentview images from HDF5 demonstration files.
"""

import argparse
import h5py
import matplotlib.pyplot as plt
import numpy as np


def visualize_demo_images(hdf5_path, demo_name="demo_1", max_frames=10):
    """
    Visualize agentview images from a demonstration in an HDF5 file.
    
    Args:
        hdf5_path: Path to the HDF5 file
        demo_name: Name of the demo (e.g., "demo_1", "demo_2")
        max_frames: Maximum number of frames to display
    """
    with h5py.File(hdf5_path, 'r') as f:
        # Navigate to the agentview images
        image_path = f"/data/{demo_name}/obs/agentview_image"
        
        if image_path not in f:
            print(f"Path {image_path} not found in HDF5 file.")
            print(f"Available demos: {list(f['/data'].keys())}")
            if demo_name in f['/data']:
                print(f"Available observations in {demo_name}: {list(f[f'/data/{demo_name}/obs'].keys())}")
            return
        
        # Load the images
        images = f[image_path][:]
        print(f"Loaded {len(images)} images with shape {images.shape}")
        print(f"Image dtype: {images.dtype}, min: {images.min()}, max: {images.max()}")
        
        # Determine how many images to show
        num_frames = min(len(images), max_frames)
        
        # Create a grid of subplots
        cols = min(5, num_frames)
        rows = (num_frames + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3))
        if num_frames == 1:
            axes = [axes]
        else:
            axes = axes.flatten() if rows > 1 else axes
        
        # Plot each frame
        for i in range(num_frames):
            img = images[i]
            
            # Normalize if needed (if values are in [0, 255] range)
            if img.max() > 1.0:
                img = img.astype(np.uint8)
            
            axes[i].imshow(img)
            axes[i].set_title(f"Frame {i}")
            axes[i].axis('off')
        
        # Hide any unused subplots
        for i in range(num_frames, len(axes)):
            axes[i].axis('off')
        
        plt.suptitle(f"{demo_name} - agentview_image", fontsize=16)
        plt.tight_layout()
        plt.show()


def visualize_demo_video(hdf5_path, demo_name="demo_1", interval=100):
    """
    Create an animated video of the demonstration.
    
    Args:
        hdf5_path: Path to the HDF5 file
        demo_name: Name of the demo
        interval: Milliseconds between frames
    """
    from matplotlib.animation import FuncAnimation
    
    with h5py.File(hdf5_path, 'r') as f:
        image_path = f"/data/{demo_name}/obs/agentview_image"
        
        if image_path not in f:
            print(f"Path {image_path} not found in HDF5 file.")
            return
        
        images = f[image_path][:]
        print(f"Creating animation with {len(images)} frames")
        
        # Normalize if needed
        if images.max() > 1.0:
            images = images.astype(np.uint8)
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.axis('off')
        
        im = ax.imshow(images[0])
        title = ax.set_title(f"Frame 0/{len(images)}")
        
        def update(frame):
            im.set_array(images[frame])
            title.set_text(f"Frame {frame}/{len(images)}")
            return [im, title]
        
        anim = FuncAnimation(fig, update, frames=len(images), 
                           interval=interval, blit=True, repeat=True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize agentview images from HDF5 demo files")
    parser.add_argument("hdf5_file", type=str, help="Path to HDF5 file")
    parser.add_argument("--demo", type=str, default="demo_1", help="Demo name (e.g., demo_1, demo_2)")
    parser.add_argument("--max-frames", type=int, default=10, help="Maximum frames to show in grid")
    parser.add_argument("--video", action="store_true", help="Show as animated video instead of grid")
    parser.add_argument("--interval", type=int, default=100, help="Milliseconds between frames (for video mode)")
    
    args = parser.parse_args()
    
    if args.video:
        visualize_demo_video(args.hdf5_file, args.demo, args.interval)
    else:
        visualize_demo_images(args.hdf5_file, args.demo, args.max_frames)

