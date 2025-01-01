import json
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from openai import OpenAI

PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)


def handler(event, context):
    print(event)  # Check CloudWatch Logs for this output

    headers = event.get("headers", {})
    signature = headers.get("x-signature-ed25519")
    timestamp = headers.get("x-signature-timestamp")
    body = event.get("body", "")

    if not signature or not timestamp or not body:
        return {
            "statusCode": 401,
            "body": "Invalid request: missing required headers or body",
        }

    try:
        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return {"statusCode": 401, "body": "Invalid request signature"}

    try:
        payload = json.loads(body)

        if payload.get("type") == 1:  # PING type
            return {"statusCode": 200, "body": json.dumps({"type": 1})}

        if payload.get("type") == 2:  # application command type
            user_input = payload["data"]["options"][0]["value"]

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                model="gpt-4o",
                max_tokens=200,
                n=1,
                stop=["[STOP]"],
            )

            # Create a response message
            response_message = {
                "type": 4,  # Type 4 is "CHANNEL_MESSAGE_WITH_SOURCE"
                "data": {
                    "content": f"_prompt:_\n```{user_input}```\n_response:_\n```{chat_completion.choices[0].message.content}```"
                },
            }

            return {"statusCode": 200, "body": json.dumps(response_message)}

    except json.JSONDecodeError:
        return {"statusCode": 400, "body": "Invalid JSON payload"}

    # Handle other types of interactions (if needed)
    return {"statusCode": 400, "body": "Unknown interaction type"}
