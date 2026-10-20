# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

doc = Document()

# 全局默认字体
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

def set_cell_font(cell, text, bold=False, size=10, color=None):
    cell.text = ''
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = 'Calibri'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    if color:
        run.font.color.rgb = RGBColor(*color)

def add_table(rows, header, col_widths):
    table = doc.add_table(rows=1, cols=len(header))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for i, h in enumerate(header):
        set_cell_font(hdr[i], h, bold=True, size=10.5, color=(255, 255, 255))
        shd = hdr[i]._element.get_or_add_tcPr().makeelement(qn('w:shd'), {qn('w:fill'): '2E75B6'})
        hdr[i]._element.get_or_add_tcPr().append(shd)
    for r in rows:
        cells = table.add_row().cells
        for i, c in enumerate(r):
            set_cell_font(cells[i], c, bold=False, size=10)
    for i, w in enumerate(col_widths):
        for row in table.rows:
            row.cells[i].width = Inches(w)
    return table

def heading(text, level=1):
    p = doc.add_heading('', level=level)
    run = p.add_run(text)
    run.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)
    run.font.name = 'Calibri'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    return p

# 标题
def set_run(run, size, color, bold=False, ea='微软雅黑'):
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(*color)
    run.bold = bold
    run.font.name = 'Calibri'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), ea)

title = doc.add_heading('', level=0)
tr = title.add_run('Python 常用库使用方法总结')
set_run(tr, 24, (0x1F, 0x4E, 0x79), bold=True)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sr = sub.add_run('涵盖：pyautogui · cnocr · docx · requests · selenium · os · random · shutil · cv2')
set_run(sr, 11, (0x55, 0x55, 0x55))

HEADER = ['函数 / 类', '功能说明', '示例代码', '备注']
WIDTHS = [1.4, 1.8, 3.4, 1.6]

# ---------- 1. pyautogui ----------
heading('1. pyautogui —— 鼠标键盘自动化')
add_table([
    ['import pyautogui', '导入模块，实现 GUI 自动化', 'import pyautogui', '需安装：pip install pyautogui'],
    ['size()', '获取屏幕分辨率', 'w, h = pyautogui.size()', '返回 (宽, 高) 元组'],
    ['moveTo(x, y, t)', '移动鼠标到指定坐标，t 为耗时', 'pyautogui.moveTo(100, 200, 0.5)', '坐标原点在左上角'],
    ['click(x, y)', '在指定位置单击', 'pyautogui.click(500, 300)', '可加 button="right" 右键'],
    ['doubleClick()', '双击', 'pyautogui.doubleClick()', '默认在当前位置'],
    ['typewrite(text)', '模拟键盘输入文字', 'pyautogui.typewrite("hello")', '可用 interval 控制间隔'],
    ['hotkey(*keys)', '按下组合键', 'pyautogui.hotkey("ctrl", "c")', '如复制、粘贴等'],
    ['screenshot()', '截取屏幕并返回 Image', 'img = pyautogui.screenshot()', '可用 img.save() 保存'],
    ['locateOnScreen()', '在屏幕查找图片位置', 'p = pyautogui.locateOnScreen("a.png")', '返回 None 表示未找到'],
    ['press(key)', '按下并松开单个按键', 'pyautogui.press("enter")', '支持 "tab"、"esc" 等'],
    ['FAILSAFE', '安全退出机制', 'pyautogui.FAILSAFE = True', '鼠标移至左上角会抛异常终止'],
], HEADER, WIDTHS)

