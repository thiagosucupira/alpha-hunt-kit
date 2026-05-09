# Blog rewrite outline: Package the Alpha Hunt, Not the Agent

The old post failed because it was a spec dump. The rewrite should be short, visual, and product-shaped.

## Section order

1. The mistake: exporting a private agent is the wrong product.
2. The short version: source, rank, test, remember.
3. The loop in one picture.
4. A day in the Alpha Hunt.
5. The portable package boundary: reads/writes/never touches.
6. What ships in the GitHub repo.
7. Data access without locking readers out.
8. Safety boundary.
9. First local proof.
10. What readers can copy.

## Visual slots

- Hero: `assets/alpha-hunt-package-boundary.png`.
- Loop diagram: `assets/alpha-hunt-loop.png`.
- Data ladder: `assets/alpha-hunt-data-access-ladder.png`.
- Manim 1: Four Loop Orbit.
- Manim 2: Cheap Experiment Gauntlet.

## Tone

Write for a smart reader who has never seen the private machine. Runtime names are adapters, not the center.
