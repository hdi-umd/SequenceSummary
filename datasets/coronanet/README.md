# CoronaNet dataset

## The raw dataset

The raw dataset is available at the [Coronanet webpage](https://www.coronanet-project.org/download.html)

`coronanet_release.csv`  - containing covid-19 policy data of countries arounf the world

## The notebook

The > `coronanet_release.csv` dataset is analyzed in  `Coronanet_analysis.ipynb`

## The processed dataset

1. `coronanet_shortened.csv` contains filtered data where both Start and End date of a policy is defined. We also omit the corrected entries, keeping only original ones

2. `coronanet_subset_shortened.csv` contains data of 22 countries we selected for analysis.

3. `events.csv` and `recordAttributes.csv` were used for analysis with MAQUI.
