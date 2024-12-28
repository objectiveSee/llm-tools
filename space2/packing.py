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

def load_container():
    """Load container information from Container.tsv"""
    with open('Container.tsv', 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        container_data = next(reader)  # Get first (and only) row
        return container_data

def pack_bins(container):
    """Pack bins into the container using py3dbp Packer for optimal fitting"""
    # Load bins and container
    bins = load_bins()
    container_data = load_container()
    
    # Create packer instance
    packer = Packer()
    
    # Create and add container from Container.tsv dimensions
    container_bin = Bin(
        "Container1",
        float(container_data['Width']),
        float(container_data['Height']),
        float(container_data['Depth']),
        float(container_data['MaxWeight'])
    )
    packer.add_bin(container_bin)
    
    # Sort bins by height (Z dimension) in descending order
    bins.sort(key=lambda x: x.depth, reverse=True)
    
    # Add all bins to the packer
    for bin_item in bins:
        packer.add_item(Item(bin_item.name, bin_item.width, bin_item.height, bin_item.depth, bin_item.weight))
    
    # Run the packing algorithm
    packer.pack(
        bigger_first=True,
        distribute_items=False,  # Don't spread items across container
        number_of_decimals=0
    )
    
    # Get the container results
    container_result = packer.bins[0]  # We only have one container
    
    # Update our container with fitted and unfitted items
    fitted_items = []
    unfitted_items = []
    
    # Convert items to our format and get their initial positions
    for item in container_result.items:
        fitted_item = Item(
            name=item.name,
            width=float(str(item.width)),
            height=float(str(item.height)),
            depth=float(str(item.depth)),
            weight=float(str(item.weight))
        )
        fitted_item.position = [
            float(str(item.position[0])), 
            float(str(item.position[1])), 
            float(str(item.position[2]))
        ]
        fitted_item.rotation_type = item.rotation_type
        fitted_items.append(fitted_item)
    
    # Sort items by Z position (bottom to top)
    fitted_items.sort(key=lambda x: x.position[2])
    
    # Apply gravity to each item
    for i, item in enumerate(fitted_items):
        # Start at container floor
        min_height = 0
        
        # Check all items below this one for collision
        for other in fitted_items[:i]:
            # Check if items overlap in X-Y plane (horizontal plane)
            x_overlap = (
                item.position[0] < other.position[0] + other.width and 
                item.position[0] + item.width > other.position[0]
            )
            y_overlap = (
                item.position[1] < other.position[1] + other.height and 
                item.position[1] + item.height > other.position[1]
            )
            
            # If there's overlap in X-Y plane, this item must rest on top of the other
            if x_overlap and y_overlap:
                min_height = max(min_height, other.position[2] + other.depth)
        
        # Move item down to rest on highest surface below it
        current_height = item.position[2]
        if current_height > min_height:
            # Only move down if item is floating
            item.position[2] = min_height
    
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
