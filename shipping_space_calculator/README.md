# Shipping Space Calculator

A powerful Python-based shipping container space optimization system that helps calculate and visualize how to pack items into standard shipping containers.

> **Note**: If your environment is already set up with the required dependencies (`py3dbp`, `matplotlib`, `numpy`), you can skip the installation section and jump straight to the [Quick Start](#quick-start) guide.

## Features

- Support for multiple container sizes (20ft, 40ft)
- Handles both standard bin sizes and custom items
- 3D visualization of packing arrangements
- Detailed packing reports and statistics
- Stack height constraint enforcement
- Volume utilization tracking
- Multiple viewing angles for visualizations

## Installation

1. Clone the repository
2. Create and activate a virtual environment:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

# Your prompt should change to indicate the virtual environment is active
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

> **Note**: Always ensure your virtual environment is activated before running the calculator. You'll know it's activated when you see `(venv)` at the beginning of your terminal prompt.

## Quick Start

```python
from shipping_calculator import ShippingCalculator
from visualizer import visualize_packing, save_visualization

# Initialize calculator (20ft or 40ft container)
calc = ShippingCalculator("20ft")
container = calc.add_container()

# Add standard bins
bin_quantities = {
    "small": 5,    # 5 small bins
    "medium": 3,   # 3 medium bins
    "large": 2,    # 2 large bins
    "xl": 1        # 1 extra large bin
}
calc.add_standard_bins(bin_quantities)

# Add custom items (width, height, depth in inches)
calc.add_custom_item("custom-item", (30, 25, 40), weight=175)

# Calculate packing arrangement
results = calc.calculate_packing()

# Print detailed report
calc.print_packing_report(results)

# Create and save visualization
fig = visualize_packing(calc.container, results["packed_items"])
save_visualization(fig, "packing_visualization.png")
```

## Container Specifications

### Available Container Types
- **20ft Container**: 232"(W) × 238"(H) × 468"(D)
- **40ft Container**: 232"(W) × 238"(H) × 936"(D)

### Standard Bin Sizes
- **Small**: 12"(W) × 12"(H) × 18"(D), Max weight: 50 lbs
- **Medium**: 18"(W) × 18"(H) × 24"(D), Max weight: 100 lbs
- **Large**: 24"(W) × 24"(H) × 36"(D), Max weight: 150 lbs
- **XL**: 36"(W) × 36"(H) × 48"(D), Max weight: 200 lbs

## API Reference

### ShippingCalculator Class

```python
calc = ShippingCalculator(container_type="20ft")
```

#### Methods

- `add_container()`: Initialize the shipping container
- `add_standard_bins(bin_quantities: dict)`: Add multiple standard bins
- `add_custom_item(name: str, dimensions: Tuple[float, float, float], weight: float)`: Add custom-sized item
- `calculate_packing()`: Calculate optimal packing arrangement
- `print_packing_report(results: dict)`: Print detailed packing report

### Visualization Functions

```python
from visualizer import visualize_packing, save_visualization

# Create visualization
fig = visualize_packing(container, packed_items)

# Save to file
save_visualization(fig, "output.png")
```

## Packing Results

The `calculate_packing()` method returns a dictionary containing:

```python
{
    "success": bool,              # True if all items packed successfully
    "packed_items": List[Item],   # Successfully packed items
    "unpacked_items": List[Item], # Items that couldn't be packed
    "volume_utilization": float,  # Container volume utilization percentage
    "total_volume_used": float,   # Total volume of packed items
    "container_volume": float,    # Total container volume
    "max_height_violated": bool   # True if stack height limit exceeded
}
```

## Visualization Output

The system generates 3D visualizations showing:
- Container boundaries (transparent gray)
- Packed items (colored boxes)
- Item labels
- Grid for size reference
- Multiple viewing angles

The visualization is saved as a PNG file and includes:
- Axis labels (Width, Depth, Height in inches)
- Container type in title
- Color-coded items for easy identification

## Example Output

Running the example code will generate:
1. A detailed console report showing packing arrangement
2. A PNG file with the 3D visualization
3. Statistics including volume utilization and packing success

## Notes

- Stack height constraints are automatically enforced
- Items are packed considering weight limits
- The system provides warnings for unpacked items or height violations
- Visualizations can be used to guide actual loading operations

## Practical Example: Multiple Box Calculation

Here's a complete example of calculating space for multiple boxes of the same type:

```python
from shipping_calculator import ShippingCalculator
from visualizer import visualize_packing, save_visualization

# Create calculator for a 20ft container
calc = ShippingCalculator("20ft")

# Add the container
calc.add_container()

# Add multiple boxes of the same type
bin_quantities = {
    "large": 20,   # 20 large boxes
    "medium": 20   # 20 medium boxes
}
calc.add_standard_bins(bin_quantities)

# Calculate packing
results = calc.calculate_packing()

# Print detailed report
calc.print_packing_report(results)

# Create and save visualization
fig = visualize_packing(calc.container, results["packed_items"])
save_visualization(fig, "packing_visualization_multiple_boxes.png")
```

This script will:
1. Calculate if all boxes fit in a 20ft container
2. Generate a detailed report showing the position of each box
3. Create a 3D visualization of the packing arrangement
4. Show volume utilization statistics

Remember to run this script in your activated virtual environment:
```bash
source venv/bin/activate  # On macOS/Linux
python your_script.py
```
