from dotenv import load_dotenv
import logging
import boto3
import os
import time
import subprocess

# Load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('AWS_REGION', 'ap-northeast-2')

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)


def get_instance_id(file_path):
    retries = 5
    while retries > 0:
        try:
            with open(file_path, 'r') as file:
                instance_id = file.read().strip()
                return instance_id
        except Exception as e:
            logger.error(f"Error fetching instance ID from file: {e}")
            retries -= 1
            time.sleep(2)
    return None


def get_availability_zone():
    retries = 5
    while retries > 0:
        try:
            result = subprocess.run(['ec2metadata', '--availability-zone'], stdout=subprocess.PIPE, text=True)
            if result.returncode == 0:
                availability_zone = result.stdout.strip()
                return availability_zone
            else:
                logger.error(f"Failed to fetch availability zone, return code: {result.returncode}")
        except Exception as e:
            logger.error(f"Error fetching availability zone: {e}")
            retries -= 1
            time.sleep(2)
    return None


def get_region_name(availability_zone):
    return availability_zone[:-1] if availability_zone else None


def terminate_instance():
    # Terminate the EC2 instance if running on AWS\
    INSTANCE_ID_FILE = "/var/lib/cloud/data/instance-id"
    instance_id = get_instance_id(INSTANCE_ID_FILE)
    availability_zone = get_availability_zone()
    region_name = get_region_name(availability_zone)

    if instance_id and region_name:
        try:
            ec2 = boto3.client('ec2', region_name=region_name)
            ec2.terminate_instances(InstanceIds=[instance_id])
            logger.info(f"Terminating instance {instance_id} in region {region_name}")
        except Exception as e:
            logger.error(f"Failed to terminate instance: {e}")
    else:
        if not instance_id:
            logger.error("Failed to retrieve instance ID after multiple attempts.")
        if not region_name:
            logger.error("Failed to retrieve region name after multiple attempts.")


# Run the main function
if __name__ == "__main__":
    terminate_instance()
