from fileless.core import LOLBinExecutor,FilelessDetector
l=LOLBinExecutor()
print("Available LOLBins:")
for b in l.check_available_lolbins(): print(f"  {b}")
d=FilelessDetector()
print(f"\nProcess scan findings: {len(d.scan_processes())}")
