from models.container import Container
from services.packing_service import PackingService
from services.visualization_service import VisualizationService
from utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """Main entry point for the bin packing application."""
    try:
        # Create container from data
        logger.info('Loading container from Container.tsv')
        container = Container.from_data()
        
        # Log container details
        logger.info(f'Loaded container:')
        print(f"Container: {container.name}")
        print(f"  Dimensions: {container.width} x {container.height} x {container.depth}")
        print(f"  Max Weight: {container.max_weight}")
        
        # Pack bins into container
        packing_service = PackingService()
        packed_container = packing_service.pack_bins(container)
        
        # Show 3D visualization
        visualization_service = VisualizationService()
        visualization_service.show_interactive_plot(packed_container)
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == '__main__':
    main()
