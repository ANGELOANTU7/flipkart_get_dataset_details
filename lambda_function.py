import boto3
from collections import defaultdict
import yaml
import os
import json

def lambda_handler(event, context):
    """
    AWS Lambda function to count YOLOv5 annotations per class and save the results to S3.

    Parameters:
        event (dict): Input event containing S3 bucket and prefix information.
        context (object): Lambda execution context (unused).

    Returns:
        dict: Status message.
    """



    # Extract input parameters from the event
    bucket_name = "flipkartdataset1"
    train_prefix =  "train/"
    val_prefix =  "valid/"
    test_prefix =  "test/"
    yaml_key = "data.yaml"
    output_bucket = "flipkartprocessedpreview"
    output_prefix = "dataset_details"

    if not bucket_name or not output_bucket:
        return {"status": "Error", "message": "Missing required bucket parameters."}

    # Initialize S3 client
    s3 = boto3.client('s3')

    try:
        # Download and read the YAML file from S3
        yaml_path = '/tmp/data.yaml'
        s3.download_file(Bucket=bucket_name, Key=yaml_key, Filename=yaml_path)
        with open(yaml_path, 'r') as f:
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
                    file_path = f"/tmp/{os.path.basename(file_key)}"
                    s3.download_file(Bucket=bucket_name, Key=file_key, Filename=file_path)

                    # Process the file
                    with open(file_path, 'r') as f:
                        for line in f:
                            class_id = int(line.split()[0])  # Extract class ID
                            class_counts[class_names[class_id]] += 1

        # Process train, val, and test prefixes
        process_prefix(train_prefix)
        process_prefix(val_prefix)
        process_prefix(test_prefix)

        # Prepare the data to save
        data = {
            "total_classes": len(class_names),
            "class_counts": dict(class_counts)
        }

        # Save to a JSON file
        json_path = '/tmp/class_counts.json'
        with open(json_path, 'w') as temp_json:
            json.dump(data, temp_json, indent=4)

        # Upload the JSON file to S3
        output_key = os.path.join(output_prefix, "class_counts.json")
        s3.upload_file(json_path, output_bucket, output_key)

        print(f"Class counts saved to s3://{output_bucket}/{output_key}")
        return {"status": "Success", "message": f"Data saved to s3://{output_bucket}/{output_key}"}

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "Error", "message": str(e)}
