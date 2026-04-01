def evaluate_scaling_action(cpu_utilization):
    """
    Evaluates CPU usage and returns a scaling decision.
    Thresholds:
    - CPU > 70%: SCALE_UP
    - CPU < 20%: SCALE_DOWN (Mark Idle)
    - Otherwise: DO_NOTHING
    """
    if cpu_utilization is None:
        return "ERROR: No data"

    print(f"[ENGINE] Evaluating CPU: {cpu_utilization}%")

    if cpu_utilization > 70.0:
        return "SCALE_UP"
    elif cpu_utilization < 20.0:
        return "SCALE_DOWN"
    else:
        return "DO_NOTHING"

# Quick test block
if __name__ == "__main__":
    # Let's test our brain with different scenarios
    test_cpus = [15.5, 45.0, 85.2, None]
    
    for cpu in test_cpus:
        decision = evaluate_scaling_action(cpu)
        print(f"CPU: {cpu}% -> Action: {decision}\n")