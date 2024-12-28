import csv
from py3dbp import Packer, Item
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
    """Pack bins into a simple row without container fitting"""
    # Load bins
    bins = load_bins()
    
    # Group bins by type
    bin_groups = {}
    for bin_item in bins:
        bin_type = bin_item.name.split('_')[0]
        if bin_type not in bin_groups:
            bin_groups[bin_type] = []
        bin_groups[bin_type].append(bin_item)
    
    # Place bins in order: XL -> Large -> Medium -> Small
    fitted_items = []
    current_x = 0
    spacing = 2  # Increased spacing between bins
    
    for bin_type in ['XL', 'Large', 'Medium', 'Small']:
        if bin_type not in bin_groups:
            continue
            
        # Add extra spacing between different bin types
        if fitted_items:  # If we already placed some bins
            current_x += spacing * 2  # Extra spacing between different types
            
        for bin_item in bin_groups[bin_type]:
            bin_item.rotation_type = 0  # No rotation
            bin_item.position = [float(current_x), 0.0, 0.0]  # Place at ground level
            fitted_items.append(bin_item)
            
            # Move x position for next bin
            current_x += bin_item.width + spacing  # Add spacing between bins
    
    # Update container with results
    container.items = fitted_items
    container.unfitted_items = []  # No unfitted items since we're not checking container bounds
    
    logger.info(f'Placed {len(container.items)} bins in a row')
    print(f"\nPlacement Results:")
    print(f"Total bins placed: {len(container.items)}")
    
    # Print positions of bins
    print("\nBin positions:")
    for item in container.items:
        print(f"{item.name}: Position ({item.position[0]}, {item.position[1]}, {item.position[2]})")
    
    return container
