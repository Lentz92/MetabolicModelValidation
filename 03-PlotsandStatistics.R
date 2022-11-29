##  ---------------------------
##  03-Plots and statistics
##
##  Final analysis for the result section of the paper, focusing on both the energy expenditure calculated by 
##  pulmonary gas exchange and from musculoskeletal models. 
##  ´
##  Author: "Nicki lentz"
##  Date: "20/1/2021"
##
##  Email: nickilentz@hotmail.com
## ---------------------------

#Reminder of correctly mappings of initials and FP number.
#ID: "AD" \~ "FP1" "MB" \~ "FP2" "MM" \~ "FP3" "MS" \~ "FP4" "NL" \~ "FP5"

library(tidyverse)

## -- Prepare data -- ##

#Main objective with this chunk is to import the original modelled data from anybody (metabolicModels) 
#and the data from the python script that went through the pulmonary gas exchange data (metabolicEquation)
#then merging them.

#We are mainly interested in the "anymet" column from this csv
metabolicModels <- data.table::fread("metabolisme_data.csv") %>% 
  mutate(
    subjects = case_when(
      subjects ==  "AD" ~ "FP1",
      subjects ==  "MB" ~ "FP2",
      subjects ==  "MM" ~ "FP3",
      subjects ==  "MS" ~ "FP4",
      subjects ==  "NL" ~ "FP5"),
    intensity = substr(intensity, 1,2),
    ID = paste(subjects, contraction, intensity, sep="_")
  )

#All the data which were prepared by the 02-DataTransformation.py script.
path = "../data/vynProcessedData/"
dataList <- list.files(path = path, pattern = ".csv", full.names = TRUE) %>% 
  map(~data.table::fread(.))

#Make one large dataframe, and renaming contraction column variables to create new shorter ID column
metabolicEquation <- dataList %>% 
  bind_rows() %>% 
  mutate(
    Contraction = case_when(
      Contraction == "con" ~ "Concentric",
      Contraction == "exc" ~ "Eccentric"),
    ID = paste(Subject, Contraction, Load, sep="_")
  )



#merge them so we have the output from the musculoskeletal model with the gas exchange + other information
df <- merge(metabolicModels,
            metabolicEquation,
            by = "ID",
            allow.cartesian = TRUE) %>% 
  select(ID, AnyMet, model, MetabolicWorkPerRep, MetabolicCalculation, Ekstension_time, 
         Flexion_time, Work.y, Watt, Subject, Load, Contraction, Bw) %>% 
  rename(work = Work.y,
         modelled_work_per_rep = AnyMet) %>% 
  janitor::clean_names() %>% 
  #Calculate important metrics for plots and statistics
  mutate(
    mech_watt_kg = (watt / bw),
    modelled_watt_kg= (modelled_work_per_rep /  (`ekstension_time` + `flexion_time`)) / bw,
    metabolic_watt_kg = (metabolic_work_per_rep /  (`ekstension_time` + `flexion_time`)) / bw
  )

data.table::fwrite(df, "cleaned_metabolisme_data.csv")


## -- PLOTS -- ##

