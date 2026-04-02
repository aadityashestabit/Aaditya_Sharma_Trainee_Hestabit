# Data Report for the dataset 

## Dataset 

```
https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
```

## Target Distribution
![Target Class Distribution](../../images/target_distribution.png)

## Feature Distribution
![Feature Distribution](../../images/feature_distributions.png)

## Correlation Matrix
![Correlation Matrix](../../images/correlation_matrix.png)

## Missing Value Heatmap
![Missing Value Heatmap](../../images/missing_values_heatmap.png)
### *Missing value heatmap empty because of no empty values

## Outlies before clipping
![Outliers before Clipping](../../images/Outliers_before_clipping.png)

## Outlies after clipping
![Outliers after Clipping](../../images/Outliers_after_clipping.png)

---

### Outlier clipping is used in the data pipeline instead of outlier removal because of low training samples in data set.

```
 df[col] = df[col].clip(lower, upper)
```