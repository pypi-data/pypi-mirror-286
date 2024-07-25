"""Module for defining allowed context structures.

This module provides a TypedDict for specifying the structure of allowed contexts
used in logging, including device IMEI, packet creation and processed times, and truck ID.
"""

from datetime import datetime
from typing import TypedDict


class AllowedContext(TypedDict, total=False):
    """
    Defines the structure of the allowed context for logging.

    Attributes:
        imei (str | int): The IMEI number of the device.
        packet_created_time (str): The creation time of the packet.
        packet_processed_time (str): The processed time of the packet.
        truck_id (str | int): The ID of the truck.
    """

    imei: str | int
    packet_created_time: str | datetime
    packet_processed_time: str | datetime
    truck_id: str | int
