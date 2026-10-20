from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

W, H = 1600, 1000
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

top = (120, 60, 120)
mid = (255, 120, 60)
horizon = (255, 210, 120)
horizon_y = int(H * 0.78)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

for y in range(horizon_y):
    t = y / (horizon_y - 1)
    c = lerp(top, mid, t) if t < 0.55 else lerp(mid, horizon, (t - 0.55) / 0.45)
    draw.line([(0, y), (W, y)], fill=c)

sun_x, sun_y, sun_r = W // 2, int(H * 0.42), 130
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([sun_x - sun_r * 3, sun_y - sun_r * 3, sun_x + sun_r * 3, sun_y + sun_r * 3],
           fill=(255, 220, 120, 120))
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
draw = ImageDraw.Draw(img)
draw.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r],
             fill=(255, 235, 160))

dark = (50, 25, 40)

def draw_person(dx, ground_y, s, arm_raise=1.0, lean=0):
    shoulder_y = ground_y - 0.72 * s
    hip_y = ground_y - 0.42 * s
    head_r = 0.085 * s
    head_cy = ground_y - 0.90 * s
    lw = int(0.075 * s)
    shoulder_x = dx + lean * 0.15 * s
    draw.ellipse([shoulder_x - head_r, head_cy - head_r, shoulder_x + head_r, head_cy + head_r], fill=dark)
    draw.line([(shoulder_x, ground_y - 0.80 * s), (shoulder_x, hip_y)], fill=dark, width=lw)
    half = 0.10 * s
    for side in (-1, 1):
        sx = shoulder_x + side * half
        hy = ground_y - 0.28 * s
        hx = sx + side * 0.20 * s * arm_raise
        hy2 = shoulder_y - 0.32 * s * arm_raise
        draw.line([(sx, shoulder_y), (hx, hy2)], fill=dark, width=lw)
        leg_x = shoulder_x + side * half * 0.8
        knee_x = leg_x + side * 0.05 * s
        knee_y = ground_y - 0.20 * s
        draw.line([(leg_x, hip_y), (knee_x, knee_y), (knee_x, ground_y - 1)], fill=dark, width=lw)

def draw_flag(dx, ground_y, s):
    px = dx
    ph = s * 1.1
    draw.line([(px, ground_y), (px, ground_y - ph)], fill=(80, 40, 50), width=int(0.03 * s))
    fw, fh = 0.42 * s, 0.26 * s
    fx, fy = px, ground_y - ph
    draw.polygon([(fx, fy), (fx + fw, fy + fh * 0.5), (fx, fy + fh)], fill=(200, 30, 40))

ground_y = horizon_y + 40
figures = [
    (-340, 1.0, 0),
    (-120, 1.18, 0),
    (0, 1.0, -0.4),
    (150, 1.24, 0),
    (350, 0.9, 0),
]
for dx, sc, lean in figures:
    draw_person(W // 2 + dx, ground_y, 260 * sc, arm_raise=1.0, lean=lean)

draw_flag(W // 2 - 520, ground_y, 300)

hill = (75, 35, 45)
draw.polygon([(0, ground_y), (0, ground_y + 60), (W, ground_y + 60), (W, ground_y),
              (W * 0.6, ground_y - 40), (W * 0.3, ground_y)], fill=hill)
ground = (40, 20, 28)
draw.rectangle([0, ground_y + 30, W, H], fill=ground)

bird = (60, 30, 45)
for bx, by, sc in [(-300, 200, 1), (-180, 130, 0.7), (240, 180, 0.85), (360, 120, 0.6)]:
    x = W // 2 + bx
    y = int(H * 0.25 + by)
    lw = int(3 * sc)
    draw.line([(x - 24 * sc, y - 10 * sc), (x, y), (x + 24 * sc, y - 10 * sc)], fill=bird, width=lw)

title = "筑梦新时代"
font = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 140)
bbox = draw.textbbox((0, 0), title, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = (W - tw) // 2 - bbox[0]
y = 70 - bbox[1]

shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.text((x + 6, y + 6), title, font=font, fill=(0, 0, 0, 120))
shadow = shadow.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
draw = ImageDraw.Draw(img)
draw.text((x, y), title, font=font, fill=(255, 215, 90))

sub = "青春向党 · 逐梦远航"
sfont = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 52)
sbbox = draw.textbbox((0, 0), sub, font=sfont)
sw = sbbox[2] - sbbox[0]
sx = (W - sw) // 2 - sbbox[0]
draw.text((sx, y + th + 40), sub, font=sfont, fill=(255, 240, 200))

out = "筑梦新时代_青少年.png"
img.convert("RGB").save(out)
print("saved", out)
