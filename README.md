
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">
  <defs>
    <radialGradient id="bg">
      <stop offset="0" stop-color="#39204e"/>
      <stop offset=".55" stop-color="#17152f"/>
      <stop offset="1" stop-color="#080b18"/>
    </radialGradient>
    <radialGradient id="light">
      <stop offset="0" stop-color="#fff" stop-opacity=".9"/>
      <stop offset=".25" stop-color="#e5b8ff" stop-opacity=".5"/>
      <stop offset="1" stop-color="#b66cff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#fff1ff"/>
      <stop offset=".45" stop-color="#c18aff"/>
      <stop offset="1" stop-color="#ff9ecb"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="7" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .portal {
        transform-origin:600px 270px;
        animation: spin 12s linear infinite;
      }
      .pulse { animation: pulse 3s ease-in-out infinite; }
      .gem {
        transform-box:fill-box;
        transform-origin:center;
        animation: gemGlow 2s ease-in-out infinite alternate;
      }
      .scene {
        opacity:0;
        animation: appear 16s infinite;
      }
      .s1 { animation-delay:0s; }
      .s2 { animation-delay:4s; }
      .s3 { animation-delay:8s; }
      .s4 { animation-delay:12s; }
      @keyframes spin { to { transform:rotate(360deg); } }
      @keyframes pulse {
        0%,100% { opacity:.35; transform:scale(.94); }
        50% { opacity:.9; transform:scale(1.06); }
      }
      @keyframes gemGlow {
        from { filter:drop-shadow(0 0 3px #fff); }
        to { filter:drop-shadow(0 0 14px #e7aaff); }
      }
      @keyframes appear {
        0%,5% { opacity:0; transform:translateY(22px) scale(.88); }
        12%,20% { opacity:1; transform:translateY(0) scale(1); }
        25%,100% { opacity:0; transform:translateY(-18px) scale(1.06); }
      }
    </style>
  </defs>

  <rect width="1200" height="600" fill="url(#bg)"/>

  <g fill="#fff">
    <circle cx="90" cy="90" r="2"/><circle cx="190" cy="230" r="1.5"/>
    <circle cx="300" cy="75" r="2"/><circle cx="430" cy="180" r="1.5"/>
    <circle cx="800" cy="85" r="2"/><circle cx="990" cy="150" r="1.5"/>
    <circle cx="1100" cy="90" r="2"/><circle cx="1060" cy="420" r="1.5"/>
    <circle cx="140" cy="440" r="2"/><circle cx="350" cy="500" r="1.5"/>
    <circle cx="870" cy="480" r="2"/><circle cx="720" cy="120" r="1.5"/>
  </g>

  <ellipse cx="600" cy="265" rx="430" ry="260" fill="url(#light)" class="pulse"/>

  <g class="portal" fill="none" stroke="url(#ring)" filter="url(#glow)">
    <ellipse cx="600" cy="270" rx="240" ry="190" stroke-width="3"/>
    <ellipse cx="600" cy="270" rx="210" ry="165" stroke-width="1.5" stroke-dasharray="12 15"/>
    <ellipse cx="600" cy="270" rx="175" ry="135" stroke-width="1" stroke-dasharray="4 12"/>
  </g>

  <g fill="none" stroke="#f7dfff" opacity=".7">
    <path d="M600 35V100 M600 440V505 M350 270H420 M780 270H850"/>
    <path d="M420 90L465 135 M735 405L780 450 M420 450L465 405 M735 135L780 90"/>
  </g>

  <!-- AMETHYST -->
  <g class="scene s1">
    <ellipse cx="600" cy="270" rx="130" ry="155" fill="#b47aff" opacity=".12" filter="url(#glow)"/>
    <path d="M545 190 Q500 205 510 290 L530 365 L565 345 L580 390 L620 390 L640 345 L680 365 L690 270 Q700 200 650 185Z" fill="#7139a1" stroke="#e8c7ff" stroke-width="3"/>
    <path d="M550 195 Q600 140 660 195 L675 250 Q630 225 600 250 Q560 225 525 260Z" fill="#eee0ff"/>
    <path d="M560 250 Q600 235 640 250 L650 315 Q600 350 550 315Z" fill="#d8a5ff"/>
    <path d="M585 270 L615 270" stroke="#44235f" stroke-width="5" stroke-linecap="round"/>
    <path d="M580 300 Q600 315 620 300" fill="none" stroke="#44235f" stroke-width="4"/>
    <path class="gem" d="M600 350 L615 365 L600 380 L585 365Z" fill="#d9b2ff" stroke="#fff" stroke-width="2"/>
    <text x="600" y="455" fill="#e7c5ff" font-size="22" letter-spacing="7" text-anchor="middle">AMETHYST</text>
  </g>

  <!-- STEVEN -->
  <g class="scene s2">
    <ellipse cx="600" cy="270" rx="130" ry="155" fill="#ff9db9" opacity=".14" filter="url(#glow)"/>
    <path d="M535 205 Q535 145 600 150 Q665 145 665 205 L680 350 L520 350Z" fill="#4a253b" stroke="#ffc4d7" stroke-width="3"/>
    <path d="M550 205 Q555 155 600 160 Q650 155 650 205 L650 270 L550 270Z" fill="#e9b5a1"/>
    <path d="M535 205 Q550 145 600 160 Q645 145 665 205 Q635 185 615 200 Q575 180 535 225Z" fill="#3c2635"/>
    <path d="M550 280 L650 280 L675 390 L525 390Z" fill="#d84c72"/>
    <path d="M600 300 L625 325 L600 350 L575 325Z" fill="#fff0ed" stroke="#fff" stroke-width="2"/>
    <circle cx="580" cy="235" r="5" fill="#402b38"/><circle cx="620" cy="235" r="5" fill="#402b38"/>
    <path d="M585 255 Q600 265 615 255" fill="none" stroke="#75404c" stroke-width="3"/>
    <text x="600" y="455" fill="#ffc1d5" font-size="22" letter-spacing="7" text-anchor="middle">STEVEN</text>
  </g>

  <!-- GARNET -->
  <g class="scene s3">
    <ellipse cx="600" cy="270" rx="130" ry="155" fill="#e95c9b" opacity=".14" filter="url(#glow)"/>
    <path d="M530 190 Q530 115 600 130 Q670 115 670 190 L650 260 L550 260Z" fill="#29203f" stroke="#e6a5ff" stroke-width="3"/>
    <path d="M550 210 L650 210 L665 370 L535 370Z" fill="#8d2c6a"/>
    <path d="M565 205 L590 225 L575 245 L550 230Z M635 205 L610 225 L625 245 L650 230Z" fill="#f4c4e8"/>
    <rect x="555" y="220" width="90" height="25" rx="8" fill="#211d37" stroke="#e8b6ff" stroke-width="2"/>
    <path d="M600 350 L620 370 L600 390 L580 370Z" fill="#ed9dc8" stroke="#fff" stroke-width="2"/>
    <text x="600" y="455" fill="#ffb4dc" font-size="22" letter-spacing="7" text-anchor="middle">GARNET</text>
  </g>

  <!-- PEARL -->
  <g class="scene s4">
    <ellipse cx="600" cy="270" rx="130" ry="155" fill="#8fe9ed" opacity=".14" filter="url(#glow)"/>
    <path d="M600 120 L630 185 L665 220 L650 300 L630 355 L570 355 L550 300 L535 220 L570 185Z" fill="#bcebed" stroke="#fff" stroke-width="3"/>
    <path d="M600 150 L625 205 L600 230 L575 205Z" fill="#f8e4e5"/>
    <path d="M560 250 Q600 230 640 250 L650 385 L550 385Z" fill="#e5a9bb"/>
    <path d="M600 335 L617 355 L600 375 L583 355Z" fill="#a9f1ee" stroke="#fff" stroke-width="2"/>
    <circle cx="580" cy="240" r="4" fill="#486c7a"/><circle cx="620" cy="240" r="4" fill="#486c7a"/>
    <path d="M590 260 L610 260" stroke="#486c7a" stroke-width="2"/>
    <text x="600" y="455" fill="#c6ffff" font-size="22" letter-spacing="7" text-anchor="middle">PEARL</text>
  </g>

  <g text-anchor="middle" font-family="Georgia,serif" fill="#fff">
    <text x="600" y="45" font-size="15" letter-spacing="8" opacity=".8">WELCOME TO</text>
    <text x="600" y="535" font-size="34" letter-spacing="10">VITÓRIA COSTA</text>
    <text x="600" y="565" font-size="12" letter-spacing="5" opacity=".75">SOFTWARE ENGINEERING  ✦  CRYSTAL GEMS</text>
  </g>
</svg>
