# -*- coding: utf-8 -*-
"""
Some constants for carbatpy usage are set here

* The two (!) Refprop installation directories (with dll, fluids etc.)
* he directory, where the results shall be written.

Created on Sun Nov  5 16:01:02 2023

@author: atakan
"""

import os
import copy
# global _T_SURROUNDING, _P_SURROUNDING, _RESULTS_DIR, _CARBATPY_BASE_DIR
_T_SURROUNDING = 288.15 # K
_P_SURROUNDING =1.013e5  # Pa
TREND = {"TREND_INSTALLED":True,
          "USE_TREND":False, 
          "TREND_DLL":"", 
          'TREND_PATH':""}

directory = os.getcwd()
try:
    _CARBATPY_BASE_DIR = os.environ["CARBATPY_BASE_DIR"]
except:
    _CARBATPY_BASE_DIR = directory

# The two installations of REFPROP , one for the working fluid
# and one for the secondary fluid. With only one installation, the instances
# mix up ...
os.environ['RPPREFIX'] = r'C:/Program Files (x86)/REFPROP'
os.environ['RPPREFIXs'] = r'C:/Program Files (x86)/REFPROP/secondCopyREFPROP'
if TREND["TREND_INSTALLED"]:
    try:
        TREND["TREND_DLL"] = os.environ['TREND_DLL']
        TREND["TREND_PATH"] = os.environ['TREND_PATH']
    except:
        print("Trend not found! Check the environmentvariable TREND_DLL, TREND_PATH")
        TREND_DLL = ""
        TREND_PATH = ''
        TREND["TREND_INSTALLED"] = False
    
try:
    _RESULTS_DIR = os.environ['CARBATPY_RES_DIR']
except:
    try:
        _RESULTS_DIR = os.environ['TEMP']
    except:
        try:
            
            _RESULTS_DIR = directory + r"\\tests\\test_files"
        except Exception as no_file:
            print("Please set the envirionment variable: CARBATPY_RES_DIR !", no_file)
            
# Default values:-------------------------------------------------
fl_properties_names = ("Temperature", "Pressure", "spec_Enthalpy",
                        "spec_Volume", "spec_Entropy", "quality",
                        "spec_internal_Energy",
                        "viscosity", "thermal_conductivity",
                        "Prandtl_number", "k_viscosity", "molecular_mass",
                        "speed_of_sound")
THERMO_STRING = "T;P;H;V;S;QMASS;E"
TRANS_STRING = THERMO_STRING + ";VIS;TCX;PRANDTL;KV;M;W"
THERMO_TREND = request = ["T", "P", "H", "D",
                           "S", "QEOS", "U"]  # careful density not volume
TRANS_STRING = THERMO_STRING + ";VIS;TCX;PRANDTL;KV;M;W"
TRANS_TREND = copy.copy(THERMO_TREND)
TRANS_TREND.extend(["ETA", "TCX", "CP"])

CB_FLUID_DEFAULT = {"PROPS": "REFPROP",  # choice: "TREND" or "REFPROP"
                    "DLL_SELECT": "2dll",  # choice: "2dll" or "dll" 
                    "UNITS": "MASS BASE SI",
                    "Property_Names":fl_properties_names,
                    "THERMO_STRING":THERMO_STRING,
                    "TRANS_STRING":TRANS_STRING ,
                    "THERMO_TREND": THERMO_TREND,
                    "TRANS_TREND": TRANS_TREND,
                    "TREND":TREND,
                    "RPPREFIX":os.environ['RPPREFIX'] 
                    
                    
                    
    }
# This dictionary will be generally imported with carbatpy
CB_DEFAULTS={
    "Fluid_Defaults": CB_FLUID_DEFAULT,
    "General":{"T_SUR":_T_SURROUNDING,
               "P_SUR": _P_SURROUNDING,
               "RES_DIR": _RESULTS_DIR
               }
    }