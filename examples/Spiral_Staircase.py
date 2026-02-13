import xmlrpc.client

# 连接到 FreeCAD MCP Server
server = xmlrpc.client.ServerProxy("http://localhost:9875")

try:
    # 生成精美的螺旋楼梯模型
    server.execute_code("""
import FreeCAD as App
import Part
import Draft
import math

# 创建新文档
App.newDocument('SpiralStaircase')
doc = App.activeDocument()

# 螺旋楼梯参数
num_steps = 16  # 台阶数量
radius = 80  # 半径
step_width = 15  # 台阶宽度
step_length = 60  # 台阶长度
step_thickness = 5  # 台阶厚度
height_per_step = 20  # 每个台阶的高度差
center_pole_radius = 10  # 中心柱半径

# 创建中心支撑柱
pole = doc.addObject("Part::Cylinder", "CenterPole")
pole.Radius = center_pole_radius
pole.Height = num_steps * height_per_step
pole.ViewObject.ShapeColor = (0.3, 0.3, 0.3, 1.0)  # 深灰色

# 创建螺旋台阶
for i in range(num_steps):
    # 计算每个台阶的角度和高度
    angle = i * (360 / num_steps) * math.pi / 180
    height = i * height_per_step
    
    # 创建台阶（长方体）
    step = doc.addObject("Part::Box", f"Step_{i:02d}")
    step.Length = step_length
    step.Width = step_width
    step.Height = step_thickness
    
    # 计算台阶位置
    x = (radius - step_length / 2) * math.cos(angle)
    y = (radius - step_length / 2) * math.sin(angle)
    
    # 设置台阶位置和旋转
    step.Placement = App.Placement(
        App.Vector(x, y, height),
        App.Rotation(App.Vector(0, 0, 1), angle * 180 / math.pi)
    )
    
    # 设置台阶颜色（木纹色，逐渐变化）
    color_variation = i / num_steps * 0.2
    step.ViewObject.ShapeColor = (0.6 + color_variation, 0.4 + color_variation, 0.2, 1.0)

# 创建外围扶手（螺旋曲线）
handrail_points = []
handrail_height = step_thickness + 90  # 扶手高度
handrail_segments = num_steps * 10

for i in range(handrail_segments + 1):
    angle = i * (360 / num_steps) * math.pi / 180 * (num_steps / handrail_segments)
    height = i * height_per_step * (num_steps / handrail_segments) + handrail_height
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    handrail_points.append(App.Vector(x, y, height))

# 创建扶手曲线
import Draft
handrail_wire = Draft.make_wire(handrail_points)

# 创建扶手横截面（圆形）
handrail_profile = doc.addObject("Part::Circle", "HandrailProfile")
handrail_profile.Radius = 3

# 将扶手横截面移到起始位置
handrail_profile.Placement.Base = handrail_points[0]

# 沿曲线扫掠创建扶手
handrail = doc.addObject("Part::Sweep", "Handrail")
handrail.Sections = [handrail_profile]
handrail.Spine = handrail_wire
handrail.Solid = True
handrail.ViewObject.ShapeColor = (0.2, 0.2, 0.2, 1.0)  # 深色扶手

doc.recompute()

# 调整视图并保存截图
import FreeCADGui as Gui
Gui.activeDocument().activeView().viewIsometric()  # 设置为等轴测视图
Gui.SendMsgToActiveView("ViewFit")  # 自动缩放以适应窗口
import os
script_dir = 'c:/Main_files/Commo_products/Projects_RD/Freecad_github_mcp'
image_dir = os.path.join(script_dir, 'images')
os.makedirs(image_dir, exist_ok=True)
image_path = os.path.join(image_dir, 'Spiral_Staircase.png')
Gui.activeDocument().activeView().saveImage(image_path, 1920, 1080, 'White')
print(f'截图已保存到: {image_path}')
""")
    print("✅ 螺旋楼梯模型已生成！去 FreeCAD 窗口查看效果！")
except Exception as e:
    print(f"❌ 连接或执行失败: {e}")
    print("\n请确保：")
    print("1. FreeCAD MCP Server 已启动")
    print("2. Server 监听在 http://localhost:9875")
