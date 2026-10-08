"""Inline SVG: logo, UI icons, service icons and the animated service illustrations."""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_vb, _blue, _grey = open(os.path.join(_HERE, "logo-paths.txt")).read().split("\n")[:3]

LOGO_SYMBOL = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="logo" viewBox="%s">'
        '<path style="fill:var(--logo-b,#2A5598)" fill-rule="evenodd" d="%s"/><path style="fill:var(--logo-s,#9AA0AC)" fill-rule="evenodd" d="%s"/></symbol></svg>') % (_vb, _blue, _grey)
LOGO = '<svg class="logo" viewBox="%s" role="img" aria-label="BlueTech Sanitaire"><use href="#logo"/></svg>' % _vb


def i(d, cls="ic", vb="0 0 24 24"):
    return '<svg class="%s" viewBox="%s" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % (cls, vb, d)


ARROW = i('<path d="M4 12h15M13 6l6 6-6 6"/>')
ARROW_UR = i('<path d="M7 17 17 7M8 7h9v9"/>')
PHONE = i('<path d="M5 3.5h3.2l1.6 4.2-2.1 1.4a11.5 11.5 0 0 0 5.2 5.2l1.4-2.1 4.2 1.6V17a2.5 2.5 0 0 1-2.5 2.5A15.5 15.5 0 0 1 2.5 6 2.5 2.5 0 0 1 5 3.5Z"/>')
MAIL = i('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>')
PIN = i('<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/>')
PLUS = i('<path d="M12 5v14M5 12h14"/>')
CLOSE = i('<path d="M6 6l12 12M18 6 6 18"/>')
CHECK = i('<path d="m5 12.5 4.2 4L19 7"/>')
CHEV = i('<path d="m6 9 6 6 6-6"/>')
LEFT = i('<path d="M15 5l-7 7 7 7"/>')
RIGHT = i('<path d="m9 5 7 7-7 7"/>')
WA = ('<svg class="ic ic--wa" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Zm0 18.15c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 4.54 0 8.24 3.7 8.24 8.24 0 4.55-3.7 8.24-8.24 8.24Zm4.52-6.16c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.13-.17.24-.64.8-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28Z"/></svg>')
GOOGLE = ('<svg class="g-logo" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.4-.4-3.5Z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7Z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44Z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5Z"/></svg>')
STAR = '<svg class="star" viewBox="0 0 20 20" aria-hidden="true"><path fill="currentColor" d="m10 1.6 2.6 5.3 5.8.8-4.2 4.1 1 5.8L10 14.9l-5.2 2.7 1-5.8L1.6 7.7l5.8-.8L10 1.6Z"/></svg>'
STARS = '<span class="stars" aria-label="5 étoiles sur 5">' + STAR * 5 + '</span>'

# service icons (24px line)
SICON = {
    "install": i('<path d="M3 8.5h6.5a3 3 0 0 1 3 3V21"/><path d="M3 4.5h6.5a7 7 0 0 1 7 7V21"/><path d="M2.5 3.5v6M11.5 16.5h6M16.5 3l4 4M18.5 5l-2.8 2.8"/>'),
    "shower": i('<path d="M5 21V8a4 4 0 0 1 4-4h1a4 4 0 0 1 4 4"/><path d="M10 8h8"/><path d="M11 12v.5M14 12v.5M17 12v.5M12 15.5v.5M15.5 15.5v.5M13.5 19v.5M17 19v.5"/>'),
    "radiator": i('<rect x="3.5" y="6" width="17" height="12" rx="1.5"/><path d="M7.5 6v12M11.5 6v12M15.5 6v12M3.5 20.5h2M18.5 20.5h2M5 3c.8.8.8 1.7 0 2.5M12 3c.8.8.8 1.7 0 2.5M19 3c.8.8.8 1.7 0 2.5"/>'),
    "tap": i('<path d="M4 9h9a5 5 0 0 1 5 5v1"/><path d="M4 5v8M8 9V6M6 6h4"/><path d="M18 18.5c0 1.1-.7 2-1.6 2s-1.6-.9-1.6-2c0-1 1.6-2.8 1.6-2.8s1.6 1.8 1.6 2.8Z"/>'),
    "gauge": i('<circle cx="12" cy="13" r="8"/><path d="M12 13l4-4M7.5 13h1M12 7.5v1M15.5 16.5h1"/><path d="M10 3h4M12 3v2"/>'),
    "boiler": i('<rect x="6" y="2.5" width="12" height="19" rx="6"/><path d="M9.5 15.5c.8-.8 1.7-.8 2.5 0s1.7.8 2.5 0M12 7v5"/><circle cx="12" cy="12.5" r="1"/>'),
}

