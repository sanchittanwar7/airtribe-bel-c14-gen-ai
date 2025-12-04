from langchain.tools import tool

# ✅ Name reads like action: search_logs, create_ticket, query_metrics
# ✅ Clear arguments with types
# ✅ Simple return format (text or basic JSON)
# ✅ Focused responsibility (one thing per tool)


@tool
def query_metrics(service: str, metric: str, time_range: str) -> str:
    """Fetch metrics for a service.
    
    Args:
        service: Service identifier
        metric: Metric name (cpu, memory, latency)
        time_range: Time window (1h, 24h, 7d)
    """
    # Simple, structured return
    return f"Service: {service} | Metric: {metric} | Value: 42%"

# Bad tool design: Too vague, mixed responsibilities
@tool
def do_stuff(query: str) -> str:
    """Do system things"""
    # ❌ Model can't understand what to pass
    pass