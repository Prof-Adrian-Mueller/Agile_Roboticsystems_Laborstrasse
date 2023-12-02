## TODO
## Ujwal Subedi
1. [ ] Code Cleanup & Code Comments
2. [ ] PC Transformer2023 Prio 1
3. [ ] Relative Folder Structure fix for Labor PC
4. [ ] Layout View for Experiment, Plasmid, Tubes using Mock Data
5. [ ] Export of Data , downloadable Excel File

## Wissam Alamareen
1. [ ] Return all Experiments of a Labor Assistant using laborant id
2. [ ] Return all Tubes of specific Experiments using Experiment Id

## Completed Tasks
### Ujwal Subedi
1. [x] Display QR code Image in UI
2. [x] Standard Error/Output/input (stdout stderr stdin) displayed in a window on GUI
3. [x] QR Code Generator Layout in UI
4. [x] Navigation Left Menu Layout
5. [x] Cross-process communication

### Wissam Alamareen
1. [x] Experiment creation or import
2. [x] Import of Plasmid metadata
3. [x] List of Tubes creation with Plasmid and Experiment ID
   - [x] QR Code Generation and assign it to Tube
4. [x] Return Experiment Data of a specific Experiments using Experiment Id
5. [x] Return Number of Experiments of a Labor Assistant using their Name 

## On Progress
### Ujwal Subedi
1. [ ] Experiment Preparation with multiple Page System 
    - Experiment Creation / Import
    - Show all the provided Plasmid Nr as a List 
        -  Show Input Field for each Plasmid Nr to accept Tube Nr in comma separated List eg. (5,7,8,12,24)
2. [ ] Adding filter to Experiment Creation Form

### Wissam Alamareen
1. [ ] Check if Experiment Exists
2. [ ] Add new Tube with Plasmid Id, Experiment Nr, QR Code and Probe Nr
   * Generate QR Code for each Probe Nr
     * Save in Database
3. [ ] Plasmid Metadata update
4. [ ] Experiment Import tweak for Experiment Preparation

### Process for Labor Assistant
- Experiment Preparation
  - Enter Experiment Id, Name, Lastname ,Nr of Plasmid, Nr of Tubes, List of Plasmid in comma separated text eg. (2,5,6,4)
  - Enter List of Tubes (Probe Nr) in comma separated text
  - View List of QR Codes and Probe Nr 
    - Print QR Code Image 
  - Start Monitoring Application
