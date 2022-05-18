from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import aiohttp


class CardGenerator:
    def __init__(self) -> None:
        self.thinfont = ImageFont.truetype("font/MADE TOMMY Thin_PERSONAL USE.otf", 30)
        self.boldfont = ImageFont.truetype("font/MADE Tommy Soft Bold PERSONAL USE.otf", 25)
        self.extraboldfont = ImageFont.truetype("font/MADE Tommy Soft ExtraBold PERSONAL USE.otf", 40)
        self.sayi = ImageFont.truetype("font/MADE Tommy Soft Bold PERSONAL USE.otf", 35)
        self.orta = 610 + (890 - 610) / 2

    def remap(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    async def generate(self, pf, name, discrim, level, currentxp, startxp, nextlevelxp, **kwargs):
        main_color = kwargs.get("main_color") or "white"

        cardImage = Image.new(size=(900, 220), mode="RGB", color="#37393f")

        if kwargs.get("background"):
            async with aiohttp.ClientSession() as ses:
                async with ses.get(kwargs.get("background")) as r:
                    if r.status == 200:
                        cardImage.paste(Image.open(BytesIO(await r.read())))
                    else:
                        raise Exception("Bruh")

        async with aiohttp.ClientSession() as ses:
            async with ses.get(pf) as r:
                if r.status == 200:
                    profileImage = Image.open(BytesIO(await r.read()))
                else:
                    raise Exception("Bruh")

        profileMask = Image.new(mode="RGBA", size=profileImage.size)

        cardImageDraw = ImageDraw.Draw(cardImage, mode="RGBA")
        cardImageDraw.rounded_rectangle((10, 10, 600, 210), radius=7, fill=(0, 0, 0, 110))
        cardImageDraw.rounded_rectangle((610, 10, 890, 105), radius=7, fill=(0, 0, 0, 110))
        cardImageDraw.rounded_rectangle((610, 115, 890, 210), radius=7, fill=(0, 0, 0, 110))
        cardImageDraw.ellipse(
            (48, int(220 / 2 - profileImage.size[1] / 2) - 2, 180, int(220 / 2 - profileImage.size[1] / 2) + 130),
            width=2, outline=main_color)

        profileMaskDraw = ImageDraw.Draw(profileMask)
        profileMaskDraw.ellipse((0, 0) + profileImage.size, fill=main_color)
        profileMask.paste(profileImage, (0, 0), profileMask)

        cardImageDraw.text((self.orta - self.boldfont.getlength("LEVEL") / 2, 10), "LEVEL", fill="#37393f",
                           font=self.boldfont)
        cardImageDraw.text((self.orta - self.boldfont.getlength("EXP") / 2, 115), "EXP", fill="#37393f",
                           font=self.boldfont)

        cardImageDraw.text((210, 30), name, fill=main_color, font=self.extraboldfont)
        cardImageDraw.text((210 + self.extraboldfont.getlength(name), 45), discrim, fill="#d1d1d1", font=self.boldfont)
        cardImageDraw.text((self.orta - self.sayi.getlength(str(level)) / 2, 50), str(level), fill=main_color,
                           font=self.sayi)

        xpImage = Image.new("RGBA", (
        int(self.boldfont.getlength(f"/{nextlevelxp}") + self.sayi.getlength(str(currentxp))),
        self.sayi.getsize(str(currentxp))[1]))
        xpImageDraw = ImageDraw.Draw(xpImage)
        xpImageDraw.text((0, 0), str(currentxp), fill=main_color, font=self.sayi)
        xpImageDraw.text((self.sayi.getlength(str(currentxp)), 8), f"/{nextlevelxp}", fill="#d1d1d1",
                         font=self.boldfont)
        cardImage.paste(xpImage, (int(self.orta - xpImage.size[0] / 2), 155), xpImage)

        barImage = Image.new("RGBA", (592, 7))
        barImageDraw = ImageDraw.Draw(barImage)
        barImageDraw.rectangle((0, 0, self.remap(currentxp, startxp, nextlevelxp, 0, 592), 7), fill=main_color)
        barMask = Image.new("RGBA", (592, 7))
        barMaskDraw = ImageDraw.Draw(barMask)
        barMaskDraw.rounded_rectangle((1, 0, 591, 7), radius=7, fill="grey")
        barMaskDraw.rectangle((1, 0, 591, 1), fill="grey")
        barMask.paste(barImage, (0, 0), barMask)

        cardImage.paste(barMask, (9, 204), barMask)
        cardImage.paste(profileMask, (50, int(110 - profileImage.size[1] / 2)), profileMask)

        bytes = BytesIO()
        cardImage.save(bytes, "png")
        bytes.seek(0)
        return bytes