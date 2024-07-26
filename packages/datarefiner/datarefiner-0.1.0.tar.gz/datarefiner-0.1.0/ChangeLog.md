

---------------------------------------------------------------------

# Version 0.1.0 (First version)

+ Add infors (CODE_OF_CONDUCT.md, MANIFEST.in, LICENSE, README.md, requirements.txt, CITATION.cff)
+ Add package `ml` (machine learning) and `ts` (time series)
+ `ml` package has:
  + `label` module has:
    + `LabelEncoder` class
  + `scaler` module has:
    + `StandardScaler` class
    + `MinMaxScaler` class
    + `MaxAbsScaler` class
    + `RobustScaler` class
    + `Log1pScaler` class
    + `LogeScaler` class
    + `SqrtScaler` class
    + `BoxCoxScaler` class
    + `YeoJohnsonScaler` class
    + `SinhArcSinhScaler` class
    + `DataTransformer` class that can be used with all of the above scalers
+ `ts` package has:
  + `differencing` module has:
    + `DifferenceScaler` class
  + `window` module has:
    + `SlidingTransformer` class
    + `RollingStatisticTransformer` class
    + `ExpandingStatisticTransformer` class
+ Add examples folders
