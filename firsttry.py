import xmlrpc.client

# 1. 连接到你刚刚启动的 FreeCAD Server
server = xmlrpc.client.ServerProxy("http://localhost:9875")

try:
    # 2. 尝试创建一个新文档和立方体
    # 注意：这些方法名取决于 freecad-mcp 暴露的 API，通常如下：
    server.new_document("AICreator")
    server.create_box(20.0, 20.0, 20.0, "MyFirstAICube")
    print("成功！去 FreeCAD 窗口看看，是不是多了一个立方体？")
except Exception as e:
    print(f"连接或执行失败: {e}")