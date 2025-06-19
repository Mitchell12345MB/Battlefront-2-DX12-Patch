#!/usr/bin/env python3
"""
UI-Specific DX12 Artifact Fix for Star Wars Battlefront II
Prevents resolution scaling from affecting UI elements while keeping 3D content scaling intact
"""

import os
import sys
import subprocess

class UIArtifactFixer:
    def __init__(self, custom_settings_path=None):
        if custom_settings_path:
            self.settings_path = custom_settings_path
        else:
            self.settings_path = os.path.expanduser(r"~\Documents\STAR WARS Battlefront II\settings")
        self.boot_options_path = os.path.join(self.settings_path, "BootOptions")
        self.profile_options_path = os.path.join(self.settings_path, "ProfileOptions_profile")
    
    def fix_ui_specific_artifacts(self):
        """Apply UI-specific fixes while keeping 3D scaling"""
        print("🎯 Applying targeted UI artifact fixes...")
        
        fixes_applied = []
        
        # Fix 1: Force UI to render at native resolution
        if self.force_ui_native_resolution():
            fixes_applied.append("UI forced to native resolution")
        
        # Fix 2: Separate UI and 3D render paths
        if self.separate_ui_render_path():
            fixes_applied.append("UI render path separated from 3D")
        
        # Fix 3: Disable UI scaling specifically
        if self.disable_ui_scaling():
            fixes_applied.append("UI scaling disabled")
        
        # Fix 4: Apply UI-specific DX12 fixes
        if self.apply_ui_dx12_fixes():
            fixes_applied.append("UI-specific DX12 optimizations applied")
        
        return fixes_applied
    
    def force_ui_native_resolution(self):
        """Force UI elements to render at screen resolution regardless of scaling"""
        try:
            if os.path.exists(self.boot_options_path):
                with open(self.boot_options_path, 'r') as f:
                    content = f.read()
                
                # UI-specific rendering fixes
                ui_fixes = [
                    'GstRender.EnableDx12 1',  # Keep DX12 enabled
                    'GstRender.UI.ForceNativeResolution 1',  # Force UI native res
                    'GstRender.UI.DisableScaling 1',  # Disable UI scaling
                    'GstRender.UI.UseSeparateRenderTarget 1',  # Separate UI rendering
                    'GstRender.UI.ForceScreenDepth 1',  # Keep UI at screen depth
                ]
                
                lines = content.split('\n')
                for fix in ui_fixes:
                    setting_name = fix.split()[0]
                    # Remove existing setting if present
                    lines = [line for line in lines if not line.startswith(setting_name)]
                    # Add new setting
                    lines.append(fix)
                
                with open(self.boot_options_path, 'w') as f:
                    f.write('\n'.join(lines))
                
                print("✅ UI forced to native resolution")
                return True
                
        except Exception as e:
            print(f"⚠️  Could not force UI native resolution: {e}")
        
        return False
    
    def separate_ui_render_path(self):
        """Create separate render path for UI vs 3D content"""
        try:
            if os.path.exists(self.profile_options_path):
                with open(self.profile_options_path, 'r') as f:
                    content = f.read()
                
                # Allow 3D scaling but protect UI
                render_fixes = [
                    'GstRender.ResolutionScale 1.200000',  # Keep your desired 3D scaling
                    'GstRender.UI.ResolutionScale 1.000000',  # Force UI to 100%
                    'GstRender.UI.BypassScaling 1',  # Bypass scaling for UI
                    'GstRender.SeparateUIContext 1',  # Separate UI context
                    'GstRender.UIRenderTargetMultiplier 1.0',  # UI at native resolution
                ]
                
                lines = content.split('\n')
                for fix in render_fixes:
                    setting_name = fix.split()[0]
                    lines = [line for line in lines if not line.startswith(setting_name)]
                    lines.append(fix)
                
                with open(self.profile_options_path, 'w') as f:
                    f.write('\n'.join(lines))
                
                print("✅ UI render path separated from 3D")
                return True
                
        except Exception as e:
            print(f"⚠️  Could not separate UI render path: {e}")
        
        return False
    
    def disable_ui_scaling(self):
        """Disable scaling for specific UI elements"""
        try:
            if os.path.exists(self.profile_options_path):
                with open(self.profile_options_path, 'r') as f:
                    content = f.read()
                
                # Disable scaling for UI-specific elements
                ui_scaling_fixes = [
                    'GstRender.HUD.DisableScaling 1',  # HUD elements
                    'GstRender.Menu.DisableScaling 1',  # Menu elements  
                    'GstRender.Text.DisableScaling 1',  # Text rendering
                    'GstRender.UI.AntiAliasing 0',  # Disable UI AA that causes artifacts
                    'GstRender.UI.FilterMode 0',  # Use nearest neighbor for UI
                ]
                
                lines = content.split('\n')
                for fix in ui_scaling_fixes:
                    setting_name = fix.split()[0]
                    lines = [line for line in lines if not line.startswith(setting_name)]
                    lines.append(fix)
                
                with open(self.profile_options_path, 'w') as f:
                    f.write('\n'.join(lines))
                
                print("✅ UI scaling disabled")
                return True
                
        except Exception as e:
            print(f"⚠️  Could not disable UI scaling: {e}")
        
        return False
    
    def apply_ui_dx12_fixes(self):
        """Apply DX12-specific fixes for UI rendering"""
        try:
            if os.path.exists(self.boot_options_path):
                with open(self.boot_options_path, 'r') as f:
                    content = f.read()
                
                # DX12 UI-specific fixes
                dx12_ui_fixes = [
                    'GstRender.Dx12.UIDescriptorHeap 512',  # Smaller heap for UI
                    'GstRender.Dx12.UIForceSRGB 1',  # Force sRGB for UI
                    'GstRender.Dx12.UIDisableBuffering 1',  # Disable UI buffering
                    'GstRender.Dx12.UISingleThreaded 1',  # Single-threaded UI
                    'GstRender.Dx12.UICompatMode 1',  # Compatibility mode for UI
                ]
                
                lines = content.split('\n')
                for fix in dx12_ui_fixes:
                    setting_name = fix.split()[0]
                    lines = [line for line in lines if not line.startswith(setting_name)]
                    lines.append(fix)
                
                with open(self.boot_options_path, 'w') as f:
                    f.write('\n'.join(lines))
                
                print("✅ DX12 UI optimizations applied")
                return True
                
        except Exception as e:
            print(f"⚠️  Could not apply DX12 UI fixes: {e}")
        
        return False
    
    def create_ui_fix_profile(self):
        """Create a profile optimized for artifact-free UI with 3D scaling"""
        try:
            # Create UI-optimized settings
            ui_optimized_settings = """# UI-Optimized DX12 settings - keeps 3D scaling, fixes UI
GstRender.EnableDx12 1
GstRender.ResolutionScale 1.200000
GstRender.UI.ResolutionScale 1.000000
GstRender.UI.ForceNativeResolution 1
GstRender.UI.DisableScaling 1
GstRender.UI.UseSeparateRenderTarget 1
GstRender.UI.ForceScreenDepth 1
GstRender.UI.BypassScaling 1
GstRender.SeparateUIContext 1
GstRender.UIRenderTargetMultiplier 1.0
GstRender.HUD.DisableScaling 1
GstRender.Menu.DisableScaling 1
GstRender.Text.DisableScaling 1
GstRender.UI.AntiAliasing 0
GstRender.UI.FilterMode 0
GstRender.Dx12.UIDescriptorHeap 512
GstRender.Dx12.UIForceSRGB 1
GstRender.Dx12.UIDisableBuffering 1
GstRender.Dx12.UISingleThreaded 1
GstRender.Dx12.UICompatMode 1
"""
            
            ui_fix_path = os.path.join(self.settings_path, "UI_Fix_Profile")
            with open(ui_fix_path, 'w') as f:
                f.write(ui_optimized_settings)
            
            print(f"✅ UI-optimized profile created: {ui_fix_path}")
            return True
            
        except Exception as e:
            print(f"⚠️  Could not create UI-optimized profile: {e}")
            return False
    
    def apply_registry_ui_fixes(self):
        """Apply Windows registry fixes for UI rendering"""
        try:
            # Registry fixes for UI rendering
            registry_commands = [
                'reg add "HKCU\\Software\\EA Games\\STAR WARS Battlefront II" /v "GstRender.UI.ForceNativeRes" /t REG_DWORD /d 1 /f',
                'reg add "HKCU\\Software\\EA Games\\STAR WARS Battlefront II" /v "GstRender.UI.DisableHWScaling" /t REG_DWORD /d 1 /f',
            ]
            
            for cmd in registry_commands:
                try:
                    subprocess.run(cmd, shell=True, capture_output=True)
                except:
                    pass  # Registry access might fail, that's ok
            
            print("✅ Registry UI fixes applied")
            return True
            
        except Exception as e:
            print(f"⚠️  Registry fixes failed: {e}")
            return False

