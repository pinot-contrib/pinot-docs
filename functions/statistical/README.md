# Statistical Functions

Pinot provides statistical aggregation functions for computing variance, standard deviation, covariance, skewness, and kurtosis. These functions are useful for data analysis, quality monitoring, and understanding the distribution of your data.

## Variance Functions

### VAR_POP / VARPOP

```sql
VAR_POP(col)
```

Returns the population variance of a numeric column as `Double`. Population variance measures how far values are spread out from the mean, using all data points.

```sql
SELECT VAR_POP(playerScore) AS score_variance
FROM gameStats
```

### VAR_SAMP / VARSAMP

```sql
VAR_SAMP(col)
```

Returns the sample variance of a numeric column as `Double`. Sample variance uses Bessel's correction (divides by N-1 instead of N), making it an unbiased estimator when working with a sample of the population.

```sql
SELECT VAR_SAMP(responseTime) AS response_variance
FROM apiMetrics
```

## Standard Deviation Functions

### STDDEV_POP / STDDEVPOP

```sql
STDDEV_POP(col)
```

Returns the population standard deviation of a numeric column as `Double`. This is the square root of the population variance.

```sql
SELECT STDDEV_POP(latency) AS latency_stddev
FROM requestMetrics
```

### STDDEV_SAMP / STDDEVSAMP

```sql
STDDEV_SAMP(col)
```

Returns the sample standard deviation of a numeric column as `Double`. This is the square root of the sample variance.

```sql
SELECT STDDEV_SAMP(revenue) AS revenue_stddev
FROM salesData
```

## Covariance Functions

### COVAR_POP / COVARPOP

```sql
COVAR_POP(col1, col2)
```

Returns the population covariance between two numeric columns as `Double`. Covariance measures how two variables change together.

```sql
SELECT COVAR_POP(adSpend, revenue) AS spend_revenue_covariance
FROM campaignMetrics
```

### COVAR_SAMP / COVARSAMP

```sql
COVAR_SAMP(col1, col2)
```

Returns the sample covariance between two numeric columns as `Double`.

```sql
SELECT COVAR_SAMP(temperature, energyUsage) AS temp_energy_covariance
FROM sensorData
```


## Distribution Shape Functions

### SKEWNESS

```sql
SKEWNESS(col)
```

Returns the skewness of a numeric column as `Double`. Skewness measures the asymmetry of the probability distribution. A positive skew indicates a longer right tail, while a negative skew indicates a longer left tail.

```sql
SELECT SKEWNESS(orderAmount) AS amount_skewness
FROM orders
```

### KURTOSIS

```sql
KURTOSIS(col)
```

Returns the kurtosis of a numeric column as `Double`. Kurtosis measures the "tailedness" of the probability distribution. Higher kurtosis indicates more outliers (heavier tails).

```sql
SELECT KURTOSIS(responseTime) AS latency_kurtosis
FROM apiMetrics
```

## Notes

- All statistical functions return `Double.NaN` or `Double.NEGATIVE_INFINITY` when no records are selected.
- These functions operate on numeric columns only (`INT`, `LONG`, `FLOAT`, `DOUBLE`).
- For variance and standard deviation, use the `_POP` variant when you have the entire population and the `_SAMP` variant when working with a sample.
- All statistical functions are supported in both the Single-Stage Engine (SSE) and Multi-Stage Engine (MSE).
