import subprocess

def check_gpu():
    print("     [*] Analyzing GPU state...")
    try:
        output = subprocess.check_output(["powershell", "-Command", "Get-CimInstance Win32_VideoController | Select-Object Name"], text=True)
        gpus = [line.strip() for line in output.splitlines() if line.strip() and "Name" not in line and "----" not in line]
        for gpu in gpus:
            print(f"     [+] Detected GPU: {gpu}")
        
        if any("NVIDIA" in g for g in gpus):
            try:
                smi_output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"], text=True)
                util = int(smi_output.strip())
                if util > 0:
                    print(f"     [!] NVIDIA dGPU is awake (Utilization: {util}%)")
                    print("         WHY: dGPU wakeups drain battery rapidly. Check for background apps using hardware acceleration.")
                else:
                    print("     [+] NVIDIA dGPU is asleep (0% utilization).")
            except:
                print("     [i] nvidia-smi not found or failed.")
    except Exception as e:
        print(f"     [!] Could not check GPUs: {e}")

if __name__ == "__main__":
    check_gpu()
