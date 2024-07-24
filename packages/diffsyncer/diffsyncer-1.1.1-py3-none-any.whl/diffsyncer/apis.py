import os
import shutil
from typing import Annotated, Any, List
from fastapi import APIRouter, Body, Depends, Form, UploadFile
from pydantic import BaseModel

from diffsyncer import config, decoder, syncer, auth


class LoginModel(BaseModel):
    username: str
    password: str


# unified response model
class ResponseModel(BaseModel):
    code: int = 0
    data: Any = None
    message: str = None
    error: Any = None


apis = APIRouter()


@apis.post("/login")
def login(data: Annotated[LoginModel, Body()]):
    user = auth.verify_user(data.username, data.password)

    if not user:
        return ResponseModel(code=1, message="Unauthorized")

    access_token = auth.create_access_token(data={"sub": user.username})

    return ResponseModel(code=0, data=access_token, message="Login success")


@apis.get("/user")
async def user_info(current_user: Annotated[auth.User, Depends(auth.get_current_user)]):
    return ResponseModel(code=0, data=current_user)


# upload multiple files api
@apis.post("/upload")
def upload_files(
    files: Annotated[List[UploadFile], Form()],
    repo_url: Annotated[str, Form()],
    branch: Annotated[str, Form()] = "main",
):

    upload_dir = config.UPLOAD_DIR

    # clear upload directory
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)

    # check if upload directory exists
    os.makedirs(upload_dir)

    # store files to upload directory
    file_length = len(files)
    for file in files:
        with open(f"{upload_dir}/{file.filename}", "wb") as f:
            f.write(file.file.read())

    # decode qr codes
    print(f"Decoding QR codes from: {file_length} files")
    decode_dir = decoder.execute(upload_dir)

    # git commit
    print("Git sync")
    syncer.sync(repo_url, decode_dir, branch)

    print("Decoding QR codes success")

    return ResponseModel(
        code=0, data={"decode_dir": decode_dir}, message="Decoding QR codes done"
    )


@apis.post("/sync")
def sync_by_scan(
    data: Annotated[List[str], Body()],
    repo_url: Annotated[str, Body()],
    branch: Annotated[str, Body()] = "main",
):
    # sync data by scanning qr codes
    print(f"Syncing data by scanning QR codes: {len(data)}")
    decode_dir = decoder.decode_by_scan(data)

    # git commit
    print("Git sync")
    syncer.sync(repo_url, decode_dir, branch)

    return ResponseModel(
        code=0, data={"decode_dir": decode_dir}, message="Syncing data done"
    )


# This is for testing
@apis.get("/decode")
def decode_qr_codes():
    output_dir = config.OUTPUT_DIR

    # decode qr codes
    print("Decoding QR codes")
    decode_dir = decoder.execute(output_dir)

    print("Decoding QR codes done")

    return {"decode_dir": decode_dir}
