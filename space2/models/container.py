from typing import List, Optional
from py3dbp import Bin as Py3dbpBin
from models.bin import PackingBin
from utils.file_loader import load_container_data

class Container:
    """
    Represents a container that can hold multiple bins.
    """
    def __init__(self, name: str, width: float, height: float, depth: float, max_weight: float):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.max_weight = max_weight
        self.items: List[PackingBin] = []
        self.unfitted_items: List[PackingBin] = []

    @classmethod
    def from_data(cls) -> 'Container':
        """
        Create a Container instance from Container.tsv data.
        
        Returns:
            Container: New Container instance
        """
        data = load_container_data()
        return cls(
            name=data['ID'],
            width=float(data['Width']),
            height=float(data['Height']),
            depth=float(data['Depth']),
            max_weight=float(data['MaxWeight'])
        )

    def to_py3dbp_bin(self) -> Py3dbpBin:
        """
        Convert to py3dbp Bin format for packing algorithm.
        
        Returns:
            Py3dbpBin: Container in py3dbp format
        """
        return Py3dbpBin(
            self.name,
            self.width,
            self.height,
            self.depth,
            self.max_weight
        )

    def add_fitted_item(self, item: PackingBin) -> None:
        """Add a successfully fitted item to the container."""
        self.items.append(item)

    def add_unfitted_item(self, item: PackingBin) -> None:
        """Add an item that couldn't be fitted to the unfitted items list."""
        self.unfitted_items.append(item)

    def get_volume(self) -> float:
        """
        Calculate the total volume of the container.
        
        Returns:
            float: Container volume in cubic units
        """
        return self.width * self.height * self.depth

    def get_packed_volume(self) -> float:
        """
        Calculate the total volume of all packed bins.
        
        Returns:
            float: Total volume of packed bins in cubic units
        """
        return sum(item.get_volume() for item in self.items)

    def get_unpacked_volume(self) -> float:
        """
        Calculate the total volume of all unpacked bins.
        
        Returns:
            float: Total volume of unpacked bins in cubic units
        """
        return sum(item.get_volume() for item in self.unfitted_items)

    def get_volume_utilization(self) -> float:
        """
        Calculate the volume utilization percentage.
        
        Returns:
            float: Volume utilization as a percentage
        """
        container_volume = self.get_volume()
        if container_volume == 0:
            return 0.0
        return (self.get_packed_volume() / container_volume) * 100

    def get_packing_summary(self, include_positions: bool = False) -> str:
        """
        Get a summary of the packing results.
        
        Args:
            include_positions: Whether to include detailed bin positions in the summary
            
        Returns:
            str: Summary of fitted and unfitted items
        """
        summary = [
            f"\nPacking Results:",
            f"Successfully packed: {len(self.items)} bins",
            f"Unable to pack: {len(self.unfitted_items)} bins",
            f"\nVolume Analysis:",
            f"Container Volume: {self.get_volume():.2f} cubic units",
            f"Packed Volume: {self.get_packed_volume():.2f} cubic units",
            f"Unpacked Volume: {self.get_unpacked_volume():.2f} cubic units",
            f"Volume Utilization: {self.get_volume_utilization():.1f}%"
        ]
        
        if include_positions:
            summary.append("\nBin positions:")
            for item in self.items:
                summary.append(
                    f"{item.name}: Position ({item.position[0]}, {item.position[1]}, {item.position[2]}), "
                    f"Rotation {item.rotation_type}"
                )
        
        if self.unfitted_items:
            summary.append("\nUnfitted bins:")
            for item in self.unfitted_items:
                summary.append(f"{item.name}")
        
        return "\n".join(summary)
