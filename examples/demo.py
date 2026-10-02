#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

COMMANDS=[
    ["cyberai","--version"],
    ["cyberai","doctor"],
    ["cyberai","module","list"],
    ["cyberai","module","run","http","examples/request.txt"],
    ["cyberai","module","run","headers","examples/response-headers.txt","--output","demo-output/headers.html","--format","html"],
    ["cyberai","module","run","logs","examples/app.log","--output","demo-output/logs.json","--format","json"],
    ["cyberai","dashboard","--root","workspaces","--output","demo-output/dashboard.html"],
]

def main():
    Path("demo-output").mkdir(exist_ok=True)
    for command in COMMANDS:
        print("\n$", " ".join(command))
        result=subprocess.run(command,check=False)
        if result.returncode:
            print(f"Command exited with status {result.returncode}.",file=sys.stderr)
            return result.returncode
    print("\nDemo complete. See demo-output/.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