#Main Plot
koeligvinPlot <- function(metabolicCalculation){
  #--------------------------------
  # Creates figure with 6 subplots, depicting the validity of the calculated
  # energy compared to the measured. The plot is inspired by the work of Koelewijn et al. (2019)
  # https://doi.org/10.1371/journal.pone.0222037
  
  # Args:
  #   metabolicCalculation: string, from the 'metabolic_calculation' column in df.
  #
  # Returns: Plot
  #--------------------------------
  p1 <- df %>% 
    filter(model != "Bhargava_on" & model != "Margaria1" & model != "ModifiedMargaria") %>%
    filter(metabolic_calculation == metabolicCalculation) %>% 
    mutate(modelConType = as_factor(paste(model, contraction, sep=" ")),
           modelConType = factor(modelConType, 
                                 levels = c("Margaria Concentric", 
                                            "Margaria Eccentric", 
                                            "Bhargava Concentric",
                                            "Bhargava Eccentric",
                                            "Umberger Concentric",
                                            "Umberger Eccentric"))) %>% 
    ggplot(aes(x = metabolic_watt_kg, y = modelled_watt_kg, color = subject)) + 
    geom_point(alpha = .5) + 
    stat_smooth(method = "lm", formula = y ~ x, se = FALSE, alpha=.5, lwd = .5) + 
    stat_smooth(aes(group = model), method = "lm", formula = y ~ x, se = FALSE, color = "black", lwd = 1.25) +
    geom_abline(intercept = 0, slope = 1, linetype = "dashed") +
    xlim(0,2.75) + 
    ylim(0,2.75) + 
    facet_wrap(~modelConType, ncol = 2,
               labeller = label_wrap_gen(width=10)) + 
    labs(
      x = "Calculated [watt / kg]",
      y = "Measured [watt / kg]"
    ) + 
    theme_minimal() + 
    theme(
      aspect.ratio = 0.75,
      strip.text.x = element_text(
        size = 15, face = "bold"),
      axis.title = element_text(
        size = 15, face="bold"),
      legend.position = "none",
      axis.text.x = element_text(size = 18),
      axis.text.y = element_text(size= 18),
      plot.title = element_text(size = 25, face = "bold")
    )
  
  return(p1)
}

p1 <- koeligvinPlot("original_peronnet")
ggsave(file="../resultater/KoeleWijnPlotSecondRun.jpeg", plot = p1, width=10, height=8, dpi = 1200)




# Plot difference between two interpretations of Péronnet & Massicotte (1991) work on metabolic calculations
# original_peronnet are energy expenditure calculated based on the works of Péronnet & Massicotte (1991) 
# which uses a table of nonprotein respiratory quotient. The "peronnet" variable is an interpretation from
# Kipp et al. (2018) that uses an equation to arrive at the same results as Péronnet & Massicotte (1991)
# This plot shows that the results are not the same, wherefore, the current study chose to use the
# original work from 1991.
p2 <- df %>% 
  filter(metabolic_calculation %in% c("peronnet", "original_peronnet")) %>% 
  ggplot(aes(x = load, y = metabolic_watt_kg, color = metabolic_calculation)) + 
  geom_line() + 
  geom_point() + 
  facet_grid(contraction ~ subject) + 
  labs(x = "Load [N]",
       y = "Metabolic energy [J/s/bw]") + 
  scale_color_manual(name = "Metabolic Calculation", 
                     labels = c("Péronnet & Massicotte (1991)", "Kipp et al. (2018)"),
                     values = c("dodgerblue4","firebrick4")) + 
  theme_minimal() + 
  theme(legend.position = "top",
        legend.key.size = unit(2,"cm"),
        legend.title = element_text(size=14),
        legend.text = element_text(size=14),
        plot.title = element_text(size = 16, face='bold'),
        plot.subtitle = element_text(size = 14)) + 
  ggtitle("Difference between Péronnet & Massicotte (1991) equation and Peronnet formula from Kipp et al. (2018)",
          subtitle = "y-axis shows metabolic energy produced relative to time and bodyweight")

ggsave(file="../resultater/PeronnetDifference.jpeg", plot = p2, width=10, height=8, dpi = 1200)



## -- Statistics calculation -- ##

# Focus is on the metabolic calculation done by Péronnet & Massicotte (1991) and the metabolic models
# by Margaria, Bhargava and Umberger.
df_peronnet <- df %>% 
  filter(metabolic_calculation == "original_peronnet", 
         model %in% c("Margaria", "Bhargava", "Umberger"))


# Linear models extracting metrics with broom::tidy directly from linear models

#Linear models for the musculoskeletal models
AnyMet_lm_tidy <- df_peronnet %>% 
  group_by(model, contraction) %>% 
  do(broom::tidy(lm(modelled_watt_kg ~ mech_watt_kg, .)))