# ---------------------------------------------------------------- service illustrations
# All 480x480, technical-drawing style. .d = drawn on scroll, .fl = flowing water, .an = mono annotation.

def _dim(x1, y1, x2, y2, label, tx, ty, anchor="middle"):
    return ('<g class="dim"><path d="M%s %sL%s %s"/><path class="dim__t" d="M%s %sl0 0"/>'
            '<text x="%s" y="%s" text-anchor="%s">%s</text></g>') % (x1, y1, x2, y2, x1, y1, tx, ty, anchor, label)


ART = {}

ART["install"] = '''
<svg class="art" viewBox="0 0 480 480" aria-hidden="true">
 <g class="grid-ax"><path d="M240 30V460"/><path d="M40 330H450"/></g>
 <text class="an an--ax" x="246" y="44">AXE WC</text>
 <g class="d frame"><path d="M150 70V420M330 70V420M150 70H330M150 420H330M150 260H330M150 300H330"/><path d="M160 420v22M320 420v22M140 442h40M300 442h40"/></g>
 <g class="d"><rect x="176" y="96" width="128" height="148" rx="10"/><path d="M196 118h88v26h-88z"/></g>
 <clipPath id="cist"><rect x="177" y="97" width="126" height="146" rx="9"/></clipPath>
 <g clip-path="url(#cist)"><rect class="flush" x="170" y="150" width="140" height="100"/></g>
 <g class="d"><path d="M240 244v52"/><path d="M226 296h28l-4 34h-20z"/></g>
 <path class="d pipe" d="M240 330v40a30 30 0 0 0 30 30h190"/>
 <path class="fl fl--drain" d="M240 332v38a30 30 0 0 0 30 30h190"/>
 <path class="d pipe pipe--c" d="M20 170h156"/>
 <path class="fl fl--c" d="M20 170h156"/>
 <path class="d ghost" d="M190 330c0-8 6-12 14-12h72c8 0 14 4 14 12v6c0 26-22 44-50 44s-50-18-50-44z"/>
 <text class="an" x="24" y="160">ALIMENTATION EF Ø 16</text>
 <text class="an" x="350" y="392">ÉVACUATION PE Ø 90</text>
 <text class="an" x="342" y="120">BÂTI-SUPPORT</text><path class="lead" d="M340 116h-10"/>
 <g class="dim dim--v"><path d="M110 70V420"/><path d="M104 70h12M104 420h12"/><text x="100" y="250" transform="rotate(-90 100 250)" text-anchor="middle">H 112 cm</text></g>
</svg>'''

ART["shower"] = '''
<svg class="art" viewBox="0 0 480 480" aria-hidden="true">
 <g class="grid-ax"><path d="M30 420H450"/><path d="M250 20V430"/></g>
 <path class="d" d="M60 30V420"/>
 <path class="d" d="M60 70h150a20 20 0 0 1 20 20v18"/>
 <g class="d"><path d="M180 112h140"/><rect x="190" y="108" width="120" height="10" rx="5"/></g>
 <g class="drops">
  <path d="M205 132v14M225 140v14M245 130v14M265 142v14M285 134v14M300 146v14M215 176v14M235 186v14M255 172v14M275 184v14M295 176v14M210 222v14M230 230v14M250 218v14M270 228v14M290 220v14M220 268v14M240 276v14M260 266v14M280 274v14M300 270v14M212 318v14M232 326v14M252 314v14M272 322v14M292 318v14M224 362v14M244 370v14M264 360v14M284 368v14"/>
 </g>
 <g class="d"><circle cx="60" cy="250" r="22"/><path d="M60 228v-8M60 272v8M38 250h-8M82 250h8"/><path d="M60 250l12-10"/></g>
 <path class="d pipe pipe--c" d="M20 300h22v-28"/><path class="fl fl--c" d="M20 300h22v-28"/>
 <path class="d pipe pipe--h" d="M20 214h22v14"/><path class="fl fl--h" d="M20 214h22v14"/>
 <path class="d" d="M60 420h390"/>
 <g class="d"><path d="M330 420v-8h50v8"/><path d="M335 415h40"/></g>
 <path class="d glass" d="M430 120V420"/>
 <g class="dim"><path d="M120 440l200 -12"/><path d="M314 424l6 4-6 5"/><text x="210" y="460" text-anchor="middle">PENTE 2 %</text></g>
 <text class="an" x="96" y="256">MITIGEUR THERMOSTATIQUE</text>
 <text class="an" x="236" y="100">PLUIE Ø 300</text>
 <text class="an" x="318" y="400">CANIVEAU</text>
 <text class="an an--ax" x="256" y="36">AXE DOUCHE</text>
</svg>'''

