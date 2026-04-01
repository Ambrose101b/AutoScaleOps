import boto3
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load AWS credentials
load_dotenv()

def get_cloudwatch_client():
    """Initializes the AWS CloudWatch client."""
    try:
        return boto3.client('cloudwatch')
    except Exception as e:
        print(f"Error connecting to CloudWatch: {e}")
        return None

def get_cpu_utilization(instance_id):
    """Fetches the average CPU utilization over the last 5 minutes."""
    cw_client = get_cloudwatch_client()
    if not cw_client:
        return None

    # We need to look at a specific time window. Let's check the last 5 minutes.
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=5)

    try:
        # Ask CloudWatch for the CPU metrics
        response = cw_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300, # 300 seconds = 5 minutes
            Statistics=['Average']
        )

        # Extract the actual number from the AWS response
        datapoints = response.get('Datapoints', [])
        if datapoints:
            # Get the most recent data point
            latest_datapoint = sorted(datapoints, key=lambda x: x['Timestamp'])[-1]
            return round(latest_datapoint['Average'], 2)
        else:
            # If the instance just launched, CloudWatch might not have data for a few minutes
            return 0.0 

    except Exception as e:
        print(f"Error fetching metrics for {instance_id}: {e}")
        return None

# Quick test block
if __name__ == "__main__":
    # Your actual instance ID!
    test_instance_id = "i-0a3b89183927ac1d6" 
    print(f"Checking CPU for {test_instance_id}...")
    
    cpu = get_cpu_utilization(test_instance_id)
    print(f"Current CPU Utilization: {cpu}%")