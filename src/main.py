from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.services.aws_client import get_ec2_client, manage_instance

app = FastAPI(title="AutoScaleOps API", version="1.0.0")

# Tell FastAPI where our HTML files are
templates = Jinja2Templates(directory="src/templates")

# 1. Route to serve the actual webpage
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    # FIXED: Using the updated Starlette/FastAPI syntax for template rendering
    return templates.TemplateResponse(request=request, name="index.html")

# 2. API Route to fetch all instances and their status
@app.get("/api/instances")
def get_instances():
    ec2 = get_ec2_client()
    if not ec2:
        return {"instances": []}
    
    response = ec2.describe_instances()
    instances = []
    
    for reservation in response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instances.append({
                "id": instance['InstanceId'],
                "type": instance['InstanceType'],
                "state": instance['State']['Name']
            })
            
    return {"instances": instances}

# 3. API Route to handle Start and Stop buttons
@app.get("/api/instances/{instance_id}/{action}")
def control_instance(instance_id: str, action: str):
    # 'action' will be either 'start' or 'stop' from the frontend
    result = manage_instance(instance_id, action.upper())
    return result