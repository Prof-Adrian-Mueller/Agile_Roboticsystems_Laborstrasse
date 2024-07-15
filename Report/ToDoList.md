## TODO
## Ujwal Subedi
1. [ ] Code Cleanup & Code Comments
3. [ ] Relative Folder Structure fix for Labor PC
4. [ ] Layout View for Experiment, Plasmid, Tubes using Mock Data
5. [ ] Export of Data , downloadable Excel File
6. [ ] update README 

## Wissam Alamareen
1. [ ] Return all Experiments of a Labor Assistant using laborant id

## Completed Tasks
### Ujwal Subedi
1. [x] Display QR code Image in UI
2. [x] Standard Error/Output/input (stdout stderr stdin) displayed in a window on GUI
3. [x] QR Code Generator Layout in UI
4. [x] Navigation Left Menu Layout
5. [x] Cross-process communication
6. [x] Added Experiment Tubes Table to show Experiment Info about Current Experiment
7. [x] Added Json-based Application Caching to Save previous application data for the startup
    - Loads Experiment Tubes Information of Previous Experiment on Startup
    - Loads QR-Codes of Previous Experiment on Startup
8. [x] Implement Borg Singleton for Runtime shared cache
9. [x] Experiment Preparation with multiple Page System 
    - Experiment Creation / Import
    - Show all the provided Plasmid Nr as a List 
        -  Show Input Field for each Plasmid Nr to accept Tube Nr in comma separated List eg. (5,7,8,12,24)
10. [x] Adding filter to Experiment Creation Form
11. [x] Redesign QR-Image view row list near Experiment Tubes view
12. [x] PC Transformer2023 Prio 1
13. [x] Send Tube Nr to Dobot
14. [x] Live View Layout adjusted
    - It Loads all Tubes to Live view after Experiment Preparation
    - Clicking More Button will show Details about the certain Tube
    - Each Station button click will load details about station and current status
    - Stations color will change if tube reached certain Station
    - Tubes and Station data will be updated in real time using interprocess communication and observer pattern
15. [x] Available QR Codes are shown in Experiment Preparation
16. [x] Export Funktion for Search Results and Current Experiment Data
17. [x] Live View Simulation added using log_detail.csv , which is old log file
18. [x] Adjusted Custom Dialog
19. [x] Only Current Experiment could be updated
20. [x] Load tubes of specific plasmid while updating current Experiment
21. [x] Export QR Code Images to a Folder

## Completed Tasks
### Wissam Alamareen
1. [x] Experiment creation or import
2. [x] Check if Experiment Exists
3. [x] Import of Plasmid metadata
4. [x] List of Tubes creation with Plasmid and Experiment ID
    - [x] QR Code Generation and assign it to Tube
5. [x] Return Experiment Data of a specific Experiments using Experiment Id
6. [x] Return Number of Experiments of a Labor Assistant using their Name
7. [x] Return all Tubes of specific Experiments using Experiment Id
8. [x] Return Tube Data per probe_ne(id)
9. [x] Return plasmid Data per plasmid_nr(id)
10. [x] Return all Tubes data of specific Experiment
11. [x] Return all Experiments of a Labor Assistant using laborant id
12. [x] Available QR Codes are shown in Experiment Preparation
13. [x] Only new tubes will be added while updating the current Experiment
14. [x] Load tubes of specific plasmid while updating current Experiment


## On Progress
### Ujwal Subedi
1. Export Data from the result Tables


### TODO
### Wissam Alamareen


### Process for Labor Assistant
- Experiment Preparation
  - Enter Experiment Id, Name, Lastname ,Nr of Plasmid, Nr of Tubes, List of Plasmid in comma separated text eg. (2,5,6,4)
  - Enter List of Tubes (Probe Nr) in comma separated text
  - View List of QR Codes and Probe Nr 
    - Print QR Code Image 
  - Start Monitoring Application
