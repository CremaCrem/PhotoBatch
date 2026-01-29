import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False
    DND_FILES = None
    TkinterDnD = None
import shutil
from datetime import datetime
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

class ModernImageRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("PhotoBatch")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set window icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass  # Icon not found or invalid, use default
        
        # Make window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Color scheme - Modern take on classic gray (Neo-Retro)
        self.colors = {
            'primary': '#3D5A80',      # Muted steel blue
            'primary_dark': '#2C4157',
            'primary_light': '#E8ECF0',
            'success': '#457B4D',       # Muted green
            'warning': '#C4933F',       # Muted gold
            'danger': '#B54747',        # Muted red
            'bg_main': '#E4E4E4',       # Light warm gray
            'bg_card': '#F0F0F0',       # Slightly lighter card
            'bg_secondary': '#D0D0D0',  # Medium gray
            'accent': '#3D5A80',        # Steel blue accent
            'text_primary': '#1A1A1A',  # Near black
            'text_secondary': '#5A5A5A', # Medium gray text
            'border': '#B0B0B0',        # Subtle border
            'border_light': '#FFFFFF',  # Highlight
            'border_dark': '#888888',   # Shadow
            'hover': '#D8D8D8',
            'button_face': '#E8E8E8',   # Modern button
            'title_bar': '#3D5A80',     # Steel blue header
            'selection': '#B8D4E8'      # Soft blue selection
        }
        
        self.root.configure(bg=self.colors['bg_main'])
        
        # State management
        self.current_folder = None
        self.selected_files = []
        self.files_to_rename = []
        self.rename_history = []
        self.preview_data = []
        self.preview_item_paths = {}
        
        # Export settings
        self.custom_export_dir = None  # None means use default (script directory)
        
        # Configure styles
        self.setup_styles()
        
        # Build UI
        self.create_header()
        self.create_main_content()
        self.create_footer()
        self.setup_drag_and_drop()
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.browse_files())
        self.root.bind('<Control-r>', lambda e: self.preview_rename())
        self.root.bind('<Control-z>', lambda e: self.undo_last_rename())
        self.root.bind('<F1>', lambda e: self.show_help())
        
    def setup_styles(self):
        """Configure ttk styles - Modern Neo-Retro look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles - Primary (Modern with subtle depth)
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=1,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('Segoe UI', 9, 'bold'),
                       relief='raised')
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_dark']),
                           ('pressed', self.colors['primary_dark']),
                           ('disabled', self.colors['border'])],
                 relief=[('pressed', 'sunken')])
        
        # Configure button styles - Secondary (Subtle raised)
        style.configure('Secondary.TButton',
                       background=self.colors['button_face'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       focuscolor='none',
                       padding=(16, 8),
                       font=('Segoe UI', 9),
                       relief='raised')
        
        style.map('Secondary.TButton',
                 background=[('active', self.colors['hover']),
                           ('pressed', self.colors['bg_secondary'])],
                 relief=[('pressed', 'sunken')])
        
        # Configure frame style
        style.configure('Card.TFrame',
                       background=self.colors['bg_card'],
                       relief='groove',
                       borderwidth=1)
        
        # Configure entry style
        style.configure('Modern.TEntry',
                       fieldbackground='white',
                       borderwidth=1,
                       relief='sunken')
        
        # Configure treeview - clean modern look with classic structure
        style.configure('Modern.Treeview',
                       background='white',
                       foreground=self.colors['text_primary'],
                       fieldbackground='white',
                       borderwidth=1,
                       font=('Segoe UI', 9),
                       rowheight=26,
                       relief='sunken')
        
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       font=('Segoe UI', 9, 'bold'),
                       relief='raised',
                       padding=(8, 4))
        
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['selection'])],
                 foreground=[('selected', self.colors['text_primary'])])
    
    def create_header(self):
        """Create application header - modern take on classic title bar"""
        # Modern header with gradient feel
        header_frame = tk.Frame(self.root, bg=self.colors['title_bar'], pady=12)
        header_frame.pack(fill='x', padx=0, pady=(0, 0))
        
        # Title with icon - clean modern style
        title = tk.Label(header_frame,
                        text="  PhotoBatch",
                        font=('Segoe UI', 14, 'bold'),
                        bg=self.colors['title_bar'],
                        fg='white',
                        anchor='w')
        title.pack(side='left', padx=12)
        
        # Subtitle
        subtitle = tk.Label(header_frame,
                           text="Batch Image Renaming Made Simple",
                           font=('Segoe UI', 9),
                           bg=self.colors['title_bar'],
                           fg='#A0B8D0')
        subtitle.pack(side='left', padx=(0, 12))
        
        # Version in header
        version = tk.Label(header_frame,
                          text="v1.0.0",
                          font=('Segoe UI', 9),
                          bg=self.colors['title_bar'],
                          fg='#A0B8D0',
                          anchor='e')
        version.pack(side='right', padx=12)
    
    def create_main_content(self):
        """Create main content area - fills available space"""
        # Main container that fills space properly
        main_container = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True, padx=12, pady=12)
        
        # Configure grid weights for proper expansion
        main_container.grid_rowconfigure(2, weight=1)  # Preview card expands
        main_container.grid_columnconfigure(0, weight=1)
        
        # Step 1: Image Selection Card (fixed height)
        self.create_folder_selection_card(main_container)
        
        # Step 2: Naming Configuration Card (fixed height)
        self.create_naming_card(main_container)
        
        # Step 3: Preview Card (expands to fill remaining space)
        self.create_preview_card(main_container)
    
    def create_folder_selection_card(self, parent):
        """Create image selection section - modern neo-retro style"""
        card = self.create_card(parent, "Select Images")
        card.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        
        # Content frame
        content = tk.Frame(card, bg=self.colors['bg_card'])
        content.pack(fill='x', padx=16, pady=12)
        
        # Path entry with subtle sunken style
        self.path_entry = tk.Entry(content,
                                   font=('Segoe UI', 10),
                                   bg='white',
                                   fg=self.colors['text_primary'],
                                   relief='sunken',
                                   bd=1,
                                   highlightthickness=1,
                                   highlightcolor=self.colors['primary'],
                                   highlightbackground=self.colors['border'])
        self.path_entry.pack(fill='x', pady=(0, 10), ipady=6)
        self.path_entry.insert(0, "No images selected... (Click Browse or drag files here)")
        self.path_entry.config(state='readonly')
        
        # Buttons row
        btn_frame = tk.Frame(content, bg=self.colors['bg_card'])
        btn_frame.pack(fill='x')
        
        browse_btn = ttk.Button(btn_frame,
                               text="Browse...",
                               command=self.browse_files,
                               style='Primary.TButton')
        browse_btn.pack(side='left', padx=(0, 6))
        
        self.clear_btn = ttk.Button(btn_frame,
                               text="Clear All",
                               command=self.clear_selection,
                               style='Secondary.TButton',
                               state='disabled')
        self.clear_btn.pack(side='left', padx=(0, 12))
        
        # File count indicator with icon
        self.file_count_label = tk.Label(btn_frame,
                                        text="0 images selected",
                                        font=('Segoe UI', 9),
                                        bg=self.colors['bg_card'],
                                        fg=self.colors['text_secondary'])
        self.file_count_label.pack(side='left', padx=8)
    
    def create_naming_card(self, parent):
        """Create naming configuration section - modern neo-retro style"""
        card = self.create_card(parent, "Configure Naming")
        card.grid(row=1, column=0, sticky='ew', pady=(0, 8))
        
        content = tk.Frame(card, bg=self.colors['bg_card'])
        content.pack(fill='x', padx=16, pady=12)
        
        # Base name input row
        name_row = tk.Frame(content, bg=self.colors['bg_card'])
        name_row.pack(fill='x', pady=(0, 10))
        
        label = tk.Label(name_row,
                        text="Base Name:",
                        font=('Segoe UI', 10),
                        bg=self.colors['bg_card'],
                        fg=self.colors['text_primary'])
        label.pack(side='left', padx=(0, 10))
        
        self.name_entry = tk.Entry(name_row,
                                   font=('Segoe UI', 10),
                                   bg='white',
                                   fg=self.colors['text_primary'],
                                   relief='sunken',
                                   bd=1,
                                   highlightthickness=1,
                                   highlightcolor=self.colors['primary'],
                                   highlightbackground=self.colors['border'])
        self.name_entry.pack(side='left', fill='x', expand=True, ipady=6)
        self.name_entry.insert(0, "V-2025-U-0772")
        self.name_entry.bind('<KeyRelease>', lambda e: self.auto_preview())
        
        # Format options row
        format_frame = tk.Frame(content, bg=self.colors['bg_card'])
        format_frame.pack(fill='x', pady=(0, 0))
        
        tk.Label(format_frame,
                text="Format:",
                font=('Segoe UI', 10),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(side='left', padx=(0, 10))
        
        self.format_var = tk.StringVar(value="parentheses")
        
        formats = [
            ("Name (1).jpg", "parentheses"),
            ("Name_1.jpg", "underscore"),
            ("Name-1.jpg", "dash"),
            ("Name 1.jpg", "space")
        ]
        
        for text, value in formats:
            rb = tk.Radiobutton(format_frame,
                               text=text,
                               variable=self.format_var,
                               value=value,
                               font=('Segoe UI', 9),
                               bg=self.colors['bg_card'],
                               fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_card'],
                               activebackground=self.colors['hover'],
                               highlightthickness=0,
                               command=self.auto_preview)
            rb.pack(side='left', padx=6)
        
        # Options row (delete originals toggle)
        options_frame = tk.Frame(content, bg=self.colors['bg_card'])
        options_frame.pack(fill='x', pady=(12, 0))
        
        self.delete_originals_var = tk.BooleanVar(value=False)
        
        delete_cb = tk.Checkbutton(options_frame,
                                   text="Delete original files after export",
                                   variable=self.delete_originals_var,
                                   font=('Segoe UI', 9),
                                   bg=self.colors['bg_card'],
                                   fg=self.colors['text_primary'],
                                   selectcolor='white',
                                   activebackground=self.colors['bg_card'],
                                   highlightthickness=0)
        delete_cb.pack(side='left')
        
        # Warning label
        self.delete_warning_label = tk.Label(options_frame,
                                             text="⚠ This cannot be undone!",
                                             font=('Segoe UI', 9),
                                             bg=self.colors['bg_card'],
                                             fg=self.colors['danger'])
        
        # Show/hide warning based on checkbox state
        def toggle_warning(*args):
            if self.delete_originals_var.get():
                self.delete_warning_label.pack(side='left', padx=(10, 0))
            else:
                self.delete_warning_label.pack_forget()
        
        self.delete_originals_var.trace_add('write', toggle_warning)
        
        # Export location row
        export_loc_frame = tk.Frame(content, bg=self.colors['bg_card'])
        export_loc_frame.pack(fill='x', pady=(12, 0))
        
        tk.Label(export_loc_frame,
                text="Export to:",
                font=('Segoe UI', 10),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(side='left', padx=(0, 10))
        
        # Export path display
        self.export_path_var = tk.StringVar(value="Default (App Directory)")
        self.export_path_label = tk.Label(export_loc_frame,
                                          textvariable=self.export_path_var,
                                          font=('Segoe UI', 9),
                                          bg=self.colors['bg_card'],
                                          fg=self.colors['text_secondary'],
                                          anchor='w')
        self.export_path_label.pack(side='left', fill='x', expand=True)
        
        # Change location button
        change_btn = ttk.Button(export_loc_frame,
                                text="Browse...",
                                style='Secondary.TButton',
                                command=self.change_export_location)
        change_btn.pack(side='left', padx=(10, 5))
        
        # Reset to default button
        self.reset_export_btn = ttk.Button(export_loc_frame,
                                           text="Reset",
                                           style='Secondary.TButton',
                                           command=self.reset_export_location,
                                           state='disabled')
        self.reset_export_btn.pack(side='left')
    
    def create_preview_card(self, parent):
        """Create preview section with file list - modern neo-retro style"""
        card = self.create_card(parent, "Preview & Export")
        card.grid(row=2, column=0, sticky='nsew', pady=(0, 0))
        
        # Configure card to expand
        card.grid_rowconfigure(1, weight=1)
        card.grid_columnconfigure(0, weight=1)
        
        content = tk.Frame(card, bg=self.colors['bg_card'])
        content.pack(fill='both', expand=True, padx=16, pady=12)
        
        # Configure content to expand
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)
        
        # Treeview for preview with subtle sunken border
        tree_frame = tk.Frame(content, bg='white', relief='sunken', bd=1)
        tree_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Remove fixed height - let it expand naturally
        self.preview_tree = ttk.Treeview(tree_frame,
                                        columns=('Original', 'Arrow', 'New'),
                                        show='headings',
                                        style='Modern.Treeview',
                                        yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=self.preview_tree.yview)
        
        # Configure columns - use percentages for responsive width
        self.preview_tree.heading('Original', text='Original Name')
        self.preview_tree.heading('Arrow', text='>')
        self.preview_tree.heading('New', text='New Name')
        
        self.preview_tree.column('Original', width=400, minwidth=150, anchor='w')
        self.preview_tree.column('Arrow', width=40, minwidth=30, anchor='center')
        self.preview_tree.column('New', width=400, minwidth=150, anchor='w')
        
        self.preview_tree.pack(fill='both', expand=True)
        self.preview_tree.bind('<Double-1>', self.open_image_preview)
        self.preview_tree.bind('<Delete>', self.remove_selected_images)
        self.preview_tree.bind('<BackSpace>', self.remove_selected_images)
        
        # Right-click context menu
        self.tree_menu = tk.Menu(self.preview_tree, tearoff=0)
        self.tree_menu.add_command(label="Preview Image", command=self.preview_selected_image)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label="Remove from List", command=self.remove_selected_images)
        self.preview_tree.bind('<Button-3>', self.show_tree_menu)
        
        # Action buttons row
        btn_frame = tk.Frame(content, bg=self.colors['bg_card'])
        btn_frame.pack(fill='x')
        
        preview_btn = ttk.Button(btn_frame,
                                text="Preview",
                                command=self.preview_rename,
                                style='Secondary.TButton')
        preview_btn.pack(side='left', padx=(0, 4))
        
        self.rename_btn = ttk.Button(btn_frame,
                                    text="Export Files",
                                    command=self.execute_rename,
                                    style='Primary.TButton',
                                    state='disabled')
        self.rename_btn.pack(side='left', padx=(0, 4))
        
        remove_btn = ttk.Button(btn_frame,
                             text="Remove",
                             command=self.remove_selected_images,
                             style='Secondary.TButton')
        remove_btn.pack(side='left', padx=(0, 4))
        
        undo_btn = ttk.Button(btn_frame,
                             text="Undo",
                             command=self.undo_last_rename,
                             style='Secondary.TButton')
        undo_btn.pack(side='left', padx=(0, 4))
        
        help_btn = ttk.Button(btn_frame,
                             text="Help",
                             command=self.show_help,
                             style='Secondary.TButton')
        help_btn.pack(side='left', padx=(0, 4))
        
        credits_btn = ttk.Button(btn_frame,
                                text="Credits",
                                command=self.show_credits,
                                style='Secondary.TButton')
        credits_btn.pack(side='left')
    
    def create_footer(self):
        """Create footer with modern status bar"""
        # Modern status bar
        footer = tk.Frame(self.root, bg=self.colors['bg_secondary'])
        footer.pack(fill='x', side='bottom')
        
        # Inner padding frame
        inner = tk.Frame(footer, bg=self.colors['bg_secondary'])
        inner.pack(fill='x', padx=12, pady=6)
        
        # Status label
        self.status_label = tk.Label(inner,
                                     text="Ready",
                                     font=('Segoe UI', 9),
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['text_primary'],
                                     anchor='w')
        self.status_label.pack(side='left')
        
        # Progress label
        self.progress_label = tk.Label(inner,
                                      text="",
                                      font=('Segoe UI', 9),
                                      bg=self.colors['bg_secondary'],
                                      fg=self.colors['success'])
        self.progress_label.pack(side='left', padx=(16, 0))
        
        # Help hints on right
        help_label = tk.Label(inner,
                            text="F1 Help  •  Ctrl+O Open  •  Del Remove  •  Ctrl+Z Undo",
                            font=('Segoe UI', 8),
                            bg=self.colors['bg_secondary'],
                            fg=self.colors['text_secondary'])
        help_label.pack(side='right')
    
    def setup_drag_and_drop(self):
        """Enable drag-and-drop if TkinterDnD is available"""
        if not DND_AVAILABLE:
            return
        
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)
        self.path_entry.drop_target_register(DND_FILES)
        self.path_entry.dnd_bind('<<Drop>>', self.handle_drop)
    
    def handle_drop(self, event):
        """Handle drag-and-drop of files"""
        file_paths = list(self.root.tk.splitlist(event.data))
        if not file_paths:
            return
        
        self.selected_files = file_paths
        self.current_folder = os.path.dirname(self.selected_files[0])
        self.path_entry.config(state='normal')
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, f"{len(self.selected_files)} files selected")
        self.path_entry.config(state='readonly')
        
        self.scan_selection()
        self.update_status(f"Loaded {len(self.selected_files)} image files", 'success')
    
    def create_card(self, parent, title):
        """Create a modern group box style container with classic inspiration"""
        # Outer frame with subtle border (modern take on classic)
        card_container = tk.Frame(parent, bg=self.colors['bg_card'],
                                 relief='solid', bd=1,
                                 highlightbackground=self.colors['border'],
                                 highlightthickness=0)
        
        # Title bar with subtle background
        title_bar = tk.Frame(card_container, bg=self.colors['bg_secondary'])
        title_bar.pack(fill='x')
        
        title_label = tk.Label(title_bar,
                              text="  " + title,
                              font=('Segoe UI', 10, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'],
                              anchor='w')
        title_label.pack(fill='x', padx=8, pady=8)
        
        return card_container
    
    def browse_files(self):
        """Open file selection dialog for images"""
        file_paths = filedialog.askopenfilenames(
            title="Select images to rename",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp *.tiff *.tif"),
                ("All files", "*.*")
            ]
        )
        if file_paths:
            self.selected_files = list(file_paths)
            self.current_folder = os.path.dirname(self.selected_files[0])
            self.path_entry.config(state='normal')
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, f"{len(self.selected_files)} files selected")
            self.path_entry.config(state='readonly')
            
            # Scan selected files
            self.scan_selection()
            self.update_status(f"Loaded {len(self.selected_files)} image files", 'success')
    
    def scan_selection(self):
        """Scan selected files for image types"""
        if not self.selected_files:
            return
        
        valid_exts = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif')
        try:
            self.files_to_rename = [
                f for f in self.selected_files if f.lower().endswith(valid_exts)
            ]
            self.files_to_rename.sort()
            
            count = len(self.files_to_rename)
            self.file_count_label.config(
                text=f"{count} image{'s' if count != 1 else ''} selected",
                fg=self.colors['success'] if count > 0 else self.colors['warning']
            )
            
            if count > 0:
                self.clear_btn.config(state='normal')
                self.auto_preview()
            else:
                self.clear_preview()
                self.show_warning(
                    "No Images Found",
                    "No image files were selected.\n\nSupported formats: JPG, PNG, GIF, BMP, WEBP, TIFF"
                )
        except Exception as e:
            self.update_status(f"Error scanning selection: {str(e)}", 'error')
            self.show_error("Error", f"Could not scan selection:\n{str(e)}")
    
    def auto_preview(self):
        """Automatically update preview when settings change"""
        if self.files_to_rename:
            self.preview_rename()
    
    def preview_rename(self):
        """Generate and display rename preview"""
        if not self.files_to_rename:
            self.show_info(
                "No Files Selected",
                "Please select images first."
            )
            return
        
        base_name = self.name_entry.get().strip()
        if not base_name:
            self.show_warning(
                "Missing Base Name",
                "Please enter a base name for the files."
            )
            return
        
        # Clear existing preview
        self.clear_preview()
        
        # Generate preview data
        self.preview_data = []
        format_type = self.format_var.get()
        
        self.preview_item_paths = {}
        for i, file_path in enumerate(self.files_to_rename, 1):
            filename = os.path.basename(file_path)
            ext = os.path.splitext(filename)[1]
            
            # Apply selected format
            if format_type == "parentheses":
                new_name = f"{base_name} ({i}){ext}"
            elif format_type == "underscore":
                new_name = f"{base_name}_{i}{ext}"
            elif format_type == "dash":
                new_name = f"{base_name}-{i}{ext}"
            else:  # space
                new_name = f"{base_name} {i}{ext}"
            
            self.preview_data.append((file_path, new_name))
            
            # Add to tree with alternating colors
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            item_id = self.preview_tree.insert('', 'end', values=(filename, '→', new_name), tags=(tag,))
            self.preview_item_paths[item_id] = file_path
        
        # Configure row colors - subtle alternating
        self.preview_tree.tag_configure('evenrow', background='#F5F5F5')
        self.preview_tree.tag_configure('oddrow', background='white')
        
        # Enable rename button
        self.rename_btn.config(state='normal')
        self.update_status(f"Preview ready: {len(self.preview_data)} files will be exported", 'info')
    
    def open_image_preview(self, event=None):
        """Open a larger preview of the selected image"""
        item_id = None
        if event is not None:
            item_id = self.preview_tree.identify_row(event.y)
        if not item_id:
            selected = self.preview_tree.selection()
            item_id = selected[0] if selected else None
        
        if not item_id:
            return
        
        image_path = self.preview_item_paths.get(item_id)
        if not image_path or not os.path.exists(image_path):
            self.show_error("Image Not Found", "The selected image could not be found.")
            return
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Preview - {os.path.basename(image_path)}")
        preview_window.geometry("900x700")
        preview_window.configure(bg=self.colors['bg_main'])
        
        # Header bar
        header = tk.Frame(preview_window, bg=self.colors['primary'])
        header.pack(fill='x')
        
        title = tk.Label(header,
                        text=f"  {os.path.basename(image_path)}",
                        font=('Segoe UI', 11, 'bold'),
                        bg=self.colors['primary'],
                        fg='white')
        title.pack(side='left', pady=10, padx=8)
        
        # Main frame
        main_frame = tk.Frame(preview_window, bg=self.colors['bg_main'])
        main_frame.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Image container
        img_container = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        img_container.pack(fill='both', expand=True)
        
        try:
            if PIL_AVAILABLE:
                image = Image.open(image_path)
                image.thumbnail((860, 580), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
            else:
                photo = tk.PhotoImage(file=image_path)
        except Exception as e:
            self.show_warning(
                "Preview Unavailable",
                f"Could not open image:\n{str(e)}\n\n"
                "Tip: install Pillow for wider image support."
            )
            preview_window.destroy()
            return
        
        img_label = tk.Label(img_container, image=photo, bg='white')
        img_label.image = photo
        img_label.pack(expand=True, padx=8, pady=8)
        
        # Button frame
        btn_container = tk.Frame(preview_window, bg=self.colors['bg_main'])
        btn_container.pack(fill='x', padx=16, pady=(0, 16))
        
        close_btn = ttk.Button(
            btn_container,
            text="Close",
            command=preview_window.destroy,
            style='Primary.TButton'
        )
        close_btn.pack()
    
    def execute_rename(self):
        """Execute the actual file renaming"""
        if not self.preview_data:
            self.show_warning("No Preview", "Please preview changes first.")
            return
        
        # Check if deleting originals
        delete_originals = self.delete_originals_var.get()
        
        # Confirmation dialog with appropriate warning
        if delete_originals:
            confirm = self.ask_confirm(
                "Confirm Export & Delete",
                f"Are you sure you want to export {len(self.preview_data)} files?\n\n"
                "⚠ WARNING: Original files will be PERMANENTLY DELETED!\n"
                "This cannot be undone!"
            )
        else:
            confirm = self.ask_confirm(
                "Confirm Export",
                f"Are you sure you want to export {len(self.preview_data)} files?\n\n"
                "Original files will be kept. You can undo this action."
            )
        
        if not confirm:
            return
        
        try:
            base_name = self.name_entry.get().strip()
            if not base_name:
                self.show_warning(
                    "Missing Base Name",
                    "Please enter a base name for the files."
                )
                return
            
            # Use custom export directory or default to script directory
            if self.custom_export_dir:
                export_base = self.custom_export_dir
            else:
                export_base = os.path.dirname(os.path.abspath(__file__))
            
            output_dir = os.path.join(export_base, base_name)
            os.makedirs(output_dir, exist_ok=True)
            
            # Check for name collisions in output folder
            collisions = []
            for _, new_name in self.preview_data:
                target_path = os.path.join(output_dir, new_name)
                if os.path.exists(target_path):
                    collisions.append(new_name)
            if collisions:
                self.show_error(
                    "Name Collision",
                    "Some files already exist in the output folder:\n\n"
                    + "\n".join(collisions[:10]) +
                    ("\n..." if len(collisions) > 10 else "") +
                    "\n\nPlease change the base name or remove existing files."
                )
                return
            
            # Store for undo capability (only if not deleting originals)
            rename_record = {
                'folder': output_dir,
                'changes': [],
                'timestamp': datetime.now(),
                'deleted_originals': delete_originals
            }
            
            # Perform copy + rename into output folder
            success_count = 0
            deleted_count = 0
            for old_path, new_name in self.preview_data:
                new_path = os.path.join(output_dir, new_name)
                
                # Check if file still exists
                if os.path.exists(old_path):
                    shutil.copy2(old_path, new_path)
                    rename_record['changes'].append(new_path)
                    success_count += 1
                    
                    # Delete original if option is enabled
                    if delete_originals:
                        try:
                            os.remove(old_path)
                            deleted_count += 1
                        except Exception as del_err:
                            # Log but continue if deletion fails
                            print(f"Could not delete {old_path}: {del_err}")
            
            # Save to history (undo only works if originals weren't deleted)
            self.rename_history.append(rename_record)
            
            # Update UI
            if delete_originals:
                self.progress_label.config(
                    text=f"✅ {success_count} exported, {deleted_count} originals deleted",
                    fg=self.colors['success']
                )
                self.update_status(f"Exported {success_count} files, deleted {deleted_count} originals", 'success')
                
                self.show_dialog(
                    "Success",
                    f"Successfully exported {success_count} image files!\n\n"
                    f"Output folder:\n{output_dir}\n\n"
                    f"Deleted {deleted_count} original files.\n\n"
                    "Note: Deletion cannot be undone.",
                    dialog_type='success'
                )
            else:
                self.progress_label.config(
                    text=f"✅ {success_count} files exported successfully!",
                    fg=self.colors['success']
                )
                self.update_status(f"Successfully exported {success_count} files to {base_name}", 'success')
                
                self.show_dialog(
                    "Success",
                    f"Successfully exported {success_count} image files!\n\n"
                    f"Output folder:\n{output_dir}\n\n"
                    "You can undo this action using 'Undo Last' or Ctrl+Z.",
                    dialog_type='success'
                )
            
            self.reset_selection()
            
        except Exception as e:
            self.update_status(f"Error during export: {str(e)}", 'error')
            self.show_error(
                "Export Error",
                f"An error occurred during export:\n\n{str(e)}\n\n"
                "Some files may have been exported. Please check the output folder."
            )
    
    def undo_last_rename(self):
        """Undo the last export operation"""
        if not self.rename_history:
            self.show_info(
                "Nothing to Undo",
                "No recent export operations to undo."
            )
            return
        
        # Check if last operation deleted originals
        last_op = self.rename_history[-1]
        if last_op.get('deleted_originals', False):
            self.show_warning(
                "Cannot Undo",
                "The last export operation deleted the original files.\n\n"
                "This action cannot be undone. The exported files will remain in the output folder."
            )
            return
        
        confirm = self.ask_confirm(
            "Confirm Undo",
            "Do you want to undo the last export operation?\n\n"
            "This will delete the exported files."
        )
        
        if not confirm:
            return
        
        try:
            # Get last operation
            last_operation = self.rename_history.pop()
            folder = last_operation['folder']
            
            # Reverse the changes by removing exported files
            undo_count = 0
            for new_path in last_operation['changes']:
                if os.path.exists(new_path):
                    os.remove(new_path)
                    undo_count += 1
            
            # Remove empty output folder
            if os.path.isdir(folder) and not os.listdir(folder):
                os.rmdir(folder)
            
            self.update_status(f"Undone: removed {undo_count} exported files", 'success')
            self.progress_label.config(
                text=f"↩️ Removed {undo_count} exported files",
                fg=self.colors['primary']
            )
            
            # Rescan selection
            self.scan_selection()
            
            self.show_dialog(
                "Undo Complete",
                f"Successfully removed {undo_count} exported files.\n\n"
                "Your original files are intact.",
                dialog_type='success'
            )
            
        except Exception as e:
            self.update_status(f"Undo error: {str(e)}", 'error')
            self.show_error(
                "Undo Error",
                f"An error occurred during undo:\n\n{str(e)}"
            )
    
    def clear_preview(self):
        """Clear the preview tree"""
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        self.preview_data = []
        self.preview_item_paths = {}
    
    def show_tree_menu(self, event):
        """Show right-click context menu"""
        # Select row under cursor
        item = self.preview_tree.identify_row(event.y)
        if item:
            self.preview_tree.selection_set(item)
            self.tree_menu.post(event.x_root, event.y_root)
    
    def preview_selected_image(self):
        """Preview the currently selected image in the tree"""
        self.open_image_preview()
    
    def remove_selected_images(self, event=None):
        """Remove selected images from the list"""
        selected = self.preview_tree.selection()
        if not selected:
            return
        
        # Get the file paths to remove
        paths_to_remove = set()
        for item_id in selected:
            if item_id in self.preview_item_paths:
                paths_to_remove.add(self.preview_item_paths[item_id])
        
        # Remove from selected files and files_to_rename
        self.selected_files = [f for f in self.selected_files if f not in paths_to_remove]
        self.files_to_rename = [f for f in self.files_to_rename if f not in paths_to_remove]
        
        # Update the path entry
        if self.selected_files:
            self.path_entry.config(state='normal')
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, f"{len(self.selected_files)} files selected")
            self.path_entry.config(state='readonly')
        
        # Update file count
        count = len(self.files_to_rename)
        removed_count = len(paths_to_remove)
        if count > 0:
            self.file_count_label.config(
                text=f"{count} image{'s' if count != 1 else ''} selected",
                fg=self.colors['success']
            )
            self.clear_btn.config(state='normal')
            # Refresh preview
            self.preview_rename()
            self.update_status(f"Removed {removed_count} image(s), {count} remaining", 'info')
        else:
            # No more files, reset
            self.reset_selection()
            self.update_status(f"Removed {removed_count} image(s), selection cleared", 'info')
    
    def reset_selection(self):
        """Clear selected files and reset UI"""
        self.selected_files = []
        self.files_to_rename = []
        self.current_folder = None
        self.clear_preview()
        self.rename_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        self.path_entry.config(state='normal')
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, "No images selected...")
        self.path_entry.config(state='readonly')
        self.file_count_label.config(
            text="0 images selected",
            fg=self.colors['text_secondary']
        )
        self.progress_label.config(text="")
    
    def clear_selection(self):
        """Clear all selected images"""
        self.reset_selection()
        self.update_status("Selection cleared", 'info')
    
    def change_export_location(self):
        """Open dialog to select custom export directory"""
        directory = filedialog.askdirectory(
            title="Select Export Directory",
            initialdir=self.custom_export_dir or os.path.dirname(os.path.abspath(__file__))
        )
        
        if directory:
            self.custom_export_dir = directory
            # Truncate long paths for display
            display_path = directory
            if len(display_path) > 50:
                display_path = "..." + display_path[-47:]
            self.export_path_var.set(display_path)
            self.reset_export_btn.config(state='normal')
            self.update_status(f"Export location set to: {directory}", 'success')
    
    def reset_export_location(self):
        """Reset export location to default (app directory)"""
        self.custom_export_dir = None
        self.export_path_var.set("Default (App Directory)")
        self.reset_export_btn.config(state='disabled')
        self.update_status("Export location reset to default", 'info')
    
    def update_status(self, message, status_type='info'):
        """Update status bar with colored message"""
        colors = {
            'success': self.colors['success'],
            'error': self.colors['danger'],
            'warning': self.colors['warning'],
            'info': self.colors['text_secondary']
        }
        self.status_label.config(text=message, fg=colors.get(status_type, colors['info']))
    
    def show_dialog(self, title, message, dialog_type='info', confirm=False):
        """Show a modern dialog centered on screen"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=self.colors['bg_card'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Determine dialog dimensions based on message length
        lines = message.count('\n') + 1
        message_length = len(message)
        
        # Calculate appropriate size
        width = min(480, max(380, message_length * 2))
        height = min(350, max(200, 140 + lines * 22))
        
        dialog.geometry(f"{width}x{height}")
        
        # Center dialog on parent window
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Icon colors
        icon_colors = {
            'info': self.colors['primary'],
            'warning': self.colors['warning'],
            'error': self.colors['danger'],
            'success': self.colors['success']
        }
        icon_map = {
            'info': 'ℹ',
            'warning': '⚠',
            'error': '✕',
            'success': '✓'
        }
        icon = icon_map.get(dialog_type, 'ℹ')
        icon_color = icon_colors.get(dialog_type, self.colors['primary'])
        
        # Header with colored accent
        header = tk.Frame(dialog, bg=icon_color, height=4)
        header.pack(fill='x')
        
        # Main content area
        main_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        main_frame.pack(fill='both', expand=True)
        
        # Content area with icon and message
        content = tk.Frame(main_frame, bg=self.colors['bg_card'])
        content.pack(fill='both', expand=True, padx=24, pady=20)
        
        # Icon - centered vertically with message
        icon_label = tk.Label(
            content,
            text=icon,
            font=('Segoe UI', 32),
            bg=self.colors['bg_card'],
            fg=icon_color
        )
        icon_label.pack(side='left', padx=(0, 20), anchor='n', pady=4)
        
        # Message container
        msg_container = tk.Frame(content, bg=self.colors['bg_card'])
        msg_container.pack(side='left', fill='both', expand=True)
        
        # Title in message area
        title_label = tk.Label(
            msg_container,
            text=title,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            anchor='w'
        )
        title_label.pack(fill='x', pady=(0, 8))
        
        # Message
        message_label = tk.Label(
            msg_container,
            text=message,
            font=('Segoe UI', 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            wraplength=width - 120,
            justify='left',
            anchor='nw'
        )
        message_label.pack(fill='both', expand=True)
        
        # Button frame
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
        btn_frame.pack(fill='x', padx=24, pady=(0, 20))
        
        result = {'value': False}
        
        def on_confirm():
            result['value'] = True
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        if confirm:
            cancel_btn = ttk.Button(
                btn_frame,
                text="Cancel",
                command=on_cancel,
                style='Secondary.TButton'
            )
            cancel_btn.pack(side='right', padx=(8, 0))
            
            ok_btn = ttk.Button(
                btn_frame,
                text="OK",
                command=on_confirm,
                style='Primary.TButton'
            )
            ok_btn.pack(side='right')
        else:
            ok_btn = ttk.Button(
                btn_frame,
                text="OK",
                command=on_cancel,
                style='Primary.TButton'
            )
            ok_btn.pack(side='right')
        
        dialog.protocol("WM_DELETE_WINDOW", on_cancel)
        dialog.wait_window()
        return result['value']
    
    def show_info(self, title, message):
        return self.show_dialog(title, message, dialog_type='info', confirm=False)
    
    def show_warning(self, title, message):
        return self.show_dialog(title, message, dialog_type='warning', confirm=False)
    
    def show_error(self, title, message):
        return self.show_dialog(title, message, dialog_type='error', confirm=False)
    
    def ask_confirm(self, title, message):
        return self.show_dialog(title, message, dialog_type='warning', confirm=True)
    
    def show_help(self):
        """Display help dialog"""
        help_text = """
PhotoBatch - Help

BASIC USAGE:
1. Select the images you want to rename
2. Enter a base name for your files
3. Choose a naming format
4. Preview the changes
5. Click 'Apply Rename' to export renamed files

KEYBOARD SHORTCUTS:
• Ctrl+O: Select images
• Ctrl+R: Preview changes
• Ctrl+Z: Undo last rename
• Delete/Backspace: Remove selected image
• F1: Show this help

FEATURES:
• Safe renaming with preview
• Undo capability for peace of mind
• Multiple naming format options
• Automatic file sorting
• Real-time preview updates
• Double-click a row to preview the image
• Right-click to remove or preview image
• Drag and drop images into the window
• Clear button to reset selection
• Option to delete originals after export
• Customizable export location

SUPPORTED FORMATS:
JPG, JPEG, PNG, GIF, BMP, WEBP, TIFF

EXPORT LOCATION:
• Default: Files are exported to a folder next to this script
• Custom: Click "Browse..." to choose a different directory
• Click "Reset" to return to the default location
• The folder name is based on your chosen base name

DELETE ORIGINALS:
• Check "Delete original files after export" to remove source files
• WARNING: This action cannot be undone!
• Original files are permanently deleted after successful export
• Use with caution - make sure you have backups if needed

TIPS:
• Always preview before renaming
• Use descriptive base names
• Undo is available only if originals were NOT deleted
• Files are sorted alphabetically before renaming
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("550x640")
        help_window.configure(bg=self.colors['bg_main'])
        help_window.transient(self.root)
        
        # Center the help window
        help_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 275
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 320
        help_window.geometry(f"550x640+{x}+{y}")
        
        # Header
        header = tk.Frame(help_window, bg=self.colors['primary'])
        header.pack(fill='x')
        
        title = tk.Label(header,
                        text="  Help & User Guide",
                        font=('Segoe UI', 11, 'bold'),
                        bg=self.colors['primary'],
                        fg='white')
        title.pack(side='left', pady=10, padx=8)
        
        # Main frame
        main_frame = tk.Frame(help_window, bg=self.colors['bg_main'])
        main_frame.pack(fill='both', expand=True, padx=16, pady=16)
        
        # Content frame
        text_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        text_frame.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        text_widget = tk.Text(text_frame,
                             wrap='word',
                             font=('Segoe UI', 10),
                             bg='white',
                             fg=self.colors['text_primary'],
                             relief='flat',
                             padx=16,
                             pady=16,
                             yscrollcommand=scrollbar.set)
        text_widget.pack(fill='both', expand=True)
        scrollbar.config(command=text_widget.yview)
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
        
        # Button frame
        btn_frame = tk.Frame(help_window, bg=self.colors['bg_main'])
        btn_frame.pack(fill='x', padx=16, pady=(0, 16))
        
        close_btn = ttk.Button(btn_frame,
                              text="Close",
                              command=help_window.destroy,
                              style='Primary.TButton')
        close_btn.pack(side='right')
    
    def show_credits(self):
        """Display credits dialog"""
        credits_window = tk.Toplevel(self.root)
        credits_window.title("About PhotoBatch")
        credits_window.geometry("480x550")
        credits_window.configure(bg=self.colors['bg_main'])
        credits_window.resizable(False, False)
        credits_window.transient(self.root)
        credits_window.grab_set()
        
        # Set icon for credits window too
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
            if os.path.exists(icon_path):
                credits_window.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Center the credits window
        credits_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 240
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 275
        credits_window.geometry(f"480x550+{x}+{y}")
        
        # Header
        header = tk.Frame(credits_window, bg=self.colors['primary'])
        header.pack(fill='x')
        
        title = tk.Label(header,
                        text="  About PhotoBatch",
                        font=('Segoe UI', 11, 'bold'),
                        bg=self.colors['primary'],
                        fg='white')
        title.pack(side='left', pady=12, padx=8)
        
        # Main content frame
        main_frame = tk.Frame(credits_window, bg=self.colors['bg_card'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # App title
        app_title = tk.Label(main_frame,
                            text="PhotoBatch",
                            font=('Segoe UI', 20, 'bold'),
                            bg=self.colors['bg_card'],
                            fg=self.colors['primary'])
        app_title.pack(pady=(30, 8))
        
        # Tagline
        tagline = tk.Label(main_frame,
                          text="Batch Image Renaming Made Simple",
                          font=('Segoe UI', 10, 'italic'),
                          bg=self.colors['bg_card'],
                          fg=self.colors['text_secondary'])
        tagline.pack()
        
        # Version
        version_label = tk.Label(main_frame,
                                text="Version 1.0.0",
                                font=('Segoe UI', 10),
                                bg=self.colors['bg_card'],
                                fg=self.colors['text_secondary'])
        version_label.pack(pady=(5, 0))
        
        # Divider
        divider = tk.Frame(main_frame, height=1, bg=self.colors['border'])
        divider.pack(fill='x', pady=25, padx=40)
        
        # Credits info
        credits_text = """Created by the Interns of BSIT 2026

Developed with care for efficient image management.

Built with Python & Tkinter

Features:
• Batch rename with multiple formats
• Image preview & drag-and-drop
• Custom export locations
• Delete originals option
• Undo functionality

Thank you for using PhotoBatch!"""
        
        credits_label = tk.Label(main_frame,
                                text=credits_text,
                                font=('Segoe UI', 10),
                                bg=self.colors['bg_card'],
                                fg=self.colors['text_primary'],
                                justify='center')
        credits_label.pack(pady=(0, 25))
        
        # Copyright
        copyright_label = tk.Label(main_frame,
                                  text="© 2026 All Rights Reserved",
                                  font=('Segoe UI', 9),
                                  bg=self.colors['bg_card'],
                                  fg=self.colors['text_secondary'])
        copyright_label.pack(side='bottom', pady=(0, 20))
        
        # Button frame
        btn_frame = tk.Frame(credits_window, bg=self.colors['bg_main'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        close_btn = ttk.Button(btn_frame,
                              text="Close",
                              command=credits_window.destroy,
                              style='Primary.TButton')
        close_btn.pack(side='right')

if __name__ == "__main__":
    if DND_AVAILABLE:
        # Try to use TkinterDnD for drag-and-drop support
        root = TkinterDnD.Tk()
    else:
        # Fall back to regular Tk if TkinterDnD not available
        root = tk.Tk()
    
    app = ModernImageRenamer(root)
    root.mainloop()