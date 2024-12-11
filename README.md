# YOLOv5 Annotation Class Count Lambda Function

This AWS Lambda function processes YOLOv5 annotation files stored in an S3 bucket, counts the number of annotations for each class, and saves the results to another S3 bucket in JSON format.

## Description

The function is designed to:

1. Download a YAML configuration file (`data.yaml`) from the input S3 bucket, which contains the class names used in the YOLOv5 annotations.
2. Process the annotation files (with `.txt` extension) stored in the S3 prefixes (`train/`, `valid/`, and `test/`).
3. Count the number of annotations for each class based on the class IDs in the annotation files.
4. Save the class counts in a JSON file and upload it to the specified output S3 bucket.

## Features

- Downloads the `data.yaml` file from an S3 bucket to get class names.
- Reads and processes YOLOv5 annotation files (in `.txt` format).
- Counts the occurrences of each class in the annotations.
- Saves the results as a JSON file and uploads it to the output S3 bucket.
- Handles multiple prefixes (`train/`, `valid/`, and `test/`) for annotation files.

## Inputs

- **S3 Bucket Names:**
  - `bucket_name` (Input S3 bucket containing YOLOv5 annotation files and `data.yaml`).
  - `output_bucket` (Output S3 bucket to store the class count results).

- **Prefixes:**
  - `train_prefix` (Prefix in the input bucket where training annotation files are stored).
  - `val_prefix` (Prefix in the input bucket where validation annotation files are stored).
  - `test_prefix` (Prefix in the input bucket where test annotation files are stored).

- **YAML File:**
  - The function expects the YAML file (`data.yaml`) to contain a key `names` with a list of class names in the format:
    ```yaml
    names:
      - class_1
      - class_2
      - class_3
      ...
    ```

## Outputs

- **JSON File:**
  - A JSON file (`class_counts.json`) containing the class counts, which is uploaded to the output S3 bucket.

Example output:
```json
{
  "total_classes": 80,
  "class_counts": {
    "class_1": 1200,
    "class_2": 1500,
    ...
  }
}
```

- The JSON file is saved under the `dataset_details` prefix in the specified output S3 bucket.

## AWS Lambda Function Flow

1. The Lambda function is triggered and receives event data with S3 bucket and prefix information.
2. The function downloads the `data.yaml` file from the input S3 bucket to get the class names.
3. The function iterates through the S3 prefixes (`train/`, `valid/`, and `test/`) and processes annotation files:
   - Downloads annotation files (`.txt`) from S3.
   - Parses each annotation file to extract the class ID from each line and updates the count for that class.
4. After processing all annotation files, the function creates a JSON file containing the total count for each class.
5. The JSON file is uploaded to the specified output S3 bucket.

## Error Handling

- If the required input parameters (bucket names) are missing, the function will return an error.
- If no files are found in a given prefix, the function will log a message and continue processing other prefixes.
- Any other exceptions encountered during the process are caught and returned in the error message.

## Requirements

- AWS Lambda with appropriate IAM permissions for accessing the input and output S3 buckets.
- AWS SDK (`boto3`) for interacting with S3.
- YAML library (`PyYAML`) to parse the `data.yaml` file.

## Setup Instructions

1. **Create an S3 Bucket:**
   - Create an input S3 bucket (`flipkartdataset1`) to store your YOLOv5 annotations and the `data.yaml` file.
   - Create an output S3 bucket (`flipkartprocessedpreview`) to store the resulting JSON file.

2. **Prepare `data.yaml`:**
   - The `data.yaml` file should contain the class names in the format shown above.

3. **Upload Annotations:**
   - Upload your YOLOv5 annotations (as `.txt` files) to the appropriate prefixes (`train/`, `valid/`, `test/`) in your input S3 bucket.

4. **Deploy Lambda Function:**
   - Deploy the provided Lambda function to AWS Lambda.
   - Ensure the Lambda execution role has the necessary permissions to read from the input S3 bucket and write to the output S3 bucket.

5. **Trigger Lambda:**
   - You can trigger the Lambda function based on an event, such as a file upload to the input S3 bucket, or you can invoke it manually.

## Example Invocation

```json
{
  "bucket_name": "flipkartdataset1",
  "output_bucket": "flipkartprocessedpreview"
}
```

After the Lambda function executes, you can find the output `class_counts.json` file in the `dataset_details` prefix of the output S3 bucket.

