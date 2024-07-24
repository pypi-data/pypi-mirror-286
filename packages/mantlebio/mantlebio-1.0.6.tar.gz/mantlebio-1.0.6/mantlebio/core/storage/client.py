from abc import ABC, abstractmethod
import os
from pathlib import Path
import time
from typing import Iterable, Optional, List
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.helpers.decorators import deprecated
import requests
from proto import data_type_pb2, tenant_pb2
from google.protobuf.message import DecodeError
from mantlebio.exceptions import MantleInvalidParameterError, MantleProtoError, MantleResourceNotFoundError, MantlebioError, StorageUploadError
import asyncio


class _IStorageClient(ABC):
    """Abstract class for interacting with cloud storage API.

    This class defines the interface for interacting with a cloud storage API.
    Subclasses of this class should implement the methods defined here.

    """

    @abstractmethod
    def download_file_from_storage(self, bucket: str, key: str, path: str):
        pass

    @abstractmethod
    def download_file(self, bucket: str, key: str, path: str):
        pass

    @abstractmethod
    def download(self, bucket: str, key: str, path: str):
        pass

    @abstractmethod
    def download_files_from_directory(self, bucket: str, prefix: str, path: str):
        pass

    @abstractmethod
    def upload(self, path: str, upload_key: Optional[str] = None):
        pass

    @abstractmethod
    def upload_file(self, path: str, upload_key: Optional[str] = None)-> data_type_pb2.S3File:
        pass

    @abstractmethod
    def upload_file_to_storage(self, path: str, upload_key: Optional[str] = None)-> data_type_pb2.S3File:
        pass

    @property
    @abstractmethod
    def upload_bucket(self) -> str:
        pass

    @property
    @abstractmethod
    def upload_prefix(self) -> str:
        pass

    @deprecated("2.0.0", "upload bucket is managed intenally and should not be accessed directly")
    @abstractmethod
    def get_upload_bucket(self) -> str:
        pass