ART["radiator"] = '''
<svg class="art" viewBox="0 0 480 480" aria-hidden="true">
 <g class="grid-ax"><path d="M30 400H450"/></g>
 <g class="heat"><path d="M120 150c-12-16 12-28 0-44s12-28 0-44"/><path d="M180 150c-12-16 12-28 0-44s12-28 0-44"/><path d="M240 150c-12-16 12-28 0-44s12-28 0-44"/><path d="M300 150c-12-16 12-28 0-44s12-28 0-44"/></g>
 <g class="d"><rect x="80" y="170" width="260" height="170" rx="10"/><path d="M112 170v170M144 170v170M176 170v170M208 170v170M240 170v170M272 170v170M304 170v170"/></g>
 <g class="d"><path d="M340 200h22"/><rect x="362" y="184" width="26" height="40" rx="8"/><path d="M368 196h14M368 204h14M368 212h14"/></g>
 <path class="d pipe pipe--h" d="M100 340v60H20"/><path class="fl fl--h" d="M100 342v58H20"/>
 <path class="d pipe pipe--r" d="M320 340v40h130"/><path class="fl fl--r" d="M320 342v38h130"/>
 <text class="an" x="24" y="420">ALLER 55 °C</text>
 <text class="an" x="368" y="372">RETOUR</text>
 <text class="an" x="364" y="246">VANNE THERMO.</text>
 <g class="thermo"><rect class="d" x="410" y="60" width="18" height="110" rx="9"/><circle class="d" cx="419" cy="182" r="14"/><rect class="thermo__fill" x="414" y="70" width="8" height="112" rx="4"/><text class="an" x="398" y="50" text-anchor="middle"><tspan class="thermo__val">21</tspan> °C</text></g>
</svg>'''

ART["tap"] = '''
<svg class="art" viewBox="0 0 480 480" aria-hidden="true">
 <g class="grid-ax"><path d="M30 440H450"/><path d="M290 30V440"/></g>
 <path class="d" d="M60 30V440"/>
 <g class="d"><path d="M60 150h70"/><rect x="130" y="128" width="54" height="44" rx="8"/><path d="M184 142h70a36 36 0 0 1 36 36v18"/><path d="M184 158h62a28 28 0 0 1 28 28v10"/><path d="M270 196h40"/></g>
 <g class="d"><path d="M157 128V92"/><rect x="132" y="80" width="50" height="12" rx="6"/></g>
 <g class="drip"><path class="drip__drop" d="M290 206c0 0-9 12-9 18a9 9 0 0 0 18 0c0-6-9-18-9-18z"/></g>
 <g class="splash"><ellipse cx="290" cy="420" rx="40" ry="6"/><ellipse cx="290" cy="420" rx="70" ry="10"/></g>
 <path class="d" d="M200 420h180"/>
 <g class="wrench"><path class="d" d="M380 250l-60 60a14 14 0 0 1-20-20l60-60a30 30 0 0 1 36-40l-18 18 4 16 16 4 18-18a30 30 0 0 1-36 40z"/></g>
 <path class="d pipe pipe--c" d="M20 236h40"/><path class="fl fl--c" d="M20 236h40"/>
 <text class="an" x="70" y="226">VANNE D’ARRÊT</text>
 <text class="an" x="196" y="118">JOINT · CARTOUCHE</text>
 <text class="an an--hot" x="306" y="236">FUITE</text>
</svg>'''

ART["gauge"] = '''
<svg class="art" viewBox="0 0 480 480" aria-hidden="true">
 <g class="d"><circle cx="190" cy="210" r="130"/><circle cx="190" cy="210" r="112"/></g>
 <g class="ticks">''' + "".join(
    '<path d="M%.1f %.1fL%.1f %.1f"/>' % (
        190 + 104 * __import__("math").cos(__import__("math").radians(135 + k * 27)),
        210 + 104 * __import__("math").sin(__import__("math").radians(135 + k * 27)),
        190 + (88 if k % 2 == 0 else 96) * __import__("math").cos(__import__("math").radians(135 + k * 27)),
        210 + (88 if k % 2 == 0 else 96) * __import__("math").sin(__import__("math").radians(135 + k * 27)))
    for k in range(11)) + '''</g>
 <path class="zone-ok" d="M%s"/>
 <g class="needle"><path d="M190 210L190 118" /><circle cx="190" cy="210" r="10"/></g>
 <text class="an" x="190" y="290" text-anchor="middle">BAR</text>
 <g class="d"><path d="M190 340v40h-60"/><path d="M110 372h20v16h-20z"/></g>
 <path class="d pipe pipe--c" d="M20 380h90"/><path class="fl fl--c" d="M20 380h90"/>
 <g class="checks">
  <g><path class="ck" d="M350 132l8 8 16-16"/><text class="an" x="384" y="138">PRESSION</text></g>
  <g><path class="ck" d="M350 192l8 8 16-16"/><text class="an" x="384" y="198">ROBINETS</text></g>
  <g><path class="ck" d="M350 252l8 8 16-16"/><text class="an" x="384" y="258">BOILER</text></g>
  <g><path class="ck" d="M350 312l8 8 16-16"/><text class="an" x="384" y="318">ÉCOULEMENTS</text></g>
 </g>
</svg>'''

