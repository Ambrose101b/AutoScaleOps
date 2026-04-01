import asyncio
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.services.aws_client import get_ec2_client, manage_instance
from src.services.monitor import get_cpu_utilization
from src.core.engine import evaluate_scaling_action

app = FastAPI(title="AutoScaleOps API", version="1.0.0")
templates = Jinja2Templates(directory="src/templates")

# Global list to store logs of what the auto-scaler is doing
scaling_logs = []

async def monitor_and_scale():
    """Background task that monitors CPU and takes action automatically."""
    while True:
        instance_id = "i-0a3b89183927ac1d6" # Your specific instance
        cpu = get_cpu_utilization(instance_id)
        
        if cpu is not None:
            decision = evaluate_scaling_action(cpu)
            log_entry = f"CPU: {cpu}% | Decision: {decision}"
            print(f"[AUTO-SCALER] {log_entry}")
            scaling_logs.append(log_entry)

            # Keep only last 10 logs
            if len(scaling_logs) > 10: scaling_logs.pop(0)

            # Execute scaling (For safety in this demo, we only log SCALE_UP)
            if decision == "SCALE_DOWN":
                manage_instance(instance_id, "STOP")
        
        await asyncio.sleep(60) # Wait 1 minute before checking again

@app.on_event("startup")
async def startup_event():
    # Start the monitoring loop when the app starts
    asyncio.create_task(monitor_and_scale())

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/instances")
def get_instances():
    ec2 = get_ec2_client()
    if not ec2: return {"instances": []}
    response = ec2.describe_instances()
    instances = []
    for reservation in response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instances.append({
                "id": instance['InstanceId'],
                "type": instance['InstanceType'],
                "state": instance['State']['Name'],
                "logs": scaling_logs # Pass logs to the frontend
            })
    return {"instances": instances}

@app.get("/api/instances/{instance_id}/{action}")
def control_instance(instance_id: str, action: str):
    return manage_instance(instance_id, action.upper())