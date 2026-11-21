#!/usr/bin/env python3
"""Draw an invented passport spread for the Republic of Aerthwaite.

Pure Python 3.13 standard library only. A tiny rasterizer draws the spread
onto an RGB canvas, then a hand-rolled PNG encoder (zlib + struct) writes
/output/entry.png. Fully deterministic: the same bytes every run.
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- PNG encoder

def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, rgb, w, h):
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    raw = b"".join(b"\x00" + rgb[y * w * 3:(y + 1) * w * 3] for y in range(h))
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(raw, 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 bits, most significant bit on the left.

FONT = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0, 0, 0, 0, 0, 0, 0),
    "-": (0, 0, 0, 0x0E, 0, 0, 0),
    "<": (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    ">": (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
    "/": (0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10),
    ".": (0, 0, 0, 0, 0, 0, 0x0C),
    ",": (0, 0, 0, 0, 0, 0x04, 0x08),
    ":": (0, 0x0C, 0, 0, 0, 0x0C, 0),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "+": (0, 0x04, 0x04, 0x0E, 0x04, 0x04, 0),
    "*": (0, 0x15, 0x0E, 0x1F, 0x0E, 0x15, 0),
    "%": (0x19, 0x1A, 0x02, 0x04, 0x08, 0x0B, 0x13),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x06, 0x04, 0, 0x04),
    "=": (0, 0, 0x1F, 0, 0x1F, 0, 0),
    "_": (0, 0, 0, 0, 0, 0, 0x1F),
    '"': (0x0A, 0x0A, 0, 0, 0, 0, 0),
}


def text_width(s, scale):
    return len(s) * 6 * scale - scale


# ---------------------------------------------------------------- canvas

class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = c

    def fill_rect(self, x0, y0, x1, y1, c):
        x0 = max(0, x0); y0 = max(0, y0)
        x1 = min(self.w, x1); y1 = min(self.h, y1)
        for y in range(y0, y1):
            i = (y * self.w + x0) * 3
            self.px[i:(y * self.w + x1) * 3] = bytes(c) * (x1 - x0)

    def rect(self, x0, y0, x1, y1, c, t=1):
        self.fill_rect(x0, y0, x1, y0 + t, c)
        self.fill_rect(x0, y1 - t, x1, y1, c)
        self.fill_rect(x0, y0, x0 + t, y1, c)
        self.fill_rect(x1 - t, y0, x1, y1, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x + a, y + b, c)
            if x == x1 and y == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy; x += sx
            if e2 < dx:
                err += dx; y += sy

    def circle(self, cx, cy, r, c, t=1, fill=False):
        x, y, d = 0, r, 3 - 2 * r
        while x <= y:
            pts = [(cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y),
                   (cx - x, cy - y), (cx + y, cy + x), (cx - y, cy + x),
                   (cx + y, cy - x), (cx - y, cy - x)]
            if fill:
                for yy in range(cy - y, cy + y + 1):
                    self.line(cx - x, yy, cx + x, yy, c)
                for yy in range(cy - x, cy + x + 1):
                    self.line(cx - y, yy, cx + y, yy, c)
            else:
                for px, py in pts:
                    for a in range(t):
                        for b in range(t):
                            self.set(px + a, py + b, c)
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1

    def ellipse(self, cx, cy, rx, ry, c):
        for yy in range(cy - ry, cy + ry + 1):
            t = 1.0 - ((yy - cy) / ry) ** 2
            if t < 0:
                continue
            dx = int(rx * (t ** 0.5))
            self.line(cx - dx, yy, cx + dx, yy, c)

    def poly(self, pts, c):
        # Scanline fill of a simple polygon.
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.line(int(xs[i]), y, int(xs[i + 1]), y, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            g = FONT.get(ch.upper(), FONT[" "])
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       cx + (col + 1) * scale,
                                       y + (row + 1) * scale, c)
            cx += 6 * scale

    def centred(self, cx, y, s, scale, c):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, c)

# ---------------------------------------------------------------- palette

DESK = bytes((34, 52, 60))
SHADOW = bytes((18, 30, 36))
PAPER = bytes((244, 236, 217))
PAPER2 = bytes((238, 228, 204))
INK = bytes((31, 42, 51))
TEAL = bytes((30, 90, 107))
GOLD = bytes((176, 141, 62))
RED = bytes((163, 59, 50))
BLUE = bytes((44, 79, 138))
PHOTO_BG = bytes((178, 198, 210))
SLATE = bytes((52, 74, 92))
FAINT = bytes((110, 96, 74))


def draw_spread(cv):
    cv.fill_rect(0, 0, W, H, DESK)
    # Page shadows, then the two cream pages.
    cv.fill_rect(42, 116, 502, 876, SHADOW)
    cv.fill_rect(534, 116, 994, 876, SHADOW)
    cv.fill_rect(36, 110, 496, 870, PAPER)
    cv.fill_rect(528, 110, 988, 870, PAPER)
    cv.fill_rect(508, 110, 516, 870, bytes((210, 196, 168)))
    draw_data_page(cv)
    draw_visa_page(cv)


def draw_data_page(cv):
    cx = 266
    cv.centred(cx, 140, "REPUBLIC OF AERTHWAITE", 2, TEAL)
    cv.centred(cx, 168, "PASSPORT", 4, INK)
    cv.line(76, 202, 456, 202, GOLD, 2)
    cv.line(76, 208, 456, 208, GOLD, 1)
    # Small flag: teal / white / gold bands with a cloud dot.
    cv.fill_rect(396, 226, 456, 236, TEAL)
    cv.fill_rect(396, 236, 456, 246, bytes((250, 248, 240)))
    cv.fill_rect(396, 246, 456, 258, GOLD)
    cv.circle(426, 241, 6, bytes((255, 255, 255)), fill=True)
    cv.rect(396, 226, 456, 258, INK, 1)
    cv.text(76, 232, "TYPE P  CODE AER", 2, INK)
    cv.text(76, 256, "NO  AW202600417", 2, INK)
    # Portrait box.
    cv.fill_rect(76, 290, 216, 470, PHOTO_BG)
    cv.rect(76, 290, 216, 470, INK, 2)
    for yy in range(300, 460, 12):
        cv.line(78, yy, 214, yy, bytes((160, 182, 196)), 1)
    cv.circle(146, 358, 28, SLATE, fill=True)
    cv.ellipse(146, 438, 50, 26, SLATE)
    cv.rect(76, 290, 216, 470, INK, 2)
    # Fields beside the portrait.
    fields = [
        ("SURNAME", "VESSEL"),
        ("GIVEN NAMES", "MARA ELLIN"),
        ("NATIONALITY", "AERTHWAITE"),
        ("DATE OF BIRTH", "14 FEB 1994"),
        ("PLACE OF BIRTH", "CIRRUS TERRACE"),
        ("DATE OF ISSUE", "12 MAR 2026"),
        ("DATE OF EXPIRY", "12 MAR 2036"),
    ]
    y = 292
    for label, value in fields:
        cv.text(236, y, label, 2, TEAL)
        cv.text(236, y + 15, value, 2, INK)
        y += 40
    cv.text(76, 486, "SEX F", 2, INK)
    # Signature squiggle.
    import math
    for i in range(120):
        sx = 76 + i
        sy = 566 + int(4 * math.sin(i / 9.0))
        cv.set(sx, sy, INK)
        cv.set(sx, sy + 1, INK)
    cv.line(76, 580, 216, 580, INK, 1)
    cv.text(76, 588, "HOLDER'S SIGNATURE", 2, FAINT)
    # Machine-readable zone.
    cv.fill_rect(76, 768, 456, 832, PAPER2)
    cv.text(76, 776, "P<AERVESSEL<<MARA<ELLIN<<<<<<<", 2, INK)
    cv.text(76, 802, "AW202600417AER9402148F3603122<08", 2, INK)


def draw_visa_page(cv):
    cx = 758
    cv.centred(cx, 140, "VISAS", 3, TEAL)
    cv.line(568, 172, 948, 172, GOLD, 2)
    cv.line(568, 178, 948, 178, GOLD, 1)
    # Arrival stamp, Port Zenith.
    cv.rect(592, 210, 924, 330, BLUE, 3)
    cv.centred(cx, 226, "ARRIVAL", 3, BLUE)
    cv.centred(cx, 262, "PORT ZENITH", 2, BLUE)
    cv.centred(cx, 288, "04 JUN 2026", 2, BLUE)
    cv.circle(872, 246, 36, BLUE, t=2)
    cv.text(856, 232, "04 JUN", 1, BLUE)
    cv.text(862, 244, "2026", 1, BLUE)
    # Visa stamp: the impossible condition.
    cv.rect(592, 360, 924, 520, RED, 3)
    cv.centred(cx, 378, "VISA - CLASS CLOUD", 3, RED)
    cv.centred(cx, 414, "VALID ONLY WHEN CLOUD BASE", 2, RED)
    cv.centred(cx, 438, "ABOVE 2,000 M", 2, RED)
    cv.centred(cx, 468, "FEE: 3 SONGS - PAID", 2, RED)
    # Departure stamp, Lowlandia.
    cv.rect(592, 550, 924, 660, TEAL, 3)
    cv.centred(cx, 568, "DEPARTURE", 3, TEAL)
    cv.centred(cx, 602, "LOWLANDIA", 2, TEAL)
    cv.centred(cx, 628, "18 JUN 2026", 2, TEAL)
    # Notes box.
    cv.rect(592, 690, 924, 840, GOLD, 2)
    cv.text(616, 706, "NOTES", 2, TEAL)
    cv.text(616, 736, "HOLDER IS ADVISED NOT TO", 2, INK)
    cv.text(616, 760, "DESCEND BELOW CLOUD LEVEL.", 2, INK)
    cv.text(616, 790, "LANGUAGES: AERTH,", 2, INK)
    cv.text(616, 814, "ENGLISH, WIND", 2, INK)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = Canvas(W, H, DESK)
    draw_spread(cv)
    write_png(os.path.join(out_dir, "entry.png"), cv.px, W, H)


if __name__ == "__main__":
    main()
