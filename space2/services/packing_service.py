from typing import List
from py3dbp import Packer
from models.container import Container
from models.bin import PackingBin
from utils.logger import setup_logger
from utils.file_loader import load_bins_data

logger = setup_logger(__name__)

class PackingService:
    """
    Service for handling bin packing operations.
    """
    @staticmethod
    def load_bins() -> List[PackingBin]:
        """
        Load bins from Bins.tsv and convert to PackingBin instances.
        
        Returns:
            List[PackingBin]: List of bins to be packed
        """
        bins_data = load_bins_data()
        bins = []
        
        for row in bins_data:
            # Create multiple items based on quantity
            for i in range(int(row['Quantity'])):
                bin_item = PackingBin(
                    name=f"{row['Type']}_{i+1}",
                    width=float(row['Width']),
                    height=float(row['Height']),
                    depth=float(row['Depth']),
                    weight=float(row['Weight'])
                )
                bins.append(bin_item)
        
        return bins

    @staticmethod
    def apply_gravity(container: Container) -> None:
        """
        Apply gravity to make items rest on surfaces below them.
        
        Args:
            container: Container with items to apply gravity to
        """
        # Sort items by Z position (bottom to top)
        container.items.sort(key=lambda x: x.position[2])
        
        for i, item in enumerate(container.items):
            # Start at container floor
            min_height = 0
            
            # Check all items below this one for collision
            for other in container.items[:i]:
                # If there's overlap in X-Y plane, this item must rest on top of the other
                if item.overlaps_xy(other):
                    min_height = max(min_height, other.get_top_surface_height())
            
            # Move item down to rest on highest surface below it
            if item.position[2] > min_height:
                item.position[2] = min_height

    def pack_bins(self, container: Container) -> Container:
        """
        Pack bins into the container using py3dbp Packer for optimal fitting.
        
        Args:
            container: Container to pack bins into
            
        Returns:
            Container: Container with packed items
        """
        # Load bins
        bins = self.load_bins()
        
        # Create packer instance and add container
        packer = Packer()
        packer.add_bin(container.to_py3dbp_bin())
        
        # Sort bins by height (Z dimension) in descending order
        bins.sort(key=lambda x: x.depth, reverse=True)
        
        # Add all bins to the packer
        for bin_item in bins:
            packer.add_item(bin_item.to_py3dbp_item())
        
        # Run the packing algorithm
        packer.pack(
            bigger_first=True,
            distribute_items=False,  # Don't spread items across container
            number_of_decimals=0
        )
        
        # Get the container results
        container_result = packer.bins[0]  # We only have one container
        
        # Process fitted items
        for item in container_result.items:
            fitted_item = PackingBin.from_py3dbp_item(item)
            container.add_fitted_item(fitted_item)
        
        # Process unfitted items
        for item in container_result.unfitted_items:
            unfitted_item = PackingBin.from_py3dbp_item(item)
            container.add_unfitted_item(unfitted_item)
        
        # Apply gravity to make items rest on surfaces below them
        self.apply_gravity(container)
        
        # Log results
        logger.info(f'Packed {len(container.items)} bins into container')
        logger.info(f'Unable to pack {len(container.unfitted_items)} bins')
        
        # Print packing summary without position details
        print(container.get_packing_summary(include_positions=False))
        
        return container