class StorageClient(_IStorageClient):
    def __init__(self, session: _ISession):
        """
        Initializes a StorageClient object.

        Args:
            session (_ISession): The session object used for making requests.

        Raises:
            MantleProtoError: If there is an error parsing the storage configuration.
        """
        self._session = session
        self._route_stem = f"/blob/"
        self._max_retries = 3
        self._retryable_statuses = [429, 500, 502, 503, 504]

        req = self._session.make_request(
            "GET",
            f"{self._route_stem}config"
        )

        if not req.ok:
            req.raise_for_status()

        try:
            config = tenant_pb2.StorageConfiguration()
            config.ParseFromString(req.content)
            self._upload_bucket = config.upload_bucket
            self._upload_prefix = config.upload_prefix
        
        except DecodeError as e:
            raise MantleProtoError(req.content, tenant_pb2.StorageConfiguration) from e


    @deprecated("2.0.0", "use download instead")  
    def download_file_from_storage(self, bucket: str, key: str, path: str):
        """
        Download File from cloud storage will be removed in version 2.0.0 in favor of download_file

        Args:
            path (str): local path where the file will be downloaded
            bucket (str): storage bucket from which the file is to be downloaded
            key (str): cloud storage location at which the file will be downloaded
        """
        return self.download(bucket, key, path)
    
    @deprecated("2.0.0", "use download instead")
    def download_files_from_directory(self, bucket: str, prefix: str, path: str):
        self._download_files_from_directory(bucket, prefix, path)

    def _download_files_from_directory(self, bucket: str, prefix: str, path: str):
        keys = self._list_files(bucket=bucket, prefix=prefix)

        # TODO(ME-564): make this async
        for key in keys:
            try:
                self._download_file(bucket=bucket, key=key, path=os.path.join(path, key[len(prefix):]))
            except Exception as e:
                print(f"error downloading file {key}: {e}")
        return

    
    def download(self, bucket: str, key: str, path: str):
        """
        Download File(s) from cloud storage
        Args:            
            bucket (str): storage bucket from which the file(s) are to be downloaded
            key (str): cloud storage location at which the file(s) are located
            path (str): local path where the file(s) will be downloaded to
        """
        if key.endswith("/"):
            self._download_files_from_directory(bucket, key, path)
        else:
            self._download_file(bucket, key, path)

    def _download_file(self, bucket: str, key: str, path: str):
        directory_path = os.path.join(os.getcwd(), os.path.dirname(path))
        if not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path, exist_ok=True)
            except Exception as e:
                raise MantleInvalidParameterError(f"invalid path: failed to create directory {directory_path}: ${e}")
        
        payload = {
            "bucket": bucket,
            "key": key,
        }
        
        res = self._session.make_request(
            "POST",
            f"{self._route_stem}signdownloadurl",
            json=payload
        )

        if not res.ok:
            if res.status_code == 404:
                raise MantleResourceNotFoundError(f"{bucket}/{key}", res.content) from res.raise_for_status()
            res.raise_for_status()
        try:
            s3_file_proto = data_type_pb2.S3File()
            s3_file_proto.ParseFromString(res.content)
        
        except DecodeError as e:
            raise MantleProtoError(res.content, data_type_pb2.S3File) from e

        signed_url = s3_file_proto.download_url

        if not signed_url:
            raise MantlebioError("Download URL not found in response")
        
        res = requests.get(signed_url, stream=True)

        if not res.ok:
            res.raise_for_status()

        try:
            with open(path, 'wb') as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

        except Exception as e:
            raise MantlebioError(f"Failed to write to file: {path}") from e

    @deprecated("2.0.0", "use download instead")
    def download_file(self, bucket: str, key: str, path: str):
        """
        Download File from cloud storage
        Args:            
            bucket (str): storage bucket from which the file is to be downloaded
            key (str): cloud storage location at which the file will be downloaded
            path (str): local path where the file will be downloaded from
        """
        self.download(file=bucket, key=key, path=path)
        
    
    def upload(self, path: str, upload_key: Optional[str] = None)-> data_type_pb2.S3File:
        """Upload File or directory to cloud storage
        Args:
            path (str): local path to the file or directory  which is to be uploaded
            key (str): cloud storage location at which the uploaded file will be stored (optional) defaults to the file name
        """
        key = upload_key.strip('.').strip('/') if  upload_key else os.path.basename(path).strip("/")
        if os.path.isdir(path):
            # If the file path is a directory, upload all files in the directory
            if path[-1] != "/":
                path += "/"
            local_path = Path(path)
            for child_path in local_path.glob("*"):
                if child_path.is_file():
                    s3_key = f"{key}/{child_path.name}"
                    self.upload_file(path=str(child_path), upload_key=s3_key)
            return data_type_pb2.S3File(bucket=self._upload_bucket, key=f"{key}/")
        else:
            return self.upload_file(path, key)

    def upload_file(self, path: str, upload_key: Optional[str] = None)-> data_type_pb2.S3File:
        """Upload File to cloud storage
        Args:
            path (str): local path to the file which is to be uploaded
            key (str): cloud storage location at which the uploaded file will be stored (optional) defaults to the file name
        """
        if not os.path.exists(os.path.join(os.getcwd(), os.path.dirname(path))):
            raise MantleInvalidParameterError(f"Invalid path: File {path} does not exist.")
        _, tail = os.path.split(path)
        key = os.path.join(upload_key or tail)
        print(f"Uploading {path} to {self._upload_bucket}/{key}")
        file_size = os.path.getsize(path)
        print(f"File size: {file_size}")

        # If file is less than 200MB, upload directly.
        if file_size < 8 * 1024 * 1024:
            return self._upload_file_direct(self._upload_bucket, key, path)

        # If file is greater than 200MB, upload in part.
        return self._upload_file_multi_part(self._upload_bucket, key, path, file_size)
    

    @deprecated("2.0.0", "use upload_file instead")
    def upload_file_to_storage(self, path: str, upload_key: Optional[str] = None) -> data_type_pb2.S3File:
        """
        Uploads a file to the storage. Will be deprecated in version 2.0.0. in favor of upload_file.

        Args:
            path (str): The path of the file to be uploaded.
            upload_key (str, optional): The upload key for the file. Defaults to None.

        Returns:
            data_type_pb2.S3File: The uploaded file object.
        """
        return self.upload(path, upload_key)


    def _upload_file_direct(self, bucket: str, key: str, path: str) -> data_type_pb2.S3File:
        """
        Uploads a file directly to an S3 bucket using a pre-signed URL.

        Args:
            bucket (str): The name of the S3 bucket.
            key (str): The key or path of the file in the S3 bucket.
            path (str): The local path of the file to be uploaded.

        Returns:
            data_type_pb2.S3File: The S3File protobuf object containing information about the uploaded file.
        """

        payload = {
            "bucket": bucket,
            "key": key,
        }

        res = self._session.make_request(
            "POST",
            f"{self._route_stem}signuploadurl",
            json=payload
        )

        if not res.ok:
            res.raise_for_status()

        try:
            s3_file_proto = data_type_pb2.S3File()
            s3_file_proto.ParseFromString(res.content)
        except DecodeError as e:
            raise MantleProtoError(res.content, data_type_pb2.S3File) from e

        signed_url = s3_file_proto.upload_url

        if not signed_url:
            raise MantlebioError("Upload URL not found in response")

        res = requests.put(signed_url, data=open(path, "rb"))

        if not res.ok:
            res.raise_for_status()

        print(f"Upload complete to {bucket}/{key}")

        return s3_file_proto
    

    def _upload_file_multi_part(self, bucket: str, key: str, path: str, file_size: int)-> data_type_pb2.S3File:
        """
        Uploads a file in parts to the specified S3 bucket.

        Args:
            bucket (str): The name of the S3 bucket.
            key (str): The key or path of the file in the S3 bucket.
            path (str): The local path of the file to be uploaded.
            file_size (int): The size of the file to be uploaded.

        Returns:
            data_type_pb2.S3File: The uploaded file object.

        Raises:
            MantleProtoError: If there is an error parsing the response.
            StorageUploadError: If the multipart upload fails to upload a part.
        """
        req = data_type_pb2.InitiateMultipartUpload(
            file = data_type_pb2.S3File(bucket=bucket, key=key),
            size = file_size
        )
        res = self._session.make_request(
            "POST",
            f"{self._route_stem}initiateupload",
            data=req)
        if not res.ok:
            res.raise_for_status()
        try:
            multipart_upload = data_type_pb2.MultiPartUploadInitiated()
            multipart_upload.ParseFromString(res.content)
        except DecodeError as e:
            raise MantleProtoError(res.content, data_type_pb2.MultiPartUploadInitiated) from e

        upload_id = multipart_upload.upload_id
        num_parts = len(multipart_upload.parts)
        print(f"Initiated multipart upload with {num_parts} parts...")

        offset = 0
        with open(path, "rb") as f:
            for i in range(num_parts):
                print(f"Uploading part {i+1} of {num_parts}...")
                part = multipart_upload.parts[i]
                part_num = part.part_number
                part_size = part.size
                f.seek(offset)
                offset += part_size
                data = f.read(part_size)
                try:
                    etag = self._upload_part(
                        bucket, key, upload_id, part_num, data)
                except Exception as e:
                    self._abort_multipart_upload(bucket, key, upload_id)
                    raise StorageUploadError(f"Failed to upload part {part_num} of upload {upload_id}") from e

                print(f"Part {i+1} uploaded with etag {etag}")
                part.etag = etag

        print("Completing multipart upload...")
        self._complete_multipart_upload(
            bucket, key, upload_id, multipart_upload.parts)
        print(f"Upload complete to {bucket}/{key}")
        return data_type_pb2.S3File(bucket=bucket, key=key)

    def _upload_part(self, bucket: str, key: str, upload_id: str, part_num: int, data: bytes) -> str:
        """
        Uploads a part of a multipart upload to the specified S3 bucket.

        Args:
            bucket (str): The name of the S3 bucket.
            key (str): The key or path of the file in the S3 bucket.
            upload_id (str): The ID of the multipart upload.
            part_num (int): The part number.
            data (bytes): The data to be uploaded.

        Returns:
            str: The ETag of the uploaded part.
        
        Raises:
            MantleProtoError: If there is an error parsing the response.
            MantlebioError: If the upload URL is not found in the response.
        """
        req = data_type_pb2.MultipartUploadPart(
            file = data_type_pb2.S3File(bucket=bucket, key=key),
            upload_id = upload_id,
            part_number = part_num
        )

        res = self._session.make_request(
            "POST",
            f"{self._route_stem}signuploadparturl",
            data=req
        )

        if not res.ok:
            res.raise_for_status()

        try:
            part = data_type_pb2.UploadPartResponse()
            part.ParseFromString(res.content)
        except DecodeError as e:
            raise MantleProtoError(res.content, data_type_pb2.UploadPartResponse) from e

        signed_url = part.upload_url

        if not signed_url:
            raise MantlebioError("Upload URL not found in response")

        backoff = 2
        for attempt in range(1, self._max_retries + 1):
            print(f"Attempt number: {attempt} to perform multipart uplaod for part number {part_num}")

            res = requests.put(signed_url, data=data)

            if res.status_code in self._retryable_statuses:
                print(f"Transient error received ({res.status_code}), retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2
            else:
                break

        if not res.ok:
            if attempt == self._max_retries:
                print(f"Maximum retries {self._max_retries} exceeded")
            res.raise_for_status()

        etag = res.headers["ETag"]
        return etag
    
    def _complete_multipart_upload(self, bucket: str, key: str, upload_id: str, parts: Iterable[data_type_pb2.Part]):
        """
        Completes a multipart upload to the specified S3 bucket.

        Args:
            bucket (str): The name of the S3 bucket.
            key (str): The key or path of the file in the S3 bucket.
            upload_id (str): The ID of the multipart upload.
            parts (Iterable[data_type_pb2.Part]): The parts of the multipart upload.
        """
        req = data_type_pb2.CompleteMultipartUpload(
            file = data_type_pb2.S3File(bucket=bucket, key=key),
            upload_id = upload_id,
            parts = parts
        )

        res = self._session.make_request(
            "POST",
            f"{self._route_stem}completemultipartupload",
            data=req
        )

        if not res.ok:
            res.raise_for_status()


    def _abort_multipart_upload(self, bucket: str, key: str, upload_id: str):
        """
        Aborts a multipart upload for a given bucket, key, and upload ID.

        Args:
            bucket (str): The name of the bucket.
            key (str): The key of the object.
            upload_id (str): The ID of the multipart upload.

        Raises:
            StorageUploadError: If the multipart upload fails to abort.

        Returns:
            None
        """
        req = data_type_pb2.AbortMultipartUpload(
            file=data_type_pb2.S3File(bucket=bucket, key=key),
            upload_id=upload_id
        )

        res = self._session.make_request(
            "POST",
            f"{self._route_stem}abortmultipartupload",
            data=req
        )

        if not res.ok:
            raise StorageUploadError(f"Failed to abort multipart upload {upload_id}") from res.raise_for_status()

    @property
    def upload_bucket(self) -> str:
        """
        Returns the upload bucket for the storage client.

        :return: The upload bucket.
        """
        return self._upload_bucket
    
    @property
    def upload_prefix(self) -> str:
        """
        Returns the upload prefix for the storage client.

        :return: The upload prefix.
        """
        return self._upload_prefix
    
    @deprecated("2.0.0", "upload bucket is managed intenally and should not be accessed directly")
    def get_upload_bucket(self) -> str:
        """
        Returns the upload bucket for the storage client.

        :return: The upload bucket.
        """
        return self._upload_bucket
    
    def _list_files(self, bucket: str, prefix: str):
        """
        Lists all files from a bucket/prefix including from nested directories 
        Args:
            bucket (str): storage bucket from which the file is to be downloaded
            prefix (str): directory prefix from which to list contents
        """

        keys = []
        res = self._session.make_request(
            "GET",
            f"{self._route_stem}listkeys?bucket={bucket}&prefix={prefix}"
        )
        res.raise_for_status()

        keys_proto = tenant_pb2.ListKeysResponse()
        keys_proto.ParseFromString(res.content)

        # recursively traverse the nested subdirectories
        if keys_proto.keys:
            for key in keys_proto.keys:
                # we dont wnt to requery the same prefix and it is not a file so we just move to the next key
                if key == prefix:
                    continue
                if key.endswith("/"):
                    keys.extend(self._list_files(bucket=bucket, prefix=key))
                else:
                    keys.append(key)

        return keys

    