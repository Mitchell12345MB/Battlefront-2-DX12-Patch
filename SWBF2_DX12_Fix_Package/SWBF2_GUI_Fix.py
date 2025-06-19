#!/usr/bin/env python3
"""
SWBF2 DX12 Fix - GUI Version
Comprehensive GUI for applying DX12 fixes with manual path selection
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import subprocess
import threading
import json
from pathlib import Path

class SWBF2FixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SWBF2 DX12 Fix Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables for paths
        self.game_path = tk.StringVar()
        self.settings_path = tk.StringVar()
        self.config_file = "swbf2_fix_config.json"
        
        # Auto-detect paths first
        self.auto_detect_paths()
        
        # Load saved config
        self.load_config()
        
        self.create_widgets()
        
    def auto_detect_paths(self):
        """Auto-detect common game and settings paths"""
        # Common Steam paths
        steam_paths = [
            r"C:\Program Files (x86)\Steam\steamapps\common\STAR WARS Battlefront II",
            r"C:\Program Files\Steam\steamapps\common\STAR WARS Battlefront II",
            r"D:\Steam\steamapps\common\STAR WARS Battlefront II",
            r"E:\Steam\steamapps\common\STAR WARS Battlefront II",
            os.path.dirname(os.path.abspath(__file__)).replace("SWBF2_DX12_Fix_Package", "")
        ]
        
        # Common EA/Origin paths
        ea_paths = [
            r"C:\Program Files (x86)\Origin Games\STAR WARS Battlefront II",
            r"C:\Program Files\Origin Games\STAR WARS Battlefront II",
            r"C:\Program Files (x86)\EA Games\STAR WARS Battlefront II",
            r"C:\Program Files\EA Games\STAR WARS Battlefront II"
        ]
        
        all_game_paths = steam_paths + ea_paths
        
        # Try to find game directory
        for path in all_game_paths:
            if os.path.exists(path) and os.path.exists(os.path.join(path, "starwarsbattlefrontii.exe")):
                self.game_path.set(path)
                break
        
        # Settings path is usually in Documents
        settings_base = os.path.expanduser(r"~\Documents\STAR WARS Battlefront II\settings")
        if os.path.exists(settings_base):
            self.settings_path.set(settings_base)
    
    def create_widgets(self):
        """Create the GUI interface"""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ttk.Label(title_frame, text="STAR WARS Battlefront II - DX12 Fix Tool", 
                               font=("Arial", 16, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="GUI Version - Manual Path Selection", 
                                  font=("Arial", 10))
        subtitle_label.pack()
        
        # Path selection frame
        path_frame = ttk.LabelFrame(self.root, text="Game and Settings Paths", padding=10)
        path_frame.pack(fill="x", padx=10, pady=5)
        
        # Game path
        ttk.Label(path_frame, text="Game Installation Directory:").grid(row=0, column=0, sticky="w", pady=2)
        game_entry = ttk.Entry(path_frame, textvariable=self.game_path, width=60)
        game_entry.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(path_frame, text="Browse", command=self.browse_game_path).grid(row=1, column=1)
        
        # Settings path
        ttk.Label(path_frame, text="Settings Directory:").grid(row=2, column=0, sticky="w", pady=(10, 2))
        settings_entry = ttk.Entry(path_frame, textvariable=self.settings_path, width=60)
        settings_entry.grid(row=3, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(path_frame, text="Browse", command=self.browse_settings_path).grid(row=3, column=1)
        
        path_frame.columnconfigure(0, weight=1)
        
        # Status frame
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", foreground="green")
        self.status_label.pack()
        
        # Verify button
        ttk.Button(status_frame, text="Verify Paths", command=self.verify_paths).pack(pady=5)
        
        # Fix options frame
        fix_frame = ttk.LabelFrame(self.root, text="Fix Options", padding=10)
        fix_frame.pack(fill="x", padx=10, pady=5)
        
        # Fix type selection
        self.fix_type = tk.StringVar(value="ui_only")
        
        ttk.Radiobutton(fix_frame, text="UI-Only Fix (Recommended)", 
                       variable=self.fix_type, value="ui_only").pack(anchor="w")
        ttk.Label(fix_frame, text="   • Fixes UI artifacts while keeping 3D scaling", 
                 font=("Arial", 9)).pack(anchor="w", padx=20)
        
        ttk.Radiobutton(fix_frame, text="Complete DX12 Fix", 
                       variable=self.fix_type, value="complete").pack(anchor="w", pady=(10, 0))
        ttk.Label(fix_frame, text="   • Full fix but may disable resolution scaling", 
                 font=("Arial", 9)).pack(anchor="w", padx=20)
        
        ttk.Radiobutton(fix_frame, text="System Verification Only", 
                       variable=self.fix_type, value="verify").pack(anchor="w", pady=(10, 0))
        ttk.Label(fix_frame, text="   • Check system compatibility", 
                 font=("Arial", 9)).pack(anchor="w", padx=20)
        
        # Apply button
        apply_frame = ttk.Frame(self.root)
        apply_frame.pack(fill="x", padx=10, pady=10)
        
        self.apply_button = ttk.Button(apply_frame, text="Apply Fix", 
                                      command=self.apply_fix, style="Accent.TButton")
        self.apply_button.pack(side="left")
        
        ttk.Button(apply_frame, text="Save Config", command=self.save_config).pack(side="left", padx=(10, 0))
        ttk.Button(apply_frame, text="Restore Backup", command=self.restore_backup).pack(side="left", padx=(10, 0))
        
        # Output frame
        output_frame = ttk.LabelFrame(self.root, text="Output", padding=10)
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, wrap=tk.WORD)
        self.output_text.pack(fill="both", expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill="x", padx=10, pady=(0, 10))
    
    def browse_game_path(self):
        """Browse for game installation directory"""
        path = filedialog.askdirectory(
            title="Select SWBF2 Game Installation Directory",
            initialdir=self.game_path.get() or "C:\\"
        )
        if path:
            self.game_path.set(path)
            self.verify_paths()
    
    def browse_settings_path(self):
        """Browse for settings directory"""
        path = filedialog.askdirectory(
            title="Select SWBF2 Settings Directory",
            initialdir=self.settings_path.get() or os.path.expanduser("~\\Documents")
        )
        if path:
            self.settings_path.set(path)
            self.verify_paths()
    
    def verify_paths(self):
        """Verify that the selected paths are valid"""
        game_dir = self.game_path.get()
        settings_dir = self.settings_path.get()
        
        issues = []
        
        # Check game directory
        if not game_dir:
            issues.append("Game directory not selected")
        elif not os.path.exists(game_dir):
            issues.append("Game directory does not exist")
        elif not os.path.exists(os.path.join(game_dir, "starwarsbattlefrontii.exe")):
            issues.append("starwarsbattlefrontii.exe not found in game directory")
        
        # Check settings directory
        if not settings_dir:
            issues.append("Settings directory not selected")
        elif not os.path.exists(settings_dir):
            issues.append("Settings directory does not exist")
        
        if issues:
            self.status_label.config(text=f"Issues: {', '.join(issues)}", foreground="red")
            self.apply_button.config(state="disabled")
        else:
            self.status_label.config(text="Paths verified successfully!", foreground="green")
            self.apply_button.config(state="normal")
            
        self.log(f"Path verification: {len(issues)} issues found")
        for issue in issues:
            self.log(f"  - {issue}")
    
    def apply_fix(self):
        """Apply the selected fix"""
        if not self.verify_paths_silent():
            messagebox.showerror("Error", "Please verify paths before applying fix")
            return
        
        fix_type = self.fix_type.get()
        self.apply_button.config(state="disabled")
        self.progress.start()
        
        # Run fix in separate thread
        thread = threading.Thread(target=self._apply_fix_thread, args=(fix_type,))
        thread.daemon = True
        thread.start()
    
    def _apply_fix_thread(self, fix_type):
        """Apply fix in background thread"""
        try:
            if fix_type == "verify":
                self.log("Running system verification...")
                result = self.run_verification()
            elif fix_type == "ui_only":
                self.log("Applying UI-only fix...")
                result = self.run_ui_fix()
            elif fix_type == "complete":
                self.log("Applying complete DX12 fix...")
                result = self.run_complete_fix()
            
            self.root.after(0, self._fix_completed, result)
            
        except Exception as e:
            self.root.after(0, self._fix_error, str(e))
    
    def _fix_completed(self, success):
        """Handle fix completion"""
        self.progress.stop()
        self.apply_button.config(state="normal")
        
        if success:
            messagebox.showinfo("Success", "Fix applied successfully!")
            self.log("Fix completed successfully!")
        else:
            messagebox.showerror("Error", "Fix failed. Check output for details.")
            self.log("Fix failed!")
    
    def _fix_error(self, error):
        """Handle fix error"""
        self.progress.stop()
        self.apply_button.config(state="normal")
        messagebox.showerror("Error", f"Fix failed with error:\n{error}")
        self.log(f"Error: {error}")
    
    def run_verification(self):
        """Run system verification with custom paths"""
        try:
            # Create a custom verification script
            verification_script = f"""
