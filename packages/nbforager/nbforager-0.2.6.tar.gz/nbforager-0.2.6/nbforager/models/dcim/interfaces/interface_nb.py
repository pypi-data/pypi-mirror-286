"""Netbox.dcim.interfaces model."""
from pydantic import BaseModel, Field


class InterfaceNb(BaseModel):  # TODO test
    """Netbox.dcim.interfaces model."""

    device: int = Field(ge=0, description="Device id")
    name: str = Field(max_length=100, description="Interface name")
    type: str = Field(default="1000base-x-sfp", max_length=50, description="Interface type")
    enabled: bool = Field(default=True, description="Administrative status")
    mgmt_only: bool = Field(default=False, description="Management interface")
    description: str = Field(max_length=200, description="Interface description")
