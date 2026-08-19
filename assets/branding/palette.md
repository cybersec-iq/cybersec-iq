# cybersec-iq — Visual Design System

Single source of truth for the profile + GitHub Pages experience.

## Core palette

| Token            | Hex       | Role |
|------------------|-----------|------|
| `--void`         | `#05070A` | Page background / deepest layer |
| `--surface`      | `#0A0E13` | Panels, terminal body |
| `--surface-2`    | `#111820` | Raised surface, title bars |
| `--line`         | `#1B2733` | Hairlines, grid, borders |
| `--neon`         | `#39FF14` | Primary accent — identity, prompts |
| `--lime`         | `#C6FF00` | Secondary accent — highlights |
| `--cyan`         | `#00E5FF` | Structural accent — headings, data |
| `--blue`         | `#2979FF` | Depth accent — links, cool contrast |
| `--amber`        | `#FFD400` | Warning / status, used sparingly |
| `--text`         | `#D7E3EC` | Primary text |
| `--muted`        | `#7C8B99` | Secondary text |

## Rules

1. **Two accents maximum per component.** Neon + cyan is the default pairing.
2. **Amber is a status colour only** — never decorative.
3. **Contrast floor: 4.5:1** for any text under 18px against its own surface.
4. **Motion is ambient, never attention-seeking.** No flashing above 3Hz.
   Every animation is wrapped in `prefers-reduced-motion` guards.
5. **Type is monospace-first**, with a universally available fallback chain:
   `ui-monospace, "JetBrains Mono", "Fira Code", SFMono-Regular, Menlo, Consolas, monospace`
6. **Assets are SVG.** No raster binaries, no web fonts, no external requests.

## Geometry

- Grid unit: `8px`
- Corner radius: `2px` (hard, technical) — never pill-shaped
- Hairline: `1px` at `--line`
- HUD brackets: `2px` at `--neon`, 18px arm length
