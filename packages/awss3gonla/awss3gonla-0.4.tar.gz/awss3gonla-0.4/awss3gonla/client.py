import os
import io
import json
import uuid
import boto3
import polars as pl
from dataclasses import dataclass,field
from typing import Dict, Any, Optional
from awss3gonla.storage import IStorage


@dataclass
class client(IStorage):
    aws_access_key_id:Optional[str]=None
    aws_secret_access_key:Optional[str]=None
    region_name:Optional[str]=None
    bucket_name:Optional[str]=None
    s3_client: boto3.Session.client = field(init=False, default=None)

    def __post_init__(self):
        self.__call__()

    def __call__(self):
        self.s3_client = boto3.Session(
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            region_name = self.region_name
        ).client('s3')

    def get(self, path, name):
        pass
    def list(self, path: str):
        _list = self.s3_client.list_objects_v2(Bucket=self.bucket_name,
                                       Prefix=path)
        return _list
        
    def put(self,path:str,name:str):
        self.s3_client.upload_file(path, self.bucket_name, name)

    def put_object(self, path: str, name: str, _object: str | Dict[str, Any]):
        try:
            if isinstance(_object,str):
                content_type = 'text/plain'
                content = _object.encode('utf-8')
            elif isinstance(_object,dict):
                content = json.dumps(_object,indent=4,ensure_ascii=False).encode('utf-8')
                content_type = 'application/json'
            
            bucket_name = self.bucket_name
            key = os.path.join(path,name)
            key = key.replace("\\", "/")
            self.s3_client.put_object(Bucket=bucket_name, Key=key, Body=content, ContentType=content_type)

        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except UnboundLocalError as unbound_local_error:
            print(unbound_local_error)
        except TypeError as type_error:
            print(type_error)
        except AttributeError as attribute_error:
            print(attribute_error)
    
    def put_parquet(self,
                    dataframe:pl.DataFrame,
                    path:str,
                    name:str=None,
                    partition_cols:dict=None
                    )-> str:
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
    
    def list_parquet(self,path):
        _list = self.list(path)
        parquets = []
        if 'Contents' in _list:
            for obj in _list['Contents']:
                if obj['Key'].endswith('.parquet'):
                    parquets.append(obj['Key'])
        return parquets
    def get_objects(self,
                    path:str,
                    buffer: Any):
        self.s3_client.download_fileobj(self.bucket_name, path, buffer)

    def get_parquet_partition(self,
                    path:str
                    )->pl.DataFrame:
        parquets = self.list_parquet(path)
        dataframes = []
        for parquet in parquets:
            buffer = io.BytesIO()
            self.get_objects(parquet, buffer)
            buffer.seek(0)
            df = pl.read_parquet(buffer)
            dataframes.append(df)

        dataframe_append = dataframes[0]
        for df in dataframes[1:]:
            dataframe_append = dataframe_append.vstack(df)
        return dataframe_append
    