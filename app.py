import os
import base64
import json
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# auth
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
else:
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())

service = build("gmail", "v1", credentials=creds)

# config
with open("config.json") as f:
    config = json.load(f)

allowed = config["allowed_senders"]

query = "is:unread has:attachment filename:xlsx newer_than:1d"
results = service.users().messages().list(userId="me", q=query).execute()

messages = results.get("messages", [])

for msg in messages:
    full = service.users().messages().get(userId="me", id=msg["id"]).execute()

    headers = full["payload"]["headers"]
    sender = next(h["value"] for h in headers if h["name"] == "From")

    sender_email = sender.split("<")[-1].replace(">", "").strip()

    if sender_email not in allowed:
        continue

    parts = full["payload"].get("parts", [])

    for part in parts:
        filename = part.get("filename")

        if filename.endswith(".xlsx"):
            att_id = part["body"]["attachmentId"]

            att = service.users().messages().attachments().get(
                userId="me",
                messageId=msg["id"],
                id=att_id
            ).execute()

            data = base64.urlsafe_b64decode(att["data"])

            raw_path = f"data/raw/{filename}"

            with open(raw_path, "wb") as f:
                f.write(data)

            # normalizar
            df = pd.read_excel(raw_path)

            df.columns = (
                df.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_", regex=False)
            )

            rename = {
                "id_usuario": "ID",
                "genero": "Gender",
                "edad": "AGE",
                "salario_estimado": "EstimatedSalary",
                "comprado": "Purchased"
            }

            df.rename(columns=rename, inplace=True)

            df["Origen"] = allowed[sender_email]

            output = "data/processed/output.xlsx"
            df.to_excel(output, index=False)

print("Proceso terminado")