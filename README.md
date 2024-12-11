
# Dataset Analysis Lambda Function

## Description

This AWS Lambda function processes YOLOv11 annotation files stored in an S3 bucket, counts the number of annotations for each class, and saves the results as a JSON file in another S3 bucket. The function provides a dataset analysis report, offering insights into the distribution of class occurrences within the dataset.

### Key Features

- Downloads the `data.yaml` file from an S3 bucket, which contains the class names used in the YOLOv11 annotations.
- Reads and processes YOLOv11 annotation files (with `.txt` extension) stored in `train/`, `valid/`, and `test/` prefixes.
- Counts the occurrences of each class in the annotation files.
- Saves the class count results as a JSON file and uploads it to a specified output S3 bucket.

---

## Inputs

### 1. **S3 Bucket Names**
   - **`bucket_name`**: Input S3 bucket containing YOLOv11 annotation files and `data.yaml` (e.g., `flipkartdataset1`).
   - **`output_bucket`**: Output S3 bucket to store the resulting class count JSON file (e.g., `flipkartprocessedpreview`).

### 2. **Prefixes for Annotation Files**
   - **`train_prefix`**: Prefix in the input bucket where training annotation files are stored (e.g., `train/`).
   - **`val_prefix`**: Prefix in the input bucket where validation annotation files are stored (e.g., `valid/`).
   - **`test_prefix`**: Prefix in the input bucket where test annotation files are stored (e.g., `test/`).

### 3. **YAML File**
   - The function expects the YAML file (`data.yaml`) to contain a key `names` with a list of class names. The YAML structure should look like:
     ```yaml
     names:
       - class_1
       - class_2
       - class_3
       ...
     ```

---

## Outputs

### JSON File
   - **File Name**: `dataset_analysis.json`
   - **Content**: Contains the total count for each class, formatted as follows:
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
   - **Location**: The JSON file is uploaded to the `dataset_analysis` prefix in the specified output S3 bucket.

---

## AWS Lambda Function Flow

1. **Download `data.yaml`**: The function retrieves the `data.yaml` file from the input S3 bucket to get class names.
2. **Process Annotations**: The function iterates through the `train/`, `valid/`, and `test/` prefixes, processing YOLOv11 annotation files (in `.txt` format):
   - Downloads the annotation files.
   - Extracts class IDs from the annotations and updates the count for each class.
3. **Generate JSON**: After processing all annotation files, the function creates a JSON file containing the total class count.
4. **Upload JSON**: The resulting JSON file is uploaded to the specified output S3 bucket in the `dataset_analysis` prefix.

---

## Error Handling

- **Missing Input Parameters**: If required parameters (like bucket names) are missing, the function will return an error message.
- **Empty Prefixes**: If no annotation files are found in a given prefix, the function logs a message and continues processing the remaining prefixes.
- **Exceptions**: Any exceptions encountered during the process are logged and returned in the error message.

---

## Requirements

- **IAM Permissions**: The Lambda execution role must have permissions to read from the input S3 bucket and write to the output S3 bucket.
- **Dependencies**:
  - AWS SDK (`boto3`) for interacting with S3.
  - YAML library (`PyYAML`) to parse the `data.yaml` file.

---

## Setup Instructions

### 1. **Create S3 Buckets**
   - Create an input S3 bucket (e.g., `flipkartdataset1`) to store the YOLOv11 annotations and `data.yaml` file.
   - Create an output S3 bucket (e.g., `flipkartprocessedpreview`) to store the dataset analysis JSON file.

### 2. **Prepare `data.yaml`**
   - Create a `data.yaml` file containing the class names as shown above and upload it to the input S3 bucket.

### 3. **Upload Annotations**
   - Upload your YOLOv11 annotation files (in `.txt` format) to the appropriate prefixes (`train/`, `valid/`, `test/`) in your input S3 bucket.

### 4. **Deploy Lambda Function**
   - Deploy the Lambda function to AWS Lambda.
   - Ensure that the Lambda execution role has the necessary permissions to access the input and output S3 buckets.

### 5. **Trigger Lambda**
   - You can trigger the Lambda function based on an event (e.g., an S3 file upload) or manually invoke it.

---

## Example Invocation

The function can be invoked with the following input:

```json
{
  "bucket_name": "flipkartdataset1",
  "output_bucket": "flipkartprocessedpreview"
}
```

After execution, the `dataset_analysis.json` file will be uploaded to the `dataset_analysis` prefix in the specified output S3 bucket.

---

## Sample Output (`dataset_analysis.json`)

```json
{
  "total_classes": 80,
  "class_counts": {
    "class_1": 1200,
    "class_2": 1500,
    "class_3": 1800,
    ...
  }
}
```

---

## Conclusion

This **Dataset Analysis Lambda Function** automates the counting of class occurrences in YOLOv11 annotation files stored in an S3 bucket. It provides valuable insights into the dataset distribution, generating a class count report and storing it in a JSON format for easy access and analysis.