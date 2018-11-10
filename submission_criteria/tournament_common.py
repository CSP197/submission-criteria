import botocore
import os
import pandas as pd


def _download_file(s3, s3_bucket, s3_filepath, local_filepath):
    try:
        s3.meta.client.download_file(s3_bucket, s3_filepath, local_filepath)
    except (botocore.exceptions.ClientError,
            botocore.exceptions.EndpointConnectionError) as e:
        raise Exception(f"Error when downloading {s3_filepath}: {str(e)}")


def get_file(s3, s3_bucket, s3_path, filename, local_path, download=True):
    # make dir if it does not exist
    local_path = os.path.join(local_path, s3_path)
    if not os.path.isdir(local_path):
        os.makedirs(local_path)
    s3_filepath = os.path.join(s3_path, filename)
    local_filepath = os.path.join(local_path, filename)
    if download and not os.path.isfile(local_filepath):
        print(
            f"Downloading file: s3://{s3_bucket}/{s3_filepath} to {local_filepath}"
        )
        _download_file(s3, s3_bucket, s3_filepath, local_filepath)
    print(f"Loading file: {local_filepath}")
    return pd.read_csv(local_filepath)


def get_validation_data(s3, s3_bucket, s3_path, local_path, download=True):
    return get_file(s3, s3_bucket, s3_path, "validation_data.csv", local_path,
                    download)


def get_test_data(s3, s3_bucket, s3_path, local_path, download=True):
    return get_file(s3, s3_bucket, s3_path, "test_data.csv", local_path,
                    download)
