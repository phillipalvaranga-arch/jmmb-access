#!/usr/bin/env python3
"""Create a neutral bank-and-key icon for JMMB Access (not JMMB's logo)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ICONS = ROOT / "icons"
ICONS.mkdir(exist_ok=True)

NAVY = (22, 48, 79, 255)          # #16304F
NAVY_DEEP = (14, 32, 54, 255)
CREAM = (244, 239, 227, 255)
COPPER = (184, 122, 47, 255)
COPPER_LT = (214, 164, 86, 255)
GOLD = (212, 168, 80, 255)
WHITE = (255, 255, 255, 255)
STEP = (226, 216, 196, 255)
WINDOW = (163, 196, 224, 255)
SHADOW = (8, 16, 28, 90)


def load_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/sand-box/google/Noto Sans/NotoSans-VariableFont_wdth,wght.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded_rect(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def draw_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background tile
    pad = 0 if maskable else int(size * 0.02)
    r = int(size * (0.22 if not maskable else 0.0))
    if maskable:
        d.rectangle((0, 0, size, size), fill=NAVY)
    else:
        rounded_rect(d, (pad, pad, size - pad - 1, size - pad - 1), r, NAVY)

    # Subtle top highlight
    hi = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hi)
    if maskable:
        hd.rectangle((0, 0, size, int(size * 0.55)), fill=(255, 255, 255, 22))
    else:
        hd.rounded_rectangle(
            (pad, pad, size - pad - 1, int(size * 0.55)),
            radius=r,
            fill=(255, 255, 255, 22),
        )
    img = Image.alpha_composite(img, hi)
    d = ImageDraw.Draw(img)

    # Safe content box (maskable keeps art in the center ~80%)
    cx, cy = size / 2, size / 2
    s = size * (0.72 if maskable else 0.78)

    # Building dimensions
    base_w = s * 0.62
    base_h = s * 0.48
    left = cx - base_w / 2
    right = cx + base_w / 2
    bottom = cy + s * 0.28
    top = bottom - base_h

    # Soft shadow under building
    sh = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.ellipse(
        (left + s * 0.02, bottom - s * 0.04, right + s * 0.06, bottom + s * 0.10),
        fill=SHADOW,
    )
    sh = sh.filter(ImageFilter.GaussianBlur(radius=max(2, size * 0.02)))
    img = Image.alpha_composite(img, sh)
    d = ImageDraw.Draw(img)

    # Pediment (triangle roof)
    ped_h = s * 0.18
    peak = (cx, top - ped_h)
    roof = [
        (left - s * 0.04, top + s * 0.02),
        peak,
        (right + s * 0.04, top + s * 0.02),
    ]
    d.polygon(roof, fill=COPPER)
    # Roof highlight edge
    d.line([roof[0], peak, roof[2]], fill=COPPER_LT, width=max(1, size // 180))

    # Letter J on a gold disc in the pediment
    disc_r = s * 0.09
    disc_c = (cx, top - ped_h * 0.38)
    d.ellipse(
        (disc_c[0] - disc_r, disc_c[1] - disc_r, disc_c[0] + disc_r, disc_c[1] + disc_r),
        fill=GOLD,
        outline=CREAM,
        width=max(1, size // 160),
    )
    font = load_font(max(12, int(s * 0.16)))
    j = "J"
    bbox = d.textbbox((0, 0), j, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(
        (disc_c[0] - tw / 2 - bbox[0], disc_c[1] - th / 2 - bbox[1] - size * 0.004),
        j,
        font=font,
        fill=NAVY_DEEP,
    )

    # Building body
    d.rounded_rectangle(
        (left, top, right, bottom),
        radius=max(2, int(size * 0.02)),
        fill=CREAM,
    )

    # Cornice line
    d.rectangle((left, top, right, top + s * 0.035), fill=STEP)

    # Four columns
    cols = 4
    inset = base_w * 0.10
    col_w = base_w * 0.08
    gap = (base_w - 2 * inset - cols * col_w) / (cols - 1)
    col_top = top + s * 0.08
    col_bot = bottom - s * 0.10
    for i in range(cols):
        x = left + inset + i * (col_w + gap)
        d.rounded_rectangle((x, col_top, x + col_w, col_bot), radius=max(1, size // 200), fill=NAVY)
        # capital
        d.rectangle((x - col_w * 0.18, col_top, x + col_w * 1.18, col_top + s * 0.03), fill=NAVY)
        # base
        d.rectangle((x - col_w * 0.18, col_bot - s * 0.03, x + col_w * 1.18, col_bot), fill=NAVY)

    # Door
    door_w = base_w * 0.16
    door_h = base_h * 0.32
    dx0 = cx - door_w / 2
    dy1 = bottom - s * 0.02
    dy0 = dy1 - door_h
    d.rounded_rectangle((dx0, dy0, dx0 + door_w, dy1), radius=max(1, int(door_w * 0.15)), fill=NAVY)
    # door window
    dw = door_w * 0.36
    d.ellipse((cx - dw / 2, dy0 + door_h * 0.18, cx + dw / 2, dy0 + door_h * 0.18 + dw), fill=WINDOW)

    # Steps
    for i, wmul in enumerate((0.70, 0.82, 0.94)):
        sl = cx - base_w * wmul / 2
        sr = cx + base_w * wmul / 2
        st = bottom + i * (s * 0.035)
        sb = st + s * 0.036
        d.rectangle((sl, st, sr, sb), fill=STEP if i % 2 == 0 else CREAM)
        d.line((sl, sb, sr, sb), fill=(180, 168, 145, 255), width=1)

    # Copper key, lower right, overlapping the building slightly
    kx = cx + s * 0.18
    ky = cy + s * 0.16
    key_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)
    # bow (handle)
    kr = s * 0.11
    kd.ellipse((kx - kr, ky - kr, kx + kr, ky + kr), outline=COPPER, width=max(3, int(s * 0.045)))
    kd.ellipse(
        (kx - kr * 0.42, ky - kr * 0.42, kx + kr * 0.42, ky + kr * 0.42),
        fill=(0, 0, 0, 0),
        outline=COPPER_LT,
        width=max(2, int(s * 0.02)),
    )
    # shaft
    shaft_w = max(3, int(s * 0.055))
    x1 = kx + kr * 0.85
    x2 = kx + s * 0.32
    ymid = ky
    kd.rectangle((x1, ymid - shaft_w / 2, x2, ymid + shaft_w / 2), fill=COPPER)
    # teeth
    tooth_h = s * 0.07
    tooth_w = s * 0.045
    kd.rectangle((x2 - tooth_w * 2.4, ymid + shaft_w / 2 - 1, x2 - tooth_w * 1.3, ymid + tooth_h), fill=COPPER)
    kd.rectangle((x2 - tooth_w * 0.95, ymid + shaft_w / 2 - 1, x2, ymid + tooth_h * 0.65), fill=COPPER)
    # highlight on shaft
    kd.rectangle((x1, ymid - shaft_w / 2, x2, ymid - shaft_w / 4), fill=COPPER_LT)

    # Rotate key slightly
    key_rot = key_img.rotate(-28, resample=Image.Resampling.BICUBIC, center=(kx, ky))
    img = Image.alpha_composite(img, key_rot)
    return img


def save_png(img, path, size):
    out = img.resize((size, size), Image.Resampling.LANCZOS)
    out.save(path, "PNG", optimize=True)
    print(f"wrote {path} {out.size}")


def main():
    master = draw_icon(1024, maskable=False)
    mask = draw_icon(1024, maskable=True)

    save_png(master, ICONS / "icon-512.png", 512)
    save_png(master, ICONS / "icon-192.png", 192)
    save_png(master, ICONS / "apple-touch-icon.png", 180)
    save_png(master, ICONS / "favicon.png", 32)
    save_png(mask, ICONS / "maskable-512.png", 512)
    # root copy used by some install paths
    save_png(master, ROOT / "icon-512.png", 512)

    # Multi-size ICO
    ico_sizes = [16, 24, 32, 48, 64, 128, 256]
    ico_images = [master.resize((s, s), Image.Resampling.LANCZOS) for s in ico_sizes]
    ico_path = ROOT / "icon.ico"
    ico_images[0].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=ico_images[1:],
    )
    # Also put a copy in icons/
    ico_images[0].save(
        ICONS / "icon.ico",
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=ico_images[1:],
    )
    print(f"wrote {ico_path} sizes={ico_sizes} bytes={ico_path.stat().st_size}")

    # Preview for QA
    master.save(ICONS / "_preview-1024.png", "PNG")


if __name__ == "__main__":
    main()
