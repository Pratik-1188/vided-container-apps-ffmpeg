from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, constr
import subprocess
import os

app = FastAPI()

class CommandRequest(BaseModel):
    cmd: constr(min_length=1)  # Ensure the command is a non-empty string
    rootDir: constr(min_length=1)  # Ensure the directory path is a non-empty string

@app.post("/execute/", status_code=status.HTTP_201_CREATED)
async def execute_command(command_request: CommandRequest):
    print(command_request.cmd)
    
    # Validate rootDir is an existing directory
    if not os.path.isdir(command_request.rootDir):
        raise HTTPException(status_code=400, detail="Invalid directory path")

    try:
        # Start the process and capture the output
        process = subprocess.Popen(
            command_request.cmd,  # Use the command as is
            cwd=command_request.rootDir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # Capture standard error as well
            text=True,
            shell=True  # Allow shell interpretation
        )

        stdout, stderr = process.communicate()  # Capture both stdout and stderr

        if process.returncode != 0:  # If the command failed
            # Log the error output
            print(stderr)
            # Raise an HTTP exception with a 400 status code
            raise HTTPException(status_code=400, detail=f"Command failed: {stderr.strip()}")

        # If successful, return the output
        return {"output": stdout.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")
