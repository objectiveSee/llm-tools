import pyvista as pv
import numpy as np

def create_box(width, height, depth, center):
    """Create a box mesh with given dimensions and center point"""
    # Create a box with dimensions centered at origin
    box = pv.Box(bounds=(-width/2, width/2, 
                        -height/2, height/2, 
                        -depth/2, depth/2))
    
    # Move box to correct position
    box.translate((
        center[0] + width/2,  # x position
        center[1] + height/2, # y position
        center[2] + depth/2   # z position
    ))
    
    return box

def visualize_packing(container, plotter=None):
    """Create 3D visualization of packed container"""
    if plotter is None:
        plotter = pv.Plotter()
    
    # Create container wireframe
    container_box = create_box(container.width, container.height, container.depth, (0, 0, 0))
    plotter.add_mesh(container_box, style='wireframe', color='black', line_width=2)
    
    # Color map for different bin types
    colors = {
        'Small': 'red',
        'Medium': 'blue',
        'Large': 'green',
        'XL': 'yellow'
    }
    
    # Add each packed item
    for item in container.items:
        # Get bin type from name (e.g., "Small_1" -> "Small")
        bin_type = item.name.split('_')[0]
        
        # Create box for item
        box = create_box(
            item.width,
            item.height,
            item.depth,
            item.position
        )
        
        # Add to plot with slight transparency
        plotter.add_mesh(box, color=colors[bin_type], opacity=0.7)
    
    # Set camera position for better initial view
    plotter.camera_position = 'iso'
    plotter.show_grid()
    
    return plotter

def show_interactive_plot(container):
    """Show interactive 3D plot"""
    plotter = visualize_packing(container)
    plotter.show()

if __name__ == '__main__':
    # Test visualization with sample data
    from main import load_container
    from packing import pack_bins
    
    container = load_container()
    packed_container = pack_bins(container)
    show_interactive_plot(packed_container)
