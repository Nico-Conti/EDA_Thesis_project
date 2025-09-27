# EDA Thesis Project – Stress Detection from Electrodermal Activity


This repository provides a Python implementation for offline analysis of **physiological signals** using **Electrodermal Activity (EDA)**.  
It includes a small custom dataset collected from multiple subjects at different acquisition sites under a standardized protocol, used to explore **machine learning methods for stress classification**.

<p align="center">
  <img src="foto/Seal_of_the_University_of_Bologna.png" alt="University of Bologna Seal" width="200">
</p>

This repository was developed as part of my **Bachelor’s Thesis in Electronic and Telecommunications Engineering** at the **University of Bologna**.  



---

## Overview
Electrodermal Activity (EDA) reflects variations in skin conductance caused by sweat gland activity, which is tightly linked to sympathetic nervous system responses.  
The aim of this work is to design an **end-to-end pipeline** for:

- **Signal acquisition & preprocessing**: denoising, normalization, tonic/phasic decomposition  
- **Feature extraction**: time- and frequency-domain features, phasic responses, skin conductance levels  
- **Classification models**: traditional machine learning algorithms such as SVM and Random Forest  
- **Evaluation**: cross-validation on benchmark datasets with metrics including Accuracy, F1-score, and ROC-AUC  

---

## Data Collection Protocol
The dataset consists of **EDA recordings from five participants**, acquired under controlled experimental conditions.  

Each session began with a **relaxation phase**, during which the participant remained calm for two minutes. This baseline segment provided a reference measure of the individual’s natural skin conductance level.  

After establishing the baseline, participants were instructed to perform the **Valsalva maneuver**, a standard physiological test involving a forced exhalation against a closed airway. The maneuver was repeated several times to induce short bursts of sympathetic activation, which could be clearly observed in the EDA signal as sharp increases in conductance.  

Since the recordings come from different individuals, the dataset naturally captures variability. Factors such as skin hydration, sweat gland density, electrode placement, and personal physiological differences all influence the signals. While this variability increases the challenge for machine learning models, it also improves realism and supports the development of approaches that can generalize better to real-world applications.  

---
