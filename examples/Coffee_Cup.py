import xmlrpc.client

# 连接到 FreeCAD MCP Server
server = xmlrpc.client.ServerProxy("http://localhost:9875")

try:
    # 生成精美的咖啡杯模型
    server.execute_code("""
import FreeCAD as App
import Part
import Draft
import math

# 创建新文档
App.newDocument('CoffeeCup')
doc = App.activeDocument()

# 咖啡杯参数
height = 100
bottom_radius = 25
top_radius = 35
wall_thickness = 3
handle_width = 8
handle_thickness = 6

# 1. 创建杯体外轮廓
outer_profile_points = [
    App.Vector(0, 0, 0),
    App.Vector(bottom_radius, 0, 0),
    App.Vector(top_radius, 0, height),
    App.Vector(0, 0, height),
    App.Vector(0, 0, 0)
]

import Draft
outer_profile = Draft.make_wire(outer_profile_points, closed=True)

# 旋转创建外杯体
outer_cup = doc.addObject("Part::Revolution", "OuterCup")
outer_cup.Source = outer_profile
outer_cup.Axis = App.Vector(0, 0, 1)
outer_cup.Base = App.Vector(0, 0, 0)
outer_cup.Angle = 360
outer_cup.Solid = True

# 2. 创建内部空腔
inner_profile_points = [
    App.Vector(0, 0, wall_thickness),
    App.Vector(bottom_radius - wall_thickness, 0, wall_thickness),
    App.Vector(top_radius - wall_thickness, 0, height),
    App.Vector(0, 0, height),
    App.Vector(0, 0, wall_thickness)
]

inner_profile = Draft.make_wire(inner_profile_points, closed=True)

# 旋转创建内空腔
inner_cavity = doc.addObject("Part::Revolution", "InnerCavity")
inner_cavity.Source = inner_profile
inner_cavity.Axis = App.Vector(0, 0, 1)
inner_cavity.Base = App.Vector(0, 0, 0)
inner_cavity.Angle = 360
inner_cavity.Solid = True

# 3. 切割出空心杯体
hollow_cup = doc.addObject("Part::Cut", "HollowCup")
hollow_cup.Base = outer_cup
hollow_cup.Tool = inner_cavity

# 4. 创建把手（使用圆环和切割）
handle_outer_radius = 25
handle_inner_radius = handle_outer_radius - handle_width
handle_center_y = top_radius + handle_outer_radius - 5
handle_center_z = height * 0.6

# 创建把手外环
handle_outer_torus = doc.addObject("Part::Torus", "HandleOuter")
handle_outer_torus.Radius1 = handle_outer_radius
handle_outer_torus.Radius2 = handle_thickness / 2
handle_outer_torus.Placement = App.Placement(
    App.Vector(0, handle_center_y, handle_center_z),
    App.Rotation(App.Vector(1, 0, 0), 90)
)

# 创建切割块（只保留把手的一半）
cutter_box = doc.addObject("Part::Box", "HandleCutter")
cutter_box.Length = 80
cutter_box.Width = 80
cutter_box.Height = 60
cutter_box.Placement.Base = App.Vector(-40, 0, handle_center_z - 30)

# 切割把手
handle = doc.addObject("Part::Cut", "Handle")
handle.Base = handle_outer_torus
handle.Tool = cutter_box

# 5. 连接杯体上的两个接触点
# 上接触点
upper_connect = doc.addObject("Part::Sphere", "UpperConnect")
upper_connect.Radius = handle_thickness
upper_connect.Placement.Base = App.Vector(
    0,
    top_radius,
    handle_center_z + handle_outer_radius * 0.7
)

# 下接触点
lower_connect = doc.addObject("Part::Sphere", "LowerConnect")
lower_connect.Radius = handle_thickness
lower_connect.Placement.Base = App.Vector(
    0,
    top_radius,
    handle_center_z - handle_outer_radius * 0.7
)

# 6. 合并所有部件
coffee_cup = doc.addObject("Part::MultiFuse", "CoffeeCup")
coffee_cup.Shapes = [hollow_cup, handle, upper_connect, lower_connect]

# 7. 设置颜色（咖啡色陶瓷）
coffee_cup.ViewObject.ShapeColor = (0.85, 0.65, 0.45, 1.0)

doc.recompute()

# 调整视图并保存截图
import FreeCADGui as Gui
Gui.activeDocument().activeView().viewIsometric()  # 设置为等轴测视图
Gui.SendMsgToActiveView("ViewFit")  # 自动缩放以适应窗口
import os
script_dir = 'c:/Main_files/Commo_products/Projects_RD/Freecad_github_mcp'
image_dir = os.path.join(script_dir, 'images')
os.makedirs(image_dir, exist_ok=True)
image_path = os.path.join(image_dir, 'Coffee_Cup.png')
Gui.activeDocument().activeView().saveImage(image_path, 1920, 1080, 'White')
print(f'截图已保存到: {image_path}')
""")
    print("✅ 咖啡杯模型已生成！去 FreeCAD 窗口查看效果！")
except Exception as e:
    print(f"❌ 连接或执行失败: {e}")
    print("\n请确保：")
    print("1. FreeCAD MCP Server 已启动")
    print("2. Server 监听在 http://localhost:9875")
