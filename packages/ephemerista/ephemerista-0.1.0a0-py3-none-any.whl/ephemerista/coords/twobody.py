from __future__ import annotations

import abc
from typing import Literal, Self

import lox_space as lox
import numpy as np
from pydantic import Field, PrivateAttr

from ephemerista import BaseModel, bodies
from ephemerista.angles import Angle
from ephemerista.coords import N_DIMS, anomalies, shapes
from ephemerista.coords.anomalies import MeanAnomaly, TrueAnomaly
from ephemerista.frames import ReferenceFrame
from ephemerista.time import Time

type Origin = bodies.Barycenter | bodies.CelestialBody

DEFAULT_ORIGIN: Origin = bodies.Planet(name="Earth")
DEFAULT_FRAME: ReferenceFrame = ReferenceFrame(abbreviation="ICRF")


class TwoBody(BaseModel, abc.ABC):
    """
    Abstract base class for two-body states.
    """

    time: Time = Field(description="Epoch of the state vector")
    origin: Origin = Field(
        default=DEFAULT_ORIGIN,
        discriminator=bodies.DISCRIMINATOR,
        description="Origin of the coordinate system",
    )

    @abc.abstractmethod
    def to_cartesian(self) -> Cartesian:
        pass

    @abc.abstractmethod
    def to_keplerian(self) -> Keplerian:
        pass


