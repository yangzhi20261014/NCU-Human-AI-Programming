from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

W, H = 1600, 1000
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

top = (214, 40, 40)
bottom = (126, 10, 60)
for y in range(H):
    t = y / (H - 1)
    c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    draw.line([(0, y), (W, y)], fill=c)

gold = (255, 215, 130)
for i in range(60):
    x = int((i * 137.5) % W)
    y = int((i * 97.3) % H)
    r = 1 + (i % 3)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=gold)

for i in range(6):
    a = i / 6 * 2 * math.pi
    cx = W // 2 + 420 * math.cos(a)
    cy = H // 2 + 320 * math.sin(a)
    r = 60
    glow = Image.new("RGBA", (r * 8, r * 8), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([r * 4 - r, r * 4 - r, r * 4 + r, r * 4 + r], fill=(255, 200, 100, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img.paste(glow, (int(cx - r * 4), int(cy - r * 4)), glow)

text = "筑梦新时代"
font = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 180)
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = (W - tw) // 2 - bbox[0]
y = (H - th) // 2 - bbox[1]

shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.text((x + 8, y + 10), text, font=font, fill=(0, 0, 0, 120))
shadow = shadow.filter(ImageFilter.GaussianBlur(12))
img = Image.alpha_composite(img.convert("RGBA"), shadow)

draw = ImageDraw.Draw(img)
for dx, dy in [(-5, -5), (5, 5), (5, -5), (-5, 5)]:
    draw.text((x + dx, y + dy), text, font=font, fill=(255, 245, 210))
draw.text((x, y), text, font=font, fill=(255, 210, 80))

sub = "建功新时代 · 奋进新征程"
sfont = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 56)
sbbox = draw.textbbox((0, 0), sub, font=sfont)
sw = sbbox[2] - sbbox[0]
sx = (W - sw) // 2 - sbbox[0]
sy = y + th + 80
draw.text((sx + 3, sy + 3), sub, font=sfont, fill=(0, 0, 0))
draw.text((sx, sy), sub, font=sfont, fill=(255, 235, 170))

out = "筑梦新时代.png"
img.convert("RGB").save(out)
print("saved", out)