# ---------- 2. cnocr ----------
heading('2. cnocr —— 中文 OCR 文字识别')
add_table([
    ['from cnocr import CnOcr', '导入中文 OCR 识别类', 'from cnocr import CnOcr', 'pip install cnocr'],
    ['CnOcr()', '创建识别器实例', 'ocr = CnOcr()', '默认识别中文+英文'],
    ['ocr.ocr(图片)', '识别图片中的文字', 'res = ocr.ocr("img.png")', '返回列表，每项含 text/score'],
    ['res[i]["text"]', '获取识别出的文字', 'text = res[0]["text"]', 'score 为置信度(0~1)'],
    ['ocr.ocr_for_single_line()', '识别单行文字', 'r = ocr.ocr_for_single_line(img)', '适用于验证码/单行文本'],
    ['CnOcr(rec_model_name=...)', '指定识别模型', 'ocr = CnOcr(rec_model_name="densenet_lite_136-fc")', '模型越大精度越高、越慢'],
    ['det_model_name 参数', '指定文字检测模型', 'CnOcr(det_model_name="ch_PP-OCRv3_det")', '影响文字定位效果'],
    ['numpy 数组输入', '支持 ndarray 输入', 'ocr.ocr(np_array)', '需 shape 为 (H, W, C)'],
], HEADER, WIDTHS)

# ---------- 3. docx ----------
heading('3. python-docx —— 操作 Word 文档')
add_table([
    ['import docx', '导入 Word 处理库', 'import docx', 'pip install python-docx'],
    ['Document()', '新建空白文档', 'doc = docx.Document()', '可传路径打开已有文件'],
    ['Document("a.docx")', '打开已有文档', 'doc = docx.Document("a.docx")', '路径需存在'],
    ['add_paragraph(text)', '添加段落', 'doc.add_paragraph("你好")', '返回 Paragraph 对象'],
    ['add_heading(text, level)', '添加标题', 'doc.add_heading("标题", level=1)', 'level 1~9'],
    ['add_table(rows, cols)', '添加表格', 't = doc.add_table(1, 3)', '需手动填充单元格'],
    ['add_picture(path)', '插入图片', 'doc.add_picture("a.png")', '可加 width 参数控制大小'],
    ['run 字体设置', '设置字体/字号/加粗', 'r = p.add_run("x"); r.bold = True', 'r.font.size = Pt(12)'],
    ['save(path)', '保存文档', 'doc.save("out.docx")', '文件名以 .docx 结尾'],
    ['cell.text = ...', '写入表格单元格', 't.cell(0, 0).text = "值"', '行、列从 0 开始'],
], HEADER, WIDTHS)

# ---------- 4. requests ----------
heading('4. requests —— HTTP 请求')
add_table([
    ['import requests', '导入 HTTP 请求库', 'import requests', 'pip install requests'],
    ['get(url)', '发送 GET 请求', 'r = requests.get(url)', '返回 Response 对象'],
    ['post(url, data/json)', '发送 POST 请求', 'r = requests.post(url, data={...})', '可用 json= 传 JSON'],
    ['r.status_code', '获取响应状态码', 'code = r.status_code', '200 表示成功'],
    ['r.text', '获取响应文本', 'text = r.text', '按编码解析，可 r.encoding 设置'],
    ['r.json()', '解析 JSON 响应', 'data = r.json()', '响应需为 JSON 格式'],
    ['r.content', '获取二进制内容', 'img = r.content', '常用于下载图片/文件'],
    ['headers 参数', '自定义请求头', 'requests.get(url, headers={"User-Agent": "..."})', '模拟浏览器'],
    ['params 参数', 'URL 查询参数', 'requests.get(url, params={"q": "x"})', '自动拼接 ?q=x'],
    ['timeout', '设置超时', 'requests.get(url, timeout=5)', '超时抛异常'],
    ['Session()', '保持会话(登录态)', 's = requests.Session()', '可自动携带 cookies'],
], HEADER, WIDTHS)

