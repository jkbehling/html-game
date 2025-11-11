"""
HTML Timberman page generator
---------------------------------
This script renders the game page (`index.html`) from the Jinja template
`templates/game.html` by:

1) Generating a valid "tree" string via `generate_tree(length)` that obeys:
     - Starts with 'N' and ends with 'N'
     - Every 'L' or 'R' is separated by an 'N' (no adjacent L/R)
     - Current implementation fixes the penultimate character to 'R' to reuse
         an existing victory animation.

2) Building a `sequence` structure used by the template to determine which
     button is correct for the next step and which GIF to display.
     For each position i (except the last, which is the victory frame), the
     structure is:

             sequence[i] = [
                     [correct_button, main_gif_basename],
                     [wrong_button,   death_gif_basename]
             ]

     where:
     - `correct_button` is either 'L' or 'R' and drives popover navigation
     - `main_gif_basename` is the base name of the animated frame to copy into
         `static/game_frame_copies/` as `<basename>_<i>.gif`
     - `death_gif_basename` is the base name of the failure animation referenced
         directly from `static/`

3) Preparing assets by clearing `static/game_frame_copies/` and copying the
     required GIFs for each frame into that folder.

Outputs and side effects:
- Writes the rendered HTML to `index.html` in the project root.
- Deletes and recreates `static/game_frame_copies/`, then populates it with
    per-step copies named `<basename>_<index>.gif`.

Requirements:
- Jinja2 template at `templates/game.html`
- Source GIFs under `static/game_frames/`

Usage:
        python3 create_game.py

Errors and constraints:
- `generate_tree(length)` requires an odd `length >= 5` and raises ValueError
    otherwise.
- File operations will fail if expected directories/assets are missing.
"""

import shutil
import random
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

template = env.get_template("game.html")

def create_gif_copy(name, num):
    """Copy a game frame GIF into the per-run copies folder with an index.

    Args:
        name: Base filename (without extension) found under static/game_frames/.
        num:  Zero-based frame index to suffix the copied filename with.
    """
    shutil.copyfile(f"static/game_frames/{name}.gif", f"static/game_frame_copies/{name}_{num}.gif")

def generate_tree(length):
    """Generate a valid tree string of the requested odd length.

    Rules enforced:
    - Must start with 'N' and end with 'N'
    - Every 'L' or 'R' must be followed (and therefore separated) by 'N'
    - Penultimate character is fixed to 'R' to match available victory assets

    Args:
        length: Odd integer >= 5. The resulting sequence used by the template
                will have `length - 1` steps (last position is the victory).

    Returns:
        A string of length `length` composed of 'N', 'L', and 'R'.

    Raises:
        ValueError: If length is even or less than 5.
    """
    # length must be odd and at least 5
    if length < 5 or length % 2 == 0:
        raise ValueError("Length must be an odd number and at least 5")
    tree = ['N']
    while len(tree) < length - 2:
        if tree[-1] == 'N':
            tree.append(random.choice(['R', 'L']))
        else:
            tree.append('N')
    # Second to last must be R because I didn't want to make another victory GIF.
    tree.append('R')
    tree.append('N')
    return ''.join(tree)    

# Set up the tree
# Note that the final sequence created from this tree will be 1 less than the length of the tree
tree = generate_tree(101)

# Clear the game_frame_copies directory
shutil.rmtree('static/game_frame_copies')
shutil.os.mkdir('static/game_frame_copies')

# Set up frames sequence
sequence = [] # [[success frame, death frame], ...]
for index, block in enumerate(tree):
    # No need to process the last block because it will be the victory frame
    if index == len(tree) - 1:
        continue

    next_block = tree[index + 1]

    # If we're at the second to last block, set the next_next_block to L
    # so we can properly set up for the victory frame
    if index == len(tree) - 2:
        next_next_block = 'L'
    # Otherwise, get the actual next next block
    else:
        next_next_block = tree[index + 2]
    # Determine which gif to use based on current, next, and next next blocks
    match (block, next_block, next_next_block):
        case('L', 'N', 'L'):
            sequence.append([['R', 'LNL'], ['L', 'LN_DEATH']])
            create_gif_copy('LNL', index)
        case('L', 'N', 'R'):
            sequence.append([['R', 'LNR'], ['L', 'LN_DEATH']])
            create_gif_copy('LNR', index)
        case('R', 'N', 'L'):
            sequence.append([['L', 'RNL'], ['R', 'RN_DEATH']])
            create_gif_copy('RNL', index)
        case('R', 'N', 'R'):
            sequence.append([['L', 'RNR'], ['R', 'RN_DEATH']])
            create_gif_copy('RNR', index)
        case('N', 'L', 'N'):
            sequence.append([['R', 'NLN'], ['L', 'NLN_DEATH']])
            create_gif_copy('NLN', index)
        case('N', 'R', 'N'):
            sequence.append([['L', 'NRN'], ['R', 'NRN_DEATH']])
            create_gif_copy('NRN', index)

context = {
    "sequence": sequence
}

output = template.render(context)

with open("index.html", "w") as f:
    f.write(output)

