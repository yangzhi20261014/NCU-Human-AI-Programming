# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

W, H = 1600, 1000
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

top = (14, 24, 62)
bot = (44, 62, 110)
for y in range(H):
    draw.line([(0, y), (W, y)], fill=lerp(top, bot, y / H))

def draw_moon(cx, cy, r):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - r * 3, cy - r * 3, cx + r * 3, cy + r * 3], fill=(255, 235, 180, 110))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(252, 244, 205))
    for i in range(5):
        ox = (i - 2) * r * 0.42
        oy = ((i * 37) % 3 - 1) * r * 0.22
        rr = r * (0.16 + 0.03 * (i % 2))
        d.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr], fill=(242, 228, 175))

draw_moon(W * 0.5, H * 0.40, 190)

def draw_cloud(cx, cy, s, alpha=80):
    cloud = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cloud)
    color = (200, 215, 235, alpha)
    cd.ellipse([cx - s, cy - s * 0.4, cx + s, cy + s * 0.4], fill=color)
    cd.ellipse([cx - s * 0.6, cy - s * 0.55, cx + s * 0.3, cy + s * 0.25], fill=color)
    cd.ellipse([cx + s * 0.2, cy - s * 0.5, cx + s * 0.9, cy + s * 0.2], fill=color)
    cloud = cloud.filter(ImageFilter.GaussianBlur(10))
    img.paste(cloud, (0, 0), cloud)

draw_cloud(W * 0.22, H * 0.28, 130)
draw_cloud(W * 0.80, H * 0.30, 110)
draw_cloud(W * 0.14, H * 0.55, 140)

def draw_lantern(x, top_y, s):
    d = ImageDraw.Draw(img)
    body_w = s * 0.42
    body_h = s * 0.52
    d.line([(x, 0), (x, top_y)], fill=(180, 150, 70), width=max(2, int(s * 0.04)))
    d.rectangle([x - s * 0.06, top_y, x + s * 0.06, top_y + s * 0.08], fill=(190, 150, 60))
    body_y = top_y + s * 0.08
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([x - body_w * 1.6, body_y, x + body_w * 1.6, body_y + body_h], fill=(255, 150, 80, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(img)
    d.ellipse([x - body_w, body_y, x + body_w, body_y + body_h], fill=(215, 40, 40))
    d.line([(x - body_w * 0.5, body_y + body_h * 0.45), (x + body_w * 0.5, body_y + body_h * 0.45)],
           fill=(255, 215, 120), width=max(2, int(s * 0.05)))
    d.rectangle([x - s * 0.06, body_y + body_h, x + s * 0.06, body_y + body_h + s * 0.08], fill=(190, 150, 60))
    tassel_top = body_y + body_h + s * 0.08
    d.line([(x, tassel_top), (x, tassel_top + s * 0.16)], fill=(200, 50, 40), width=max(2, int(s * 0.03)))
    for t in range(3):
        tx = x + (t - 1) * s * 0.1
        d.line([(x, tassel_top + s * 0.16), (tx, tassel_top + s * 0.28)], fill=(255, 190, 60), width=2)

draw_lantern(W * 0.16, 90, 200)
draw_lantern(W * 0.86, 110, 170)
draw_lantern(W * 0.30, 60, 130)

def draw_rabbit(cx, ground_y, s):
    d = ImageDraw.Draw(img)
    col = (240, 244, 235)
    shade = (210, 218, 205)
    body_w = s * 0.52
    body_h = s * 0.5
    bx = cx
    by = ground_y - body_h
    d.ellipse([bx - body_w, by - body_h * 0.4, bx + body_w, by + body_h * 0.6], fill=col)
    head_r = s * 0.2
    hx = bx + body_w * 0.55
    hy = by - body_h * 0.25
    d.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r], fill=col)
    for i in range(2):
        ex = hx + (0.1 if i == 0 else -0.02) * s
        ey = hy - head_r
        ew = s * 0.09
        eh = s * 0.34
        d.ellipse([ex - ew, ey - eh, ex + ew, ey + eh * 0.5], fill=col)
        d.ellipse([ex - ew * 0.5, ey - eh * 0.85, ex + ew * 0.5, ey + eh * 0.25], fill=shade)
    d.ellipse([bx - body_w * 1.05, by - body_h * 0.05, bx - body_w * 0.7, by + body_h * 0.3], fill=col)
    d.ellipse([hx - head_r * 0.45, hy - head_r * 0.3, hx - head_r * 0.1, hy], fill=(120, 130, 125))
    d.ellipse([hx + head_r * 0.1, hy - head_r * 0.3, hx + head_r * 0.45, hy], fill=(120, 130, 125))
    d.polygon([(hx, hy + head_r * 0.1), (hx - head_r * 0.5, hy + head_r * 0.45), (hx + head_r * 0.3, hy + head_r * 0.4)], fill=shade)
    d.ellipse([bx - body_w * 0.3, ground_y - s * 0.1, bx + body_w * 0.3, ground_y + s * 0.06], fill=shade)

ground_y = H - 120
d = ImageDraw.Draw(img)
d.polygon([(0, ground_y), (0, H), (W, H), (W, ground_y),
           (W * 0.65, ground_y - 60), (W * 0.35, ground_y - 20)], fill=(20, 34, 56))