class Cartesian(TwoBody):
    state_type: Literal["cartesian"] = Field(
        default="cartesian",
        frozen=True,
        repr=False,
        alias="type",
        description="The type of two-body state",
    )
    frame: ReferenceFrame = Field(default=DEFAULT_FRAME, description="Reference frame of the coordinate system")
    x: float = Field(description="x coordinate of the position vector [km]")
    y: float = Field(description="y coordinate of the position vector [km]")
    z: float = Field(description="z coordinate of the position vector [km]")
    vx: float = Field(description="velocity in x direction")
    vy: float = Field(description="velocity in y direction")
    vz: float = Field(description="velocity in z direction")
    _cartesian: lox.State = PrivateAttr()

    def __init__(self, cartesian: lox.State | None = None, **data):
        super().__init__(**data)
        if not cartesian:
            self._cartesian = lox.State(
                self.time._time,
                (self.x, self.y, self.z),
                (self.vx, self.vy, self.vz),
                self.origin._body,
                self.frame._frame,
            )
        else:
            self._cartesian = cartesian

    @classmethod
    def _from_lox(cls, cartesian: lox.State) -> Self:
        time = Time._from_lox(cartesian.time())
        frame = ReferenceFrame._from_lox(cartesian.reference_frame())
        origin = bodies._from_lox(cartesian.origin())
        x, y, z = cartesian.position()
        vx, vy, vz = cartesian.velocity()
        return cls(
            time=time,
            frame=frame,
            origin=origin,
            x=x,
            y=y,
            z=z,
            vx=vx,
            vy=vy,
            vz=vz,
        )

    @classmethod
    def from_rv(
        cls,
        time: Time,
        r: np.ndarray,
        v: np.ndarray,
        origin: Origin = DEFAULT_ORIGIN,
        frame: ReferenceFrame = DEFAULT_FRAME,
    ) -> Self:
        if r.size != N_DIMS:
            msg = f"position vector must have exactly 3 elements, size was {r.size}"
            raise ValueError(msg)
        if v.size != N_DIMS:
            msg = f"velocity vector must have exactly 3 elements, size was {r.size}"
            raise ValueError(msg)
        return cls(time=time, origin=origin, frame=frame, x=r[0], y=r[1], z=r[2], vx=v[0], vy=v[1], vz=v[2])

    @property
    def position(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

    @property
    def velocity(self) -> np.ndarray:
        return np.array([self.vx, self.vy, self.vz])

    def to_cartesian(self) -> Cartesian:
        return self

    def to_keplerian(self) -> Keplerian:
        keplerian = self._cartesian.to_keplerian()
        return Keplerian._from_lox(keplerian)

    def rotation_lvlh(self) -> np.ndarray:
        return np.array(self._cartesian.rotation_lvlh()).reshape((3, 3)).T

    def to_frame(self, frame: ReferenceFrame) -> Cartesian:
        cartesian = self._cartesian.to_frame(frame._frame)
        return Cartesian._from_lox(cartesian)

    def isclose(self, cart2: Cartesian, atol_p: float = 1e-6, atol_v: float = 1e-9) -> bool:
        return (np.linalg.norm(self.position - cart2.position) < atol_p) and (
            np.linalg.norm(self.velocity - cart2.velocity) < atol_v
        )


class Inclination(Angle):
    degrees: float = Field(ge=0, le=180)


class Keplerian(TwoBody):
    state_type: Literal["keplerian"] = Field(default="keplerian", frozen=True, repr=False, alias="type")
    shape: shapes.Shape = Field(discriminator=shapes.DISCRIMINATOR)
    inc: Inclination = Field(alias="inclination")
    node: Angle = Field(alias="ascendingNode")
    arg: Angle = Field(alias="periapsisArgument")
    anomaly: TrueAnomaly | MeanAnomaly = Field(discriminator=anomalies.DISCRIMINATOR)
    _keplerian: lox.Keplerian = PrivateAttr()

    def __init__(self, keplerian: lox.Keplerian | None = None, **data):
        super().__init__(**data)

        if not keplerian:
            barycenter_origin = isinstance(self.origin, bodies.Barycenter)
            if barycenter_origin and isinstance(self.shape, shapes.AltitudesShape):
                msg = "orbital shape definition via apsis altitudes is invalid for barycenter origins"
                raise ValueError(msg)
            sma = self.semi_major_axis
            ecc = self.eccentricity
            inc = self.inclination
            node = self.ascending_node
            arg = self.periapsis_argument
            nu = self.true_anomaly
            self._keplerian = lox.Keplerian(
                self.time._time,
                sma,
                ecc,
                inc,
                node,
                arg,
                nu,
                self.origin._body,
            )
        else:
            self._keplerian = keplerian

    @classmethod
    def _from_lox(cls, keplerian: lox.Keplerian) -> Self:
        time = Time._from_lox(keplerian.time())
        origin = bodies._from_lox(keplerian.origin())
        shape = shapes.SemiMajorAxisShape(sma=keplerian.semi_major_axis(), ecc=keplerian.eccentricity())
        inc = Inclination.from_radians(keplerian.inclination())
        node = Angle.from_radians(keplerian.longitude_of_ascending_node())
        arg = Angle.from_radians(keplerian.argument_of_periapsis())
        nu = TrueAnomaly.from_radians(keplerian.true_anomaly())
        return cls(
            time=time,
            origin=origin,
            shape=shape,
            inclination=inc,
            ascendingNode=node,
            periapsisArgument=arg,
            anomaly=nu,
        )

    @staticmethod
    def _parse_angles(
        inclination: float,
        ascending_node: float,
        periapsis_argument: float,
        anomaly_value: float,
        angle_unit: Literal["degrees"] | Literal["radians"] = "degrees",
        anomaly_type: Literal["true"] | Literal["mean"] = "true",
    ):
        inc = (
            Inclination.from_degrees(inclination) if angle_unit == "degrees" else Inclination.from_radians(inclination)
        )
        node = Angle.from_degrees(ascending_node) if angle_unit == "degrees" else Angle.from_radians(ascending_node)
        arg = (
            Angle.from_degrees(periapsis_argument)
            if angle_unit == "degrees"
            else Angle.from_radians(periapsis_argument)
        )
        true_anomaly = TrueAnomaly.from_degrees if angle_unit == "degrees" else TrueAnomaly.from_radians
        mean_anomaly = MeanAnomaly.from_degrees if angle_unit == "degrees" else MeanAnomaly.from_radians
        anomaly = true_anomaly(anomaly_value) if anomaly_type == "true" else mean_anomaly(anomaly_value)
        return {"inclination": inc, "ascendingNode": node, "periapsisArgument": arg, "anomaly": anomaly}

    @classmethod
    def from_elements(
        cls,
        time: Time,
        semi_major_axis: float,
        eccentricity: float,
        inclination: float,
        ascending_node: float,
        periapsis_argument: float,
        anomaly: float,
        origin: Origin = DEFAULT_ORIGIN,
        angle_unit: Literal["degrees"] | Literal["radians"] = "degrees",
        anomaly_type: Literal["true"] | Literal["mean"] = "true",
    ) -> Self:
        angles = cls._parse_angles(inclination, ascending_node, periapsis_argument, anomaly, angle_unit, anomaly_type)
        return cls(
            time=time,
            origin=origin,
            shape=shapes.SemiMajorAxisShape(sma=semi_major_axis, ecc=eccentricity),
            **angles,
        )

    @classmethod
    def from_radii(
        cls,
        time: Time,
        apoapsis_radius: float,
        periapsis_radius: float,
        inclination: float,
        ascending_node: float,
        periapsis_argument: float,
        anomaly: float,
        origin: Origin = DEFAULT_ORIGIN,
        angle_unit: Literal["degrees"] | Literal["radians"] = "degrees",
        anomaly_type: Literal["true"] | Literal["mean"] = "true",
    ) -> Self:
        angles = cls._parse_angles(inclination, ascending_node, periapsis_argument, anomaly, angle_unit, anomaly_type)
        return cls(
            time=time,
            origin=origin,
            shape=shapes.RadiiShape(ra=apoapsis_radius, rp=periapsis_radius),
            **angles,
        )

    @classmethod
    def from_altitudes(
        cls,
        time: Time,
        apoapsis_altitude: float,
        periapsis_altitude: float,
        inclination: float,
        ascending_node: float,
        periapsis_argument: float,
        anomaly: float,
        origin: Origin = DEFAULT_ORIGIN,
        angle_unit: Literal["degrees"] | Literal["radians"] = "degrees",
        anomaly_type: Literal["true"] | Literal["mean"] = "true",
    ) -> Self:
        angles = cls._parse_angles(inclination, ascending_node, periapsis_argument, anomaly, angle_unit, anomaly_type)
        return cls(
            time=time,
            origin=origin,
            shape=shapes.AltitudesShape(apoapsisAltitude=apoapsis_altitude, periapsisAltitude=periapsis_altitude),
            **angles,
        )

    @property
    def _mean_radius(self) -> float:
        return 0 if isinstance(self.origin, bodies.Barycenter) else self.origin.mean_radius

    @property
    def semi_major_axis(self) -> float:
        """float: semi-major axis [km]"""
        mean_radius = self._mean_radius
        return self.shape.semi_major_axis(mean_radius)

    @property
    def eccentricity(self) -> float:
        """float: eccentricity"""
        mean_radius = self._mean_radius
        return self.shape.eccentricity(mean_radius)

    @property
    def inclination(self) -> float:
        """float: inclination [rad]"""
        return self.inc.radians

    @property
    def ascending_node(self) -> float:
        """float: right ascension of the ascending node [rad]"""
        return self.node.radians

    @property
    def periapsis_argument(self) -> float:
        """float: argument of periapsis [rad]"""
        return self.arg.radians

    @property
    def true_anomaly(self) -> float:
        """float: true anomaly [rad]"""
        return self.anomaly.true_anomaly(self.eccentricity)

    @property
    def mean_anomaly(self) -> float:
        """float: mean anomaly [rad]"""
        return self.anomaly.mean_anomaly(self.eccentricity)

    @property
    def apoapsis_radius(self) -> float:
        """float: apoapsis radius [km]"""
        mean_radius = self._mean_radius
        return self.shape.apoapsis_radius(mean_radius)

    @property
    def periapsis_radius(self) -> float:
        """float: periapsis radius [km]"""
        mean_radius = self._mean_radius
        return self.shape.periapsis_radius(mean_radius)

    @property
    def orbital_period(self) -> float:
        """float: orbital period [s]"""
        return self._keplerian.orbital_period()

    def to_cartesian(self) -> Cartesian:
        cartesian = self._keplerian.to_cartesian()
        return Cartesian._from_lox(cartesian)

    def to_keplerian(self) -> Keplerian:
        return self


type TwoBodyType = Cartesian | Keplerian
