def get_telemetry():
    """
    Example Vendor Plugin: ASUS ROG/Armoury Crate Intelligence.
    Detects ASUS-specific power hogs.
    """
    telemetry = []
    # In a real ASUS plugin, we would check for 'AsusOptimization.exe' or specific lighting ACPI nodes.
    telemetry.append({
        "category": "vendor_asus",
        "severity": "info",
        "source": "ROG_Optimizer",
        "message": "ASUS-specific power intelligence module active. Monitoring Armoury Crate impact."
    })
    return telemetry