# ---------- 5. selenium ----------
heading('5. selenium —— 浏览器自动化')
add_table([
    ['from selenium import webdriver', '导入浏览器驱动', 'from selenium import webdriver', 'pip install selenium'],
    ['webdriver.Chrome()', '启动 Chrome 浏览器', 'drv = webdriver.Chrome()', '需匹配版本的驱动'],
    ['get(url)', '打开网页', 'drv.get("https://baidu.com")', '等待页面加载'],
    ['find_element(by, value)', '定位单个元素', 'el = drv.find_element("id", "kw")', 'by 可为 id/name/xpath/css'],
    ['find_elements(...)', '定位多个元素', 'els = drv.find_elements("tag", "a")', '返回元素列表'],
    ['el.click()', '点击元素', 'el.click()', '模拟鼠标点击'],
    ['el.send_keys(text)', '输入内容', 'el.send_keys("关键词")', '常用于搜索框/表单'],
    ['el.text', '获取元素文本', 't = el.text', '返回可见文本'],
    ['get_attribute(name)', '获取属性值', 'v = el.get_attribute("href")', '如取链接、src 等'],
    ['page_source', '获取页面源码', 'html = drv.page_source', '可交给解析库处理'],
    ['quit() / close()', '关闭浏览器', 'drv.quit()', 'quit 关闭全部窗口'],
    ['WebDriverWait', '显式等待', 'from selenium.webdriver.support.ui import WebDriverWait', '等待元素出现再操作'],
    ['By', '定位方式枚举', 'from selenium.webdriver.common.by import By', 'drv.find_element(By.ID, "kw")'],
], HEADER, WIDTHS)

# ---------- 6. os ----------
heading('6. os —— 系统与路径操作')
add_table([
    ['import os', '导入系统模块（标准库）', 'import os', '无需安装'],
    ['getcwd()', '获取当前工作目录', 'cwd = os.getcwd()', '返回字符串路径'],
    ['chdir(path)', '切换工作目录', 'os.chdir("D:/work")', '改变当前目录'],
    ['listdir(path)', '列出目录内容', 'fs = os.listdir(".")', '返回文件名列表'],
    ['mkdir(path)', '创建目录', 'os.mkdir("new_dir")', '父目录需存在'],
    ['makedirs(path)', '递归创建目录', 'os.makedirs("a/b/c")', '自动创建中间目录'],
    ['remove(path)', '删除文件', 'os.remove("a.txt")', '仅能删文件'],
    ['rmdir(path)', '删除空目录', 'os.rmdir("dir")', '目录非空会报错'],
    ['rename(a, b)', '重命名文件/目录', 'os.rename("a.txt", "b.txt")', '也可用于移动'],
    ['path.exists(p)', '判断路径是否存在', 'os.path.exists("a.txt")', '返回布尔值'],
    ['path.join(a, b)', '拼接路径', 'os.path.join("dir", "f.txt")', '自动处理分隔符'],
    ['path.basename(p)', '获取文件名', 'os.path.basename("d/f.txt")', '返回 "f.txt"'],
    ['path.splitext(p)', '分离扩展名', 'os.path.splitext("f.txt")', '返回 ("f", ".txt")'],
    ['path.isfile/isdir', '判断文件/目录', 'os.path.isfile("a.txt")', '返回布尔值'],
], HEADER, WIDTHS)

# ---------- 7. random ----------
heading('7. random —— 随机数生成')
add_table([
    ['import random', '导入随机模块（标准库）', 'import random', '无需安装'],
    ['random()', '生成 [0,1) 随机浮点数', 'x = random.random()', '左闭右开'],
    ['randint(a, b)', '生成 [a,b] 随机整数', 'n = random.randint(1, 10)', '包含两端'],
    ['uniform(a, b)', '生成 [a,b] 随机浮点数', 'f = random.uniform(0, 100)', '含 a、b'],
    ['choice(seq)', '随机选一个元素', 'c = random.choice([1,2,3])', '序列可为列表/元组'],
    ['shuffle(seq)', '原地打乱序列', 'random.shuffle(lst)', '无返回值，直接修改'],
    ['sample(seq, k)', '随机抽样 k 个', 's = random.sample(lst, 3)', '不重复抽样'],
    ['randrange(a, b, step)', '按步长取随机整数', 'n = random.randrange(0, 10, 2)', '结果为偶数'],
    ['seed(n)', '设置随机种子', 'random.seed(42)', '固定结果便于复现'],
    ['random() 结合字符', '生成随机验证码', 'code = "".join(random.choices("0123", k=4))', 'choices 可重复抽样'],
], HEADER, WIDTHS)

