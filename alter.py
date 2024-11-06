import json

stats = {}

# 遍历事件数组
def summary_event(json_data):
  for event in json_data:
    service_name = event["serviceName"]
    anormal_status = event["anormalStatus"]
    anormal_type = event["anormalType"]
    time = event["timestamp"]
    
    # 初始化服务名字典
    if service_name not in stats:
        stats[service_name] = {}
    
    if anormal_type not in stats[service_name]:
        stats[service_name][anormal_type] = {
            "add": 0,
            "duplicate": 0,
            "resolve": 0,
            "keep": 0,
            "lastTime": time,
            "fristTime": time
        }

    if time < stats[service_name][anormal_type]["fristTime"]:
        stats[service_name][anormal_type]["fristTime"] = time
    
    if time > stats[service_name][anormal_type]["lastTime"]:
        stats[service_name][anormal_type]["lastTime"] = time

    match anormal_status:
        case "startFiring":
            stats[service_name][anormal_type]["add"] += 1
        case "resolved":
            stats[service_name][anormal_type]["resolve"] += 1
        case "updatedFiring":
            stats[service_name][anormal_type]["duplicate"] += 1


def summary_keep_event(json_data):
    for event in json_data:
        service_name = event["serviceName"]
        anormal_type = event["anormalType"]
        stats[service_name][anormal_type]["keep"] += 1


if __name__ == '__main__':
  with open('alter_input.json', 'r') as file:
    data = json.load(file)
  
  json_data = data["deltaAnormalEvents"]
  summary_event(json_data)
  json_data = data["finalAnormalEvents"]
  summary_keep_event(json_data)
  text = json.dumps(stats, indent=4)
  print(text)
  with open("alter_output.json", "w") as file:
        file.write(text)