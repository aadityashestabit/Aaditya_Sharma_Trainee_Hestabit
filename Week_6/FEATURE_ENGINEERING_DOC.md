#  FEATURE-ENGINEERING-DOC

##  Overview

The pipeline enhances predictive power by:
- Encoding domain knowledge
- Capturing non-linear relationships
- Reducing skewness
- Creating interaction features

---

##  Pipeline Flow

```
Raw Data
  ↓
Binning (Categorization)
  ↓
Binary Feature Creation
  ↓
Feature Interactions
  ↓
Log Transformations
  ↓
Drop Redundant Columns
  ↓
One-Hot Encoding
  ↓
Final Feature Matrix
```

---

##  Input Features

### Core Variables
- `Pregnancies` → Number of pregnancies  
- `Glucose` → Plasma glucose concentration  
- `BloodPressure` → Diastolic blood pressure  
- `BMI` → Body Mass Index  
- `DiabetesPedigreeFunction` → Genetic diabetes likelihood  
- `Age` → Age of patient  

---

##  Step 1: Categorical Binning

### Age → AgeGroup
```
0–30     → Young
30–45    → Adult
45–60    → MiddleAge
60+      → Senior
```

### BMI → BMICategory
```
<18.5    → Underweight
18.5–25  → Normal
25–30    → Overweight
>30      → Obese
```

###  Purpose
- Convert continuous variables into meaningful groups  
- Capture non-linear relationships  
- Improve interpretability  

---

##  Step 2: Binary Risk Features

### Created Features
- `HighGlucose` = 1 if Glucose > 140 else 0  
- `HighBP` = 1 if BloodPressure > 90 else 0  
- `MultiplePregnancies` = 1 if Pregnancies ≥ 3 else 0  

###  Purpose
- Encode domain-specific thresholds  
- Simplify model learning  
- Improve performance for linear & tree models  

---

##  Step 3: Feature Interactions

### Interaction Features
- `BMI_Age` = BMI × Age  
- `Glucose_BMI` = Glucose × BMI  
- `Age_Glucose` = Age × Glucose  

###  Purpose
- Capture combined effects between variables  
- Introduce non-linearity  
- Improve predictive signal  

---

## Step 4: Log Transformations

### Transformed Features
- `DPF_log` = log(1 + DiabetesPedigreeFunction)  
- `Age_log` = log(1 + Age)  

###  Purpose
- Reduce skewness  
- Handle outliers  
- Stabilize variance  

---

##  Step 5: Dropping Original Columns

### Removed Features
- `DiabetesPedigreeFunction`  
- `Age`  

###  Reason
- Replaced by transformed or derived features  
- Avoid redundancy  
- Reduce multicollinearity  

---

##  Step 6: One-Hot Encoding

### Applied To
- `AgeGroup`  
- `BMICategory`  

### Example
```
AgeGroup → Young, Adult, MiddleAge, Senior

After Encoding (drop_first=True):
- AgeGroup_Adult
- AgeGroup_MiddleAge
- AgeGroup_Senior
```

###  Purpose
- Convert categorical → numerical  
- Avoid dummy variable trap  
- Enable model compatibility  

---

##  Final Feature Set

### Numerical Features
- Pregnancies  
- Glucose  
- BloodPressure  
- BMI  

### Binary Features
- HighGlucose  
- HighBP  
- MultiplePregnancies  

### Interaction Features
- BMI_Age  
- Glucose_BMI  
- Age_Glucose  

### Log Features
- DPF_log  
- Age_log  

### Encoded Features
- AgeGroup_Adult  
- AgeGroup_MiddleAge  
- AgeGroup_Senior  
- BMICategory_Normal  
- BMICategory_Overweight  
- BMICategory_Obese  

---

## Design Principles

###  Domain Knowledge
- Medical thresholds for glucose, BMI, BP  

###  Non-Linearity Handling
- Binning  
- Feature interactions  

###  Distribution Handling
- Log transformations  

###  Model Efficiency
- Binary flags  
- Reduced redundancy  

### Clean Representation
- Dropping unnecessary columns  
- Proper encoding  

---

##  Notes

- Missing values must be handled before applying this pipeline  
- Log transform requires non-negative inputs  
- Binning ranges can be tuned based on dataset distribution  
- Feature scaling may be applied after this step if needed  

---

## Summary

This feature engineering pipeline:
- Enhances predictive signal  
- Encodes domain expertise  
- Reduces skewness and noise  
- Improves model performance  
- Maintains interpretability  

---

##  Final Flow Summary

```
Numerical Features
      ↓
Binning + Binary Flags
      ↓
Feature Interactions
      ↓
Log Transformations
      ↓
Encoding
      ↓
Final ML Dataset
```

---

 

---

![Feature importance summary SHAP](../images/shap_summary.png)
