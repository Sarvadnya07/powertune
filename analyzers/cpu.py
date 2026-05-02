import subprocess

def check_cpu():
    print("     [*] Analyzing CPU state...")
    try:
        # Check active scheme
        output = subprocess.check_output(["powercfg", "/getactivescheme"], text=True)
        print(f"     [+] Active Scheme: {output.strip()}")
    except Exception as e:
        print(f"     [!] Failed to get CPU scheme: {e}")

if __name__ == "__main__":
    check_cpu()
