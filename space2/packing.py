import csv
from py3dbp import Packer, Item, Bin
import logging

logger = logging.getLogger(__name__)

def load_bins():
    """Load bin information from Bins.tsv"""
    bins = []
    with open('Bins.tsv', 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            # Create multiple items based on quantity
            for i in range(int(row['Quantity'])):
                bin_item = Item(
                    name=f"{row['Type']}_{i+1}",
                    width=float(row['Width']),
                    height=float(row['Height']),
                    depth=float(row['Depth']),
                    weight=float(row['Weight'])
                )
                bins.append(bin_item)
    return bins

def pack_bins(container):
    """Pack bins into the container using py3dbp Packer for optimal fitting"""
    # Load bins
    bins = load_bins()
    
    # Create packer instance
    packer = Packer()
    
    # Create and add container from Container.tsv dimensions
    container_bin = Bin("Container1", float(232), float(238), float(468), float(44000))
    packer.add_bin(container_bin)
    
    # Add all bins to the packer
    for bin_item in bins:
        packer.add_item(Item(bin_item.name, bin_item.width, bin_item.height, bin_item.depth, bin_item.weight))
    
    # Run the packing algorithm
    packer.pack(
        bigger_first=True,
        distribute_items=True,
        number_of_decimals=0
    )
    
    # Get the container results
    container_result = packer.bins[0]  # We only have one container
    
    # Update our container with fitted and unfitted items
    fitted_items = []
    unfitted_items = []
    
    # Process fitted items
    for item in container_result.items:
        # Create Item object with position from packing result
        fitted_item = Item(
            name=item.name,
            width=float(str(item.width)),
            height=float(str(item.height)),
            depth=float(str(item.depth)),
            weight=float(str(item.weight))
        )
        # Ensure all position values are float type by converting through string
        fitted_item.position = [
            float(str(item.position[0])), 
            float(str(item.position[1])), 
            float(str(item.position[2]))
        ]
        fitted_item.rotation_type = item.rotation_type
        fitted_items.append(fitted_item)
    
    # Process unfitted items
    for item in container_result.unfitted_items:
        unfitted_item = Item(
            name=item.name,
            width=float(str(item.width)),
            height=float(str(item.height)),
            depth=float(str(item.depth)),
            weight=float(str(item.weight))
        )
        unfitted_items.append(unfitted_item)
    
    # Update container with results
    container.items = fitted_items
    container.unfitted_items = unfitted_items
    
    # Log results
    logger.info(f'Packed {len(fitted_items)} bins into container')
    logger.info(f'Unable to pack {len(unfitted_items)} bins')
    
    print(f"\nPacking Results:")
    print(f"Successfully packed: {len(fitted_items)} bins")
    print(f"Unable to pack: {len(unfitted_items)} bins")
    
    # Print positions of fitted bins
    print("\nBin positions:")
    for item in fitted_items:
        print(f"{item.name}: Position ({item.position[0]}, {item.position[1]}, {item.position[2]}), "
              f"Rotation {item.rotation_type}")
    
    # Print unfitted bins if any
    if unfitted_items:
        print("\nUnfitted bins:")
        for item in unfitted_items:
            print(f"{item.name}")
    
    return container
