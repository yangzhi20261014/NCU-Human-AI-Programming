# -*- coding: utf-8 -*-
"""
九一八事变 纪念视频生成器
生成一段 10~30 秒的纪念视频（本示例约 20 秒），输出为 九一八.mp4
需安装：pip install moviepy pillow numpy
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip

# ---------- 参数 ----------
W, H = 1280, 720
FPS = 24
OUT = "九一八.mp4"

# ---------- 中文字体 ----------
FONT_CANDIDATES = [
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simkai.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/NotoSerifSC-VF.ttf",
    "C:/Windows/Fonts/NotoSansSC-VF.ttf",
]


def find_font(paths):
    for p in paths:
        try:
            ImageFont.truetype(p, 20)
            return p
        except Exception:
            continue
    return None


FONT_MAIN = find_font(FONT_CANDIDATES)
FONT_BOLD = find_font(["C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/msyhbd.ttc"] + FONT_CANDIDATES)
if FONT_MAIN is None:
    raise SystemExit("未找到中文字体，请检查 C:/Windows/Fonts 目录")


def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_MAIN
    return ImageFont.truetype(path, size)


# ---------- 配色（庄严肃穆） ----------
BG_TOP = (8, 8, 12)
BG_BOT = (28, 22, 24)
TEXT_MAIN = (220, 215, 205)       # 米白
TEXT_SUB = (150, 145, 140)        # 灰
ACCENT = (176, 30, 34)            # 深红
ACCENT_DIM = (120, 28, 30)        # 暗红


# ---------- 场景脚本 ----------
# (主标题, 副标题, 时长秒, 是否红色强调)
SCENES = [
    ("历史不会忘记", "谨以此片纪念", 2.6, False),
    ("1931年9月18日", "一个刻骨铭心的日子", 3.0, False),
    ("九一八事变", "日军悍然发动侵略战争", 3.0, True),
    ("山河破碎", "东北三省沦陷", 2.6, True),
    ("十四年抗战", "三千五百万同胞伤亡", 3.2, True),
    ("勿忘国耻", "山河已无恙，吾辈当自强", 2.8, True),
    ("铭记历史", "珍爱和平，开创未来", 3.0, False),
]


# ---------- 逐帧渲染 ----------
def draw_frame(scene, progress, fade):
    """scene: (title, sub, _, red); progress: 0~1 场景内进度; fade: 0~1 整体透明度"""
    title, sub, _, red = scene
    # 背景渐变
    img = Image.new("RGB", (W, H), BG_TOP)
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)

    draw = ImageDraw.Draw(img, "RGBA")

    # 底部暗红光晕
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W // 2 - 420, H - 220, W // 2 + 420, H + 260], fill=(140, 25, 28, 90))
    img = Image.alpha_composite(img.convert("RGBA"), glow)

    draw = ImageDraw.Draw(img, "RGBA")

    # 顶部小字（年份水印）
    f_small = font(30)
    draw.text((W // 2, 60), "九一八事变", font=f_small,
              fill=(*ACCENT_DIM, int(200 * fade)), anchor="mm")

    # 分隔线（随进度展开）
    line_w = int(W * 0.5 * min(1.0, progress * 1.5))
    line_y = H // 2 - 70
    draw.line([(W // 2 - line_w // 2, line_y), (W // 2 + line_w // 2, line_y)],
              fill=(*ACCENT, int(220 * fade)), width=3)

    # 主标题（缩放淡入）
    scale = 0.9 + 0.1 * min(1.0, progress * 3)
    f_main = font(int(96 * scale), bold=True)
    color = ACCENT if red else TEXT_MAIN
    draw.text((W // 2, H // 2), title, font=f_main,
              fill=(*color, int(255 * fade)), anchor="mm")

    # 副标题
    f_sub = font(36)
    draw.text((W // 2, H // 2 + 120), sub, font=f_sub,
              fill=(*TEXT_SUB, int(230 * fade)), anchor="mm")

    # 底部小字
    f_foot = font(26)
    draw.text((W // 2, H - 70), "1931 · 9 · 18", font=f_foot,
              fill=(*ACCENT_DIM, int(180 * fade)), anchor="mm")

    return img


def render_scene(scene, fps=FPS):
    title, sub, dur, red = scene
    n = int(dur * fps)
    frames = []
    fade_in = int(0.5 * fps)
    fade_out = int(0.6 * fps)
    for i in range(n):
        progress = i / n
        # 淡入淡出
        alpha = 1.0
        if i < fade_in:
            alpha = i / fade_in
        if i >= n - fade_out:
            alpha = max(0.0, (n - i) / fade_out)
        img = draw_frame(scene, progress, alpha)
        frames.append(np.array(img))
    return frames


def main():
    print("开始渲染……")
    all_frames = []
    for sc in SCENES:
        all_frames.extend(render_scene(sc))
    total = len(all_frames) / FPS
    print(f"共 {len(all_frames)} 帧，时长 {total:.1f} 秒")

    clip = ImageSequenceClip(all_frames, fps=FPS)
    clip.write_videofile(OUT, codec="libx264", audio=False,
                         preset="medium", logger=None)
    print(f"已保存：{OUT}")


if __name__ == "__main__":
    main()
