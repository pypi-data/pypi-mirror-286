"""Allows a user to specify custom colors and ensure there are consistent across all plots"""

import os

DEFAULT_GROUNDTRACK_COLOR = os.getenv("DEFAULT_GROUNDTRACK_COLOR", "rgb(248,248,255)")
DEFAULT_LAND_COLOR = os.getenv("DEFAULT_GROUNDTRACK_COLOR", "rgb(169,169,169)")
DEFAULT_OCEAN_COLOR = os.getenv("DEFAULT_GROUNDTRACK_COLOR", "rgb(47,79,79)")
DEFAULT_GROUND_STATION_COLOR = os.getenv("DEFAULT_GROUNDTRACK_COLOR", "rgb(68,178,0)")
DEFAULT_GROUND_STATION_SIZE = float(os.getenv("DEFAULT_GROUND_STATION_SIZE", "8"))
DEFAULT_PLOTLY_THEME = os.getenv("DEFAULT_PLOTLY_THEME", "plotly_dark")
DEFAULT_GRID_COLOUR = os.getenv("DEFAULT_GRID_COLOUR", "rgb(102, 102, 102)")
