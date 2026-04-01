import boto3
import os
from dotenv import load_dotenv

# Load credentials from the .env file
load_dotenv()

def get_ec2_client():
    """Initializes and returns the AWS EC2 client."""
    try:
        # Boto3 automatically looks for the environment variables we loaded
        ec2 = boto3.client('ec2')
        return ec2
    except Exception as e:
        print(f"Error connecting to AWS: {e}")
        return None

def test_aws_connection():
    """Tests the connection by fetching all EC2 instance IDs."""
    ec2 = get_ec2_client()
    if not ec2:
        return {"status": "error", "message": "Failed to initialize EC2 client"}

    try:
        # Ask AWS for a description of all instances
        response = ec2.describe_instances()
        instances = []
        
        # Loop through the AWS response to extract instance IDs
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instances.append(instance['InstanceId'])
                
        return {"status": "success", "instances_found": len(instances), "instance_ids": instances}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def manage_instance(instance_id, action):
    """
    Starts or stops an EC2 instance based on the action provided.
    Action must be either 'START' or 'STOP'.
    """
    ec2 = get_ec2_client()
    if not ec2:
        return {"status": "error", "message": "No EC2 client"}

    try:
        if action == "START":
            print(f"Attempting to START instance {instance_id}...")
            ec2.start_instances(InstanceIds=[instance_id])
            return {"status": "success", "message": f"Instance {instance_id} is starting"}
            
        elif action == "STOP":
            print(f"Attempting to STOP instance {instance_id}...")
            ec2.stop_instances(InstanceIds=[instance_id])
            return {"status": "success", "message": f"Instance {instance_id} is stopping"}
            
        else:
            return {"status": "error", "message": "Invalid action. Use START or STOP."}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Quick test block that only runs if you execute this specific file
if __name__ == "__main__":
    # Testing the STOP command on your instance
    my_instance = "i-0a3b89183927ac1d6" 
    
    result = manage_instance(my_instance, "STOP")
    print(result)