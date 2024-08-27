from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
import subprocess
import os

app = FastAPI()

class CommandRequest(BaseModel):
    cmd: constr(min_length=1)  # Ensure the command is a non-empty string
    rootDir: constr(min_length=1)  # Ensure the directory path is a non-empty string

@app.post("/execute/")
async def execute_command(command_request: CommandRequest):
    # Validate rootDir is an existing directory
    if not os.path.isdir(command_request.rootDir):
        raise HTTPException(status_code=400, detail="Invalid directory path")

    try:
        # Use list format for the command to avoid shell injection vulnerabilities
        result = subprocess.run(
            command_request.cmd.split(),  # Split command into list to avoid shell=True
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=command_request.rootDir,
            text=True  # Automatically decode stdout and stderr
        )
        return {"status": "success", "output": result.stdout}
    
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": e.stderr}