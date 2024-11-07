import json
import sys
# 从文件中读取 JSON 数据
with open('topology_input.json', 'r') as file:
    data = json.load(file)


# 构建关系字典
relation_dict = {}
for relation in data["childRelations"]:

    parent_node = f"{relation['parentService']}\n└── {relation['parentEndpoint']}"
    child_node = f"{relation['service']}\n└── {relation['endpoint']}"
    
    if parent_node not in relation_dict:
        relation_dict[parent_node] = []
    
    relation_dict[parent_node].append(child_node)

# 递归打印树状结构
def print_tree(node, depth=0):
    indent = "    " * depth
    service = node.split("\n")[0]
    endpoint = node.split("\n")[1]
    print(f"{indent}{service}\n{indent}{endpoint}")
    if node in relation_dict:
        for child in relation_dict[node]:
            print_tree(child, depth + 1)


if __name__ == "__main__":
    # 找到根节点并打印所有树
    with open('topology.out', 'w') as file:
        sys.stdout = file
        root_nodes = set(relation_dict.keys()) - {child for children in relation_dict.values() for child in children}
        for root in root_nodes:
            print_tree(root)