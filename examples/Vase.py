import xmlrpc.client

# 连接到 FreeCAD MCP Server
server = xmlrpc.client.ServerProxy("http://localhost:9875")

try:
    # 生成精美的花瓶模型
    server.execute_code("""
import FreeCAD as App
import Part
import Draft
import math

# 创建新文档
App.newDocument('Vase')
doc = App.activeDocument()

# 花瓶参数
height = 150
base_radius = 30
neck_radius = 15
belly_radius = 40

# 创建花瓶轮廓点
points = []
segments = 50

for i in range(segments + 1):
    # 计算高度位置（0到1）
    t = i / segments
    z = t * height
    
    # 使用正弦函数创建优雅的曲线
    if t < 0.2:
        # 底部
        radius = base_radius
    elif t < 0.5:
        # 向外扩张的腹部
        phase = (t - 0.2) / 0.3
        radius = base_radius + (belly_radius - base_radius) * math.sin(phase * math.pi / 2)
    elif t < 0.8:
        # 收缩的颈部
        phase = (t - 0.5) / 0.3
        radius = belly_radius - (belly_radius - neck_radius) * phase
    else:
        # 顶部展开
        phase = (t - 0.8) / 0.2
        radius = neck_radius + (base_radius * 0.8 - neck_radius) * phase
    
    points.append(App.Vector(radius, 0, z))

# 添加中心轴点（闭合轮廓）
points.append(App.Vector(0, 0, height))
points.append(App.Vector(0, 0, 0))

# 创建轮廓线
import Draft
profile = Draft.make_wire(points, closed=True)

# 旋转成花瓶
vase = doc.addObject("Part::Revolution", "Vase")
vase.Source = profile
vase.Axis = App.Vector(0, 0, 1)
vase.Base = App.Vector(0, 0, 0)
vase.Angle = 360
vase.Solid = True

# 创建内部空腔
inner_points = []
wall_thickness = 3

for i in range(segments + 1):
    t = i / segments
    z = t * height + wall_thickness
    
    if t < 0.2:
        radius = base_radius - wall_thickness
    elif t < 0.5:
        phase = (t - 0.2) / 0.3
        radius = (base_radius - wall_thickness) + ((belly_radius - wall_thickness) - (base_radius - wall_thickness)) * math.sin(phase * math.pi / 2)
    elif t < 0.8:
        phase = (t - 0.5) / 0.3
        radius = (belly_radius - wall_thickness) - ((belly_radius - wall_thickness) - (neck_radius - wall_thickness)) * phase
    else:
        phase = (t - 0.8) / 0.2
        radius = (neck_radius - wall_thickness) + ((base_radius * 0.8 - wall_thickness) - (neck_radius - wall_thickness)) * phase
    
    if radius > 0:
        inner_points.append(App.Vector(radius, 0, z))

inner_points.append(App.Vector(0, 0, height))
inner_points.append(App.Vector(0, 0, wall_thickness))

inner_profile = Draft.make_wire(inner_points, closed=True)

inner_cavity = doc.addObject("Part::Revolution", "InnerCavity")
inner_cavity.Source = inner_profile
inner_cavity.Axis = App.Vector(0, 0, 1)
inner_cavity.Base = App.Vector(0, 0, 0)
inner_cavity.Angle = 360
inner_cavity.Solid = True

# 切割内部空腔
hollow_vase = doc.addObject("Part::Cut", "HollowVase")
hollow_vase.Base = vase
hollow_vase.Tool = inner_cavity

# 设置颜色（陶瓷白）
hollow_vase.ViewObject.ShapeColor = (0.95, 0.95, 0.98, 1.0)

doc.recompute()

# 调整视图并保存截图
import FreeCADGui as Gui
Gui.activeDocument().activeView().viewIsometric()  # 设置为等轴测视图
Gui.SendMsgToActiveView("ViewFit")  # 自动缩放以适应窗口
import os
script_dir = 'c:/Main_files/Commo_products/Projects_RD/Freecad_github_mcp'
image_dir = os.path.join(script_dir, 'images')
os.makedirs(image_dir, exist_ok=True)
image_path = os.path.join(image_dir, 'Vase.png')
Gui.activeDocument().activeView().saveImage(image_path, 1920, 1080, 'White')
print(f'截图已保存到: {image_path}')
""")
    print("✅ 花瓶模型已生成！去 FreeCAD 窗口查看效果！")
except Exception as e:
    print(f"❌ 连接或执行失败: {e}")
    print("\n请确保：")
    print("1. FreeCAD MCP Server 已启动")
    print("2. Server 监听在 http://localhost:9875")