#Linear models for the pulmonary gas exchange
VynMet_lm_tidy <- df_peronnet %>% 
  group_by(contraction) %>% 
  do(broom::tidy(lm(metabolic_watt_kg ~ mech_watt_kg, .))) %>% 
  mutate(model = "original_peronnet", .before = "contraction")

lm_tidy <- bind_rows(AnyMet_lm_tidy, VynMet_lm_tidy)

#Same as above, but using broom::glance to get other statistics
AnyMet_lm_glance <- df_peronnet %>% 
  group_by(model, contraction) %>% 
  do(broom::glance(lm(modelled_watt_kg ~ mech_watt_kg, .)))

VynMet_lm_glance <- df_peronnet %>% 
  group_by(contraction) %>%
  do(broom::glance(lm(metabolic_watt_kg ~ mech_watt_kg, .))) %>% 
  mutate(model = "original_peronnet", .before = "contraction")

lm_glance <- bind_rows(AnyMet_lm_glance, VynMet_lm_glance) %>% 
  select(model, contraction, r.squared, adj.r.squared, p.value)

lmInfo <- merge(lm_tidy, lm_glance, by = c("model","contraction"))

#Calculating mean absolute error and root mean square error.
AnymetError <- df_peronnet %>% 
  group_by(model, contraction) %>% 
  mutate(mae = mean(abs(modelled_watt_kg - metabolic_watt_kg)),
         rmse = mean((modelled_watt_kg - metabolic_watt_kg)^2),
         .after = "id") %>% 
  ungroup() %>% 
  select(mae, rmse, contraction, model) %>% 
  distinct()


# Calculate the difference between pulmonary gas exchange energy and calculated EE from models, 
# for the mean repetetition in percentage
df_peronnet %>%
  mutate(totalEnergiDiff = ((modelled_work_per_rep/bw) - (metabolic_work_per_rep/bw)),
         relativeEnergiDiff = (totalEnergiDiff / (metabolic_work_per_rep/bw))*100) %>% 
  group_by(contraction) %>% 
  summarise(m = mean(relativeEnergiDiff),
            s = sd(relativeEnergiDiff))

#Plot the difference in J/kg
df_peronnet %>%
  mutate(moveID = paste(contraction, load, model, sep="_")) %>% 
  group_by(moveID) %>% 
  mutate(modMean = mean(modelled_work_per_rep/bw),
         modsd = sd(modelled_work_per_rep/bw),
         metMean = mean(metabolic_work_per_rep/bw),
         metsd = sd(metabolic_work_per_rep/bw)) %>% 
  ungroup() %>% 
  ggplot(aes(x = load, y = modMean)) + 
  geom_line(size = 2.5, alpha = 0.5, color = "#a9a9a9") + 
  geom_point(size = 7) + 
  geom_errorbar(aes(ymin = modMean-modsd, ymax = modMean + modsd), width = 6, position = position_dodge(.9)) + 
  geom_line(aes(y = metMean), size = 2.5, alpha = 0.5, color = "#343434") + 
  geom_point(aes( y = metMean), size = 7) + 
  geom_errorbar(aes(ymin = metMean-metsd, ymax = metMean+metsd), width = 6, position = position_dodge(.9)) +
  facet_grid(contraction ~ model) + 
  labs(x = "Torque [Nm]",
       y = "Energy Expenditure [J/kg]"
  ) + 
  theme_minimal() + 
  theme(
    strip.text.x = element_text(
      size = 30, color = "black", face = "bold"
    ),
    strip.text.y = element_text(
      size = 30, color = "black", face = "bold"
    ),
    axis.title = element_text(
      size = 34, face = "bold"
    ),
    axis.text.x = element_text(size = 30),
    axis.text.y = element_text(size= 30),
    panel.spacing = unit(2, "lines")
  ) + 
  scale_x_continuous(limits = c(10,90), breaks = c(20,40,60,80))

ggsave(file="../resultater/UnderEstimateKcal.jpeg", width=25, height=12, dpi = 1200)

