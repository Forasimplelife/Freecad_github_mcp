import xmlrpc.client

# 连接到 FreeCAD MCP Server
server = xmlrpc.client.ServerProxy("http://localhost:9875")

try:
    # 生成精美的弹簧模型
    server.execute_code("""
import FreeCAD as App
import Part
import Draft
import math

# 创建新文档
App.newDocument('Spring')
doc = App.activeDocument()

# 弹簧参数
coil_radius = 20  # 线圈半径
wire_radius = 3  # 弹簧线直径
num_coils = 10  # 线圈数量
pitch = 15  # 螺距（每圈的高度间隔）
segments_per_coil = 50  # 每圈的分段数

# 创建螺旋线路径点
helix_points = []
total_segments = num_coils * segments_per_coil

for i in range(total_segments + 1):
    # 计算角度和高度
    t = i / segments_per_coil  # 圈数
    angle = t * 2 * math.pi
    height = t * pitch
    
    # 计算螺旋线上的点
    x = coil_radius * math.cos(angle)
    y = coil_radius * math.sin(angle)
    z = height
    
    helix_points.append(App.Vector(x, y, z))

# 创建螺旋线
import Draft
helix_wire = Draft.make_wire(helix_points)

# 创建弹簧线的横截面（圆形）
wire_profile = doc.addObject("Part::Circle", "WireProfile")
wire_profile.Radius = wire_radius

# 将横截面移到螺旋线起点
wire_profile.Placement.Base = helix_points[0]

# 沿螺旋线扫掠创建弹簧
spring = doc.addObject("Part::Sweep", "Spring")
spring.Sections = [wire_profile]
spring.Spine = helix_wire
spring.Solid = True

# 设置弹簧颜色（金属银色）
spring.ViewObject.ShapeColor = (0.75, 0.75, 0.8, 1.0)

# 创建底部支撑平面（可选）
bottom_plate = doc.addObject("Part::Cylinder", "BottomPlate")
bottom_plate.Radius = coil_radius * 1.3
bottom_plate.Height = 2
bottom_plate.Placement.Base = App.Vector(0, 0, -5)
bottom_plate.ViewObject.ShapeColor = (0.3, 0.3, 0.3, 1.0)

# 创建顶部支撑平面（可选）
top_plate = doc.addObject("Part::Cylinder", "TopPlate")
top_plate.Radius = coil_radius * 1.3
top_plate.Height = 2
top_plate.Placement.Base = App.Vector(0, 0, num_coils * pitch + 3)
top_plate.ViewObject.ShapeColor = (0.3, 0.3, 0.3, 1.0)

doc.recompute()

# 调整视图并保存截图
import FreeCADGui as Gui
Gui.activeDocument().activeView().viewIsometric()  # 设置为等轴测视图
Gui.SendMsgToActiveView("ViewFit")  # 自动缩放以适应窗口
import os
script_dir = 'c:/Main_files/Commo_products/Projects_RD/Freecad_github_mcp'
image_dir = os.path.join(script_dir, 'images')
os.makedirs(image_dir, exist_ok=True)
image_path = os.path.join(image_dir, 'Spring.png')
Gui.activeDocument().activeView().saveImage(image_path, 1920, 1080, 'White')
print(f'截图已保存到: {image_path}')
""")
    print("✅ 弹簧模型已生成！去 FreeCAD 窗口查看效果！")
except Exception as e:
    print(f"❌ 连接或执行失败: {e}")
    print("\n请确保：")
    print("1. FreeCAD MCP Server 已启动")
    print("2. Server 监听在 http://localhost:9875")
