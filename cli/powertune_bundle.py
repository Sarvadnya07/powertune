import zipfile
import os
import sys
import datetime

def create_bundle(root_dir="."):
    print("     [*] Generating Portable Diagnostic Bundle...")
    reports_dir = os.path.join(root_dir, "reports")
    if not os.path.exists(reports_dir):
        print("     [!] No reports directory found. Run 'powertune analyze' first.")
        return
        
    date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    bundle_name = f"powertune_report_{date_str}.zip"
    bundle_path = os.path.join(root_dir, bundle_name)
    
    with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(reports_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zf.write(file_path, arcname=os.path.join("reports", file))
                
    print(f"     [+] Bundle created successfully: {bundle_path}")
    print("         WHY: This bundle contains sanitized reports for GitHub issues and community troubleshooting.")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    create_bundle(root)
