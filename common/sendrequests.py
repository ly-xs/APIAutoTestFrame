import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from typing import Optional, Dict, Any
import requests


def send_requests(session: requests.Session, api_data: Dict[str, Any]) -> Optional[requests.Response]:
    try:
        # 获取请求参数
        method = api_data.get("method")
        url = api_data.get("url")
        params = api_data.get("params")
        headers = api_data.get("headers")
        body_data = api_data.get("body")
        data_type = api_data.get("type", "data")

        # 解析参数
        if params:
            try:
                params = json.loads(params)
            except json.JSONDecodeError:
                print(f"Error decoding JSON params: {params}")
                return None

        if headers:
            try:
                headers = json.loads(headers)
            except json.JSONDecodeError:
                print(f"Error decoding JSON headers: {headers}")
                return None

        if body_data:
            try:
                body_data = json.loads(body_data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON body_data: {body_data}")
                return None

        # 设置请求体
        if data_type == "data":
            body = body_data
        elif data_type == "json":
            body = json.dumps(body_data)
        else:
            body = body_data

        # 发送请求
        response = session.request(method=method, url=url, headers=headers, params=params, data=body, verify=False)
        return response

    except (ValueError, TypeError, SyntaxError) as e:
        print(f"Error parsing request parameters: {e}")
    except requests.RequestException as e:
        print(f"HTTP request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None
