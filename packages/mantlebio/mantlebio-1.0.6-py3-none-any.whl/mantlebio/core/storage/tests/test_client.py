import json
from pathlib import Path
from typing import List, Optional
import unittest
from unittest import mock
import os
from mantlebio.core.storage.client import StorageClient
from mantlebio.exceptions import MantleInvalidParameterError, MantleProtoError, MantlebioError, MantleResourceNotFoundError
from mantlebio.tests.helpers import create_large_test_file, create_test_reponse, create_test_session

from requests import HTTPError
from proto import data_type_pb2, tenant_pb2

        
class TestStorageClient(unittest.TestCase):
    def setUp(self):
        # add test_upload.txt to current directory
        with open(f"{os.getcwd()}/test_upload.txt", "w") as f:
            f.write("test content")

        create_large_test_file(f"{os.getcwd()}/test_large_upload.txt", size_mb=205)

        os.mkdir(f"{os.getcwd()}/test_folder")

        with open(f"{os.getcwd()}/test_folder/file1.txt", "w") as f:
            f.write("test content")

        with open(f"{os.getcwd()}/test_folder/file2.txt", "w") as f:
            f.write("test content")

        self.test_bucket = "test_bucket"
        self.test_key = "test_key"
        self.test_download_path = f"test_out.txt"
        self.test_download_dir = "test_output_dir"
        self.test_download_paths = [f"{os.getcwd()}/{self.test_download_dir}/file1.txt", f"{os.getcwd()}/{self.test_download_dir}/file2.txt"]
        self.test_upload_path = f"test_upload.txt"
        self.test_upload_folder = f"test_folder"
        self.test_upload_folder_contents = [Path(f"{self.test_upload_folder}/file1.txt"), Path(f"{self.test_upload_folder}/file2.txt")]

        self.upload_id = "test_upload_id"
        self.part_num = 1
        self.data = b"test data"

        self.test_storage_config = tenant_pb2.StorageConfiguration(
            upload_bucket=self.test_bucket,
            upload_prefix="test_prefix"
        )
        self.test_s3_file_download = data_type_pb2.S3File(
            bucket=self.test_bucket,
            key=self.test_key,
            download_url="https://example.com/test-object?signature=5cb5f867-5712-4f39-b45e-481f1f21f65b&expires=1708813241"
        )
        self.test_s3_file_upload = data_type_pb2.S3File(
            bucket=self.test_bucket,
            key=self.test_key,
            upload_url="https://example.com/test-object?signature=5cb5f867-5712-4f39-b45e-481f1f21f65b&expires=1708813241"
        )
        self.test_file_upload_size = 100
        self.test_file_download_content = b'test download content'
        self.test_directory_list_key = tenant_pb2.ListKeysResponse(keys=[f"{self.test_key}/", f"{self.test_key}/file1.txt", f"{self.test_key}/file2.txt"])

    def tearDown(self):
        os.remove(self.test_upload_path)
        os.remove(f"{os.getcwd()}/test_large_upload.txt")
        if os.path.exists(self.test_download_path):
            os.remove(self.test_download_path)

        os.remove(f"{os.getcwd()}/test_folder/file1.txt")
        os.remove(f"{os.getcwd()}/test_folder/file2.txt")
        os.rmdir(f"{os.getcwd()}/test_folder")

        if os.path.exists(f"{os.getcwd()}/test_output_dir/file1.txt"):
            os.remove(f"{os.getcwd()}/test_output_dir/file1.txt")
        if os.path.exists(f"{os.getcwd()}/test_output_dir/file2.txt"):
            os.remove(f"{os.getcwd()}/test_output_dir/file2.txt")
        if os.path.exists(f"{os.getcwd()}/test_output_dir"):
            os.rmdir(f"{os.getcwd()}/test_output_dir")
                 
    @mock.patch('requests.get')
    def test_download_success(self, mock_get: mock.MagicMock):
        test_session = create_test_session(make_request_fns=[
                                                    lambda: create_test_reponse(
                                                        status_code=200,
                                                        content=self.test_storage_config.SerializeToString()
                                                    ),
                                                    lambda: create_test_reponse(
                                                        status_code=200,
                                                        content=self.test_s3_file_download.SerializeToString()
                                                        )
                                                ])

        mock_get.return_value.status_code = 200
        mock_get.return_value.stream = True 
        mock_get.return_value.iter_content.return_value = [self.test_file_download_content]

        client = StorageClient(test_session)

        client.download(self.test_bucket, self.test_key, self.test_download_path)

        with open(self.test_download_path, "rb") as f:
            self.assertEqual(f.read(), self.test_file_download_content)

    @mock.patch('requests.get')
    def test_download_success_s3_directory(self, mock_get: mock.MagicMock):
        test_session = create_test_session(make_request_fns=[
                                                    lambda: create_test_reponse(
                                                        status_code=200,
                                                        content=self.test_storage_config.SerializeToString()
                                                    ),
                                                    lambda: create_test_reponse(
                                                        status_code=200,
                                                        content=self.test_directory_list_key.SerializeToString()
                                                    ),
                                                    lambda: create_test_reponse(
                                                        status_code=200,
                                                        content=self.test_s3_file_download.SerializeToString()
                                                        ),
                                                    lambda: create_test_reponse(
                                                        status_code=200,
                                                        content=self.test_s3_file_download.SerializeToString()
                                                        )

                                                ])

        mock_get.return_value.status_code = 200
        mock_get.return_value.stream = True 
        mock_get.return_value.iter_content.return_value = [self.test_file_download_content]

        client = StorageClient(test_session)

        client.download(self.test_bucket, self.test_key+"/", self.test_download_dir)

        for path in self.test_download_paths:
            with open(path, "rb") as f:
                self.assertEqual(f.read(), self.test_file_download_content)
    
    
    # test failed multi part upload
    @mock.patch('requests.put')
    def test_upload_part(self, mock_put: mock.MagicMock):
        # Set up a list of mock responses with different status codes
        # status codes change everytime put reqeust is called
        mock_responses = [
            mock.MagicMock(status_code=429, headers={"Retry-After": "1"}),
            mock.MagicMock(status_code=500),
            mock.MagicMock(status_code=200, headers={"ETag": "test_etag"})
        ]
        # Use side_effect to return a different response each time the mock is called
        mock_put.side_effect = mock_responses
        
        test_session = create_test_session(
            make_request_fns=[
            lambda: create_test_reponse(
                status_code=200,
                content=self.test_storage_config.SerializeToString()
            ),
            lambda: create_test_reponse(
                status_code=200,
                content=data_type_pb2.UploadPartResponse(
                    upload_id=self.upload_id,
                    file=data_type_pb2.S3File(bucket=self.test_bucket, key=self.test_key),
                    part_number=self.part_num,
                    upload_url="https://example.com/test-object"
                ).SerializeToString()
            ),
            lambda: create_test_reponse(
                status_code=429
            ),
            lambda: create_test_reponse(
                status_code=500
            ),
            lambda: create_test_reponse(
                status_code=200
            ),
        ])

        client = StorageClient(test_session)

        etag = client._upload_part(self.test_bucket, self.test_key, self.upload_id, self.part_num, self.data)

        mock_put.assert_has_calls([
            mock.call("https://example.com/test-object", data=self.data),
            mock.call("https://example.com/test-object", data=self.data),
            mock.call("https://example.com/test-object", data=self.data)
        ])

        self.assertEqual(etag, "test_etag")
    
    def test_download_http_error(self):
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(
                status_code=200,
                content=self.test_storage_config.SerializeToString()
            ),
            lambda: create_test_reponse(status_code=404)
            ])
        client = StorageClient(test_session)

        with self.assertRaises(MantleResourceNotFoundError):
            client.download(self.test_bucket, self.test_key, self.test_download_path)

    def test_download_protocol_buffer_error(self):
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(
                status_code=200,
                content=self.test_storage_config.SerializeToString()
            ),
            lambda: create_test_reponse(status_code=200, content=b'{"a":"Not S3 File Response"}')
            ])
        client = StorageClient(test_session)
        
        with self.assertRaises(MantleProtoError):
            client.download(self.test_bucket, self.test_key, self.test_download_path)

    def test_download_invalid_path(self):
        test_session = create_test_session(make_request_fns=[ 
            lambda: create_test_reponse(
                status_code=200,
                content=self.test_storage_config.SerializeToString()
            )
            ])
        client = StorageClient(test_session)
        
        with mock.patch('os.makedirs', side_effect=PermissionError("Permission denied")):
            with self.assertRaises(MantleInvalidParameterError):
                client.download(self.test_bucket, self.test_key, "/invalid/path")

    def test_download_invalid_signed_url(self):
        test_s3_file_download_no_url = data_type_pb2.S3File(
            bucket=self.test_bucket,
            key=self.test_key,
            download_url=""
        )
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            lambda: create_test_reponse(status_code=200, content=test_s3_file_download_no_url.SerializeToString())])
        client = StorageClient(test_session)
        
        with self.assertRaises(MantlebioError):
            client.download(self.test_bucket, self.test_key, self.test_download_path)

    @mock.patch('requests.get')
    def test_download_file_write_error(self, mock_get: mock.MagicMock):
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            lambda: create_test_reponse(status_code=200, content=self.test_s3_file_download.SerializeToString())
            ])
        mock_get.return_value.status_code = 200
        mock_get.return_value.stream = True
        mock_get.return_value.iter_content.return_value = ['test invalid data']
        client = StorageClient(test_session)
        
        with self.assertRaises(MantlebioError):
            client.download(self.test_bucket, self.test_key, self.test_download_path)

    @mock.patch('os.path.exists')
    @mock.patch('requests.put')
    @mock.patch('builtins.print')
    def test_upload_with_directory(self, mock_print: mock.MagicMock, mock_put: mock.MagicMock, mock_exists: mock.MagicMock):
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            lambda: create_test_reponse(status_code=200, content=self.test_s3_file_upload.SerializeToString()),
            lambda: create_test_reponse(status_code=200, content=self.test_s3_file_upload.SerializeToString())
            ])

        mock_put.return_value.status_code = 200
        mock_exists.return_value = True

        client = StorageClient(test_session)

        uploadResult = client.upload(self.test_upload_folder)

        assert uploadResult == data_type_pb2.S3File(bucket=self.test_bucket, key=f"{self.test_upload_folder}/")

        mock_print.assert_has_calls([
            mock.call(f'Upload complete to {self.test_bucket}/{self.test_upload_folder}/file1.txt'),
            mock.call(f'Upload complete to {self.test_bucket}/{self.test_upload_folder}/file2.txt')
        ], any_order=True)

        

    @mock.patch('os.path.exists')
    @mock.patch('requests.put')
    @mock.patch('builtins.print')
    def test_upload_with_directory_include_key(self, mock_print: mock.MagicMock, mock_put: mock.MagicMock, mock_exists: mock.MagicMock):
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            lambda: create_test_reponse(status_code=200, content=self.test_s3_file_upload.SerializeToString()),
            lambda: create_test_reponse(status_code=200, content=self.test_s3_file_upload.SerializeToString())
            ])

        mock_put.return_value.status_code = 200
        mock_exists.return_value = True

        client = StorageClient(test_session)

        client.upload(self.test_upload_folder, f"./{self.test_upload_folder}")

        mock_print.assert_has_calls([
            mock.call(f'Upload complete to {self.test_bucket}/{self.test_upload_folder}/file1.txt'),
            mock.call(f'Upload complete to {self.test_bucket}/{self.test_upload_folder}/file2.txt')
        ], any_order=True)

    @mock.patch('os.path.exists')
    @mock.patch('requests.put')
    @mock.patch('builtins.print')
    def test_upload_file_small(self,mock_print: mock.MagicMock,mock_put: mock.MagicMock, mock_exists: mock.MagicMock):
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            lambda: create_test_reponse(status_code=200, content=self.test_s3_file_upload.SerializeToString())
            ])

        mock_put.return_value.status_code = 200
        mock_exists.return_value = True

        client = StorageClient(test_session)

        client.upload_file(self.test_upload_path, self.test_key)

        mock_print.assert_called_with(f'Upload complete to {self.test_bucket}/{self.test_key}')
    
    @mock.patch('os.path.exists')
    def test_upload_file_invalid_path(self, mock_exists: mock.MagicMock):
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            ])
        client = StorageClient(test_session)
        
        mock_exists.return_value = False

        with self.assertRaises(MantleInvalidParameterError):
            client.upload_file("/invalid/path", self.test_key)

    def test_upload_file_no_signed_url(self):
        test_s3_file_upload_no_url = data_type_pb2.S3File(
            bucket=self.test_bucket,
            key=self.test_key
        )
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            lambda: create_test_reponse(status_code=200, content=test_s3_file_upload_no_url.SerializeToString())
            ])
        client = StorageClient(test_session)
        
        with self.assertRaises(MantlebioError):
            client.upload_file(self.test_upload_path, self.test_key)
    
    def test_upload_file_http_error(self):
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            lambda: create_test_reponse(status_code=404,url="https://someurl.com", content=b'{"error" : "not found"}')])
        client = StorageClient(test_session)
        
        with self.assertRaises(MantleResourceNotFoundError):
            client.upload_file(self.test_upload_path, self.test_key)

    def test_upload_file_protocol_buffer_error(self):
        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            lambda: create_test_reponse(status_code=200, content=b'{"a":"Not S3 File Response"}')
            ])
        client = StorageClient(test_session)
        
        with self.assertRaises(MantleProtoError):
            client.upload_file(self.test_upload_path, self.test_key)

    @mock.patch('requests.put')
    @mock.patch('builtins.print')
    def test_upload_file_large(self,mock_print: mock.MagicMock ,mock_put: mock.MagicMock,):
        test_session = create_test_session(
            make_request_fns=[
                lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
                lambda: create_test_reponse(
                    status_code=200,
                    content=data_type_pb2.MultiPartUploadInitiated(
                        upload_id="abc123",
                        first_upload=data_type_pb2.UploadPartResponse(
                            upload_id="abc123",
                            part_number=1,
                            upload_url="https://example.com/test-object?signature=5cb5f867-5712-4f39-b45e-481f1f21f65b&expires=1708813241"
                        ),
                        parts=[ 
                            data_type_pb2.Part(part_number=1, size=100, etag="abc123"),
                            data_type_pb2.Part(part_number=2, size=100, etag="abc124"),
                            data_type_pb2.Part(part_number=3, size=5, etag="abc125")
                        ]
                    ).SerializeToString()),
                lambda: create_test_reponse(
                    status_code=200,
                    content=data_type_pb2.UploadPartResponse(
                        upload_id="abc123",
                        file=data_type_pb2.S3File(bucket=self.test_bucket, key=self.test_key),
                        part_number=1,
                        upload_url="https://example.com/test-object?signature=5cb5f867-5712-4f39-b45e-481f1f21f65b&expires=1708813241"
                    ).SerializeToString()),
                lambda: create_test_reponse(
                    status_code=200, 
                    content=data_type_pb2.UploadPartResponse(
                        upload_id="abc124",
                        file=data_type_pb2.S3File(bucket=self.test_bucket, key=self.test_key),
                        part_number=2,
                        upload_url="https://example.com/test-object?signature=5cb5f867-5712-4f39-b45e-481f1f21f65b&expires=1708813241"
                    ).SerializeToString()),
                lambda: create_test_reponse(
                    status_code=200, 
                    content=data_type_pb2.UploadPartResponse(
                        upload_id="abc125",
                        file=data_type_pb2.S3File(bucket=self.test_bucket, key=self.test_key),
                        part_number=3,
                        upload_url="https://example.com/test-object?signature=5cb5f867-5712-4f39-b45e-481f1f21f65b&expires=1708813241"
                    ).SerializeToString()),
                lambda: create_test_reponse(status_code=200)
            ]
        )

        mock_put.return_value.status_code = 200
        mock_put.return_value.headers = {"ETag": "abc123"}

        client = StorageClient(test_session)

        client.upload_file(f"{os.getcwd()}/test_large_upload.txt", self.test_key)
        mock_print.assert_called_with(f'Upload complete to {self.test_bucket}/{self.test_key}')

        mock_put.assert_has_calls(calls =[
            mock.call("https://example.com/test-object?signature=5cb5f867-5712-4f39-b45e-481f1f21f65b&expires=1708813241", data=b'0' * 100),
            mock.call("https://example.com/test-object?signature=5cb5f867-5712-4f39-b45e-481f1f21f65b&expires=1708813241", data=b'0' * 100),
            mock.call("https://example.com/test-object?signature=5cb5f867-5712-4f39-b45e-481f1f21f65b&expires=1708813241", data=b'0' * 5)
        ], any_order=True)

    def test_list_files_with_nested_directories(self):
        """
        Tests that _list_files correctly handles nested directory structures.
        """
        test_bucket = "test_bucket"
        test_prefix = "test_dir/"

        test_session = create_test_session(make_request_fns=[
            lambda: create_test_reponse(status_code=200, content=self.test_storage_config.SerializeToString()),
            lambda: create_test_reponse(
                status_code=200,
                content=tenant_pb2.ListKeysResponse(
                    keys=["test_dir/","test_dir/file1.txt", "test_dir/subdir/"]
                ).SerializeToString()),
            lambda: create_test_reponse(
                status_code=200,
                content=tenant_pb2.ListKeysResponse(
                    keys=["test_dir/subdir/","test_dir/subdir/file2.txt"]
                ).SerializeToString()),
            ]
        )

        client = StorageClient(test_session)
        keys = client._list_files(test_bucket, test_prefix)

        self.assertEqual(["test_dir/file1.txt","test_dir/subdir/file2.txt"], keys)

