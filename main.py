
from datetime import datetime
import email
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
from google_drive_upload import generate_invitation, letterOptions, write_to_sheet

origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST","GET"],
    allow_headers=["*"],
)

format = '%Y-%m-%d'
datei = date.strftime(date.today(), format)

class InvitationData(BaseModel):
    fullname: str
    address: str
    dob: str
    passport_no: str
    letterdate: date = None
    letteropt: dict = None
    desc: str = None
    email: str



@app.get("/")
def read_root():
    return {"success": "Hello World! I'm only responsible for generating letters"}


@app.post("/invitation")
async def create_invitation(invitation_data: InvitationData):
    
    today = datetime.strptime(str(date.today()), format).date()
    
    letterdata = ""

    if invitation_data.letteropt is None:
       letterdata = letterOptions('attendee', invitation_data)
    else:
       letterdata=letterOptions(invitation_data.letteropt['key'], invitation_data)
    
    invite = InvitationData(
        fullname=invitation_data.fullname,
        address=invitation_data.address,
        dob=invitation_data.dob,
        passport_no=invitation_data.passport_no,
        letterdate=today,
        desc=letterdata,
        email=invitation_data.email
    )

    invite_link = generate_invitation(invite)
    
    sw = write_to_sheet(invite.fullname,invite.email, invite_link)

    return {"status": sw}
    

