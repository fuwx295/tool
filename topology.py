import json

# 从文件中读取 JSON 数据
with open('topology_input.json', 'r') as file:
    data = json.load(file)

# 构建父子关系字典
relations = {}
for relation in data["childRelations"]:
    parent_service = relation["parentService"]
    child_service = relation["service"]
    parent_endpoint = relation["parentEndpoint"]
    child_endpoint = relation["endpoint"]

    if parent_service not in relations:
        relations[parent_service] = []
    relations[parent_service].append((child_service, child_endpoint))
# 递归构建树形结构字符串
def build_tree(service, endpoint, indent=""):
    tree_str = f"{indent}{service}\n"
    tree_str += f"{indent}└── {endpoint}\n"
    if service in relations:
        for i, (child_service, child_endpoint) in enumerate(relations[service]):
            if i == len(relations[service]) - 1:
                tree_str += build_tree(child_service, child_endpoint, indent + "    ")
            else:
                tree_str += build_tree(child_service, child_endpoint, indent + "    ")
    return tree_str



if __name__ == "__main__":
    # 获取当前服务和端点
    current_service = data["current"]["service"]
    current_endpoint = data["current"]["endpoint"]

    # 构建树形结构字符串
    tree_representation = build_tree(current_service, current_endpoint)

    # 打印树形结构
    print(tree_representation)

    # 保存到文件
    with open("topology_output.json", "w") as file:
        file.write(tree_representation)