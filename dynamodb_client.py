import boto3
import uuid
from datetime import datetime

table = "certificates"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table)

# record =
#      {
#        "email": "sample@sample.com",
#        "csrContent": "samplesample",
#        "comment": "samplecomment"
#      }

def put(record):
    # 一意のIDを生成
    unique_id = str(uuid.uuid4())
    # 現在時刻をISO 8601形式で取得
    timestamp = datetime.utcnow().isoformat()

    # DynamoDBに保存するデータ
    item = {
        "id": unique_id,               # 一意のID
        "email": record["email"],       # 入力データのemail
        "csrContent": record["csrContent"],  # 入力データのcsrContent
        "comment": record["comment"],   # 入力データのcomment
        "registrationDate": timestamp  # 登録日時
    }

    # データをDynamoDBに保存
    table.put_item(Item=item)

    # 成功レスポンスを返す
    return unique_id