import math as _m
def _arc(cx, cy, r, a0, a1):
    x0, y0 = cx + r * _m.cos(_m.radians(a0)), cy + r * _m.sin(_m.radians(a0))
    x1, y1 = cx + r * _m.cos(_m.radians(a1)), cy + r * _m.sin(_m.radians(a1))
    return "%.1f %.1fA%s %s 0 0 1 %.1f %.1f" % (x0, y0, r, r, x1, y1)
ART["gauge"] = ART["gauge"].replace('d="M%s"', 'd="M%s"' % _arc(190, 210, 100, 135 + 4 * 27, 135 + 7 * 27))

ART["boiler"] = '''
<svg class="art" viewBox="0 0 480 480" aria-hidden="true">
 <defs><linearGradient id="bgrad" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#3D8BFF"/><stop offset=".55" stop-color="#8C7CF0"/><stop offset="1" stop-color="#F0603F"/></linearGradient>
 <clipPath id="tank"><rect x="152" y="62" width="176" height="356" rx="86"/></clipPath></defs>
 <g clip-path="url(#tank)"><rect class="boil" x="150" y="60" width="180" height="360" fill="url(#bgrad)"/></g>
 <g class="d"><rect x="150" y="60" width="180" height="360" rx="88"/><rect x="138" y="48" width="204" height="384" rx="100" class="ghost"/></g>
 <g class="d element"><path d="M180 390h20l10-16 10 32 10-32 10 32 10-32 10 32 10-16h20"/></g>
 <path class="d pipe pipe--c" d="M20 400h130"/><path class="fl fl--c" d="M20 400h130"/>
 <path class="d pipe pipe--h" d="M330 100h130"/><path class="fl fl--h" d="M330 100h130"/>
 <g class="d"><rect x="66" y="384" width="36" height="32" rx="4"/><path d="M84 384v-16M76 368h16"/></g>
 <text class="an" x="24" y="440">EAU FROIDE</text><text class="an" x="56" y="356">GROUPE DE SÉCURITÉ</text>
 <text class="an" x="350" y="88">EAU CHAUDE</text>
 <g class="dial"><circle class="d" cx="400" cy="250" r="34"/><text class="an an--big" x="400" y="258" text-anchor="middle"><tspan class="boil__val">60</tspan>°</text></g>
 <path class="lead" d="M330 250h36"/>
</svg>'''

# decorative pipe run for inner page heroes
ART["run"] = '''
<svg class="art art--run" viewBox="0 0 640 420" aria-hidden="true">
 <g class="grid-ax"><path d="M330 10V410"/><path d="M10 300H630"/></g>
 <path class="d pipe pipe--c" d="M640 90H400a50 50 0 0 0-50 50v110a50 50 0 0 1-50 50H40"/>
 <path class="fl fl--c" d="M640 90H400a50 50 0 0 0-50 50v110a50 50 0 0 1-50 50H40"/>
 <g class="d"><rect x="388" y="74" width="16" height="32" rx="3"/><rect x="334" y="128" width="32" height="16" rx="3"/><rect x="334" y="238" width="32" height="16" rx="3"/><rect x="296" y="284" width="16" height="32" rx="3"/></g>
 <g class="d"><circle cx="350" cy="195" r="20"/><path d="M350 175v-22M330 153h40"/></g>
 <g class="d"><path d="M520 90V52"/><circle cx="520" cy="30" r="22"/><path d="M520 30l11-9"/></g>
 <g class="d"><path d="M150 300v70M134 370h32"/><path d="M200 300v70M184 370h32"/></g>
 <text class="an" x="556" y="34">P 3,0 bar</text>
 <text class="an" x="380" y="200">VANNE D’ARRÊT</text>
 <text class="an" x="440" y="124">PE-X Ø 20 · EF</text>
 <text class="an an--ax" x="336" y="24">AXE</text>
 <text class="an" x="60" y="340">DÉPARTS</text>
</svg>'''
