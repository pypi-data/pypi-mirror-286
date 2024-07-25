import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dataclasses import dataclass, field
from tqdm.notebook import tqdm

@dataclass
class FileTransfer:
    s3: boto3.client = field(init=False)

    def __post_init__(self):
        # Initialize the source S3 client
        self.s3 = boto3.client('s3')

    def transfer_files(self, source_bucket: str, source_prefix: str, dest_bucket: str, ticket_number: str):
        try:
            # List objects in the source bucket with the specified prefix
            response = self.s3.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix)
            new_prefix = f'schema=hydration_files/{ticket_number}/' 
            
            if 'Contents' not in response:
                print(f"No files found with prefix {source_prefix} in bucket {source_bucket}")
                return
            
            # Get the total number of objects to be copied
            total_objects = len(response['Contents'])
            progress_bar = tqdm(total=total_objects, desc='Copying Files', unit='file')
            
            for obj in response['Contents']:
                source_key = obj['Key']
                dest_key = new_prefix + source_key[len(source_prefix):]  # Replace prefix
                
                # Copy object
                copy_source = {'Bucket': source_bucket, 'Key': source_key}
                self.s3.copy_object(CopySource=copy_source, Bucket=dest_bucket, Key=dest_key)
                
                # Update the progress bar
                progress_bar.update(1)
                
            progress_bar.close()
            print("File transfer completed successfully.")

        except NoCredentialsError:
            print("Credentials not available.")
        except PartialCredentialsError:
            print("Incomplete credentials provided.")
        except Exception as e:
            print(f"An error occurred: {e}")
