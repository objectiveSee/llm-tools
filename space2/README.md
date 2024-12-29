# 3D Bin Packing Visualization

A Python application for optimizing and visualizing 3D bin packing in containers.

## Project Structure

```
.
├── models/
│   ├── container.py     # Container model
│   └── bin.py          # Bin model
├── services/
│   ├── packing_service.py     # Bin packing logic
│   └── visualization_service.py # 3D visualization
├── utils/
│   ├── logger.py       # Logging configuration
│   └── file_loader.py  # Data file loading utilities
├── main.py             # Application entry point
├── Bins.tsv           # Bin specifications
├── Container.tsv      # Container specifications
└── requirements.txt   # Project dependencies
```

## Features

- Optimized 3D bin packing algorithm
- Interactive 3D visualization
- Support for multiple bin types and quantities
- Gravity simulation for realistic packing
- Automatic screenshot generation
- Comprehensive logging

## Data Files

### Container.tsv
Defines the container dimensions and weight limit:
- ID: Container identifier
- Width: Container width
- Height: Container height
- Depth: Container depth
- MaxWeight: Maximum weight capacity

### Bins.tsv
Defines the bins to be packed:
- Type: Bin type identifier
- Width: Bin width
- Height: Bin height
- Depth: Bin depth
- Weight: Bin weight
- Quantity: Number of bins of this type
- Color: Visualization color (optional)

## Running the Project

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Visualization Controls

- Mouse: Rotate view
- Scroll: Zoom in/out
- R: Reset camera position
- Left panel: Camera orientation widget

## Output

- Console output shows packing results and statistics
- Interactive 3D visualization window
- Screenshot saved as 'packing_visualization.png'
- Detailed logs in 'app.log'