draw_rabbit(W * 0.30, ground_y, 220)
draw_rabbit(W * 0.64, ground_y, 160)

def draw_osmanthus(x, y, s):
    d = ImageDraw.Draw(img)
    for i in range(4):
        ang = i * math.pi / 2 + 0.4
        px = x + s * 0.55 * math.cos(ang)
        py = y + s * 0.55 * math.sin(ang)
        d.ellipse([px - s * 0.35, py - s * 0.35, px + s * 0.35, py + s * 0.35], fill=(255, 205, 70))
    d.ellipse([x - s * 0.28, y - s * 0.28, x + s * 0.28, y + s * 0.28], fill=(235, 150, 35))

def draw_leaf(x, y, ang, s):
    d = ImageDraw.Draw(img)
    c, sn = math.cos(ang), math.sin(ang)
    tip = (x + s * c, y + s * sn)
    base1 = (x - s * 0.3 * sn, y + s * 0.3 * c)
    base2 = (x + s * 0.3 * sn, y - s * 0.3 * c)
    d.polygon([tip, base1, base2], fill=(80, 130, 70))

def draw_vine(x0, sway, length):
    d = ImageDraw.Draw(img)
    pts = []
    x, y = x0, -5
    n = max(2, int(length / 48))
    for i in range(n):
        x += sway * math.sin(i * 0.65) * 14
        y += length / n
        pts.append((x, y))
    d.line(pts, fill=(110, 80, 55), width=5)
    for i, (px, py) in enumerate(pts):
        if i % 3 == 1:
            draw_leaf(px - 10, py, math.pi * 0.2, 28)
            draw_leaf(px + 10, py, math.pi * 0.82, 28)
        if i % 3 == 2:
            draw_osmanthus(px - 18, py, 15)
            draw_osmanthus(px + 18, py + 8, 13)

draw_vine(W * 0.05, 1.0, 540)
draw_vine(W * 0.95, -1.0, 500)

def draw_mooncake(cx, cy, r):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r * 1.5, cy + r * 0.65, cx + r * 1.5, cy + r * 1.05], fill=(225, 232, 228))
    d.ellipse([cx - r * 1.3, cy + r * 0.55, cx + r * 1.3, cy + r * 0.9], fill=(205, 214, 208))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(186, 118, 46))
    for a in range(0, 360, 15):
        px = cx + r * 0.92 * math.cos(math.radians(a))
        py = cy + r * 0.92 * math.sin(math.radians(a))
        d.ellipse([px - r * 0.06, py - r * 0.06, px + r * 0.06, py + r * 0.06], fill=(150, 92, 34))
    d.ellipse([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82], fill=(216, 152, 66))
    d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5], outline=(150, 92, 34), width=3)
    mf = ImageFont.truetype("C:/Windows/Fonts/STLITI.TTF", int(r * 0.85))
    mb = d.textbbox((0, 0), "月", font=mf)
    mw, mh = mb[2] - mb[0], mb[3] - mb[1]
    d.text((cx - mw / 2 - mb[0], cy - mh / 2 - mb[1]), "月", font=mf, fill=(150, 92, 34))

draw_mooncake(W * 0.80, H - 180, 75)
draw_mooncake(W * 0.88, H - 160, 55)
draw_mooncake(W * 0.72, H - 150, 60)

stars = ImageDraw.Draw(img)
for i in range(80):
    sx = (i * 131 + 40) % W
    sy = (i * 97 + 30) % int(H * 0.5)
    r = 1 + (i % 2)
    stars.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 250, 220) if i % 3 else (200, 215, 240))

title = "中秋节快乐"
tfont = ImageFont.truetype("C:/Windows/Fonts/STXINGKA.TTF", 170)
bb = draw.textbbox((0, 0), title, font=tfont)
tw, th = bb[2] - bb[0], bb[3] - bb[1]
x = (W - tw) // 2 - bb[0]
y = H - 430 - bb[1]

shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.text((x + 6, y + 6), title, font=tfont, fill=(0, 0, 0, 130))
shadow = shadow.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
d = ImageDraw.Draw(img)
d.text((x, y), title, font=tfont, fill=(255, 205, 90))

sub = "但愿人长久 · 千里共婵娟"
sfont = ImageFont.truetype("C:/Windows/Fonts/STLITI.TTF", 54)
sb = d.textbbox((0, 0), sub, font=sfont)
sw = sb[2] - sb[0]
sx = (W - sw) // 2 - sb[0]
d.text((sx, y + th + 30), sub, font=sfont, fill=(235, 220, 180))

seal_s = 110
seal_x = x + tw + 30
seal_y = y + th - seal_s
d.rounded_rectangle([seal_x, seal_y, seal_x + seal_s, seal_y + seal_s], radius=12, fill=(190, 30, 30))
sf = ImageFont.truetype("C:/Windows/Fonts/STLITI.TTF", 74)
sb2 = d.textbbox((0, 0), "团圆", font=sf)
w2, h2 = sb2[2] - sb2[0], sb2[3] - sb2[1]
d.text((seal_x + (seal_s - w2) / 2 - sb2[0], seal_y + (seal_s - h2) / 2 - sb2[1]), "团圆", font=sf, fill=(250, 240, 225))

out = "中秋节快乐.png"
img.convert("RGB").save(out)
print("saved", out)
