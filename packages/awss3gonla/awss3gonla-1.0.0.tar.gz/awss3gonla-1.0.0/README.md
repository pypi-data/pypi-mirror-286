# `awss3gonla` Library

## Overview

The `awss3gonla` class provides a Python interface for interacting with AWS S3 storage. It allows for operations such as uploading and downloading files, managing parquet files, and handling data partitions. This class is designed to work with the AWS SDK for Python (`boto3`) and the Polars library for data manipulation.

## Features

- **Configuration**: Easily configure AWS credentials and region.
- **Upload Files**: Upload files to an S3 bucket, including text, JSON, and parquet files.
- **Download Files**: Download files from an S3 bucket into a buffer.
- **List Objects**: List objects in a specific S3 path.
- **Manage Partitions**: Handle parquet file partitions and read them into Polars DataFrames.

## Installation

To use the `awss3gonla` class, ensure you have the following dependencies installed:

- `boto3`
- `polars`

You can install these packages using pip:

```bash
pip install boto3 polars
```

## Usage

### Initialization

Create an instance of the `awss3gonla` class with your AWS credentials and bucket name. You can provide the AWS credentials and bucket name directly or let the `boto3` session manage them using the default configuration.


```python
import awss3gonla

s3 = awss3gonla.client(
    aws_access_key_id='your_access_key',
    aws_secret_access_key='your_secret_key',
    region_name='your_region',
    bucket_name='your_bucket_name'
)
```
Alternatively, if you already have an s3_client created, you can pass it directly:

```python
import boto3
from awss3gonla import client

existing_s3_client = boto3.client('s3')

s3 = client(
    s3_client=existing_s3_client,
    bucket_name='your_bucket_name'
)
```
## Methods

## `get(path: str, name: str)`

### Description

Retrieves an object from S3 and returns its content based on the file type.

### Arguments

- `path` (str): The path to the object within the S3 bucket.
- `name` (str): The name of the object to retrieve.

### Returns

- `Union[str, pl.DataFrame, Dict[str, Any]]`: The content of the object, which could be:
  - a string for text files,
  - a Polars DataFrame for CSV files,
  - a dictionary for JSON files,
  - a Polars DataFrame for Parquet files.

### Example

```python
# Initialize S3Storage
s3_storage = S3Storage(bucket_name='my-s3-bucket')

# Example 1: Retrieve a text file
text_content = s3_storage.get('path/to/your/object', 'example.txt')
print("Text File Content:")
print(text_content)

# Example 2: Retrieve a CSV file and print the Polars DataFrame
csv_df = s3_storage.get('path/to/your/object', 'example.csv')
print("\nCSV File DataFrame:")
print(csv_df)

# Example 3: Retrieve a JSON file
json_content = s3_storage.get('path/to/your/object', 'example.json')
print("\nJSON File Content:")
print(json_content)

# Example 4: Retrieve a Parquet file and print the Polars DataFrame
parquet_df = s3_storage.get('path/to/your/object', 'example.parquet')
print("\nParquet File DataFrame:")
print(parquet_df)
```

## `list(path: str)`

### Description

Lists objects in an S3 bucket under a specified prefix.

This method retrieves a list of objects in the S3 bucket that match the specified prefix. It logs the progress of 
the operation and returns a dictionary containing metadata about the listed objects.

### Arguments

- `path` (str): The prefix path for filtering the objects in the S3 bucket.

### Returns

- `Dict[str, Any]`: A dictionary containing the response from the S3 `list_objects_v2` call. This typically includes 
  metadata such as 'Contents', 'Bucket', and 'Prefix'.

### Examples

```python
# Initialize S3Storage
s3_storage = S3Storage(bucket_name='my-s3-bucket')

# Example: List objects under a prefix
response = s3_storage.list('path/to/prefix/')
print(response)
# Output:
# {'Contents': [{'Key': 'path/to/prefix/file1.txt', 'Size': 1234}, {'Key': 'path/to/prefix/file2.txt', 'Size': 5678}],
#  'Bucket': 'my-bucket', 'Prefix': 'path/to/prefix/'}
```

### `put(path: str, name: str)`
Uploads a file from the local path to S3.

```python
s3.put('local/path/to/file', 'destination/name')
```

### `put_object(path: str, name: str, _object: str | Dict[str, Any])`

Uploads an object (string or dictionary) to S3. Automatically detects the content type based on the input type.

```python
s3.put_object('some/path', 'object_name', 'some string content')
s3.put_object('some/path', 'object_name', {'key': 'value'})
```
### `put_parquet(dataframe: pl.DataFrame, path: str, name: Optional[str] = None, partition_cols: Optional[dict] = None) -> str`
Uploads a Polars DataFrame to S3 as a parquet file. Supports partitioning based on specified columns.

```python
import polars as pl

df = pl.DataFrame({
    'col1': [1, 2, 3],
    'col2': ['a', 'b', 'c']
})

key = s3.put_parquet(df, 'some/path/', name='optional_name', partition_cols={'col1': 'value'})
print(f"Parquet file uploaded to S3 with key: {key}")
```

### `list_parquet(path: str)`
Lists parquet files in the specified S3 path.

```python
parquet_files = s3.list_parquet('some/path/')
print(parquet_files)
```

### `get_objects(path: str, buffer: Any)`
Downloads an object from S3 into a provided buffer.

```python
import io

buffer = io.BytesIO()
s3.get_objects('some/path/to/object', buffer)
print(buffer.getvalue())
```
### `get_parquet_partition(path: str) -> pl.DataFrame`

Retrieves all parquet files from a specified path and combines them into a single Polars DataFrame.

```python
df = s3.get_parquet_partition('some/path/')
print(df)
```

## Error Handling

### The put_object method handles common exceptions, including:

* FileNotFoundError
* UnboundLocalError
* TypeError
* AttributeError


## Notes
Ensure that AWS credentials are properly configured.
The get method is a placeholder and not yet implemented.


## License

This library is licensed under the MIT License. See the details below.

### MIT License

Copyright (c) [2024] [Gonzalo Laura]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


This section provides the legal framework for using, modifying, and distributing the software under the MIT License.
