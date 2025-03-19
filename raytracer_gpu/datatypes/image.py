import torch
import warnings
from .color import Color

class Image:
    def __init__(self, width: int, height: int, device: str = "cpu"):
        """
        Initialize an image tensor with shape (width, height, 3)
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            device: Target device ('cpu' or 'cuda')
        """
        self.width = width
        self.height = height
        self.device = torch.device(device)
        self.pixels = torch.zeros((height, width, 3), dtype=torch.float32, device=self.device)
        
    def set_pixel(self, x: int, y: int, color) -> None:
        """
        Set pixel at (x, y) to specified color
        
        Args:
            x: Horizontal coordinate (0 <= x < width)
            y: Vertical coordinate (0 <= y < height)
            color: RGB color - can be:
                - torch.Tensor (shape [3])
                - list/tuple of 3 values
                - numpy array (shape [3])
        """
        # Validate coordinates
        if not (0 <= x < self.width and 0 <= y < self.height):
            warnings.warn(f"Coordinates ({x}, {y}) out of bounds. "
                         f"Image size: {self.width}x{self.height}")
            return

        # Convert color to tensor with proper device/dtype
        if not isinstance(color, torch.Tensor):
            color_tensor = torch.as_tensor(color, 
                                        dtype=self.pixels.dtype,
                                        device=self.device)
        else:
            color_tensor = color

        # Validate color shape
        if color_tensor.shape != (3,):
            raise ValueError(f"Color must have 3 elements (RGB), got {color_tensor.shape}")

        # Set pixel value
        self.pixels[x, y] = color_tensor

    def set_pixels(self, coordinates: list, colors: list) -> None:
        """
        Batch set multiple pixels
        Args:
            coordinates: List of (x, y) tuples
            colors: List of colors (same formats as set_pixel)
        """
        for (x, y), color in zip(coordinates, colors):
            self.set_pixel(x, y, color)
            
    def set_pixels(self, x: int, y: int, color: Color) -> None:
        """
        Batch set multiple pixels
        Args:
            coordinates: List of (x, y) tuples
            colors: Color datatype
        """
        # Set pixel value
        self.pixels[x, y] = color
    
    def write_ppm(self, image_file):
        """Write image to PPM format (P3 ASCII variant) from PyTorch tensor.
        
        Optimized for:
        - GPU/CPU tensor handling
        - Batch conversion to uint8
        - Efficient memory management
        """
        
        # Ensure tensor is on CPU and detach from computation graph
        img_tensor = self.pixels.detach().cpu()
        
        # Convert from float32 [0,1] to uint8 [0,255] in one GPU-friendly operation
        byte_tensor = (img_tensor.clamp(0.0, 1.0) * 255).to(torch.uint8)
        
        # Convert to numpy once for efficient I/O (height, width, 3)
        np_image = byte_tensor.numpy().transpose(1, 0, 2)  # PyTorch (W,H,C) -> PPM (H,W,C)
        
        # Write header
        image_file.write(f"P3 {self.width} {self.height}\n255\n")
        
        # Write pixel data with buffer optimization
        for h in range(self.height):
            row = np_image[h]
            line = " ".join(f"{r} {g} {b}" for r, g, b in row)
            image_file.write(f"{line}\n")