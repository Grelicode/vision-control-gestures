"""Generuje docs/schemat.svg - schemat polaczen VisionControl (styl 'breadboard')."""
import sys

W, H = 1160, 900
out = []
a = out.append

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  'font-family="DejaVu Sans, Arial, sans-serif">')
a('''<defs>
<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
  <path d="M20 0H0V20" fill="none" stroke="#e4e4e4" stroke-width="1"/></pattern>
<pattern id="holes" width="12" height="12" patternUnits="userSpaceOnUse">
  <rect x="4" y="4" width="4" height="4" fill="#9a9a9a"/></pattern>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="#fafafa"/><rect width="{W}" height="{H}" fill="url(#grid)"/>')

# --- naglowek ---
a('<rect x="30" y="24" width="110" height="34" rx="6" fill="#fff" stroke="#ddd"/>'
  '<text x="85" y="47" text-anchor="middle" font-size="16" font-weight="bold" fill="#333">GreliCode</text>')
a('<text x="30" y="92" font-size="20" font-weight="bold" fill="#222">VisionControl – schemat połączeń</text>')
a('<text x="30" y="114" font-size="13" fill="#555">Arduino UNO R3 · LCD 16×2 (4-bit) · 6× LED · buzzer · potencjometr 10 kΩ</text>')

# --- plytka stykowa ---
BX0, BX1, BY0, BY1 = 40, 760, 200, 440
RP_T, RN_T = 214, 228          # gorne szyny: + / -
RN_B, RP_B = 412, 426          # dolne szyny: - / +
a(f'<rect x="{BX0}" y="{BY0}" width="{BX1-BX0}" height="{BY1-BY0}" rx="6" fill="#ededed" stroke="#c8c8c8"/>')
a(f'<rect x="{BX0+30}" y="{BY0+44}" width="{BX1-BX0-60}" height="62" fill="url(#holes)"/>')
a(f'<rect x="{BX0+30}" y="{BY0+124}" width="{BX1-BX0-60}" height="62" fill="url(#holes)"/>')
a(f'<rect x="{BX0+6}" y="{BY0+112}" width="{BX1-BX0-12}" height="8" fill="#d6d6d6"/>')
for y, col, sign in [(RP_T, '#d32f2f', '+'), (RN_T, '#1e63c6', '−'), (RN_B, '#1e63c6', '−'), (RP_B, '#d32f2f', '+')]:
    a(f'<line x1="{BX0+24}" y1="{y}" x2="{BX1-12}" y2="{y}" stroke="{col}" stroke-width="2"/>')
    a(f'<text x="{BX0+10}" y="{y+5}" font-size="14" font-weight="bold" fill="{col}">{sign}</text>')


def wire(pts, col, w=3.2):
    d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    a(f'<path d="{d}" fill="none" stroke="#00000033" stroke-width="{w+1.6}" stroke-linejoin="round"/>')
    a(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>')


def dot(x, y, col='#1a4fd6'):
    a(f'<circle cx="{x}" cy="{y}" r="3.6" fill="{col}"/>')


def resistor_v(x, y0, y1, label=None):
    a(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="#777" stroke-width="2"/>')
    m = (y0 + y1) / 2
    a(f'<rect x="{x-5}" y="{m-17}" width="10" height="34" rx="4" fill="#e8c99a" stroke="#a88655"/>')
    for i, c in enumerate(['#d32f2f', '#d32f2f', '#5d3a1a', '#c9a227']):
        a(f'<rect x="{x-5}" y="{m-12+i*7}" width="10" height="3" fill="{c}"/>')
    if label:
        a(f'<text x="{x+9}" y="{m+4}" font-size="10" fill="#2a62c9">{label}</text>')


# --- Arduino UNO ---
AX0, AY0, AX1, AY1 = 250, 560, 760, 830
a(f'<rect x="{AX0}" y="{AY0}" width="{AX1-AX0}" height="{AY1-AY0}" rx="14" fill="#1f7a96" stroke="#155a70" stroke-width="2"/>')
a(f'<rect x="{AX0-26}" y="{AY0+40}" width="66" height="56" rx="3" fill="#b8b8b8" stroke="#888"/>')  # USB
a(f'<rect x="{AX0-14}" y="{AY0+170}" width="54" height="50" rx="3" fill="#222"/>')                   # DC jack
a(f'<rect x="{AX0+170}" y="{AY0+150}" width="300" height="32" rx="3" fill="#222"/>')               # ATmega
a(f'<text x="{(AX0+AX1)//2+40}" y="{AY0+120}" text-anchor="middle" font-size="26" font-weight="bold" fill="#fff">Arduino UNO R3</text>')

dig = ['SCL', 'SDA', 'AREF', 'GND', '13', '12', '11', '10', '9', '8']
dig2 = ['7', '6', '5', '4', '3', '2', '1', '0']
P = {}
HY = AY0 + 18
a(f'<rect x="{AX0+142}" y="{HY-9}" width="{len(dig)*18+4}" height="18" fill="#111"/>')
a(f'<rect x="{AX0+344}" y="{HY-9}" width="{len(dig2)*18+4}" height="18" fill="#111"/>')
for i, n in enumerate(dig):
    x = AX0 + 153 + i * 18
    P['D' + n if n.isdigit() else n] = (x, HY)
for i, n in enumerate(dig2):
    x = AX0 + 355 + i * 18
    P['D' + n] = (x, HY)
bot = ['NC', 'IOREF', 'RESET', '3V3', '5V', 'GND', 'GND2', 'VIN']
ana = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']
BY = AY1 - 18
a(f'<rect x="{AX0+182}" y="{BY-9}" width="{len(bot)*18+4}" height="18" fill="#111"/>')
a(f'<rect x="{AX0+344}" y="{BY-9}" width="{len(ana)*18+4}" height="18" fill="#111"/>')
for i, n in enumerate(bot):
    P[n] = (AX0 + 193 + i * 18, BY)
for i, n in enumerate(ana):
    P[n] = (AX0 + 355 + i * 18, BY)
for name, (x, y) in P.items():
    a(f'<rect x="{x-3}" y="{y-3}" width="6" height="6" fill="#555"/>')
    lab = 'GND' if name == 'GND2' else name.replace('D', '') if name.startswith('D') else name
    if y == HY:
        a(f'<text transform="translate({x+4},{y+16}) rotate(-90)" text-anchor="end" font-size="10" fill="#fff">{lab}</text>')
    else:
        a(f'<text transform="translate({x+4},{y-14}) rotate(-90)" font-size="10" fill="#fff">{lab}</text>')
a(f'<text x="{AX0+250}" y="{HY+50}" font-size="11" fill="#cfe">DIGITAL (PWM~)</text>')
a(f'<text x="{AX0+210}" y="{BY-56}" font-size="11" fill="#cfe">POWER</text>'
  f'<text x="{AX0+370}" y="{BY-56}" font-size="11" fill="#cfe">ANALOG IN</text>')

# --- LEDy (kolejnosc jak na plytce: czerwone, zolte, zielone) ---
leds = [('D8', '#e53935'), ('D9', '#e53935'), ('D12', '#fdd835'), ('D13', '#fdd835'),
        ('D10', '#43a047'), ('D11', '#43a047')]
wire_cols = {'D8': '#ff8c1a', 'D9': '#f2c94c', 'D10': '#1a9e78', 'D11': '#f2f2f2',
             'D12': '#ff8c1a', 'D13': '#f2c94c'}
LX0 = 100
for i, (pin, col) in enumerate(leds):
    x = LX0 + i * 56
    an, ca = x, x + 14
    a(f'<line x1="{an}" y1="262" x2="{an}" y2="300" stroke="#888" stroke-width="2"/>')
    a(f'<line x1="{ca}" y1="262" x2="{ca}" y2="290" stroke="#888" stroke-width="2"/>')
    a(f'<path d="M{x-4},262 v-14 a11,11 0 0 1 22,0 v14 z" fill="{col}" stroke="#00000055"/>')
    a(f'<rect x="{x-6}" y="258" width="26" height="5" fill="{col}" stroke="#00000055"/>')
    a(f'<rect x="{x-9}" y="172" width="32" height="18" rx="3" fill="#fff" stroke="#bbb"/>')
    a(f'<text x="{x+7}" y="185" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">{pin}</text>')
    resistor_v(ca, 290, 392, '220Ω' if i == 5 else None)
    wire([(ca, 392), (ca, RN_B)], '#222', 2.6)
    dot(ca, RN_B)
    px, py = P[pin]
    lane = 520 - i * 9
    wire([(px, py), (px, lane), (an, lane), (an, 300)], wire_cols[pin])
    dot(an, 300)

# --- buzzer (D3) ---
BZX = 480
a(f'<circle cx="{BZX}" cy="262" r="30" fill="#1b1b1b"/><circle cx="{BZX}" cy="262" r="5" fill="#555"/>')
a(f'<rect x="{BZX-40}" y="172" width="80" height="18" rx="3" fill="#fff" stroke="#bbb"/>'
  f'<text x="{BZX}" y="185" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">buzzer D3</text>')
a(f'<text x="{BZX-14}" y="228" font-size="12" font-weight="bold" fill="#d32f2f">+</text>')
wire([(BZX - 10, 290), (BZX - 10, 340)], '#888', 2)
wire([(BZX + 10, 290), (BZX + 10, RN_B)], '#222', 2.6)
dot(BZX + 10, RN_B)
px, py = P['D3']
wire([(px, py), (px, 540), (BZX - 10, 540), (BZX - 10, 340)], '#1a9e78')
dot(BZX - 10, 340)

# --- potencjometr 10k (kontrast LCD) ---
PX = 600
a(f'<rect x="{PX-22}" y="244" width="44" height="40" rx="5" fill="#2f6fd6" stroke="#1d4ea0"/>'
  f'<circle cx="{PX}" cy="264" r="12" fill="#e9e9e9" stroke="#999"/><line x1="{PX}" y1="256" x2="{PX}" y2="272" stroke="#666" stroke-width="3"/>')
a(f'<text x="{PX}" y="238" text-anchor="middle" font-size="11" fill="#333">10 kΩ</text>')
for dx in (-14, 0, 14):
    a(f'<line x1="{PX+dx}" y1="284" x2="{PX+dx}" y2="300" stroke="#888" stroke-width="2"/>')
wire([(PX - 14, 300), (PX - 14, RP_B)], '#d32f2f', 2.6); dot(PX - 14, RP_B)
wire([(PX + 14, 300), (PX + 14, RN_B)], '#222', 2.6); dot(PX + 14, RN_B)

# --- LCD 16x2 ---
LCX0, LCY0, LCX1, LCY1 = 800, 140, 1130, 300
a(f'<rect x="{LCX0}" y="{LCY0}" width="{LCX1-LCX0}" height="{LCY1-LCY0}" rx="6" fill="#2e8b3a" stroke="#1d6127"/>')
a(f'<rect x="{LCX0+24}" y="{LCY0+18}" width="{LCX1-LCX0-48}" height="72" rx="3" fill="#111"/>')
a(f'<rect x="{LCX0+34}" y="{LCY0+26}" width="{LCX1-LCX0-68}" height="56" fill="#b5d334"/>')
a(f'<text x="{LCX0+46}" y="{LCY0+50}" font-family="DejaVu Sans Mono" font-size="17" fill="#2b3a07">TRYB: RUN</text>')
a(f'<text x="{LCX0+46}" y="{LCY0+74}" font-family="DejaVu Sans Mono" font-size="17" fill="#2b3a07">STARTY: 3</text>')
lcd_pins = ['VSS', 'VDD', 'V0', 'RS', 'RW', 'E', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'A', 'K']
L = {}
for i, n in enumerate(lcd_pins):
    x = LCX0 + 28 + i * 18
    L[n] = (x, LCY1)
    a(f'<circle cx="{x}" cy="{LCY1-10}" r="4" fill="#d9b44a"/>')
    a(f'<text transform="translate({x+4},{LCY1-18}) rotate(-90)" font-size="9" fill="#fff">{n}</text>')
a(f'<text x="{LCX1-6}" y="{LCY0-8}" text-anchor="end" font-size="11" fill="#333">LCD 16×2 (HD44780)</text>')

# zasilanie LCD -> szyny gornej czesci plytki
def to_rail(pin, rail_y, col):
    x, y = L[pin]
    wire([(x, y - 10), (x, y + 8 + lcd_pins.index(pin) * 0), ], col, 2.6)


ex = BX1 - 14   # koniec szyn
# VSS, RW, K -> GND ; VDD -> 5V ; A -> 220R -> 5V ; V0 -> potencjometr
def lcd_to(pin, lane_y, target, col):
    x, y = L[pin]
    wire([(x, y - 10), (x, lane_y), (target[0], lane_y), target], col, 2.6)


lcd_to('VSS', 318, (ex - 6, RN_T), '#222'); dot(ex - 6, RN_T)
lcd_to('VDD', 326, (ex - 20, RP_T), '#d32f2f'); dot(ex - 20, RP_T)
lcd_to('RW', 334, (ex - 34, RN_T), '#222'); dot(ex - 34, RN_T)
lcd_to('V0', 350, (PX, 300), '#1e63c6'); dot(PX, 300)
# A (podswietlenie) przez 220R do +5V
ax, ay = L['A']
resistor_v(ax, ay - 10, 372, None)
a(f'<text x="{ax-50}" y="{ay+40}" font-size="10" fill="#2a62c9">220Ω</text>')
wire([(ax, 372), (ax, 380), (ex - 48, 380), (ex - 48, RP_T)], '#d32f2f', 2.6); dot(ex - 48, RP_T)
kx, ky = L['K']
wire([(kx, ky - 10), (kx, 390), (ex - 62, 390), (ex - 62, RN_T)], '#222', 2.6); dot(ex - 62, RN_T)

# linie danych: RS,E,D4..D7 <- A0..A5
data = [('RS', 'A0', '#1e63c6'), ('E', 'A1', '#d32f2f'), ('D4', 'A2', '#1e63c6'),
        ('D5', 'A3', '#1e63c6'), ('D6', 'A4', '#d32f2f'), ('D7', 'A5', '#f2f2f2')]
for k, (lp, ap, col) in enumerate(data):
    lx, ly = L[lp]
    px, py = P[ap]
    yb = 850 + k * 7
    xr = 1060 + k * 12 if lp not in ('RS', 'E') else 1060 + k * 12
    up = 462 - k * 8
    wire([(px, py), (px, yb), (xr, yb), (xr, up), (lx, up), (lx, ly - 10)], col)

# polaczenie szyn gornych z dolnymi (zworki po lewej)
wire([(BX0 + 30, RP_T), (BX0 + 30, RP_B)], '#d32f2f', 2.6)
wire([(BX0 + 44, RN_T), (BX0 + 44, RN_B)], '#222', 2.6)
for p in [(BX0 + 30, RP_T), (BX0 + 30, RP_B), (BX0 + 44, RN_T), (BX0 + 44, RN_B)]:
    dot(*p)

# zasilanie z Arduino -> dolne szyny
x5, y5 = P['5V']; xg, yg = P['GND']
wire([(x5, y5), (x5, 878), (22, 878), (22, 470), (BX0 + 70, 470), (BX0 + 70, RP_B)], '#d32f2f')
wire([(xg, yg), (xg, 870), (30, 870), (30, 478), (BX0 + 84, 478), (BX0 + 84, RN_B)], '#222')
dot(BX0 + 70, RP_B); dot(BX0 + 84, RN_B)

a('</svg>')
open(sys.argv[1], 'w').write('\n'.join(out))
