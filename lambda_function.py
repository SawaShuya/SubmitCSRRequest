import json

import dynamodb_client
import ssm_client
import mailing
import csr_utils

def lambda_handler(item, context):
    try:
        check_item(item)
        id = dynamodb_client.put(item)
        mailing.send(id, item["email"])

        subject = csr_utils.read(item["csrContent"])
        ssm_client.start_automation(id, item["email"], item["comment"], item["csrContent"])

        message = {"message":"submit successfully!"}
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }
    except ValueError as e:
        print(e)
        # エラーレスポンスを返す
        return {
            "statusCode": 400,
            "body": {
                "message": f"Missing Params: {e}",
            }
        }
    except Exception as e:
        # エラーレスポンスを返す
        print(e)
        return {
            "statusCode": 500,
            "body": {
                "message": "Internal error occurred.",
            }
        }

def check_item(item):
    if not("email" in item and "comment" in item and "csrContent" in item):
        raise ValueError("Keys are not correct")
    
    if item["email"] == "" or item["csrContent"] == "":
        raise ValueError("Values are not correct")

    if not(("-----BEGIN") in item["csrContent"] and ("CERTIFICATE REQUEST-----") in item["csrContent"] and ("-----END") in item["csrContent"]):        
        raise ValueError("csrContent value are not correct")
        