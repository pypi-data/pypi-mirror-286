from pathlib import Path
from typing import Self
from uuid import uuid4

from geojson_pydantic import Feature, Point, Polygon  # type: ignore
from pydantic import UUID4, Field

from ephemerista import BaseModel, bodies
from ephemerista.assets import Asset, AssetKey, asset_id
from ephemerista.comms.channels import Channel
from ephemerista.coords.trajectories import Trajectory
from ephemerista.coords.twobody import DEFAULT_FRAME, DEFAULT_ORIGIN, Origin
from ephemerista.frames import ReferenceFrame
from ephemerista.time import Time


class Ensemble(BaseModel):
    trajectories: dict[UUID4, Trajectory]

    def __getitem__(self, asset: AssetKey) -> Trajectory:
        return self.get(asset)

    def get(self, asset: AssetKey) -> Trajectory:
        return self.trajectories[asset_id(asset)]


class Scenario(BaseModel):
    scenario_id: UUID4 = Field(alias="id", default_factory=uuid4)
    name: str = Field(description="The name of the scenario", default="Scenario")
    start_time: Time
    end_time: Time
    time_step: float = Field(default=60)
    origin: Origin = Field(
        default=DEFAULT_ORIGIN,
        discriminator=bodies.DISCRIMINATOR,
        description="Origin of the coordinate system",
    )
    frame: ReferenceFrame = Field(default=DEFAULT_FRAME, description="Reference frame of the coordinate system")
    assets: list[Asset] = Field(default=[])
    channels: list[Channel] = Field(default=[])
    points_of_interest: list[Feature[Point, dict]] = Field(default=[])
    areas_of_interest: list[Feature[Polygon, dict]] = Field(default=[])

    @classmethod
    def load_from_file(cls, path: Path | str) -> Self:
        if isinstance(path, str):
            path = Path(path)
        json = path.read_text()
        return cls.model_validate_json(json)

    def get_asset(self, asset: AssetKey | str) -> Asset:
        if isinstance(asset, str):
            return next(a for a in self.assets if a.name == asset)
        return next(a for a in self.assets if a.asset_id == asset_id(asset))

    def __getitem__(self, asset: AssetKey | str) -> Asset:
        return self.get_asset(asset)

    def channel_by_id(self, channel_id: UUID4) -> Channel:
        return next(c for c in self.channels if c.channel_id == channel_id)

    def times(self) -> list[Time]:
        return self.start_time.trange(self.end_time, self.time_step)

    def propagate(self) -> Ensemble:
        trajectories = {asset.asset_id: asset.model.propagate(self.times()) for asset in self.assets}
        return Ensemble(trajectories=trajectories)
