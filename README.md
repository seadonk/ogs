# ogs

This project consists of a simple react frontend, and a web scraper for meeting info and meeting minutes pdfs.
It is setup to be output to s3 and served from there.

Getting Started
* for frontend see the README in the frontend directory
* for backend
  * python -m venv venv
  * source venv/bin/activate
  * pip install Scrapy

Running the scraper
* `make run`

Deploying output to S3
* `make deploy`

### S3 Setup
* Install the AWS CLI:aws configure
    * `pip install awscli`
* Configure your AWS credentials:
    * `aws configure`
* Create an S3 bucket:
    * `aws s3 mb s3://your-bucket-name`
* Enable static website hosting for your bucket:
    * `aws s3 website s3://your-bucket-name/ --index-document index.html --error-document error.html`
* Sync your build directory with your S3 bucket:
    * `aws s3 sync build/ s3://your-bucket-name`
* Set the bucket policy to allow public read access:
    * `aws s3api put-bucket-policy --bucket your-bucket-name --policy file://policy.json`