import math
import tkinter as tk
from tkinter import messagebox

class RootVisualizer:
    """x^n=a的n个根可视化程序"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("x^n=a的n个根")
        self.root.geometry("1100x800")  # 增加高度以容纳输出区域
        
        # 坐标系参数
        self.origin_x = 400  # 原点x坐标（屏幕坐标）
        self.origin_y = 300  # 原点y坐标（屏幕坐标）
        self.scale = 150     # 缩放比例（每单位多少像素）
        self.x_range = (-6, 6)  # x轴显示范围
        self.y_range = (-5, 5)  # y轴显示范围
        
        self.setup_ui()
        self.draw_coordinate_system()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部控制面板
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(control_frame, text="值 a:", font=("SimHei", 12)).pack(side=tk.LEFT, padx=5)
        
        self.a_entry = tk.Entry(control_frame, width=10, font=("SimHei", 12))
        self.a_entry.pack(side=tk.LEFT, padx=5)
        self.a_entry.insert(0, "1")  # 默认值设为1
        
        tk.Label(control_frame, text="幂次 n:", font=("SimHei", 12)).pack(side=tk.LEFT, padx=5)
        
        self.power_entry = tk.Entry(control_frame, width=10, font=("SimHei", 12))
        self.power_entry.pack(side=tk.LEFT, padx=5)
        self.power_entry.bind("<Return>", lambda event: self.generate_roots())
        self.a_entry.bind("<Return>", lambda event: self.generate_roots())
        
        generate_button = tk.Button(control_frame, text="Start", command=self.generate_roots, font=("SimHei", 12))
        generate_button.pack(side=tk.LEFT, padx=5)
        
        # 创建左右分栏框架
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧画布
        self.canvas = tk.Canvas(content_frame, bg='white', highlightthickness=1, highlightbackground="black")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 右侧文本区域
        right_frame = tk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, ipadx=5, ipady=5)
        
        # 文本区域标签
        output_label = tk.Label(right_frame, text="根的值:", font=("SimHei", 12))
        output_label.pack(fill=tk.X, pady=(0, 5))
        
        # 创建滚动文本框
        output_frame = tk.Frame(right_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = tk.Text(output_frame, height=20, width=30, font=("SimHei", 10), wrap=tk.WORD)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(output_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        self.output_text.config(state=tk.DISABLED)  # 初始设置为只读
        
        # 绑定画布调整事件
        self.canvas.bind("<Configure>", self.on_canvas_resize)
    
    def to_screen_coords(self, math_x, math_y):
        """数学坐标转换为屏幕坐标"""
        screen_x = self.origin_x + math_x * self.scale
        screen_y = self.origin_y - math_y * self.scale  # y轴反向
        return screen_x, screen_y
    
    def draw_coordinate_system(self):
        """绘制坐标系"""
        self.canvas.delete("all")  # 清除画布
        
        # 获取画布尺寸
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 400
        
        # 获取坐标范围，用于刻度绘制
        x_min, x_max = self.x_range
        y_min, y_max = self.y_range
        
        # 绘制坐标轴 - 不设置任何边界，让坐标轴延伸到画布边界
        # x轴：从画布左边界到右边界
        self.canvas.create_line(0, self.origin_y, canvas_width, self.origin_y, 
                               fill="black", width=2)
        
        # y轴：从画布下边界到上边界
        self.canvas.create_line(self.origin_x, canvas_height, self.origin_x, 0, 
                               fill="black", width=2)
        
        # 绘制箭头
        arrow_size = 10
        # x轴箭头（向右）
        self.canvas.create_line(canvas_width-arrow_size, self.origin_y-arrow_size//2, 
                               canvas_width, self.origin_y, 
                               canvas_width-arrow_size, self.origin_y+arrow_size//2,
                               fill="black", width=2)
        # y轴箭头（向上）- 修复箭头方向
        self.canvas.create_line(self.origin_x-arrow_size//2, arrow_size, 
                               self.origin_x, 0, 
                               self.origin_x+arrow_size//2, arrow_size,
                               fill="black", width=2)
        
        # 绘制刻度
        # x轴刻度 - 只显示在可见范围内
        for i in range(int(math.ceil(x_min)), int(math.floor(x_max)) + 1):
            if i == 0:
                continue  # 原点不画刻度
            screen_x, screen_y = self.to_screen_coords(i, 0)
            # 只在画布可见范围内显示刻度
            if 0 <= screen_x <= canvas_width:
                self.canvas.create_line(screen_x, self.origin_y-5, 
                                       screen_x, self.origin_y+5, 
                                       fill="black")
                self.canvas.create_text(screen_x, self.origin_y+15, text=str(i))
        
        # y轴刻度 - 只显示在可见范围内
        for i in range(int(math.ceil(y_min)), int(math.floor(y_max)) + 1):
            if i == 0:
                continue  # 原点不画刻度
            screen_x, screen_y = self.to_screen_coords(0, i)
            # 只在画布可见范围内显示刻度
            if 0 <= screen_y <= canvas_height:
                self.canvas.create_line(self.origin_x-5, screen_y, 
                                       self.origin_x+5, screen_y, 
                                       fill="black")
                self.canvas.create_text(self.origin_x-20, screen_y, text=str(i))
        
        # 绘制原点标记
        self.canvas.create_text(self.origin_x+10, self.origin_y-10, text="O")
    
    def on_canvas_resize(self, event):
        """画布调整大小时重新绘制"""
        # 更新原点位置到画布中心
        self.origin_x = event.width // 2
        self.origin_y = event.height // 2
        self.draw_coordinate_system()
        
        # 如果之前有输入过power，则重新生成根
        power_text = self.power_entry.get().strip()
        if power_text.isdigit():
            self.generate_roots()
    
    def generate_roots(self):
        """生成x^n=a的n个根并绘制"""
        try:
            # 获取输入的a值（默认为1）
            a_str = self.a_entry.get().strip()
            a = float(a_str) if a_str else 1.0
            
            # 获取输入的power值
            power = int(self.power_entry.get())
            if power <= 0:
                messagebox.showerror("错误", "请输入正整数")
                return
            
            # 计算a的power次根
            root_length = math.pow(a, 1/power)
            
            # 根据a的值调整坐标轴范围 - 减小y轴范围
            if a > 1:
                # 扩大坐标轴范围，但y轴范围相对小一些
                max_range = int(root_length) + 1
                self.x_range = (-max_range, max_range)
                # 减小y轴范围，解决y轴太高的问题
                self.y_range = (-(max_range - 1), max_range - 1)
            else:
                # 恢复默认范围，但y轴范围稍小
                self.x_range = (-6, 6)
                self.y_range = (-5, 5)  # y轴范围减小
            
            # 重新绘制坐标系
            self.draw_coordinate_system()
            
            # 清空输出区域
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            
            # 计算并绘制根
            angle_step = 360 / power
            
            for i in range(power):
                # 计算角度（弧度）
                angle_rad = math.radians(i * angle_step)
                
                # 计算端点坐标（长度为root_length的点）
                end_x = root_length * math.cos(angle_rad)
                end_y = root_length * math.sin(angle_rad)
                
                # 转换为屏幕坐标
                start_x, start_y = self.to_screen_coords(0, 0)  # 原点
                end_screen_x, end_screen_y = self.to_screen_coords(end_x, end_y)
                
                # 绘制射线
                self.canvas.create_line(start_x, start_y, end_screen_x, end_screen_y, 
                                      fill="blue", width=2)
                
                # 在端点绘制点
                self.canvas.create_oval(end_screen_x-5, end_screen_y-5, 
                                      end_screen_x+5, end_screen_y+5, 
                                      fill="red")
                
                # 显示根的标签
                label_scale = 1.1 if a <= 1 else 1.05  # 根据范围调整标签位置
                label_x, label_y = self.to_screen_coords(end_x * label_scale, end_y * label_scale)
                self.canvas.create_text(label_x, label_y, text=f"x{i+1}")
                
                # 计算并显示根的表达式在界面上
                c = 2 * i / power
                if  abs(root_length - int(root_length)) < 1e-12:
                    if root_length == 1:
                        length = "" 
                    else:
                        length = int(root_length)
                else:
                    length =format(root_length, '.2f')

                if c not in [0.5, 1, 1.5, 2,0]:
                    root_expr = f"x{i+1}={length}(cos({c}π)+sin({c}π)i)"
                elif c not in [0.5, 1.5]:
                    if root_length == 1:
                        length = 1
                    if c == 1:
                        root_expr = f"x{i+1}={"-"+length}"
                    else:
                        root_expr = f"x{i+1}={length}"
                elif c not in [1, 2,0]:
                    if c == 0.5:
                        root_expr = f"x{i+1}={length}i"
                    else:
                        root_expr = f"x{i+1}={"-"+length}i"
                
                # 添加到输出文本区域
                self.output_text.insert(tk.END, root_expr + "\n")
            
            # 设置文本区域为只读
            self.output_text.config(state=tk.DISABLED)
                    
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数和浮点数")

if __name__ == "__main__":
    root = tk.Tk()
    app = RootVisualizer(root)
    root.mainloop()




