# Czech Letter Stamp Generator (Blender Scripts)

This repository contains scripts for generating letter stamps for a letterpress-style printing machine. The system supports custom fonts and includes an adjusted version of the Augusta typeface that supports the Czech alphabet.

🖨️ You can find ready-to-print STL examples and the Blender template file on Printables:  
👉 [Download on Printables](#)

---

## ✍️ What You Can Do

- Generate 3D printable letter stamps from any font.
- Customize block size and shape.
- Use the included Augusta variant or your own TTF font.

---

## 🧰 Scripts Overview

You can create your own stamps manually using the included Blender template or recreate them from scratch.

Each letter stamp is a block with a letter on top. To create new stamps:

1. Create a box (block).
2. Add a 3D text object (any character).
3. Assign your font (via `.ttf` file in Blender).
4. Extrude the text into 3D geometry.
5. Run the following scripts in order:

### `01_generate_from_template.py`
- Duplicates the base block and positions letters in a grid.

### `02_convert_to_mesh.py`
- Converts all text objects to mesh objects.

### `03_join_letters_with_blocks.py`
- Joins each letter with the block underneath it (based on X/Y position overlap).

---

MIT License – free for any use.
