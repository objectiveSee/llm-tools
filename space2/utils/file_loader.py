import csv
from typing import Dict, List, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)

def load_tsv_file(filepath: str) -> List[Dict[str, str]]:
    """
    Load data from a TSV file into a list of dictionaries.
    
    Args:
        filepath: Path to the TSV file
        
    Returns:
        List[Dict[str, str]]: List of dictionaries where each dictionary represents a row
    """
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            return list(reader)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error reading {filepath}: {str(e)}")
        raise

def load_container_data() -> Dict[str, str]:
    """
    Load container information from Container.tsv
    
    Returns:
        Dict[str, str]: Dictionary containing container data
    """
    container_data = load_tsv_file('Container.tsv')
    logger.debug(f"Loading container: {container_data[0]['ID']}")
    return container_data[0]

def load_bins_data() -> List[Dict[str, str]]:
    """
    Load bins information from Bins.tsv
    
    Returns:
        List[Dict[str, str]]: List of dictionaries containing bin data
    """
    bins_data = load_tsv_file('Bins.tsv')
    logger.debug(f"Loaded {len(bins_data)} bin types")
    return bins_data

def get_bin_colors() -> Dict[str, str]:
    """
    Get color mappings for bin types from Bins.tsv
    
    Returns:
        Dict[str, str]: Dictionary mapping bin types to their colors
    """
    try:
        bins_data = load_bins_data()
        colors = {}
        for row in bins_data:
            bin_type = row['Type']
            # Use specified color if available, otherwise default to black
            color = row.get('Color', '').strip() or 'black'
            colors[bin_type] = color
        return colors
    except Exception as e:
        logger.error(f"Error reading colors from Bins.tsv: {e}")
        return {}
