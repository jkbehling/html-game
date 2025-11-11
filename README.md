HTML Timberman — Pure HTML Edition
=================================

This project renders a simple Timberman-style game using only HTML (no JS/CSS at runtime). The page is generated from a Jinja template and uses HTML popovers and buttons to drive the flow between frames.

Quick start
-----------

1) Install dependencies

```bash
pip install -r requirements.txt
```

2) Generate the page and frame copies:

```bash
python3 create_game.py
```

This will:
- Generate a valid tree sequence
- Clear and repopulate `static/game_frame_copies/` with per-step GIF copies
- Render `index.html` from `templates/game.html`

3) Serve the site locally (any static server works). For example:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

How it works
------------

- Tree rules: A string of characters is generated to represent the tree. Possible characters include `N` (no branches), `L` (branch on left), and `R` (branch on right). The generated tree string starts and ends with `N`. Every `L` or `R` is separated by `N` (no adjacent L/R).
- Sequence structure: For each step `i` (except the final victory frame), the generator builds:

```python
sequence[i] = [
	[correct_button, main_gif_basename],
	[wrong_button,   death_gif_basename]
]
```

The template uses this to decide which popover to show next and which GIF to display. Main frame GIFs are copied to `static/game_frame_copies/` as `<basename>_<i>.gif`.

Assets layout
-------------

- Source frame GIFs: `static/game_frames/`
- Per-run copied frames: `static/game_frame_copies/` (auto-cleared/repopulated)
- Template: `templates/game.html`
- Output page: `index.html`


Non‑commercial educational use
------------------------------

This project is an educational, non‑commercial recreation. All credit for the original Timberman concept, design, and assets goes to the creators of Timberman. No ownership is claimed over the original IP, and this project is not used for monetary gain.
