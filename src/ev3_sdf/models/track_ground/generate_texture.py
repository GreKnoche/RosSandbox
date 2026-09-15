#!/usr/bin/env python3
"""Generate a 10x10 m ground texture aligned with basics_track.sdf."""

from pathlib import Path

import numpy as np
from PIL import Image

SIZE_M = 10.0
CX, CY = 0.875, 0.975
RES = 2048

# Inner corridor of the L-track (slightly under the walls).
L_X0, L_X1 = -0.53, 2.03
L_Y0, L_Y1 = -0.38, 0.38
E_X0, E_X1 = 1.37, 2.03
E_Y0, E_Y1 = -0.38, 2.33

RING_IN, RING_OUT = 2.55, 3.45
LINE_W = 0.035


def _noise(shape, rng, scale, octaves=4):
    acc = np.zeros(shape, dtype=np.float32)
    amp = 1.0
    total = 0.0
    h, w = shape
    for o in range(octaves):
        ny = max(2, h // (16 * (2**o)))
        nx = max(2, w // (16 * (2**o)))
        grid = rng.random((ny, nx), dtype=np.float32)
        sampled = np.array(
            Image.fromarray(grid, mode="F").resize((w, h), Image.BILINEAR)
        )
        acc += sampled * amp
        total += amp
        amp *= 0.5
    return (acc / total) * scale


def _dash(coord, dash=0.28, gap=0.22):
    period = dash + gap
    return np.mod(coord, period) < dash


def _band(val, center, width):
    return np.abs(val - center) < (width * 0.5)


def main():
    rng = np.random.default_rng(7)
    xs = np.linspace(CX - SIZE_M / 2, CX + SIZE_M / 2, RES, dtype=np.float32)
    ys = np.linspace(CY + SIZE_M / 2, CY - SIZE_M / 2, RES, dtype=np.float32)
    x, y = np.meshgrid(xs, ys)

    grass_n = _noise((RES, RES), rng, 1.0)
    dirt_n = _noise((RES, RES), np.random.default_rng(11), 1.0)
    asp_n = _noise((RES, RES), np.random.default_rng(23), 1.0)

    grass = np.stack(
        [
            0.32 + 0.10 * grass_n,
            0.48 + 0.12 * grass_n,
            0.24 + 0.06 * grass_n,
        ],
        axis=-1,
    )
    dirt = np.stack(
        [
            0.42 + 0.08 * dirt_n,
            0.34 + 0.06 * dirt_n,
            0.22 + 0.04 * dirt_n,
        ],
        axis=-1,
    )
    asphalt = np.stack(
        [
            0.18 + 0.07 * asp_n,
            0.18 + 0.07 * asp_n,
            0.20 + 0.06 * asp_n,
        ],
        axis=-1,
    )

    img = grass.copy()

    r = np.hypot(x - CX, y - CY)
    pad = (x >= L_X0 - 0.35) & (x <= E_X1 + 0.35) & (y >= L_Y0 - 0.35) & (y <= E_Y1 + 0.35)
    img[pad] = dirt[pad]

    ring = (r >= RING_IN) & (r <= RING_OUT)
    street = ((x >= L_X0) & (x <= L_X1) & (y >= L_Y0) & (y <= L_Y1)) | (
        (x >= E_X0) & (x <= E_X1) & (y >= E_Y0) & (y <= E_Y1)
    )
    img[ring | street] = asphalt[ring | street]

    white = np.array([0.93, 0.93, 0.90], dtype=np.float32)
    yellow = np.array([0.95, 0.78, 0.12], dtype=np.float32)

    # Street edge lines
    edges = (
        (_band(y, L_Y0 + 0.06, LINE_W) & (x >= L_X0 + 0.04) & (x <= L_X1 - 0.04) & (y <= L_Y1))
        | (_band(y, L_Y1 - 0.06, LINE_W) & (x >= L_X0 + 0.04) & (x <= E_X0 + 0.04))
        | (_band(x, L_X0 + 0.06, LINE_W) & (y >= L_Y0 + 0.04) & (y <= L_Y1 - 0.04))
        | (_band(x, E_X1 - 0.06, LINE_W) & (y >= L_Y0 + 0.04) & (y <= E_Y1 - 0.04))
        | (_band(x, E_X0 + 0.06, LINE_W) & (y >= L_Y1 - 0.04) & (y <= E_Y1 - 0.04))
        | (_band(y, E_Y1 - 0.06, LINE_W) & (x >= E_X0 + 0.04) & (x <= E_X1 - 0.04))
    )
    img[edges & street] = white

    # Yellow center dashes on the L
    mid_h = _band(y, 0.0, LINE_W) & (x >= -0.38) & (x <= 1.58) & _dash(x)
    mid_v = _band(x, 1.70, LINE_W) & (y >= 0.18) & (y <= 2.12) & _dash(y)
    img[mid_h | mid_v] = yellow

    # Circular road lines
    ang = np.arctan2(y - CY, x - CX)
    arc = 0.5 * (RING_IN + RING_OUT) * np.mod(ang + 2 * np.pi, 2 * np.pi)
    inner = _band(r, RING_IN + 0.07, LINE_W)
    outer = _band(r, RING_OUT - 0.07, LINE_W)
    mid = _band(r, 0.5 * (RING_IN + RING_OUT), LINE_W) & _dash(arc, 0.35, 0.25)
    img[ring & (inner | outer)] = white
    img[ring & mid] = yellow

    out = Path(__file__).with_name("materials") / "textures" / "track.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(img * 255, 0, 255).astype(np.uint8), mode="RGB").save(
        out, optimize=True
    )
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
