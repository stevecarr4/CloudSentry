# CloudSentry
AWS Management Made Simple



Overview

CloudSentry is a revolutionary tool that redefines the way you manage AWS resources. With its unparalleled capabilities, CloudSentry simplifies and streamlines the management of EC2 instances and S3 buckets, empowering users to effortlessly create, manage, and terminate resources.

Features

Unleash the power of CloudSentry with its extensive set of features:
Seamlessly list, create, and terminate EC2 instances with ease.
Effortlessly manage S3 buckets - list, create, and delete them effortlessly.
Embrace the simplicity of the interactive command-line interface for a delightful user experience.
Ensure the robustness of your operations with automated unit testing.
Installation

Prerequisites
Python 3.x
An AWS account with necessary permissions.
Follow these steps to install and run CloudSentry:

Clone the repository:
Clone the CloudSentry GitHub repository to your local machine using the following command:
bash
Copy code
git clone https://github.com/stevecarr4/CloudSentry
Set up Python environment:
We recommend using a Python virtual environment for running this application. Create and activate a new virtual environment with:
bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install dependencies:
Navigate to the cloned repository directory and install the required dependencies with the following command:
bash
Copy code
pip install -r requirements.txt
Configure AWS credentials:
Configure your AWS CLI with your AWS credentials. Follow the instructions provided here.
Usage

Execute the script from the command line:

bash
Copy code
python cloud_sentry_script.py
This command will launch an interactive menu. Follow the prompts to manage your AWS resources.

Testing

To run the test suite, execute the following command:

bash
Copy code
python -m unittest discover tests
Deployment

Add additional notes about how to deploy this on a live system.

Contributing

Contributions to CloudSentry are always welcome. See CONTRIBUTING.md for more details.

License

CloudSentry is licensed under the terms of the MIT license. See LICENSE for more details.

Contact

For any questions or comments, please open an issue on our GitHub repository.

Acknowledgements

CloudSentry is built with the following open source technologies:

Python
boto3
moto
tabulate
We thank these communities for their contributions to open source.
