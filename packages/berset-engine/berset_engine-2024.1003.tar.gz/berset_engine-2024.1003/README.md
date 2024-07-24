# Building Energy Retrofit Scenario Evalution Tool Engine

## Introduction

This tool use [better-analytical-engine](https://github.com/LBNL-ETA/BETTER_analytical_engine) with some minor modification to 
- figure out change-point model (i.e. piece-wise linear regression models) between building energy consumption and (dry-bulk) outdoor air temperature.
- The model coefficients, i.e. base load, heating sensibility, cooling sensibility, etc. are then benchmarked against the coefficients of buildings in the same <b>space type category</b>
- Jonhson Control's LEAN Energy Analysis is used to identify the EE measures for the building
- Finally, the potential energy and cost savings are estimated with the EE measures

Note sur change-point model coefficients:

- Heating Slope: negative value, the smaller the steeper the slope (worse) => the smaller the worse
- Heating Change-point: any value, the smaller the later building's energy consumption becomes sensitive to weather (better) => the smaller the better
- Baseload: positive value, the smaller the lower non-weather sensitive load (better) => the smaller the better
- Cooling Change-point: any value, the smaller the earlier the building's energy consumption becomes sensitive to weather (worse) => the smaller the worse
- Cooling Slope: positive value, the smaller the less steep the slope (better) => the smaller the better

Conclusion: 
- Except for heating slope and cooling change-point, the smaller the value, the better.
- The reason that the analytical engine flips the sign for heating slope medians was for pre-processing the coefficients, so that we can use the same code to benchmark it.
- The orignal pen-source code flips the sign for the heating slope medians during preprocessing to streamline the benchmarking process (you can see the heating slopes are in absolute values here). However, the web app uses benchmark statistics that retains the original sign of the heating slope, which is negative. To ensure consistency and accuracy in your benchmarking and assessment, you need to preprocess the benchmark statistics data by flipping the sign of the heating slope median.
- For example, if the heating slope median in the new benchmark statistics is -0.019, you should change it to 0.019 before running your analysis with the open-source analytical engine. This adjustment aligns the data with the processing method used in the open-source code 
## Interesting tools/projects

### Better Analytical Engine

BETTER - Building Efficiency Targeting Tool for Energy Retrofits is developed under Cooperating Research and Development Agreement (CRADA) No. FP00007338 between the Regents of the University of California Ernest Orlando Lawrence Berkeley National Laboratory under its U.S. Department of Energy (DOE) Contract No. DE-AC02-05CH11231 and Johnson Controls, Inc., with support from ICF.

[More information](https://github.com/LBNL-ETA/BETTER_analytical_engine)

### PF4EE WebCheck Tool and EEQUEST

The PF4EE WebCheck tool and the EEQuest tool were developed as part of the PF4EE Pilot, with support from the European Commission. The tools aim to support financial intermediaries in marketing dedicated energy efficiency finance, raise awareness and facilitate on-lending for energy efficiency. They allow estimating a preliminary value of potential energy savings. The tools are not intended – nor should they be used or construed as – offering accurate energy savings estimates, as would be provided by professional energy auditors or through advanced engineering software.

#### PF4EE WebCheck Tool

Pre-check the eligibility of an energy efficiency project for PF4EE financing

#### EEQuest Tool

Get an idea of the energy savings potential of typical measures accross the EU

Assess about 20 typical measures in buildings and industry

Obtain energy, cost, and CO2 savings estimates
Download a pdf summary

[More information](https://pf4ee.eib.org/Tools)

### OLFEnergy OPENEEMETER

OpenEEmeter is an open source toolkit for implementing and developing standard methods for calculating normalized metered energy consumption (NMEC) and avoided energy use.The OpenEEmeter library contains routines for estimating energy efficiency savings at the meter.

[More information](https://lfenergy.org/projects/openeemeter/)

