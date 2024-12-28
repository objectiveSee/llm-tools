import logging
import csv
from py3dbp import Packer, Bin, Item

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Create a logger
logger = logging.getLogger(__name__)

def load_container():
    """Load container information from Container.tsv"""
    with open('Container.tsv', 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        container_data = next(reader)  # Get first row
        logger.debug(f"Loading container: {container_data['ID']}")
        return Bin(
            name=container_data['ID'],
            width=float(container_data['Width']),
            height=float(container_data['Height']),
            depth=float(container_data['Depth']),
            max_weight=float(container_data['MaxWeight'])
        )

def main():
    logger.info('Loading container from Container.tsv')
    container = load_container()
    
    logger.info(f'Loaded container:')
    print(f"Container: {container.name}")
    print(f"  Dimensions: {container.width} x {container.height} x {container.depth}")
    print(f"  Max Weight: {container.max_weight}")
    
    # Pack bins into container
    from packing import pack_bins
    packed_container = pack_bins(container)
    
    # Show 3D visualization
    from visualize import show_interactive_plot
    show_interactive_plot(packed_container)

if __name__ == '__main__':
    main()
