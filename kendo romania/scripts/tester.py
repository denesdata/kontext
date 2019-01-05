import pandas as pd, numpy as np, json
import members_loader, matches_loader, clubs_loader, point_utils

members=members_loader.get_members('../data/manual/Evidenta membrilor.xlsm')
members_clean=members_loader.cleaner(members).reset_index(drop=False)

