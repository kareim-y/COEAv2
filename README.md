# Framework for Unifying Sources and Emissions models (FUSE)

## Previous name: Canadian Oilfield Envrionmental Assessor (COEA)

Repository for the Framework for Unifying Sources and Emissions models (FUSE) tool.  
This version is created by: Kareem Youssef  
With contributions and guidance from: Dr. Joule Bergerson and Julia Yuan

## Acknowledgment

This version of the FUSE tool is created based on the original tool created by Alex Bradley in 2020. If you would like to learn more about this tool and it's use cases, please refer to resource below:  
Alex Bradley's Research Paper - http://hdl.handle.net/1880/111763

## Overview

FUSE (previously named COEA) originally required python 2.7, it is now updated to run on Python 3 (tested on Python 3.12). The environment is best setup using a package management tool such as conda. The `fuse_gui.py` is the main script to run the tool. This will run the tool's Graphical User Interface (GUI) were you can provide your inputs, then click on the _submit_ button. The tool will then call various functions from the runfiles folder, ultimately exporting results to a version of the OPGEE tool where emissions intensities can be estimated. The analysis is completed based on the selection of a set of wells. The following image shows some default parameters that can be used for testing.

![Example Inputs for Search](FUSE_py3/images/example2.png)

## Datasets

The FUSE tool relies on several datasets describing several activities of the upstream Canadian O&G industry. The datasets have been obtained from Petrinex (free access) and geoSCOUT (paid license)

## Setup

### Folder Structure

To ensure that FUSE connects properly with OPGEE Python, it is important that your folder structure is as follows:

1. Create a folder anywhere on your machine, name it "LCA" for example. This folder is where the FUSE and OPGEEv4 repositories will be cloned.
2. Open a terminal page, navigate to this folder and then clone the FUSE tool using the `git clone` command followed by the HTTPS of this repository: https://github.com/kareim-y/FUSE.git
3. Once this is complete ensure that you have the following folder structure:  
   LCA/  
   └── FUSE/
4. Install the datasets required from Peterenix and geoSCOUT and move them into the `Project Data` Folder which is located inside the `FUSE/FUSE_py3` folder.
5. This should be your folder structre now:  
   LCA/  
   └── FUSE/  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── FUSE_py3/  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Project Data/*dataset folders*/

### FUSE Installation

Once the repository cloning is comepleted, follow the steps below:

1. Install miniconda on your local machine (https://www.anaconda.com/docs/getting-started/miniconda/install). Existing conda install should also work.
2. Using terminal, navigate into the `FUSE/FUSE_py3` folder then create the enviornment `conda create --name fuse` (This command will make `fuse` the name of the environment, you can pick another name by using `conda create --name <chosen name>`)
3. Once the conda environment is created, activate it using `conda activate fuse` (or `conda activate <chosen name>`)
4. Install the following required libraries while the conda environemnt is active, `pip install pandas numpy matplotlib scipy chardet shapely openpyxl`
<!-- 4. Edit the file _runfiles/map_to_drive.py_ to point to the folder containing the unzipped 'Project Data' file downloaded from the above link. -->
5. Test installation by running the script `python fuse_gui.py`, then clicking on the `Check Installation of Required Libraries` button at the bottom of the GUI.

### OPGEEv4 Installation

1. Open a new terminal and navigate to the LCA/ folder you created earlier
2. Use this link to navigate to the OPGEE documentation, specifically to the _Install opgee in an Anaconda virtual environment_ page. https://opgee.readthedocs.io/en/latest/install.html
3. If the link above doesn't work, navigate to the README.md file in the OPGEEv4 repository (https://github.com/msmasnadi/OPGEEv4) and a link to the OPGEEv4 documentation should be linked there.
4. In the _Install opgee in an Anaconda virtual environment_ tab, follow steps 1 to 3.
5. now navigate to the LCA/ folder in terminal, then run the command in step 4 in _Install opgee in an Anaconda virtual environment_, this command will clone the OPGEEv4 repository.
6. This should be your folder structre now:  
   LCA/  
   ├── FUSE/  
   &nbsp;│ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── FUSE_py3/  
   &nbsp;│ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Project Data/*dataset folders*/  
   └── OPGEEv4/
7. Your OPGEE package should be ready for use now

## Using FUSE and OPGEE

### Using FUSE

1. When the folder structuring and installation is compeleted, run the FUSE GUI by executing the `FUSE_gui.py` file.
2. Provide the inputs required by filling up textboxes and selecting/deselecting checkboxes.
3. Once your inputs are compeleted, click on _submit_ at the bottom of the page (scrolling using your mouse does not work on MacOS, use the slide bar on the right of the screen)
4. You should be greeted with a pop-up message that shows all your inputs and once you click _ok_ the FUSE tool will start executing the required files.
5. This pop-up will stay on your screen until the FUSE tools comepletes its run, you can track the progress of the FUSE tool by looking at the terminal.
6. Once the FUSE run is complete, a pop-up message will alert you and then another message will alert you when the results are transferred to OPGEEv4 for further analysis.
7. If any errors occur during the FUSE run, you will receive a pop-up with the error message. Check terminal for more details on the error.

#### Using OPGEEv4

1. If FUSE functions as intended, you will only need to enter 2 terminal commands to run OPGEEv4.
2. Navigate to the `OPGEEv4/opgee` folder using another terminal page, activate the anaconda environment you set-up earlier (by following the _OPGEEv4 Installation_ section of this document), this command should be `conda activate opgee`
3. Then run this command `opg run -o output -a FUSE_run -m etc/fuse.xml` (This command works as of version 4.1.0 of OPGEEv4, the command in this step might change as future versions of OPGEEv4 are released, if you run into issues in this step, refer to the OPGEEv4 documentation)
4. To have faster OPGEEv4 runs use the following command, which utilizes the cluster run feature in OPGEEv4 `opg run -o output -a FUSE_run -m etc/fuse.xml -c local`. Adding `-c local` initiates a parallel computing approach that analyzes several fields at once.
5. Keep an eye on terminal to see the progress of the OPGEEv4 run.
6. Once the run is complete, the results will be saved in `carbon_intensity.csv` file, in the folder `OPGEEv4/opgee/output`.
7. The `carbon_intensity.csv` file has a long-format, which might not be easy to read. Using the "OPGEE Post-Processing" section of the gui will "prettify" OPGEE outputs, and, by default, store the "prettified" CSV file in the following folder: `FUSE\FUSE_py3\OPGEE post processing`.

### Contact

Reach out to kareim.youssef@ucalgary.ca
