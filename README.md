# MetabolicModelValidation
The following scripts was used for a validation study between indirect calorimetry and metabolic models for muscuskeletal modeling.

**Lentz-Nielsen, Nicki**., Boysen, Mads., Munk-Hansen, Mathias., Steffensen, Mike., Laursen, Andreas.,
Engelund, Bjørn., Iversen, Kristoffer., Larsen, Ryan., & de Zee, Mark. (2022). VValidation of metabolic models for estimation of energy expenditure during isolated concentric and eccentric muscle contractions. *Abstract published for Danish biomechanical
association annual meeting and is currently under peer-review.*


The code consist of 3 main files and 1 modules files:

* **01-DataCleaning.R** Imports the gas exchange data from a pulmonary gas exchange system and preparing it for further analysis.
* **02-DataTransformation.py** The script calculates the metabolic energy consumed doing a concentric and eccentric knee flexion, while also calculating the needed torgue inputs used for a muscuskeletal modelling software. 
* **03-PlotsandStatistics.R** Final analysis for the result section of the paper, focusing on both the energy expenditure calculated by pulmonary gas exchange and from musculoskeletal models. 
* **modules.py** File containing most functions used in the 02-DataTransformation.py script. 

The **KneeExntesionScripts** directory contains the scripts used for musculoskeletal modeling in the AnyBody Software.

## Abstract
Studies has proved energy expenditure for human locomotion to be difficult to estimate, which may be caused by the eccentric contraction, 
as the cross-bridge theory and sliding filaments theory fail to explain certain phenomena in eccentric contractions. 
Wherefore, a controlled study investigating the energy expenditure in concentric and eccentric contractions is required. 
Therefore, the purpose of this study was to validate the metabolic models: Margaria (1968), Bhargava et al., (2004) and Umberger (2010), 
performing isolated isokinetic concentric and eccentric knee flexions at difference mechanical loads in a dynamometer. 
Each load consisted of 150 repetitions and pulmonary gas exchange was measured during each load. 
All three models underestimated the metabolic power compared to the indirect calorimetry for both contraction types. 
Reasonably, the metabolic models expected increases in energy expenditure as a function of increased load, 
though during eccentric contractions the measured energy expenditure never increased, despite the increased load, 
thus increasing the absolute error. Wherefore, future studies is needed to get more knowledge of the relationship between energy expenditure and eccentric work. 

### Validation plot

Agreement between measured metabolic power using indirect calorimetry on the x-axis [watt/kg] and estimated metabolic power using a metabolic model on the y-axis [watt/kg]. 
The dashed line indicates a perfect agreement between measured and calculated output. Each color represents a subject, and the black line is the mean of all the subjects. 
Subplots are column wise arranged after contraction type, and row arranged after the metabolic models.
![KoelewijnPlot](KoeleWijnPlot.jpeg)

### Overall underestimation 

illustrates the measured EE and calculated MM for one executed repetition, 
revealing a mean relative underestimation of the MMs of up to 55.8 ± 19.5 % and 78.5 ± 19.4 % for concentric and eccentric contractions, respectively. 
![Underestimation](UnderEstimateKcal.jpeg)

### Bonus plot: Difference between two equations based on Péronnet & Massicotte (1991) 
The original work from Péronnet & Massicotte (1991) calculates energy expenditure based on a table of nonprotein respiratory quotient.
Kipp et al. (2018) simplifies this by showing a simple linear equation that should replicate the work of Péronnet & Massicotte (1991).
The following plots depicts the difference between these two solutions. Because of this, we chose to use the work of Péronnet & Massicotte (1991).

![peronnet](PeronnetDifference.jpeg)

### Funding
No funding was recieved

### Data availability
Available upon reasonable request