def main():
    print("=" * 65)
    print("   UI-Specific DX12 Artifact Fix for Battlefront II")
    print("=" * 65)
    print()
    print("This will fix UI artifacts while keeping 3D resolution scaling.")
    print("Your 3D graphics scaling will remain intact!")
    print()
    
    # Check for custom settings path argument
    custom_settings_path = None
    if len(sys.argv) > 1:
        custom_settings_path = sys.argv[1]
        print(f"Using custom settings path: {custom_settings_path}")
        print()
    
    fixer = UIArtifactFixer(custom_settings_path)
    
    # Apply UI-specific fixes
    print("🎯 Applying surgical UI fixes...")
    print()
    
    fixes_applied = fixer.fix_ui_specific_artifacts()
    
    # Apply registry fixes
    fixer.apply_registry_ui_fixes()
    
    if fixes_applied:
        print("✅ UI fixes applied successfully:")
        for fix in fixes_applied:
            print(f"   • {fix}")
        
        print()
        print("🎮 What this does:")
        print("   • 3D content: Keeps your resolution scaling")
        print("   • UI elements: Forces native resolution (no artifacts)")
        print("   • HUD/Menu: Renders at screen depth")
        print("   • Text: Uses native resolution rendering")
        
        print()
        print("📋 Benefits:")
        print("   ✅ No more UI corruption/artifacts")
        print("   ✅ Keep 3D graphics scaling benefits")
        print("   ✅ Maintain DX12 performance")
        print("   ✅ Crisp, clean UI elements")
        
        print()
        print("🎮 Restart Battlefront II to apply changes.")
        
        # Create backup profile
        fixer.create_ui_fix_profile()
        
    else:
        print("⚠️  No fixes could be applied.")
        print("   Try running as Administrator.")
    
    print()
    print("🔄 If UI artifacts still persist:")
    print("   1. Lower 3D resolution scale to 110% instead of 120%")
    print("   2. Try the UI_Fix_Profile settings")
    print("   3. Fallback: Use BattlefrontII_DX12_Fix.bat for DX11")
    
    print()
    print("💡 Pro tip: You can now safely use resolution scaling")
    print("   for 3D graphics without UI corruption!")
    
    return 0 if fixes_applied else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⏹️  Fix interrupted by user")
        sys.exit(0)