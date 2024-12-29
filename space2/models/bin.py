from typing import List, Optional
from py3dbp import Item as Py3dbpItem

class PackingBin:
    """
    Represents a bin that can be packed into a container.
    """
    def __init__(
        self,
        name: str,
        width: float,
        height: float,
        depth: float,
        weight: float,
        position: Optional[List[float]] = None,
        rotation_type: int = 0
    ):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.position = position or [0.0, 0.0, 0.0]
        self.rotation_type = rotation_type

    @classmethod
    def from_py3dbp_item(cls, item: Py3dbpItem) -> 'PackingBin':
        """
        Create a PackingBin instance from a py3dbp Item.
        
        Args:
            item: py3dbp Item instance
            
        Returns:
            PackingBin: New PackingBin instance
        """
        return cls(
            name=item.name,
            width=float(str(item.width)),
            height=float(str(item.height)),
            depth=float(str(item.depth)),
            weight=float(str(item.weight)),
            position=[
                float(str(item.position[0])),
                float(str(item.position[1])),
                float(str(item.position[2]))
            ] if item.position else None,
            rotation_type=item.rotation_type
        )

    def to_py3dbp_item(self) -> Py3dbpItem:
        """
        Convert to py3dbp Item format for packing algorithm.
        
        Returns:
            Py3dbpItem: Bin in py3dbp format
        """
        return Py3dbpItem(
            self.name,
            self.width,
            self.height,
            self.depth,
            self.weight
        )

    @property
    def bin_type(self) -> str:
        """
        Get the type of bin from its name (e.g., "Small_1" -> "Small").
        
        Returns:
            str: Bin type
        """
        return self.name.split('_')[0]

    def overlaps_xy(self, other: 'PackingBin') -> bool:
        """
        Check if this bin overlaps with another bin in the X-Y plane.
        
        Args:
            other: Another PackingBin instance to check overlap with
            
        Returns:
            bool: True if bins overlap in X-Y plane
        """
        x_overlap = (
            self.position[0] < other.position[0] + other.width and
            self.position[0] + self.width > other.position[0]
        )
        y_overlap = (
            self.position[1] < other.position[1] + other.height and
            self.position[1] + self.height > other.position[1]
        )
        return x_overlap and y_overlap

    def get_top_surface_height(self) -> float:
        """
        Get the height of the top surface of this bin.
        
        Returns:
            float: Z-coordinate of the top surface
        """
        return self.position[2] + self.depth

    def get_volume(self) -> float:
        """
        Calculate the volume of this bin.
        
        Returns:
            float: Volume in cubic units
        """
        return self.width * self.height * self.depth
