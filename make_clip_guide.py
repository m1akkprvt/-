from PIL import Image, ImageDraw, ImageFont
import os

base_path = '/workspaces/-'
input_path = os.path.join(base_path, 'ps4_cover_clip_example.jpg')
output_path = os.path.join(base_path, 'ps4_cover_clip_guide.jpg')
if not os.path.exists(input_path):
    raise FileNotFoundError(input_path)
img = Image.open(input_path).convert('RGB')

w, h = img.size
new_w = max(2200, w + 800)
new_h = max(1200, h + 100)
canvas = Image.new('RGB', (new_w, new_h), (30, 30, 30))
canvas.paste(img, (50, 50))
draw = ImageDraw.Draw(canvas)

try:
    font = ImageFont.truetype('DejaVuSans-Bold.ttf', 34)
    font_small = ImageFont.truetype('DejaVuSans.ttf', 24)
except Exception:
    font = ImageFont.load_default()
    font_small = ImageFont.load_default()

# arrow helper
def arrow(start, end, color=(255,255,255), width=4):
    draw.line([start, end], fill=color, width=width)
    import math
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    perp = (-uy, ux)
    size = 18
    p1 = (end[0] - ux * size + perp[0] * size / 2, end[1] - uy * size + perp[1] * size / 2)
    p2 = (end[0] - ux * size - perp[0] * size / 2, end[1] - uy * size - perp[1] * size / 2)
    draw.polygon([end, p1, p2], fill=color)

# image coordinates
img_x = 50
img_y = 50
img_w = w
img_h = h

arrow((img_x + img_w - 40, img_y + 200), (img_x + img_w + 180, img_y + 160))
draw.text((img_x + img_w + 200, img_y + 140), '1. Вставляется сверху', fill=(255,255,255), font=font_small)

arrow((img_x + 100, img_y + img_h - 40), (img_x + 180, img_y + img_h + 40))
draw.text((img_x + 200, img_y + img_h - 20), '2. Нижняя защёлка', fill=(255,255,255), font=font_small)
draw.text((img_x + 200, img_y + img_h + 15), 'держится за корпус', fill=(255,255,255), font=font_small)

arrow((img_x + img_w - 40, img_y + img_h - 120), (img_x + img_w + 220, img_y + img_h - 180))
draw.text((img_x + img_w + 240, img_y + img_h - 200), '3. Передняя часть обхватывает крышку сверху', fill=(255,255,255), font=font_small)

arrow((img_x + 250, img_y + 20), (img_x + 320, img_y + 120))
draw.text((img_x + 340, img_y + 10), '4. Внутренний выступ', fill=(255,255,255), font=font_small)
draw.text((img_x + 340, img_y + 35), 'поддерживает толщину крышки', fill=(255,255,255), font=font_small)

# text section
header = 'Гайд по установке защёлки на корпус PS4'
draw.text((50, h + 70), header, fill=(255,220,130), font=font)

lines = [
    'Расположение клипсы на корпусе:',
    '• Клипса ставится на нижний край крышки.',
    '• Задняя стенка фиксируется за боковой край корпуса.',
    '• Лицевая часть обхватывает крышку сверху.',
    '',
    'Порядок установки:',
    '1. Подведите клипсу к месту крепления на корпусе.',
    '2. Зацепите заднюю стенку за выступ корпуса.',
    '3. Опустите крышку сверху внутрь клипсы.',
    '4. Убедитесь, что боковые стенки обхватили край.',
    '',
    'Рекомендации:',
    '• Принтер: Direct extruder.',
    '• Слайсер: OrcaSlicer с tree supports.',
    '• Не изменять размеры.',
    '• Начните с gap20 (0.20 мм).',
]
text_x = 50
text_y = h + 130
for line in lines:
    draw.text((text_x, text_y), line, fill=(220,220,220), font=font_small)
    text_y += 32

canvas.save(output_path, quality=90)
print('saved guide', output_path)
