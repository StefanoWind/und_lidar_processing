# Processor of raw Halo XR lidar data with LiDARGO

To install the repository on your local machine:
1. Navigate to your local folder in the command line
   `cd myfolder`
2. Clone
   `git clone https://github.com/StefanoWind/und_lidar_processing.git`
   
To install dependencies:
1. Clone FIEXTA anywhere on your machine
   `git clone https://github.com/StefanoWind/FIEXTA.git`
3. Install LiDARGO on your current environment (if using Spyder, use Anaconda prompt; if using VS Code, `conda activate myenvironment` first)
   `cd FIEXTA/lidargo` to navigate where the setup.py for LiDARGO lives and then
   `pip install -e .` to install editable package (easier to debug)

To process files:
1. Copy hpl user1 files in the data/s1.lidar.z01.raw folder
2. Create yaml config file like

   ```yaml
   
   path_data: 'myfolder/und_lidar_processing/data/' # data root folder
   path_config_format: 'myfolder/und_lidar_processing/configs/config_und_a0.xlsx' #path to configuration for LiDARGO/format
   path_config_stand: 'myfolder/und_lidar_processing/configs/config_und_b0.xlsx' #path to configuration for LiDARGO/standardize
   channels: ['s1.lidar.z01.raw'] #subfolder of path_data where raw files live

3. Create LiDARGO config (more complex, provided [here](https://drive.google.com/drive/folders/1A-9mMn6lgOVZDhJA53ZkaE6CDKcDpdKd))
                
4. Run process_lidars.py for the selected date range and pointing to yaml configuration file

Renamed raw file will be generated in 00 folder. NetCDF formatted files will be generated in a0 folder. Standardized/quality-controlled will be generated in b0 folder.
