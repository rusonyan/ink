from PIL import ImageFont, Image, ImageDraw

max_font = ImageFont.truetype('static/fonts/siyuan.otf', 35)

result = Image.new("1", (400, 300), 255)
d = ImageDraw.Draw(result)

icon = Image.open("static/img/cofa.png").resize((90, 90), Image.LANCZOS)

result.paste(icon, (80, 100), icon)
result.paste(icon, (80, 100), icon)

d.line(((200, 70), (200, 230)), fill=0, width=1)
d.text((230, 50), '已下班', font=max_font, fill=0)

d.text((40,250),'')

result.save("out.jpg", "jpeg")
result.close()
