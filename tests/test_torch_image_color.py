import torch

from conftest import *
import pytest

from raytracer_gpu.datatypes.color import Color
from raytracer_gpu.datatypes.image import Image
from raytracer_gpu.datatypes.vector import Vector

device = "cuda" if torch.cuda.is_available() else "cpu"

def test_image_write_ppm():
    """Test full pipeline: create image, set colors, write PPM"""
    # Setup - create 2x2 test image
    width, height = 2, 2
    img = Image(width, height)
    
    # Define test colors with edge cases
    colors = {
        (0, 0): Color.from_rgb(r=1.5, g=-0.5, b=0.0),  # Should clamp to (1.0, 0.0, 0.0)
        (1, 0): Color.from_rgb(r=0.0, g=1.0, b=0.0),    # Pure green
        (0, 1): Color.from_rgb(r=0.0, g=0.0, b=2.0),    # Clamps to (0.0, 0.0, 1.0)
        (1, 1): Color.from_rgb(r=1.0, g=1.0, b=1.0)     # White
    }
    
    # Set pixels using tensor data
    for (x, y), color in colors.items():
        img.set_pixel(x, y, color.get_color)
    
    # Write to temporary file
    with open ('./torch_image.ppm',mode='w') as tmp_file:
        img.write_ppm(tmp_file)
        tmp_path = tmp_file.name
    
    # Verify file contents
    with open(tmp_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    # Check header
    assert lines[0] == "P3 2 2"
    assert lines[1] == "255"
    
    # Check pixel data (PPM writes rows top-to-bottom)
    expected_pixels = [
        ["255 0 0", "0 255 0"],   # First row (y=0)
        ["0 0 255", "255 255 255"] # Second row (y=1)
    ]
    
    current_line = 2
    for y in range(height):
        actual = lines[current_line].split()
        expected = ' '.join(expected_pixels[y]).split()
        
        # Verify RGB components for each pixel in row
        assert actual == expected, f"Row {y} mismatch"
        current_line += 1

def test_from_vector_basic():
    # Create a valid Vector
    vec = Vector(_vector=torch.tensor([0.4, 0.6, 0.8], dtype=torch.float32))
    
    # Convert to Color
    color = Color.from_vector(vec)
    # Verify type and values
    assert isinstance(color, Color)
    assert torch.allclose(color._vector, torch.tensor([0.4, 0.6, 0.8]))


def test_from_vector_batched():
    # Test batch conversion
    batched_vec = Vector(_vector=torch.tensor([
        [0.1, 0.2, 0.3],
        [1.5, -0.5, 2.0]
    ]))
    
    colors = Color.from_vector(batched_vec)
    assert colors.get_color.shape == (2,3)
    assert torch.allclose(colors.get_color, torch.tensor([
        [0.1, 0.2, 0.3],
        [1.0, 0.0, 1.0]
    ]))

def test_from_vector_grad_preservation():
    # Test gradient preservation
    vec = Vector(_vector=torch.tensor([0.5, 0.5, 0.5], requires_grad=True))
    color = Color.from_vector(vec)
    
    assert color._vector.requires_grad
    # Verify computation graph
    (color._vector.sum()).backward()
    assert vec._vector.grad is not None

def test_from_vector_device_consistency():
    # Test device consistency
    vec = Vector(_vector=torch.tensor([0.1, 0.2, 0.3])).to(device)
    color = Color.from_vector(vec)
    
    assert color._vector.device.type == torch.device(device).type

def test_from_vector_invalid_input():
    # Test invalid vector shape
    with pytest.raises(AssertionError):
        invalid_vec = Vector(_vector=torch.tensor([0.1, 0.2]))  # Missing z-component
        Color.from_vector(invalid_vec)