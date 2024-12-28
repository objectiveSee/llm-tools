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
    """Basic packing of bins into container"""
    # Create packer
    packer = Packer()
    
    # Add the container
    packer.add_bin(container)
    
    # Load and add all bins
    bins = load_bins()
    for bin_item in bins:
        packer.add_item(bin_item)
    
    # Pack items
    logger.info('Starting packing process')
    packer.pack()
    
    # Get first (and only) container
    container = packer.bins[0]
    
    # Print results
    logger.info(f'Packing complete. Fitted {len(container.items)} items')
    print(f"\nPacking Results:")
    print(f"Items packed: {len(container.items)}/{len(bins)}")
    print(f"Unfitted items: {len(packer.unfit_items)}")
    
    # Print positions of fitted items
    print("\nFitted items positions:")
    for item in container.items:
        print(f"{item.name}: Position ({item.position[0]}, {item.position[1]}, {item.position[2]})")
    
    return container
