import shutil
import subprocess
from pathlib import Path

import pytest

import ephemerista
from ephemerista.analysis.link_budget import LinkBudget
from ephemerista.analysis.visibility import Visibility
from ephemerista.coords.trajectories import Trajectory
from ephemerista.propagators.orekit import start_orekit
from ephemerista.propagators.sgp4 import SGP4
from ephemerista.scenarios import Scenario
from ephemerista.time import TimeDelta

RESOURCES = Path(__file__).parent.joinpath("resources")
EOP_PATH = RESOURCES.joinpath("finals2000A.all.csv")
ephemerista.init_provider(EOP_PATH)


@pytest.fixture(scope="session")
def iss_tle():
    return """ISS (ZARYA)
1 25544U 98067A   24187.33936543 -.00002171  00000+0 -30369-4 0  9995
2 25544  51.6384 225.3932 0010337  32.2603  75.0138 15.49573527461367"""


@pytest.fixture(scope="session")
def iss_trajectory(iss_tle):
    propagator = SGP4(tle=iss_tle)
    start_time = propagator.time
    end_time = start_time + TimeDelta.from_minutes(100)
    times = start_time.trange(end_time, step=float(TimeDelta.from_minutes(1)))
    return propagator.propagate(times)


@pytest.fixture(scope="session")
def resources():
    return RESOURCES


@pytest.fixture(scope="session")
def phasma_scenario(resources):
    json = resources.joinpath("phasma/scenario.json").read_text()
    return Scenario.model_validate_json(json)


@pytest.fixture(scope="session")
def phasma_link_budget(phasma_scenario):
    lb = LinkBudget(scenario=phasma_scenario)
    return lb.analyze()


@pytest.fixture(scope="session")
def lunar_scenario(resources):
    json = resources.joinpath("lunar/scenario.json").read_text()
    return Scenario.model_validate_json(json)


@pytest.fixture(scope="session")
def lunar_visibility(lunar_scenario):
    vis = Visibility(scenario=lunar_scenario)
    return vis.analyze()


@pytest.fixture(scope="session")
def lunar_transfer(resources):
    return Trajectory.from_csv(resources.joinpath("lunar/lunar_transfer.csv"))


@pytest.fixture(scope="session")
def root_folder(resources):
    return resources.parent.parent


@pytest.fixture(scope="session")
def start_orekit_jvm():
    return start_orekit()


@pytest.fixture(scope="session")
def maven_package(root_folder):
    java_folder = root_folder / "java_additions"
    # Try to build JAR with maven
    mvn = shutil.which("mvn")
    if mvn:
        subprocess.run([mvn, "package"], cwd=java_folder, check=True)  # noqa: S603

    return True
