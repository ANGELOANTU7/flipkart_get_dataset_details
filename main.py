import boto3
from collections import defaultdict
import yaml
import os
import tempfile
import json

def get_class_counts_s3(bucket_name, train_prefix, val_prefix, test_prefix, yaml_key):
    """
    Count the number of annotations per class in a YOLOv5 dataset stored in an S3 bucket.

    Parameters:
        bucket_name (str): Name of the S3 bucket.
        train_prefix (str): Prefix for the training annotation files in the bucket.
        val_prefix (str): Prefix for the validation annotation files in the bucket.
        test_prefix (str): Prefix for the testing annotation files in the bucket.
        yaml_key (str): Key of the YAML file in the S3 bucket containing dataset information.

    Returns:
        dict: A dictionary with class names as keys and their annotation counts as values.
        int: Total number of classes.
    """
    # Initialize S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
        region_name=os.getenv("REGION_NAME")
    )

    # Download the YAML file from S3
    with tempfile.NamedTemporaryFile(delete=True) as temp_yaml:
        s3.download_file(Bucket=bucket_name, Key=yaml_key, Filename=temp_yaml.name)

        # Read class names from the YAML file
        with open(temp_yaml.name, 'r') as f:
            data = yaml.safe_load(f)
    class_names = data['names']

    # Initialize annotation counts for each class
    class_counts = defaultdict(int)

    # Helper function to process a prefix
    def process_prefix(prefix):
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' not in response:
            print(f"No files found in the specified S3 prefix: {prefix}")
            return

        for obj in response['Contents']:
            file_key = obj['Key']
            if file_key.endswith('.txt'):
                # Download the file to a temporary location
                with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                    s3.download_file(Bucket=bucket_name, Key=file_key, Filename=temp_file.name)

                    # Process the file
                    with open(temp_file.name, 'r') as f:
                        for line in f:
                            class_id = int(line.split()[0])  # Extract class ID
                            class_counts[class_names[class_id]] += 1

    # Process train, val, and test prefixes
    process_prefix(train_prefix)
    process_prefix(val_prefix)
    process_prefix(test_prefix)

    return dict(class_counts), len(class_names)

def save_class_counts_to_s3(output_bucket, output_prefix, class_counts, num_classes):
    """
    Save class count details to an S3 bucket as a JSON file.

    Parameters:
        output_bucket (str): Name of the S3 bucket where the data will be saved.
        output_prefix (str): Prefix (folder path) in the bucket where the JSON file will be stored.
        class_counts (dict): Dictionary containing class annotation counts.
        num_classes (int): Total number of classes.
    """
    # Prepare the data to save
    data = {
        "total_classes": num_classes,
        "class_counts": class_counts
    }

    # Save to a JSON file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as temp_json:
        json.dump(data, temp_json, indent=4)
        temp_json_path = temp_json.name


    # Upload the JSON file to S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
        region_name=os.getenv("REGION_NAME")
    )

    output_key = os.path.join(output_prefix, "class_counts.json")
    s3.upload_file(temp_json_path, output_bucket, output_key)

    print(f"Class counts saved to s3://{output_bucket}/{output_key}")

    # Clean up the temporary file
    os.remove(temp_json_path)

# Example usage
bucket_name = 'flipkartdataset1'  # Replace with your S3 bucket name
train_prefix = 'train/'          # Replace with the prefix for train annotations in the bucket
val_prefix = 'valid/'            # Replace with the prefix for val annotations in the bucket
test_prefix = 'test/'            # Replace with the prefix for test annotations in the bucket
yaml_file = 'data.yaml'          # Replace with the path to your YAML file in the bucket

output_bucket = 'flipkartprocessedpreview'  # Replace with your output S3 bucket
output_prefix = 'dataset_details'    # Folder in the bucket to store the JSON file

class_counts, num_classes = get_class_counts_s3(bucket_name, train_prefix, val_prefix, test_prefix, yaml_file)
save_class_counts_to_s3(output_bucket, output_prefix, class_counts, num_classes)