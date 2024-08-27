from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CommandRequest(BaseModel):
    cmd: str

@app.post("/execute/")
async def execute_command(command_request: CommandRequest):
    try:
        result = subprocess.run(
            command_request.cmd, 
            shell=True, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            cwd="/mnt"
        )
        return {"status": "success", "output": result.stdout.decode('utf-8')}
    
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": e.stderr.decode('utf-8')}