# PhotoBatch

A modern, user-friendly batch image renaming application built with Python and Tkinter.

## Features

- 🖼️ **Batch Rename**: Rename multiple images at once with customizable naming patterns
- 👀 **Live Preview**: Preview changes before applying them
- 🎨 **Multiple Formats**: Choose from parentheses, underscore, dash, or space formats
- 📁 **Custom Export**: Export renamed files to a custom location or default directory
- 🔄 **Undo Support**: Undo last rename operation (when originals are preserved)
- 🖱️ **Drag & Drop**: Drag and drop images directly into the application
- 🖼️ **Image Preview**: Double-click to preview images before renaming
- ⌨️ **Keyboard Shortcuts**: Full keyboard support for power users

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- tkinterdnd2 (for drag-and-drop support)
- Pillow (for enhanced image support)

## Installation

### Method 1: Using Git (Recommended)

1. Clone this repository:
```bash
git clone git@github.com:CremaCrem/PhotoBatch.git
cd PhotoBatch
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Method 2: Download ZIP

1. Click the green "Code" button on GitHub and select "Download ZIP"
2. Extract the ZIP file to your desired location
3. Open a terminal/command prompt in the extracted folder
4. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Installing Dependencies

If you don't have `pip` installed or encounter issues, try:

**Windows:**
```bash
python -m pip install --upgrade pip
pip install tkinterdnd2 Pillow
```

**macOS/Linux:**
```bash
python3 -m pip install --upgrade pip
pip3 install tkinterdnd2 Pillow
```

**Note:** If `tkinter` is not available, install it:
- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **Fedora:** `sudo dnf install python3-tkinter`
- **macOS:** Usually pre-installed with Python

## Usage

### Running the Application

1. Open a terminal/command prompt in the project directory
2. Run the application:
```bash
python renaming.py
```

Or on some systems:
```bash
python3 renaming.py
```

### Step-by-Step Guide

#### 1. Select Images

**Option A: Browse Files**
- Click the "Browse..." button
- Select one or more image files (hold Ctrl/Cmd to select multiple)
- Supported formats: JPG, JPEG, PNG, GIF, BMP, WEBP, TIFF

**Option B: Drag and Drop**
- Simply drag image files from your file explorer
- Drop them into the application window or the path entry field

#### 2. Configure Naming

- **Base Name**: Enter the base name for your files (e.g., "V-2025-U-0772")
- **Format**: Choose your preferred naming format:
  - **Parentheses**: `Name (1).jpg`, `Name (2).jpg`
  - **Underscore**: `Name_1.jpg`, `Name_2.jpg`
  - **Dash**: `Name-1.jpg`, `Name-2.jpg`
  - **Space**: `Name 1.jpg`, `Name 2.jpg`

#### 3. Set Export Location (Optional)

- **Default**: Files are exported to a folder next to the application
- **Custom**: Click "Browse..." next to "Export to:" to choose a different directory
- Click "Reset" to return to the default location

#### 4. Preview Changes

- Click the "Preview" button to see how files will be renamed
- Double-click any row in the preview to see the image
- Right-click a row for more options (preview, remove)

#### 5. Export Files

- Click "Export Files" to create renamed copies
- Files will be saved in a folder named after your base name
- Original files are preserved by default

#### 6. Optional: Delete Originals

⚠️ **Warning**: This action cannot be undone!

- Check "Delete original files after export" if you want to remove source files
- Only use this if you're certain you don't need the originals
- Make backups if unsure

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open file browser |
| `Ctrl+R` | Preview changes |
| `Ctrl+Z` | Undo last rename |
| `Delete` / `Backspace` | Remove selected image from list |
| `F1` | Show help dialog |
| `Double-click` | Preview selected image |

### Advanced Features

#### Removing Images from List
- Select one or more rows in the preview
- Press `Delete` or `Backspace`, or click "Remove"
- Right-click a row and select "Remove from List"

#### Undo Last Export
- Click "Undo" or press `Ctrl+Z`
- Only works if original files were NOT deleted
- Removes exported files and restores the preview

#### Image Preview
- Double-click any row in the preview table
- Or right-click and select "Preview Image"
- View images before renaming to ensure correct selection

## Troubleshooting

### Application Won't Start

**Issue**: "No module named 'tkinter'"
- **Solution**: Install tkinter (see Installation section)

**Issue**: "No module named 'tkinterdnd2'"
- **Solution**: Run `pip install tkinterdnd2`

**Issue**: "No module named 'PIL'"
- **Solution**: Run `pip install Pillow`

### Drag and Drop Not Working

- Make sure `tkinterdnd2` is installed: `pip install tkinterdnd2`
- The application will still work without drag-and-drop, just use the Browse button

### Images Not Displaying in Preview

- Install Pillow for better image support: `pip install Pillow`
- Some image formats may not preview without Pillow

### Export Fails

- Check that you have write permissions in the export directory
- Ensure there's enough disk space
- Make sure no files with the same names already exist in the output folder

### Files Not Found After Export

- Check the export location (shown in the success message)
- Default location is a folder next to `renaming.py`
- Look for a folder named after your base name

## Supported Image Formats

- JPEG / JPG
- PNG
- GIF
- BMP
- WEBP
- TIFF / TIF

## Project Structure

```
PhotoBatch/
├── renaming.py          # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

© 2026 All Rights Reserved

## Credits

Created by the Interns of BSIT 2026

Built with Python & Tkinter

---

**Need Help?** Press `F1` in the application or check the Help dialog for more information.
