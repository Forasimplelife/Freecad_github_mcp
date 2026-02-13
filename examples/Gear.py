import xmlrpc.client

# 连接到 FreeCAD MCP Server
server = xmlrpc.client.ServerProxy("http://localhost:9875")

try:
    # 生成精美的齿轮模型
    server.execute_code("""
import FreeCAD as App
import Part
import Draft
import math

# 创建新文档
App.newDocument('Gear')
doc = App.activeDocument()

# 齿轮参数
num_teeth = 20  # 齿数
module = 3  # 模数
tooth_height = module * 2.25
inner_radius = module * num_teeth / 2
outer_radius = inner_radius + tooth_height
thickness = 10  # 齿轮厚度

# 创建齿轮轮廓点
points = []
for i in range(num_teeth * 2):
    angle = i * math.pi / num_teeth
    if i % 2 == 0:
        # 齿顶
        radius = outer_radius
    else:
        # 齿根
        radius = inner_radius
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    points.append(App.Vector(x, y, 0))

# 创建齿轮轮廓
import Draft
wire = Draft.make_wire(points, closed=True)

# 拉伸成齿轮
gear = doc.addObject("Part::Extrusion", "Gear")
gear.Base = wire
gear.Dir = App.Vector(0, 0, thickness)
gear.Solid = True

# 创建中心孔
hole = doc.addObject("Part::Cylinder", "CenterHole")
hole.Radius = inner_radius * 0.4
hole.Height = thickness * 1.2
hole.Placement.Base = App.Vector(0, 0, -thickness * 0.1)

# 切割中心孔
cut = doc.addObject("Part::Cut", "GearWithHole")
cut.Base = gear
cut.Tool = hole

# 设置颜色
cut.ViewObject.ShapeColor = (0.8, 0.7, 0.3, 1.0)  # 金色

doc.recompute()

# 调整视图并保存截图
import FreeCADGui as Gui
Gui.activeDocument().activeView().viewIsometric()  # 设置为等轴测视图
Gui.SendMsgToActiveView("ViewFit")  # 自动缩放以适应窗口
import os
script_dir = 'c:/Main_files/Commo_products/Projects_RD/Freecad_github_mcp'
image_dir = os.path.join(script_dir, 'images')
os.makedirs(image_dir, exist_ok=True)
image_path = os.path.join(image_dir, 'Gear.png')
Gui.activeDocument().activeView().saveImage(image_path, 1920, 1080, 'White')
print(f'截图已保存到: {image_path}')
""")
    print("✅ 齿轮模型已生成！去 FreeCAD 窗口查看效果！")
except Exception as e:
    print(f"❌ 连接或执行失败: {e}")
    print("\n请确保：")
    print("1. FreeCAD MCP Server 已启动")
    print("2. Server 监听在 http://localhost:9875")
