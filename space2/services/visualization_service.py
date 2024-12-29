from typing import Optional, Tuple
import pyvista as pv
from models.container import Container
from models.bin import PackingBin
from utils.logger import setup_logger
from utils.file_loader import get_bin_colors

logger = setup_logger(__name__)

class VisualizationService:
    """
    Service for handling 3D visualization of packed containers.
    """
    def __init__(self):
        # Configure PyVista theme
        pv.global_theme.background = 'white'
        pv.global_theme.window_size = [1024, 768]
        self.colors = get_bin_colors()

    @staticmethod
    def create_box(width: float, height: float, depth: float, position: Tuple[float, float, float]) -> pv.Box:
        """
        Create a box mesh with given dimensions at the specified position.
        
        Args:
            width: Box width
            height: Box height
            depth: Box depth
            position: (x, y, z) position coordinates
            
        Returns:
            pv.Box: PyVista box mesh
        """
        return pv.Box(bounds=(
            position[0], position[0] + width,     # x bounds
            position[1], position[1] + height,    # y bounds
            position[2], position[2] + depth      # z bounds (up)
        ))

    def setup_plotter(self) -> pv.Plotter:
        """
        Create and configure a PyVista plotter.
        
        Returns:
            pv.Plotter: Configured plotter instance
        """
        plotter = pv.Plotter()
        plotter.enable_trackball_style()
        
        # Set initial camera orientation
        plotter.camera_position = [(300, 300, 300), (0, 0, 0), (0, 0, 1)]
        
        # Add camera orientation widget and reset camera button
        plotter.add_camera_orientation_widget()
        plotter.add_text('Press R to reset camera', position='upper_left')
        
        # Add reset camera handlers
        def reset_view(p):
            p.camera_position = [(300, 300, 300), (0, 0, 0), (0, 0, 1)]
        
        plotter.add_key_event('r', lambda: reset_view(plotter))
        plotter.add_key_event('R', lambda: reset_view(plotter))
        
        return plotter

    def add_container(self, plotter: pv.Plotter, container: Container) -> None:
        """
        Add container wireframe to the plot.
        
        Args:
            plotter: PyVista plotter instance
            container: Container to visualize
        """
        container_box = self.create_box(
            container.width,
            container.height,
            container.depth,
            (0, 0, 0)
        )
        plotter.add_mesh(container_box, color='green', opacity=0.2)

    def add_fitted_items(self, plotter: pv.Plotter, container: Container) -> None:
        """
        Add fitted items to the plot.
        
        Args:
            plotter: PyVista plotter instance
            container: Container with fitted items
        """
        for item in container.items:
            box = self.create_box(
                item.width,
                item.height,
                item.depth,
                item.position
            )
            plotter.add_mesh(
                box,
                color=self.colors.get(item.bin_type, 'black'),
                opacity=0.7,
                show_edges=True
            )

    def add_unfitted_items(self, plotter: pv.Plotter, container: Container) -> None:
        """
        Add unfitted items to the plot in a grid layout.
        
        Args:
            plotter: PyVista plotter instance
            container: Container with unfitted items
        """
        if not container.unfitted_items:
            return
            
        grid_size = 5  # Items per row
        spacing = 50   # Space between items
        start_x = container.width + spacing
        
        for i, item in enumerate(container.unfitted_items):
            row = i // grid_size
            col = i % grid_size
            
            position = [
                start_x + (col * spacing),
                row * spacing,
                0
            ]
            
            box = self.create_box(
                item.width,
                item.height,
                item.depth,
                position
            )
            
            plotter.add_mesh(
                box,
                color=self.colors.get(item.bin_type, 'black'),
                opacity=0.4,
                style='wireframe'
            )

    def visualize_packing(self, container: Container, plotter: Optional[pv.Plotter] = None) -> pv.Plotter:
        """
        Create 3D visualization of packed container.
        
        Args:
            container: Container to visualize
            plotter: Optional existing plotter to use
            
        Returns:
            pv.Plotter: Plotter with visualization
        """
        if plotter is None:
            plotter = self.setup_plotter()
        
        self.add_container(plotter, container)
        self.add_fitted_items(plotter, container)
        self.add_unfitted_items(plotter, container)
        
        plotter.show_grid()
        return plotter

    def show_interactive_plot(self, container: Container) -> None:
        """
        Show interactive 3D plot and save screenshot.
        
        Args:
            container: Container to visualize
        """
        try:
            # Create off-screen plotter for screenshot
            plotter = pv.Plotter(off_screen=True)
            plotter = self.visualize_packing(container, plotter)
            plotter.screenshot('packing_visualization.png')
            logger.info("Visualization saved to 'packing_visualization.png'")
            
            # Create new plotter for interactive display
            plotter = self.visualize_packing(container)
            plotter.show()
        except Exception as e:
            logger.error(f"Error showing plot: {e}")
