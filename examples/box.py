import xmlrpc.client

# 连接到 FreeCAD MCP Server
server = xmlrpc.client.ServerProxy("http://localhost:9875")

try:
    # 生成一个带不同厚度侧壁和后侧两个凸台（用于盖子的铰链/连接）的 box
    server.execute_code("""
import FreeCAD as App
import Part
import FreeCADGui as Gui
import os

# 新文档
App.newDocument('Box')
doc = App.activeDocument()

# 盒子参数（单位：mm）
length = 50.0
width = 50.0
height = 40.0

# 墙厚（左右、前面、后面、底）
th_left = 5.0
th_right = 5.0
th_front = 5.0
th_back = 10.0
th_bottom = 5.0

# 1) 创建外包络盒
outer = Part.makeBox(length, width, height)

# 2) 创建内腔（保留开口在顶部），内腔位置根据各侧厚度偏移
inner_x = length - th_left - th_right
inner_y = width - th_back - th_front
inner_z = height - th_bottom
inner = Part.makeBox(inner_x, inner_y, inner_z, App.Vector(th_left, th_back, th_bottom))

# 3) 切出空心盒子
hollow = outer.cut(inner)

# 4) 在后侧顶部添加凸台，旋转90度让孔朝向外侧
# 凸台设计：长宽高都是10mm，与box顶部结合
# 下部5mm是长方形，上部5mm是半径5mm的半圆柱
# 沿X方向有两个圆柱挖空：外侧5mm段挖半径2.5mm孔，内侧5mm段挖半径1.25mm孔
post_w = 10.0    # Y 方向深度
post_x = 10.0    # X 方向延伸长度
post_h = 10.0    # 总高度

# 左边凸台位置（在box左后角）
post1_y = 0.0
# 右边凸台位置（在box右后角，同样在后壁）
post2_y = 0.0

def make_u_post_hinge_left(y_pos):
    # 左侧凸台：在box左后角，大孔朝左外侧
    # 1) 底部：10x10x5 的实心方块基座（从x=0到10）
    base = Part.makeBox(post_x, post_w, 5.0, App.Vector(0.0, y_pos, height))

    # 2) 顶部：半径5mm的半圆柱，沿X方向延伸10mm
    # 圆柱中心在 Y 方向的中点 (y_pos + 5), Z 在 height+5
    full_cylinder = Part.makeCylinder(5.0, post_x, 
                                       App.Vector(0.0, y_pos + 5.0, height + 5.0), 
                                       App.Vector(1, 0, 0))
    
    # 切掉下半部分，只保留上半圆柱（Z > height+5）
    cut_box = Part.makeBox(post_x, 20.0, 5.0, App.Vector(0.0, y_pos - 5.0, height))
    semi_cylinder = full_cylinder.cut(cut_box)
    
    # 合并底座和半圆柱
    solid = base.fuse(semi_cylinder)

    # 3) 沿X方向挖两个圆柱孔以形成铰链结构
    # 外侧孔（X=0到5mm，朝左外侧）：半径2.5mm
    hole_outer = Part.makeCylinder(2.5, 5.0, 
                                   App.Vector(0.0, y_pos + 5.0, height + 5.0), 
                                   App.Vector(1, 0, 0))
    
    # 内侧孔（X=5到10mm，朝右内侧）：半径1.25mm
    hole_inner = Part.makeCylinder(1.25, 5.0, 
                                   App.Vector(5.0, y_pos + 5.0, height + 5.0), 
                                   App.Vector(1, 0, 0))
    
    # 切除两个孔
    result = solid.cut(hole_outer).cut(hole_inner)
    
    return result

def make_u_post_hinge_right(y_pos):
    # 右侧凸台：在box右后角，大孔朝右外侧
    # 1) 底部：10x10x5 的实心方块基座（从x=40到50）
    base = Part.makeBox(post_x, post_w, 5.0, App.Vector(length - post_x, y_pos, height))

    # 2) 顶部：半径5mm的半圆柱，沿X方向延伸10mm
    full_cylinder = Part.makeCylinder(5.0, post_x, 
                                       App.Vector(length - post_x, y_pos + 5.0, height + 5.0), 
                                       App.Vector(1, 0, 0))
    
    # 切掉下半部分
    cut_box = Part.makeBox(post_x, 20.0, 5.0, App.Vector(length - post_x, y_pos - 5.0, height))
    semi_cylinder = full_cylinder.cut(cut_box)
    
    # 合并底座和半圆柱
    solid = base.fuse(semi_cylinder)

    # 3) 沿X方向挖孔
    # 内侧孔（X=40到45mm，朝左内侧）：半径1.25mm
    hole_inner = Part.makeCylinder(1.25, 5.0, 
                                   App.Vector(length - post_x, y_pos + 5.0, height + 5.0), 
                                   App.Vector(1, 0, 0))
    
    # 外侧孔（X=45到50mm，朝右外侧）：半径2.5mm
    hole_outer = Part.makeCylinder(2.5, 5.0, 
                                   App.Vector(length - post_x + 5.0, y_pos + 5.0, height + 5.0), 
                                   App.Vector(1, 0, 0))
    
    # 切除两个孔
    result = solid.cut(hole_inner).cut(hole_outer)
    
    return result

post1 = make_u_post_hinge_left(post1_y)
post2 = make_u_post_hinge_right(post2_y)

# 5) 合并所有部件
result = hollow.fuse(post1.fuse(post2))

# 6) 将结果放入文档并设置颜色
obj = doc.addObject('Part::Feature', 'Box')
obj.Shape = result
obj.ViewObject.ShapeColor = (0.9, 0.5, 0.6)

doc.recompute()

# 7) 保存截图（可选）
script_dir = r'c:/Main_files/Commo_products/Projects_RD/Freecad_github_mcp'
image_dir = os.path.join(script_dir, 'images')
os.makedirs(image_dir, exist_ok=True)
image_path = os.path.join(image_dir, 'Box.png')

Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView('ViewFit')
Gui.activeDocument().activeView().saveImage(image_path, 1200, 900, 'White')
print('截图已保存到:', image_path)
""")
    print("✅ box 模型已发送到 FreeCAD MCP Server！请在 FreeCAD 中查看 'Box' 文档。")
    print("提示：若需调整凸台位置/尺寸，可修改 post_* 参数并重试。")
except Exception as e:
    print(f"❌ 连接或执行失败: {e}")
    print("\n请确保：")
    print("1. FreeCAD MCP Server 已启动")
    print("2. Server 监听在 http://localhost:9875")
