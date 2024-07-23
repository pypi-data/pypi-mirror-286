# magma-converter
Python package to convert CVGHM seismic data structures into SDS format.

## Install
```python
pip install magma-converter
```

## How to
Run this codes:
```python
from magma_converter import Convert

input_dir = 'L:\\Ijen\\Seismik Ijen'
output_dir = 'L:\\converted'
start_date: str = "2019-01-01"
end_date: str = "2019-12-31"

convert = Convert(
    input_dir=input_dir,
    output_directory=output_dir,
    directory_structure='ijen',
    min_completeness=30, # convert to SDS if completeness of data greater than 30%
)

convert.between_dates(start_date, end_date)
```
