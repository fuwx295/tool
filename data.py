import requests
import json

def get_topology_data(api_url, params, output_file):
    # 发送GET请求
    response = requests.get(api_url, params=params)
    # 检查请求是否成功
    if response.status_code == 200:
        # 获取JSON格式的数据
        data = response.json()
        
        # 将JSON数据写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Data saved to", output_file)
    else:
        print(f"Failed to get data: {response.status_code}")

def get_alert_data(api_url, payload, headers=None, output_file=None):
    # 默认请求头设置为application/json
    default_headers = {'Content-Type': 'application/json'}
    if headers is None:
        headers = default_headers
    else:
        # 如果提供了headers参数，则合并默认的Content-Type设置
        headers.update(default_headers)
    # 将payload转换为JSON字符串
    payload_json = json.dumps(payload)
    # 发送POST请求
    response = requests.post(api_url, data=payload_json, headers=headers)
    
    # 检查请求是否成功
    if response.status_code == 200: 
        print("Request was successful.")
        
        # 如果需要保存返回的数据到文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
            print(f"Response data saved to {output_file}")
    else:
        print(f"Failed to post data: {response.status_code}, {response.text}")

# 拓扑图接口
topology_api_url = "http://192.168.1.20:31406/api/service/relation"
topology_data_file = "topology_input.json"
params = {
    "startTime": 1730269110574000,
    "endTime": 1730269410574000,
    "service": "ts-gateway-service",
    "endpoint": "POST travel",
    "entryService": "ts-gateway-service",
    "entryEndpoint": "POST travel",
    "withTopoloyLevel": "true"
}

alert_api_url = "http://192.168.1.20:31406/api/alerts/descendant/anormal/delta"
alert_data_file = "alert_input.json"
payload = {
  "anormalTypes": "app,container,infra,network,error",
  "deltaEndTime": 1730808208000000,
  "deltaStartTime": 1730807308000000,
  "endTime": 1730808208000000,
  "endpoint": "POST travel",
  "service": "ts-gateway-service",
  "startTime": 1730807308000000,
  "step": 60000000
}

if __name__ == "__main__":
  get_topology_data(topology_api_url, params, topology_data_file)
  get_alert_data(alert_api_url, payload, output_file=alert_data_file)