# ---------- 8. shutil ----------
heading('8. shutil —— 高级文件操作')
add_table([
    ['import shutil', '导入高级文件操作（标准库）', 'import shutil', '无需安装'],
    ['copy(src, dst)', '复制文件', 'shutil.copy("a.txt", "b.txt")', '保留文件内容'],
    ['copy2(src, dst)', '复制并保留元数据', 'shutil.copy2("a.txt", "b.txt")', '含修改时间等'],
    ['copyfile(src, dst)', '仅复制文件内容', 'shutil.copyfile("a.txt", "b.txt")', 'dst 必须是文件路径'],
    ['copytree(src, dst)', '递归复制整个目录', 'shutil.copytree("src", "dst")', 'dst 不能已存在'],
    ['rmtree(path)', '递归删除目录树', 'shutil.rmtree("dir")', '删除目录及所有内容'],
    ['move(src, dst)', '移动文件/目录', 'shutil.move("a.txt", "dir/")', '跨盘时会复制+删除'],
    ['make_archive(...)', '创建压缩包', 'shutil.make_archive("out", "zip", "dir")', '生成 out.zip'],
    ['unpack_archive(...)', '解压压缩包', 'shutil.unpack_archive("a.zip", "dir")', '支持 zip/tar 等'],
    ['disk_usage(path)', '磁盘空间信息', 'u = shutil.disk_usage("C:/")', '返回 total/used/free'],
    ['which(cmd)', '查找命令路径', 'p = shutil.which("python")', '返回路径或 None'],
], HEADER, WIDTHS)

# ---------- 9. cv2 ----------
heading('9. cv2 (OpenCV) —— 图像处理与计算机视觉')
add_table([
    ['import cv2', '导入 OpenCV', 'import cv2', 'pip install opencv-python'],
    ['imread(path)', '读取图片', 'img = cv2.imread("a.png")', '返回 BGR 的 ndarray'],
    ['imwrite(path, img)', '保存图片', 'cv2.imwrite("b.png", img)', '格式由扩展名决定'],
    ['imshow(win, img)', '显示图片窗口', 'cv2.imshow("w", img); cv2.waitKey(0)', 'waitKey 等待按键'],
    ['cvtColor(...)', '颜色空间转换', 'gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)', 'BGR->灰度'],
    ['resize(img, dsize)', '缩放图片', 'img2 = cv2.resize(img, (w, h))', 'dsize 为 (宽, 高)'],
    ['GaussianBlur(...)', '高斯模糊', 'blur = cv2.GaussianBlur(img, (5,5), 0)', '去噪'],
    ['Canny(...)', '边缘检测', 'edges = cv2.Canny(gray, 100, 200)', '两个阈值为低/高'],
    ['threshold(...)', '二值化', 'r, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)', '返回阈值和结果'],
    ['findContours(...)', '查找轮廓', 'c, h = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)', '用于形状检测'],
    ['rectangle/circle(...)', '绘制图形', 'cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)', '颜色为 BGR'],
    ['putText(...)', '绘制文字', 'cv2.putText(img, "hi", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)', '需注意中文乱码'],
    ['matchTemplate(...)', '模板匹配', 'res = cv2.matchTemplate(img, tmpl, cv2.TM_CCOEFF_NORMED)', '在图中找子图'],
    ['VideoCapture(...)', '读取摄像头/视频', 'cap = cv2.VideoCapture(0)', '0 为默认摄像头'],
    ['shape / dtype', '获取图像尺寸/类型', 'h, w, c = img.shape', 'OpenCV 为 BGR 通道顺序'],
], HEADER, WIDTHS)

doc.save('Python库使用方法总结.docx')
print('saved Python库使用方法总结.docx')
