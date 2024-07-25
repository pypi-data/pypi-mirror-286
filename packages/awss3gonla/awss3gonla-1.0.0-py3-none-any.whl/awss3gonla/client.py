import os
import io
import json
import uuid
from io import BytesIO
from dataclasses import dataclass,field
from typing import Dict, Any, Optional,Union
import boto3
import polars as pl
from rich.progress import Progress
from rich.console import Console
from awss3gonla.storage import IStorage


@dataclass
class client(IStorage):
    """
    A client class for interacting with Amazon S3, implementing the IStorage interface.

    This class provides methods for interacting with Amazon S3, such as listing, uploading, and retrieving objects. 
    It uses AWS credentials and configuration provided via class attributes or environment variables.

    ** Attributes: **
        - `aws_access_key_id` (Optional[str]): 
          The AWS access key ID for authentication. If None, uses credentials from environment variables or IAM roles.
        - `aws_secret_access_key` (Optional[str]): 
          The AWS secret access key for authentication. If None, uses credentials from environment variables or IAM roles.
        - `region_name` (Optional[str]): 
          The AWS region where the S3 bucket is located. If None, uses the default region or environment configuration.
        - `bucket_name` (Optional[str]): 
          The name of the S3 bucket to interact with. Must be set before performing operations.
        - `s3_client` (boto3.Session.client): 
          The boto3 S3 client instance used for making S3 API calls. Initialized in the class constructor.

    **Methods:**
        - `__post_init__()`:
          Initializes the S3 client based on the provided credentials and configuration.
        - `list(path: str) -> Dict[str, Any]`:
          Lists objects in the specified S3 path.
        - `put_object(path: str, name: str, _object: str | Dict[str, Any]) -> str`:
          Uploads a string or dictionary to S3.
        - `put_parquet(dataframe: pl.DataFrame, path: str, name: str = None, partition_cols: dict = None) -> str`:
          Uploads a Polars DataFrame as a Parquet file to S3.
        - `get_parquet_partition(path: str) -> pl.DataFrame`:
          Retrieves and processes Parquet files from a specified S3 path and combines them into a single Polars DataFrame.

    **Example:**
        >>> s3_client = client(
        >>>     aws_access_key_id='your_access_key_id',
        >>>     aws_secret_access_key='your_secret_access_key',
        >>>     region_name='us-west-1',
        >>>     bucket_name='my-bucket'
        >>> )
        >>> response = s3_client.list('path/to/prefix/')
        >>> print(response)
        {'Contents': [{'Key': 'path/to/prefix/file1.txt', 'Size': 1234}, {'Key': 'path/to/prefix/file2.txt', 'Size': 5678}],
         'Bucket': 'my-bucket', 'Prefix': 'path/to/prefix/'}

        >>> key = s3_client.put_object('path/to/', 'example.txt', 'This is a test string.')
        >>> print(key)
        'path/to/example.txt'

        >>> df = pl.DataFrame({'column': [1, 2, 3]})
        >>> key = s3_client.put_parquet(df, 'path/to/', name='example_file')
        >>> print(key)
        'path/to/part-example_file.parquet'

        >>> combined_df = s3_client.get_parquet_partition('path/to/parquet/files/')
        >>> print(combined_df)
        <Polars DataFrame>
        shape: (3, 1)
        ┌──────────┐
        │ column   │
        │ ---      │
        │ i64      │
        ├──────────┤
        │ 1        │
        │ 2        │
        │ 3        │
        └──────────┘

    **Notes:**
        - The AWS credentials and region can also be set through environment variables or IAM roles, in which case the class attributes can be left as None.
       
    """
    aws_access_key_id:Optional[str]=None
    aws_secret_access_key:Optional[str]=None
    region_name:Optional[str]=None
    bucket_name:Optional[str]=None
    s3_client: boto3.Session.client = field(init=True, default=None)

    def __post_init__(self):
        self.__call__()

    def __call__(self):
        if self.s3_client is None:
            self.s3_client = boto3.Session(
                aws_access_key_id = self.aws_access_key_id,
                aws_secret_access_key = self.aws_secret_access_key,
                region_name = self.region_name
            ).client('s3')
        self.console = Console()

    def get(self, path:str, name:str)-> Union[str, pl.DataFrame, pl.DataFrame, Dict[str, Any]]:
        """
        Retrieves an object from S3 and returns its content based on the file type.

        Args:
            path (str): The path to the object within the S3 bucket.
            name (str): The name of the object to retrieve.

        Returns:
            Union[str, pd.DataFrame, pl.DataFrame]: The content of the object, which could be
            a string for text files, a pandas DataFrame for CSV files, a dictionary for JSON files,
            or a Polars DataFrame if the file is in a format supported by Polars.
        
        Example:
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
        """
        try:
            # Construct the full S3 key
            s3_key = f"{path}/{name}"
            self.console.log(f"[cyan]Retrieving object:[/cyan] [green]{s3_key}[/green]")
            with Progress() as progress:
                task = progress.add_task("[yellow]Downloading object...[/yellow]", total=100)
                # Retrieve the object from S3
                response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
                file_content = response['Body'].read()
                progress.update(task, completed=100)

            # Determine the file type based on the extension
            if name.endswith('.txt'):
                self.console.log(f"[cyan]Processing text file:[/cyan] [green]{name}[/green]")
                return file_content.decode('utf-8')
            elif name.endswith('.csv'):
                  # Use Polars to read the CSV file directly
                self.console.log(f"[cyan]Processing CSV file:[/cyan] [green]{name}[/green]")
                return pl.read_csv(BytesIO(file_content))
            elif name.endswith('.log'):
                  # Use Polars to read the CSV file directly
                self.console.log(f"[cyan]Processing log file:[/cyan] [green]{name}[/green]")
                return file_content.decode('utf-8')
            elif name.endswith('.json'):
                self.console.log(f"[cyan]Processing JSON file:[/cyan] [green]{name}[/green]")
                return json.loads(file_content.decode('utf-8'))
            elif name.endswith('.parquet'):
                self.console.log(f"[cyan]Processing Parquet file:[/cyan] [green]{name}[/green]")
                return pl.read_parquet(BytesIO(file_content))
            else:
                raise ValueError("Unsupported file format")

        except Exception as e:
            self.console.log(f"[bold red]An error occurred:[/bold red] {e}")
            return None
        
    def list(self, path: str) ->Dict[str,Any]:
        """
        Lists objects in an S3 bucket under a specified prefix.

        This method retrieves a list of objects in the S3 bucket that match the specified prefix. It logs the progress of 
        the operation and returns a dictionary containing metadata about the listed objects.

        Args:
        path (str): The prefix path for filtering the objects in the S3 bucket.

        Returns:
        Dict[str, Any]: A dictionary containing the response from the S3 `list_objects_v2` call. This typically includes 
                        metadata such as 'Contents', 'Bucket', and 'Prefix'.

        Examples:
        >>> response = self.list('path/to/prefix/')
        >>> print(response)
        {'Contents': [{'Key': 'path/to/prefix/file1.txt', 'Size': 1234}, {'Key': 'path/to/prefix/file2.txt', 'Size': 5678}],
            'Bucket': 'my-bucket', 'Prefix': 'path/to/prefix/'}

        Notes:
        - The `path` argument should be the prefix used to filter the objects. It may include subdirectories and delimiters.
        - The method logs progress updates and completion status using the `console` and `Progress` objects.
        - Ensure that `self.s3_client` and `self.console` are properly configured for S3 operations and logging.
        """
        self.console.log(f"[cyan]Listing objects in bucket:[/cyan] [green]{self.bucket_name}[/green] with prefix [yellow]{path}[/yellow]")
        with Progress() as progress:
            task = progress.add_task("[yellow]Retrieving objects...[/yellow]", total=100)
            _list = self.s3_client.list_objects_v2(Bucket=self.bucket_name,
                                       Prefix=path)
            progress.update(task, completed=100)
        self.console.log(f"[bold green]Objects listed successfully.[/bold green]")
        return _list
        
    def put(self,path:str,name:str):
        """
        Uploads a file to the specified S3 bucket.

        **Parameters:**
        - **`path`** (str): 
        The local path to the file to be uploaded.
        - **`name`** (str): 
        The name (key) under which the file will be stored in the S3 bucket.

        **Returns:**
        None

        **Example:**
        >>> s3_client = client(
        >>>     aws_access_key_id='your_access_key_id',
        >>>     aws_secret_access_key='your_secret_access_key',
        >>>     region_name='us-west-1',
        >>>     bucket_name='my-bucket'
        >>> )
        >>> s3_client.put('/local/path/to/file.txt', 'uploaded_file.txt')

        # This will upload the file 'file.txt' from the local directory to the S3 bucket
        # and store it as 'uploaded_file.txt' in the bucket.
        """
        self.console.log(f"[cyan]Uploading file:[/cyan] [green]{path}[/green] to bucket [green]{self.bucket_name}[/green] with key [green]{name}[/green]")
        self.s3_client.upload_file(path, self.bucket_name, name)

    def put_object(self, path: str, name: str, _object: str | Dict[str, Any]) ->str:
        """
        Uploads a string or dictionary as an object to an S3 bucket.

        This method uploads the given string or dictionary to an S3 bucket. The object is stored with the specified name 
        at the given path. The content type is automatically determined based on the type of the object (text/plain for 
        strings and application/json for dictionaries).

        Args:
        path (str): The S3 path where the object will be stored.
        name (str): The name of the object to be uploaded.
        _object (str | dict): The content to be uploaded. Can be either a string or a dictionary.

        Returns:
        str: The S3 key of the uploaded object.

        Examples:
        >>> key = self.put_object('s3://my-bucket/path/to/', 'example.txt', 'This is a test string.')
        >>> print(key)
        'path/to/example.txt'

        >>> key = self.put_object('s3://my-bucket/path/to/', 'example.json', {'key': 'value', 'number': 123})
        >>> print(key)
        'path/to/example.json'

        Notes:
        - If `_object` is a string, it is uploaded as plain text with a content type of 'text/plain'.
        - If `_object` is a dictionary, it is converted to a JSON string and uploaded with a content type of 'application/json'.
        - Ensure that `self.s3_client` and `self.bucket_name` are properly configured for S3 operations.
        - The method handles exceptions for common errors such as `FileNotFoundError`, `UnboundLocalError`, `TypeError`, and `AttributeError`.
        """
        try:
            if isinstance(_object,str):
                content_type = 'text/plain'
                content = _object.encode('utf-8')
                self.console.log(f"[cyan]Uploading text object[/cyan] to [green]{path}/{name}[/green]")
            elif isinstance(_object,dict):
                content = json.dumps(_object,indent=4,ensure_ascii=False).encode('utf-8')
                content_type = 'application/json'
                self.console.log(f"[cyan]Uploading JSON object[/cyan] to [green]{path}/{name}[/green]")
            bucket_name = self.bucket_name
            key = os.path.join(path,name)
            key = key.replace("\\", "/")
            with Progress() as progress:
                task = progress.add_task(f"[yellow]Uploading to S3...[/yellow]", total=100)
                self.s3_client.put_object(Bucket=bucket_name, Key=key, Body=content, ContentType=content_type)
                progress.update(task, completed=100)
            self.console.log(f"[bold green]Upload complete:[/bold green] [blue]{key}[/blue]")
        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except UnboundLocalError as unbound_local_error:
            print(unbound_local_error)
        except TypeError as type_error:
            print(type_error)
        except AttributeError as attribute_error:
            print(attribute_error)
        return key
    
    def put_parquet(self,
                    dataframe:pl.DataFrame,
                    path:str,
                    name:str=None,
                    partition_cols:dict=None
                    )-> str:
        
        """
        Uploads a Polars DataFrame as a Parquet file to an S3 bucket, with optional partitioning.

        This method uploads the DataFrame to S3 as a Parquet file. If partition columns are provided, the DataFrame is 
        partitioned by these columns before uploading. Each partition is saved as a separate Parquet file. If no partitioning 
        is specified, the entire DataFrame is saved as a single Parquet file with a generated or specified name.

        Args:
        dataframe (pl.DataFrame): The Polars DataFrame to be uploaded.
        path (str): The S3 path where the Parquet file(s) will be stored.
        name (str, optional): The name of the Parquet file. If not provided, a UUID is generated as the file name.
        partition_cols (dict, optional): A dictionary of columns to partition the DataFrame by. The keys are column names 
                                        and the values are lists of partition values.

        Returns:
        str: The S3 key of the uploaded Parquet file or the directory containing the partitioned files.

        Examples:
        >>> key = self.put_parquet(dataframe, '/path/to/data/', name='example_file')
        >>> print(key)
        'path/to/data/part-example_file.parquet'

        >>> key = self.put_parquet(dataframe, '/path/to/data/', partition_cols={'region': ['US', 'EU']})
        >>> print(key)
        'path/to/data/region=US/part-1234567890.parquet'

        Notes:
        - The `partition_cols` dictionary should specify columns to partition by, with each column name as a key and a list 
        of values for partitioning.
        - The method generates unique partition keys based on column values and ensures that the file names are unique using a hash.
        - Ensure that `self.s3_client` and `self.bucket_name` are properly configured for S3 operations.
        """
        if partition_cols:
            # Partition the DataFrame by the specified partition columns
            partitions = dataframe.partition_by(partition_cols)
            for partition in partitions:
                # Create the S3 key based on the partitions
                partition_values = [
                    f"{col}={partition[col][0]}" for col in partition_cols]
                partition_key = "/".join(partition_values)
                key = f"{path}/{partition_key}/part-{hash(tuple(partition_values))}.parquet"
                # Convert the partition to a bytes buffer
                buffer = io.BytesIO()
                partition.write_parquet(buffer)
                buffer.seek(0)
                self.s3_client.upload_fileobj(buffer, self.bucket_name, key)
                buffer.close()
        # Dataframe Without partitions
        else:
            # Assign name to partition if name is not specified
            name = name if name else uuid.uuid4()
            key = f"{path}/part-{name}.parquet"
            buffer = io.BytesIO()
            dataframe.write_parquet(buffer)
            buffer.seek(0)
            self.s3_client.upload_fileobj(buffer, self.bucket_name, key)
            buffer.close()
        return key
    
    def list_objects(self,path,extension:str=None,style=None) ->  Union[pl.DataFrame, list]:
        """
        Lists objects in a specified path and optionally filters and formats them.

        This method retrieves a list of objects from the specified path, filters them by file extension if provided, 
        and optionally formats the result into a Polars DataFrame.

        Args:
        path (str): The path from which to list objects.
        extension (str, optional): The file extension to filter objects by. If None, all objects are included.
        style (str, optional): The format of the output. If 'Dataframe', the result is returned as a Polars DataFrame.

        Returns:
        list or pl.DataFrame: A list of object metadata (dictionaries) or a Polars DataFrame containing the filtered objects.

        Examples:
        >>> objects_list = self.list_objects('/path/to/objects/', extension='.parquet')
        >>> print(objects_list)
        [{'key': 'path/to/file1.parquet', 'size': 1234, 'last_modified': '2024-01-01 12:00:00 UTC'},
            {'key': 'path/to/file2.parquet', 'size': 5678, 'last_modified': '2024-01-02 13:00:00 UTC'}]

        >>> objects_df = self.list_objects('/path/to/objects/', style='Dataframe')
        >>> print(objects_df)
        shape: (2, 3)
        ┌────────────────────┬──────────┬──────────────────────────┐
        │ key                │ size     │ last_modified             │
        │ ---                │ ---      │ ---                      │
        │ str                │ i64      │ str                      │
        ├────────────────────┼──────────┼──────────────────────────┤
        │ path/to/file1.parquet │ 1234 │ 2024-01-01 12:00:00 UTC │
        │ path/to/file2.parquet │ 5678 │ 2024-01-02 13:00:00 UTC │
        └────────────────────┴──────────┴──────────────────────────┘

        Notes:
        Ensure that the `list` method retrieves the object list in the expected format. The `LastModified` field should be a datetime object.
        """
        _list = self.list(path)
        _objects = []
        total_items = len(_list.get('Contents', []))
    
        with Progress() as progress:
            task = progress.add_task("[cyan]Reading objects...", total=total_items)
            if 'Contents' in _list:
                for obj in _list['Contents']:
                    if extension is None:
                        _objects.append(obj['Key'])
                    elif obj['Key'].endswith(extension):
                        _objects.append({'key':obj['Key'],'size':obj['Size'],'last_modified':obj['LastModified'].strftime("%Y-%m-%d %H:%M:%S %Z")})
                    progress.update(task, advance=1)
            progress.stop()

            if style == 'Dataframe':
                _objects = pl.DataFrame(_objects)
        return _objects
    def get_objects(self,
                    path:str,
                    buffer: Any):
        self.s3_client.download_fileobj(self.bucket_name, path, buffer)

    def get_parquet_partition(self,
                    path:str
                    )->pl.DataFrame:
        """
            Retrieves and processes Parquet files from a specified S3 path and combines them into a single Polars DataFrame.

            This method lists all Parquet files in the given path, reads each file into a Polars DataFrame, and concatenates 
            them into a single DataFrame. The progress of the processing is displayed using a progress bar.

            Args:
                path (str): The S3 path where Parquet files are located.

            Returns:
                pl.DataFrame: A Polars DataFrame containing the concatenated data from all Parquet files.

            Examples:
                >>> data = self.get_parquet_partition('/path/to/parquets/')
                >>> print(data)
                shape: (1000, 5)
                ┌────────────┬──────────┬──────────┬──────────┬──────────┐
                │ column_1   │ column_2 │ column_3 │ column_4 │ column_5 │
                │ ---        │ ---      │ ---      │ ---      │ ---      │
                │ i64        │ str      │ f64      │ bool     │ date     │
                ├────────────┼──────────┼──────────┼──────────┼──────────┤
                │ 1          │ 'value1' │ 1.23     │ true     │ 2024-01-01 │
                │ 2          │ 'value2' │ 4.56     │ false    │ 2024-02-01 │
                │ ...        │ ...      │ ...      │ ...      │ ...      │
                └────────────┴──────────┴──────────┴──────────┴──────────┘

            Notes:
                Ensure that the `list_objects` method returns a list of dictionaries with 'key' as one of the dictionary 
                keys and that the `get_objects` method correctly populates the provided buffer with the file data.
        """
        parquets = self.list_objects(path,'.parquet')
        dataframes = []
        total_parquets = len(parquets)
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing parquet files...", total=total_parquets)
            for parquet in parquets:
                buffer = io.BytesIO()
                self.get_objects(parquet.get('key'), buffer)
                buffer.seek(0)
                df = pl.read_parquet(buffer)
                dataframes.append(df)
                progress.update(task, advance=1)

        dataframe_append = dataframes[0]
        for df in dataframes[1:]:
            dataframe_append = dataframe_append.vstack(df)
        return dataframe_append
    