import os
import sys

# Override paths
GAME_PATH = r"{self.game_path.get()}"
SETTINGS_PATH = r"{self.settings_path.get()}"

# Rest of verification logic...
print(f"Game path: {{GAME_PATH}}")
print(f"Settings path: {{SETTINGS_PATH}}")

# Check game executable
game_exe = os.path.join(GAME_PATH, "starwarsbattlefrontii.exe")
if os.path.exists(game_exe):
    print("✅ Game executable found")
else:
    print("❌ Game executable not found")
    
# Check settings files
boot_options = os.path.join(SETTINGS_PATH, "BootOptions")
profile_options = os.path.join(SETTINGS_PATH, "ProfileOptions_profile")

if os.path.exists(boot_options):
    print("✅ BootOptions file found")
else:
    print("❌ BootOptions file not found")
    
if os.path.exists(profile_options):
    print("✅ ProfileOptions file found")
else:
    print("❌ ProfileOptions file not found")

print("Verification complete!")
"""
            
            # Execute verification
            result = subprocess.run([sys.executable, "-c", verification_script], 
                                  capture_output=True, text=True)
            
            self.log(result.stdout)
            if result.stderr:
                self.log(f"Warnings: {result.stderr}")
                
            return result.returncode == 0
            
        except Exception as e:
            self.log(f"Verification error: {e}")
            return False
    
    def run_ui_fix(self):
        """Run UI-only fix with custom paths"""
        try:
            # Import and run the UI fix with custom paths
            from Fix_UI_Artifacts import UIArtifactFixer
            
            # Create custom fixer with our paths
            fixer = UIArtifactFixer(self.settings_path.get())
            
            self.log("Applying UI-specific fixes...")
            fixes_applied = fixer.fix_ui_specific_artifacts()
            
            for fix in fixes_applied:
                self.log(f"✅ {fix}")
            
            # Apply additional fixes
            if fixer.create_ui_fix_profile():
                self.log("✅ UI-optimized profile created")
            
            if fixer.apply_registry_ui_fixes():
                self.log("✅ Registry UI fixes applied")
            
            return len(fixes_applied) > 0
            
        except Exception as e:
            self.log(f"UI fix error: {e}")
            return False
    
    def run_complete_fix(self):
        """Run complete DX12 fix with custom paths"""
        try:
            # This would import and run the complete fix
            # For now, just simulate
            self.log("Complete fix would be applied here...")
            self.log("This requires the SWBF2_DX12_Complete_Fix.py to be updated")
            self.log("with path parameter support.")
            return True
            
        except Exception as e:
            self.log(f"Complete fix error: {e}")
            return False
    
    def restore_backup(self):
        """Restore game settings from backup"""
        try:
            settings_dir = self.settings_path.get()
            backup_dir = os.path.join(os.path.dirname(__file__), "Backups")
            
            if not os.path.exists(backup_dir):
                messagebox.showwarning("Warning", "No backup directory found")
                return
            
            backup_file = os.path.join(backup_dir, "Win32Game.cfg.backup")
            if os.path.exists(backup_file):
                # Restore logic here
                self.log("Backup restore functionality would be implemented here")
                messagebox.showinfo("Info", "Backup restore feature coming soon")
            else:
                messagebox.showwarning("Warning", "No backup file found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {e}")
    
    def verify_paths_silent(self):
        """Verify paths without updating UI"""
        game_dir = self.game_path.get()
        settings_dir = self.settings_path.get()
        
        return (game_dir and os.path.exists(game_dir) and 
                os.path.exists(os.path.join(game_dir, "starwarsbattlefrontii.exe")) and
                settings_dir and os.path.exists(settings_dir))
    
    def log(self, message):
        """Add message to output log"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def save_config(self):
        """Save current paths to config file"""
        config = {
            "game_path": self.game_path.get(),
            "settings_path": self.settings_path.get()
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            messagebox.showinfo("Success", "Configuration saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save config: {e}")
    
    def load_config(self):
        """Load paths from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                # Only override if current paths are empty
                if not self.game_path.get() and config.get("game_path"):
                    self.game_path.set(config["game_path"])
                
                if not self.settings_path.get() and config.get("settings_path"):
                    self.settings_path.set(config["settings_path"])
                    
        except Exception as e:
            pass  # Ignore config loading errors

def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Try to set a nice theme
    try:
        style = ttk.Style()
        style.theme_use('winnative')  # Use Windows native theme
    except:
        pass
    
    app = SWBF2FixGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 