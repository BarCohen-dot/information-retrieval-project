import tkinter as tk            # Standard GUI toolkit
from tkinter import messagebox  # For showing pop-up messages
from tkinter import filedialog  # For file save/load dialogs
import re                       # For validating search queries
import time                     # For timing the search duration
from Ranked_search import SearchEngine  # Custom backend for search functionality

# ================================================= introduction =======================================================
"""
# Run-in phase No. 5
--------------------

Modern Search Engine GUI

Author: Bar Cohen

Description:
A modern graphical user interface (GUI) for a ranked search engine using Tkinter.
The interface allows users to:
- Input a search word and run a ranked search.
- View up to 20 results formatted with metadata.
- Switch between light and dark modes.
- Reset the form or exit.
- Save or load results from/to a .txt file.

Features:
- Keyboard shortcuts (Enter to search, ESC to exit).
- Responsive layout and theme toggle.
- Input validation, error handling, and user feedback.
"""
# ======================================================================================================================

class SearchGUI:
    def __init__(self):
        """Initialize the GUI, theme, and event loop."""
        self.engine = SearchEngine()
        self.theme_mode = 'light'
        self._set_theme_colors()

        self.root = tk.Tk()
        self.root.title("Search Engine \U0001F50D")
        self.root.geometry("900x620")
        self.root.resizable(False, False)

        self._build_interface()
        self._apply_theme()
        self.root.mainloop()

    def _set_theme_colors(self):
        """Set the GUI color palette based on current theme."""
        if self.theme_mode == 'light':
            self.bg_color = "#f5f5f5"
            self.result_bg = "#ffffff"
            self.result_fg = "#000000"
            self.fg_color = "#000000"
            self.entry_bg = "#ffffff"
            self.entry_fg = "#000000"
            self.button_bg = "#ffffff"
            self.button_fg = "#000000"
            self.accent_bg = "#e0e0e0"
            self.border_color = "#cccccc"
        else:
            self.bg_color = "#1a1a1a"
            self.result_bg = "#1a1a1a"
            self.result_fg = "#ffffff"
            self.fg_color = "#000000"  # Intentional black text in dark mode
            self.entry_bg = "#000000"
            self.entry_fg = "#ffffff"
            self.button_bg = "#333333"
            self.button_fg = "#000000"
            self.accent_bg = "#444444"
            self.border_color = "#888888"

    def _build_interface(self):
        """Construct the layout and widgets of the interface."""
        self.top_frame = tk.Frame(self.root, bg=self.bg_color)
        self.top_frame.pack(fill=tk.X, pady=10, padx=10)

        self.theme_button = self._create_button(self.top_frame, "\U0001F319 Dark Mode", self.toggle_theme_mode)
        self.theme_button.pack(side=tk.LEFT)

        self.title_label = tk.Label(self.root, text="Enter a single word to search:",
                                    font=("Helvetica", 16, "bold"), bg=self.bg_color, fg=self.fg_color)
        self.title_label.pack(pady=8)

        self.input_field = tk.Entry(self.root, width=50, font=("Helvetica", 12),
                                    bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, relief="flat")
        self.input_field.pack(pady=5)
        self.input_field.focus_set()

        self.root.bind('<Return>', lambda e: self.search_word())
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=12)

        self.search_button = self._create_button(self.button_frame, "Run", self.search_word)
        self.reset_button = self._create_button(self.button_frame, "Reset", self.clear_fields)
        self.load_button = self._create_button(self.button_frame, "Load", self.load_results_from_file)
        self.exit_button = self._create_button(self.button_frame, "Exit", self.root.destroy)

        for btn in [self.search_button, self.reset_button, self.load_button, self.exit_button]:
            btn.pack(side=tk.LEFT, padx=8)

        self.result_container = tk.Frame(self.root, bg=self.bg_color)
        self.result_container.pack(pady=8, fill=tk.BOTH, expand=True)

        self.result_frame = tk.Frame(self.result_container, bg=self.result_bg)
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.result_box = tk.Text(self.result_frame, width=100, height=20, font=("Consolas", 10),
                                  bg=self.result_bg, fg=self.result_fg, insertbackground=self.result_fg,
                                  wrap="word", relief="flat", bd=2)
        self.result_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.result_frame, command=self.result_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_box.config(yscrollcommand=self.scrollbar.set)

        self.bottom_frame = tk.Frame(self.root, bg=self.bg_color)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        self.save_button = self._create_button(self.bottom_frame, "\U0001F4BE Save Results", self.save_results_to_file)
        self.save_button.config(width=18)
        self.save_button.pack(side=tk.RIGHT)

    def _apply_theme(self):
        """Apply colors to widgets based on the current theme."""
        self.root.configure(bg=self.bg_color)
        for widget in [self.top_frame, self.button_frame, self.bottom_frame, self.result_container]:
            widget.configure(bg=self.bg_color)

        self.title_label.configure(bg=self.bg_color, fg=self.fg_color)
        self.input_field.configure(bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.result_frame.configure(bg=self.result_bg)
        self.result_box.configure(bg=self.result_bg, fg=self.result_fg, insertbackground=self.result_fg)
        self.scrollbar.configure(bg=self.bg_color)

        for btn in [self.search_button, self.reset_button, self.exit_button, self.save_button, self.theme_button, self.load_button]:
            btn.configure(bg=self.button_bg, fg=self.button_fg,
                          activebackground=self.accent_bg, activeforeground=self.button_fg,
                          highlightbackground=self.border_color)

    def _create_button(self, parent, text, command):
        """Create a styled button for use in the interface."""
        return tk.Button(
            parent, text=text, command=command,
            font=("Helvetica", 10, "bold"), width=12,
            bg=self.button_bg, fg=self.button_fg,
            activebackground=self.accent_bg, activeforeground=self.button_fg,
            relief="flat", bd=0,
            highlightbackground=self.border_color,
            highlightthickness=1,
            padx=8, pady=6
        )

    def toggle_theme_mode(self):
        """Switch between light and dark mode themes."""
        self.theme_mode = 'dark' if self.theme_mode == 'light' else 'light'
        self._set_theme_colors()
        self._apply_theme()

    def search_word(self):
        """Validate and search for the word entered by the user."""
        try:
            word = self.input_field.get().strip()
            if not word:
                messagebox.showwarning("Warning", "Please enter a word to search.")
                return
            if len(word) > 30 or not re.match("^[a-zA-Z]+$", word):
                messagebox.showerror("Invalid", "Only alphabetic characters (max 30) are allowed.")
                return

            start = time.time()
            results = self.engine.search(word)
            duration = round(time.time() - start, 4)

            self.result_box.delete("1.0", tk.END)
            if not results:
                self.result_box.insert(tk.END, "⚠️ No matching posts found.\n")
                return

            self.result_box.insert(tk.END, f"🔍 Found {len(results)} results in {duration} seconds\n\n")
            for pid in results[:20]:
                self.result_box.insert(tk.END, f"• Post ID: {pid}\n")
                metadata = self.engine.post_metadata.get(pid, {})
                for k, v in metadata.items():
                    self.result_box.insert(tk.END, f"   - {k}: {v}\n")
                self.result_box.insert(tk.END, "\n")
        except Exception as e:
            print(f"❌ Error during search: {e}")
            messagebox.showerror("Search Error", str(e))

    def save_results_to_file(self):
        """Save the content of the result box to a .txt file."""
        try:
            content = self.result_box.get("1.0", tk.END).strip()
            if not content:
                messagebox.showwarning("No Data", "No results to save.")
                return

            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if not path:
                print("ℹ️ Save canceled by user.")
                return

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Success", f"Saved to {path}")
        except Exception as e:
            print(f"❌ Save error: {e}")
            messagebox.showerror("Save Error", str(e))

    def load_results_from_file(self):
        """Load previously saved results from a .txt file into the result box."""
        try:
            path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if not path:
                print("ℹ️ Load canceled by user.")
                return

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, content)
        except Exception as e:
            print(f"❌ Load error: {e}")
            messagebox.showerror("Load Error", str(e))

    def clear_fields(self):
        """Clear the search input and the results box."""
        try:
            self.input_field.delete(0, tk.END)
            self.result_box.delete("1.0", tk.END)
            self.input_field.focus_set()
        except Exception as e:
            print(f"❌ Reset error: {e}")
            messagebox.showerror("Reset Error", str(e))


# ===================================================== Main ===========================================================
if __name__ == '__main__':
    SearchGUI()
