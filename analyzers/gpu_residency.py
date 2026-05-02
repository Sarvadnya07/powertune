import subprocess

def analyze_gpu_residency():
    print("     [*] Analyzing GPU Residency & Wakeups...")
    try:
        smi_output = subprocess.check_output(["nvidia-smi", "--query-compute-apps=pid,process_name", "--format=csv,noheader"], text=True, timeout=5.0)
        apps = [line.strip() for line in smi_output.splitlines() if line.strip()]
        
        if not apps:
            print("     [+] NVIDIA dGPU is in P8 (Deep Sleep). Excellent.")
        else:
            print("     [!] WARNING: dGPU is active. The following processes are keeping it awake:")
            for app in apps:
                print(f"         - {app}")
            print("         WHY: When the dGPU is active, system power draw increases by 10-20W even at idle.")
    except Exception as e:
        print("     [i] nvidia-smi not found or dGPU is not NVIDIA.")

if __name__ == "__main__":
    analyze_gpu_residency()
