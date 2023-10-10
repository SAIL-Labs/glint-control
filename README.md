# glint-control
Instrument control software for GLINT, using SCExAO cameras and BMC MEMS

Lightweight, modular code to perform the operation and control tasks for the GLINT instrument. It is designed for the 2023+ iteration of GLINT, which uses the ‘Apapane spectrograph in SCExAO for data acqusition and the BMC segmented MEMS DM.

The backend code which controls the instrument and acquires data (in the `glintcontrol` class) is kept separate from the GUI code (the `glintcontrol_gui`) class.

Scratch files and development scripts, experiments, etc. should be kept in the `/dev` subdirectory.

## Functionality
#### Core features
* Acquire data from ‘Apapane camera and spectral flux vectors
* Send segment positions to MEMS
* Perform per-waveguide tip/tilt optimisation scan
* Perform per-waveguide null scan (piston)
* Save data for diagnostic purposes (not full speed)

#### Future features
* Data quick-look (e.g. plot histograms, time-series, ...)
* Integrated stage controls, with chip positioning optimisation loop
* Instrument simulator
* Alignment camera viewer; PSF and pupil tracking



### Readme TODO:
* Describe software structure
* Hardware requirements
* Installation and operation
* ...


## Working notes

#### Ideas
- Have a chip object (containing a matrix, or nested dicts, or something) which describes the input-output connections of the chip, and corresponding segment numbers. This can be used both to determine which segment to poston for which baseline, etc., and also to allow simple 'simulation' functionality.
- 
