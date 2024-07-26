import json
import datetime
import os
import hashlib
from boto3 import resource, client
from botocore.exceptions import ClientError
from .config import ApplicationConfigurator, DEFAULT_CONFIG


class S3Service(object):

    host = None
    a_key = None
    s_key = None
    secure_connection = False
    entity = None

    def __init__(self, config=None):
        if config:
            self.host = config["STORAGE_HOST"]
            self.a_key = config["STORAGE_ACCESS_KEY"]
            self.s_key = config["STORAGE_SECRET_KEY"]
            self.secure_connection = config["STORAGE_SECURE_CONNECTION"]
        else:
            self.config = ApplicationConfigurator().get()
            self.host = self.config.get('STORAGE_HOST')
            self.a_key = self.config.get("STORAGE_ACCESS_KEY")
            self.s_key = os.environ.get('STORAGE_SECRET_KEY')
            self.secure_connection = self.config.get('STORAGE_SECURE_CONNECTION', False)

        self.s3_resource = resource('s3', endpoint_url=self.config["STORAGE_HOST"], aws_access_key_id=self.a_key, aws_secret_access_key=self.s_key)
        self.s3_client = client('s3', endpoint_url=self.config["STORAGE_HOST"], aws_access_key_id=self.a_key, aws_secret_access_key=self.s_key)
        self.dest_path = self.config.get('DESTINATION_PATH', '/tmp/')


    def get_buckets(self):
        buckets = self.s3_client.list_buckets()
        # print(buckets, flush=True)
        buckets_list = [{'_name': b['Name'], 'CreationDate': b['CreationDate']} for b in buckets['Buckets']]
        return buckets_list

    def get_bucket_by_name(self, bucket_name):
        try:
            response = self.s3_client.head_bucket(Bucket=bucket_name)
            return {'_name': bucket_name, 'CreationDate': response['ResponseMetadata']['HTTPHeaders']['date']}
        except ClientError as e:
            print(e, flush=True)
            return {}

    def create_object(self, file, bucket_name, supported_extensions=None, subfolder=None, file_name=None,
                      get_etag=False):
        self.validate_file_extension(file, supported_extensions)

        file_path = self.save_file_to_system(file)
        file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

        file_name = file_name if file_name else file.filename

        if subfolder:
            file_name = f"{subfolder}/{file_name}"

        with open(file_path, 'rb') as file_data:
            try:
                res = self.s3_client.upload_fileobj(file_data, bucket_name, file_name)
            except Exception as e:
                print(e, flush=True)
            os.remove(file_path)

        if get_etag:
            etag = self.get_etag(bucket_name, file_name)
            return file_name, file_hash, etag
        return file_name, file_hash

    @staticmethod
    def get_file_extension(original_file_name):
        return original_file_name.split(".")[-1]

    @staticmethod
    def validate_file_extension(file, supported_extensions=None):
        if supported_extensions and file.filename.rsplit(".")[1] not in supported_extensions:
            raise ValueError("Unsupported file extension")

    @staticmethod
    def save_file_to_system(file_object, folder_path='/tmp/'):
        file_path = folder_path + file_object.filename
        with open(file_path, 'wb') as f:
            f.write(file_object.read())
        return file_path

    def get_all_from_all_buckets(self):
        buckets = self.get_buckets()
        objects_list = []

        for bucket in buckets:
            try:
                objects_in_bucket = self.s3_client.list_objects(Bucket=bucket['_name'])
                if "Contents" in objects_in_bucket:
                    for obj in objects_in_bucket["Contents"]:
                        obj['ETag'] = self.get_etag(obj['Key'])
                        obj['_name'] = obj["Key"]
                        obj['_bucket_name'] = bucket['_name']
                        obj['_object_name'] = obj["Key"]
                        obj['_etag'] = self.get_etag(obj['Key'])
                        objects_list.append(obj)
            except ClientError as e:
                print(e, flush=True)

        return objects_list

    def get_all_from_bucket(self, bucket_name):
        objects_list = []

        try:
            objects_in_bucket = self.s3_client.list_objects(Bucket=bucket_name)
            if "Contents" in objects_in_bucket:
                for obj in objects_in_bucket:
                    obj['ETag'] = self.get_etag(obj['Key'])
                    obj['_name'] = obj["Key"]
                    obj['_bucket_name'] = bucket_name
                    obj['_object_name'] = obj["Key"]
                    obj['_etag'] = self.get_etag(obj['Key'])
                    objects_list.append(obj)
        except ClientError as e:
            print(e, flush=True)

        return objects_list

    def get_number_of_objects_in_bucket(self, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            return response.get('KeyCount', 0)
        except ClientError as e:
            print(e, flush=True)
            return 0

    def delete_bucket(self, bucket_name):
        try:
            self.s3_client.delete_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            print(e, flush=True)
            return False

    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            print(e, flush=True)
            return False

    def download_file(self, filename, bucket):
        try:
            self.s3_client.download_file(bucket, filename, '/tmp/' + filename)
        except ClientError as e:
            print(e, flush=True)

    def delete_object(self, bucket_name, object_name):
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        except ClientError as e:
            print(e, flush=True)

    def validate_object_type(self, data):
        pass

    def validate_object_content(self, data):
        pass

    def copy_file(self, source_bucket, source_object, dest_bucket, dest_object):
        try:
            result = self.s3_client.copy_object(
                CopySource={'Bucket': source_bucket, 'Key': source_object},
                Bucket=dest_bucket,
                Key=dest_object
            )
            return result
        except ClientError as e:
            print(e, flush=True)
            return None


    def move_file(self, source_bucket, source_object, dest_bucket, dest_object):
        try:
            result = self.copy_file(source_bucket, source_object, dest_bucket, dest_object)
            if result:
                self.s3_client.delete_object(Bucket=source_bucket, Key=source_object)
                etag = self.get_etag(dest_bucket, dest_object)
                return etag
            else:
                return None
        except ClientError as e:
            print(e, flush=True)
            return None

    def get_etag(self, file_name):
        etag = hashlib.md5(file_name.encode('utf-8')).hexdigest()
        return etag


    ### FROM EXECUTOR FILES_SERVICE.PY FILE

    def save_file(self, file, bucket_name, supported_extensions=None):

        self.validate_file_extension(file)

        full_file_name = file.filename

        file.save(self.dest_path + full_file_name)
        file_stat = os.stat(self.dest_path + full_file_name)
        file_hash = hashlib.md5(open(self.dest_path + full_file_name, 'rb').read()).hexdigest()

        if file_stat.st_size == 0:
            raise Exception("File is empty.")

        with open(self.dest_path + full_file_name, 'rb') as file_data:
            self.s3_client.put_object(Bucket=bucket_name, Key=full_file_name, Body=file_data, ContentLength=file_stat.st_size)
            os.remove(self.dest_path + full_file_name)

        return full_file_name, file_hash

    def get_file(self, filename, bucket=None):
        download_path = self.dest_path + filename
        self.makedirs(download_path)


        if not bucket:
            bucket = filename.split("/", 1)[0]
            filename = filename.split("/", 1)[1]

        try:
            self.s3_client.download_file(bucket, filename, download_path)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                print("The object does not exist.")
            else:
                raise e

        return download_path

    def get_local_path(self, filename):
        return self.dest_path + filename

    def upload_file(self, file, bucket_name):

        # If 'file' is a string, it's treated as a file path
        if isinstance(file, str):
            with open(file, 'rb') as f:
                # Uploading the file to S3 bucket
                self.s3_client.upload_fileobj(f, bucket_name, file.split('/')[-1])  # Upload file directly from file object
                print(f"File uploaded successfully to bucket '{bucket_name}'")
        else:
            # Uploading the file to S3 bucket
            self.s3_client.upload_fileobj(file, bucket_name, file.name)  # Upload file directly from file object
            print(f"File uploaded successfully to bucket '{bucket_name}'")

    def makedirs(self, path):
        """Wrapper of os.makedirs() ignores errno.EEXIST."""
        try:
            if path:
                directory_path = os.path.dirname(path)
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
        except OSError as exc:  # Python >2.5

            if not os.path.isdir(path):
                raise ValueError(
                    "path {0} is not a directory".format(path),
                ) from exc

    def upload_from_path(self, file_name, file_path, bucket_name, supported_extensions=None, subfolder=None):
        if not self.validate_file_extension(file_name, supported_extensions):
            return None, None

        file_stat = os.stat(file_path)

        uploadfilename = file_name

        if subfolder:
            uploadfilename = f"{subfolder}/{uploadfilename}"

        with open(file_path, 'rb') as file_data:
            self.s3_client.upload_fileobj(file_data, bucket_name, uploadfilename)
            file_hash = hashlib.md5(file_data.read()).hexdigest()
            os.remove(file_path)

        return uploadfilename, file_hash

class MinioService(S3Service):

    def __init__(self, config=None):

        super().__init__(config)
        self.service = self.s3_client
