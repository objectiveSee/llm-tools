import pyvista as pv
import numpy as np

def create_box(width, height, depth, position):
    """Create a box mesh with given dimensions at the specified position"""
    # Create box using corner coordinates
    # Note: position is the front-bottom-left corner (x,y,z)
    box = pv.Box(bounds=(
        position[0], position[0] + width,           # x bounds
        position[1], position[1] + height,          # y bounds
        position[2], position[2] + depth            # z bounds
    ))
    
    return box

def visualize_packing(container, plotter=None):
    """Create 3D visualization of packed container"""
    # Use default theme
    pv.global_theme.background = 'white'
    pv.global_theme.window_size = [1024, 768]
    
    if plotter is None:
        plotter = pv.Plotter()
        # Set trackball mode and camera controls
        plotter.enable_trackball_style()
        # Set initial camera orientation
        plotter.camera.azimuth = 180  # Rotate initial view 180 degrees
    
    # Create container wireframe
    container_box = create_box(container.width, container.height, container.depth, (0, 0, 0))
    # Add container with green color
    plotter.add_mesh(container_box, color='green', opacity=0.2)
    
    # Color map for different bin types
    colors = {
        'Small': 'tan',
        'Medium': 'tan',
        'Large': 'tan',
        'XL': 'tan'
    }
    
    # Add each packed item
    for item in container.items:
        # Get bin type from name (e.g., "Small_1" -> "Small")
        bin_type = item.name.split('_')[0]
        
        # Create box for item at its position
        box = create_box(
            item.width,
            item.height,
            item.depth,
            item.position
        )
        
        # Add to plot with slight transparency and edges visible
        plotter.add_mesh(box, color=colors[bin_type], opacity=0.7, show_edges=True)
    
    # Add unfitted items in a grid layout outside the container
    if hasattr(container, 'unfitted_items'):
        grid_size = 5  # Number of items per row in the grid
        spacing = 50   # Space between items
        start_x = container.width + spacing  # Start position X
        
        for i, item in enumerate(container.unfitted_items):
            # Calculate grid position
            row = i // grid_size
            col = i % grid_size
            
            # Get bin type
            bin_type = item.name.split('_')[0]
            
            # Create box for unfitted item
            position = [
                start_x + (col * spacing),
                row * spacing,
                0
            ]
            
            box = create_box(
                item.width,
                item.height,
                item.depth,
                position
            )
            
            # Add to plot with different opacity to distinguish from fitted items
            plotter.add_mesh(box, color=colors[bin_type], opacity=0.4, style='wireframe')
    
    # Set camera position for better initial view
    plotter.camera_position = 'iso'
    plotter.show_grid()
    
    return plotter

def show_interactive_plot(container):
    """Show interactive 3D plot"""
    try:
        # Create plotter with off-screen rendering
        plotter = pv.Plotter(off_screen=True)
        plotter = visualize_packing(container, plotter)
        
        # Save to file
        plotter.screenshot('packing_visualization.png')
        print("Visualization saved to 'packing_visualization.png'")
        
        # Try to show interactive plot
        plotter = visualize_packing(container)  # New plotter for interactive display
        plotter.show()
    except Exception as e:
        print(f"Error showing plot: {e}")

if __name__ == '__main__':
    # Test visualization with sample data
    from main import load_container
    from packing import pack_bins
    
    container = load_container()
    packed_container = pack_bins(container)
    show_interactive_plot(packed_container)
