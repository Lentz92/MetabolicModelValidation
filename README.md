# MetabolicModelValidation
The following scripts was used for a trend validation study between indirect calorimetry and metabolic models for muscuskeletal modeling.

## Abstract
The purpose of this study was to trend validate the metabolic models: Margaria
(1968), Bhargava et al. (2004) and Umberger (2010) implemented in the Anybody
Modeling System, performing a concentric knee extension and eccentric knee flexion at different mechanical loads in a dynamometer. Each load consisted of 150
repetitions and pulmonary gas exchange was measured during each load. All three models underestimated the metabolic power compared to indirect calorimetry for
both contraction types. Where the error for all metabolic models increased with the load.

### 00-DataCleaning.qmd: 
This script cleans the data as there are errors from the pulmonary gas exchange system. NA values, differences in time format and numeric / character columns.

### 01-main.py
Following script loops through all the participants at the given study for metabolic model validation.
The script calculates the metabolic energy consumed doing a concentric and eccentric knee flexion, 
while also calculating the needed torgue inputs used for a muscuskeletal modelling software, 
while also calculating rep duration, work, watt and oxygen consumption based on four different models:

Wier 1949
Brockway 1987 (as described in Kipp et al 2018)
Péronnet and Massicotte 1991 (as described in kip et al 2018)
Péronnet and Massicotte 1991 as described in its original paper

### 02-Plots_and_statistics.qmd -- In progress
Following script will make different plots and calculate different statistics that will be used in the research paper.
