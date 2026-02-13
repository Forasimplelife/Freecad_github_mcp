import xmlrpc.client

# 连接到 FreeCAD MCP Server
server = xmlrpc.client.ServerProxy("http://localhost:9875")

try:
    # 生成精美的钻石模型
    server.execute_code("""
import FreeCAD as App
import Part
import Draft
import math

# 创建新文档
App.newDocument('Diamond')
doc = App.activeDocument()

# 钻石参数
pavilion_height = 30  # 亭部高度（下部）
crown_height = 20  # 冠部高度（上部）
girdle_radius = 40  # 腰围半径
table_radius = 25  # 台面半径
num_facets = 8  # 刻面数（8的倍数效果最好）

# 1. 创建亭部（下部锥体）
pavilion_points = []
# 底部尖点
pavilion_points.append(App.Vector(0, 0, -pavilion_height))
# 腰围圆周
for i in range(num_facets):
    angle = i * 2 * math.pi / num_facets
    x = girdle_radius * math.cos(angle)
    y = girdle_radius * math.sin(angle)
    pavilion_points.append(App.Vector(x, y, 0))
# 闭合到底部尖点
pavilion_points.append(App.Vector(0, 0, -pavilion_height))

# 创建亭部线框
import Draft
pavilion_lines = []
for i in range(num_facets):
    angle = i * 2 * math.pi / num_facets
    x = girdle_radius * math.cos(angle)
    y = girdle_radius * math.sin(angle)
    line = Draft.make_line(App.Vector(0, 0, -pavilion_height), App.Vector(x, y, 0))
    pavilion_lines.append(line)

# 创建腰围圆环
girdle_circle = Draft.make_circle(girdle_radius)
girdle_circle.Placement.Base = App.Vector(0, 0, 0)

# 创建亭部实体（旋转体的组合）
pavilion_profile_points = [
    App.Vector(0, 0, -pavilion_height),
    App.Vector(girdle_radius, 0, 0),
    App.Vector(0, 0, 0)
]
pavilion_profile = Draft.make_wire(pavilion_profile_points, closed=True)

pavilion = doc.addObject("Part::Revolution", "Pavilion")
pavilion.Source = pavilion_profile
pavilion.Axis = App.Vector(0, 0, 1)
pavilion.Base = App.Vector(0, 0, 0)
pavilion.Angle = 360
pavilion.Solid = True

# 2. 创建冠部（上部）
crown_profile_points = [
    App.Vector(0, 0, 0),
    App.Vector(girdle_radius, 0, 0),
    App.Vector(table_radius, 0, crown_height),
    App.Vector(0, 0, crown_height),
    App.Vector(0, 0, 0)
]
crown_profile = Draft.make_wire(crown_profile_points, closed=True)

crown = doc.addObject("Part::Revolution", "Crown")
crown.Source = crown_profile
crown.Axis = App.Vector(0, 0, 1)
crown.Base = App.Vector(0, 0, 0)
crown.Angle = 360
crown.Solid = True

# 3. 合并亭部和冠部
diamond = doc.addObject("Part::MultiFuse", "Diamond")
diamond.Shapes = [pavilion, crown]

# 4. 创建刻面效果（通过多个切割面）
for i in range(num_facets):
    angle1 = i * 2 * math.pi / num_facets
    angle2 = (i + 1) * 2 * math.pi / num_facets
    mid_angle = (angle1 + angle2) / 2
    
    # 在冠部创建刻面
    x1 = girdle_radius * math.cos(angle1)
    y1 = girdle_radius * math.sin(angle1)
    x2 = girdle_radius * math.cos(angle2)
    y2 = girdle_radius * math.sin(angle2)
    xt = table_radius * math.cos(mid_angle)
    yt = table_radius * math.sin(mid_angle)
    
    # 创建三角形刻面
    facet_points = [
        App.Vector(x1, y1, 0),
        App.Vector(x2, y2, 0),
        App.Vector(xt, yt, crown_height),
        App.Vector(x1, y1, 0)
    ]

# 设置钻石材质颜色（透明晶体）
diamond.ViewObject.ShapeColor = (0.9, 0.95, 1.0, 0.5)
diamond.ViewObject.Transparency = 20

doc.recompute()

# 调整视图并保存截图
import FreeCADGui as Gui
Gui.activeDocument().activeView().viewIsometric()  # 设置为等轴测视图
Gui.SendMsgToActiveView("ViewFit")  # 自动缩放以适应窗口
import os
script_dir = 'c:/Main_files/Commo_products/Projects_RD/Freecad_github_mcp'
image_dir = os.path.join(script_dir, 'images')
os.makedirs(image_dir, exist_ok=True)
image_path = os.path.join(image_dir, 'Diamond.png')
Gui.activeDocument().activeView().saveImage(image_path, 1920, 1080, 'White')
print(f'截图已保存到: {image_path}')
""")
    print("✅ 钻石模型已生成！去 FreeCAD 窗口查看效果！")
except Exception as e:
    print(f"❌ 连接或执行失败: {e}")
    print("\n请确保：")
    print("1. FreeCAD MCP Server 已启动")
    print("2. Server 监听在 http://localhost:9875")
