import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import math
import random
from datetime import datetime

class KolamMath:
    """Mathematical foundations for Kolam patterns"""
    
    @staticmethod 
    def create_dot_grid(rows, cols, spacing=1.0):
        """Create a grid of dots - foundation of Kolam"""
        dots = []
        for i in range(rows):
            for j in range(cols):
                x = j * spacing
                y = i * spacing
                dots.append([x, y])
        return dots
    
    @staticmethod
    def create_circle_pattern(center, radius, points=8):
        """Create circular patterns around dots"""
        pattern = []
        for i in range(points):
            angle = 2 * math.pi * i / points
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            pattern.append([x, y])
        return pattern
    
    @staticmethod
    def create_petal_pattern(center, radius, petals=4):
        """Create petal/flower patterns"""
        pattern = []
        for i in range(petals):
            angle = 2 * math.pi * i / petals
            # Create petal shape using parametric equations
            for t in np.linspace(0, math.pi, 10):
                r = radius * math.sin(t)
                x = center[0] + r * math.cos(angle)
                y = center[1] + r * math.sin(angle)
                pattern.append([x, y])
        return pattern
    
    @staticmethod
    def create_spiral(center, max_radius, turns=2):
        """Create spiral patterns"""
        pattern = []
        steps = 50
        for i in range(steps):
            t = turns * 2 * math.pi * i / steps
            r = max_radius * i / steps
            x = center[0] + r * math.cos(t)
            y = center[1] + r * math.sin(t)
            pattern.append([x, y])
        return pattern
    
    @staticmethod
    def create_star_pattern(center, outer_radius, inner_radius, points=5):
        """Create star patterns"""
        pattern = []
        for i in range(points * 2):
            angle = math.pi * i / points
            if i % 2 == 0:
                radius = outer_radius
            else:
                radius = inner_radius
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            pattern.append([x, y])
        return pattern

class KolamAnalyzer:
    """Analyze Kolam patterns for mathematical principles"""
    
    @staticmethod
    def find_symmetries(points):
        """Find symmetries in the pattern"""
        if len(points) < 3:
            return []
        
        points = np.array(points)
        center = np.mean(points, axis=0)
        symmetries = []
        
        # Check for rotational symmetry
        for n in range(2, 9):
            if KolamAnalyzer._has_rotational_symmetry(points, center, n):
                symmetries.append(f"{n}-fold rotation")
        
        # Check for reflection symmetry
        if KolamAnalyzer._has_reflection_symmetry(points, center):
            symmetries.append("Reflection")
        
        return symmetries
    
    @staticmethod
    def _has_rotational_symmetry(points, center, n):
        """Check if pattern has n-fold rotational symmetry"""
        angle = 2 * math.pi / n
        tolerance = 0.5
        
        for point in points:
            # Rotate point around center
            dx, dy = point[0] - center[0], point[1] - center[1]
            new_x = center[0] + dx * math.cos(angle) - dy * math.sin(angle)
            new_y = center[1] + dx * math.sin(angle) + dy * math.cos(angle)
            
            # Check if rotated point exists in original set
            found = False
            for orig_point in points:
                dist = math.sqrt((orig_point[0] - new_x)**2 + (orig_point[1] - new_y)**2)
                if dist < tolerance:
                    found = True
                    break
            
            if not found:
                return False
        
        return True
    
    @staticmethod
    def _has_reflection_symmetry(points, center):
        """Check for reflection symmetry across vertical axis"""
        tolerance = 0.5
        
        for point in points:
            # Reflect across vertical line through center
            reflected_x = 2 * center[0] - point[0]
            reflected_y = point[1]
            
            # Check if reflected point exists
            found = False
            for orig_point in points:
                dist = math.sqrt((orig_point[0] - reflected_x)**2 + (orig_point[1] - reflected_y)**2)
                if dist < tolerance:
                    found = True
                    break
            
            if not found:
                return False
        
        return True
    
    @staticmethod
    def calculate_complexity(points):
        """Calculate pattern complexity"""
        if len(points) < 2:
            return 0
        
        points = np.array(points)
        
        # Calculate spread
        center = np.mean(points, axis=0)
        distances = [math.sqrt((p[0] - center[0])**2 + (p[1] - center[1])**2) for p in points]
        spread = max(distances) - min(distances) if distances else 0
        
        # Complexity based on number of points and spread
        complexity = min(10, len(points) // 5 + spread // 2)
        return int(complexity)

class KolamStudio:
    """Main Kolam design application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 Kolam Design Studio - Smart India Hackathon")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f5')
        
        # Application state
        self.current_pattern = []
        self.selected_color = '#FF6B35'
        self.grid_size = 10
        
        # Create UI
        self.setup_ui()
        
        # Welcome message
        self.show_welcome()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title bar
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🎨 Kolam Design Studio",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=15)
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#f5f5f5')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        self.create_control_panel(content_frame)
        
        # Center panel - Canvas
        self.create_canvas_panel(content_frame)
        
        # Right panel - Analysis
        self.create_analysis_panel(content_frame)
    
    def create_control_panel(self, parent):
        """Create control panel"""
        control_frame = tk.LabelFrame(
            parent,
            text="🎛️ Design Tools",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        control_frame.pack(side='left', fill='y', padx=(0, 5))
        
        # Grid controls
        grid_frame = tk.LabelFrame(control_frame, text="Grid Settings", bg='white')
        grid_frame.pack(fill='x', pady=5)
        
        tk.Label(grid_frame, text="Grid Size:", bg='white').pack(anchor='w')
        self.grid_var = tk.IntVar(value=10)
        grid_scale = tk.Scale(
            grid_frame,
            from_=5,
            to=20,
            orient='horizontal',
            variable=self.grid_var,
            bg='white'
        )
        grid_scale.pack(fill='x')
        
        tk.Button(
            grid_frame,
            text="📍 Show Grid",
            command=self.show_grid,
            bg='#3498db',
            fg='white'
        ).pack(fill='x', pady=2)
        
        # Pattern tools
        pattern_frame = tk.LabelFrame(control_frame, text="Pattern Tools", bg='white')
        pattern_frame.pack(fill='x', pady=5)
        
        patterns = [
            ("🌸 Flower", self.add_flower_pattern),
            ("⭐ Star", self.add_star_pattern),
            ("🌀 Spiral", self.add_spiral_pattern),
            ("⭕ Circle", self.add_circle_pattern)
        ]
        
        for text, command in patterns:
            tk.Button(
                pattern_frame,
                text=text,
                command=command,
                bg='#e74c3c',
                fg='white',
                width=15
            ).pack(fill='x', pady=1)
        
        # Color selection
        color_frame = tk.LabelFrame(control_frame, text="Colors", bg='white')
        color_frame.pack(fill='x', pady=5)
        
        color_btn_frame = tk.Frame(color_frame, bg='white')
        color_btn_frame.pack(fill='x')
        
        tk.Label(color_btn_frame, text="Color:", bg='white').pack(side='left')
        self.color_btn = tk.Button(
            color_btn_frame,
            text="🎨",
            command=self.choose_color,
            bg=self.selected_color,
            width=5
        )
        self.color_btn.pack(side='right')
        
        # Preset colors
        preset_frame = tk.Frame(color_frame, bg='white')
        preset_frame.pack(fill='x', pady=2)
        
        colors = ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#118AB2', '#073B4C']
        for i, color in enumerate(colors):
            btn = tk.Button(
                preset_frame,
                bg=color,
                width=2,
                height=1,
                command=lambda c=color: self.set_color(c)
            )
            btn.pack(side='left', padx=1)
        
        # Actions
        action_frame = tk.LabelFrame(control_frame, text="Actions", bg='white')
        action_frame.pack(fill='x', pady=5)
        
        actions = [
            ("🔍 Analyze", self.analyze_pattern, '#f39c12'),
            ("💾 Save", self.save_pattern, '#27ae60'),
            ("📁 Load", self.load_pattern, '#8e44ad'),
            ("🗑️ Clear", self.clear_pattern, '#e74c3c')
        ]
        
        for text, command, color in actions:
            tk.Button(
                action_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                width=15
            ).pack(fill='x', pady=1)
    
    def create_canvas_panel(self, parent):
        """Create drawing canvas"""
        canvas_frame = tk.LabelFrame(
            parent,
            text="🎨 Drawing Canvas",
            font=('Arial', 12, 'bold'),
            bg='white'
        )
        canvas_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 20)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Click to add points or use pattern tools", fontsize=12)
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, canvas_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Bind mouse events
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        
        # Update canvas
        self.update_canvas()
    
    def create_analysis_panel(self, parent):
        """Create analysis panel"""
        analysis_frame = tk.LabelFrame(
            parent,
            text="📊 Pattern Analysis",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        analysis_frame.pack(side='right', fill='y', padx=(5, 0))
        
        # Analysis results
        self.analysis_text = tk.Text(
            analysis_frame,
            width=30,
            height=20,
            bg='#f8f9fa',
            font=('Consolas', 9),
            wrap='word'
        )
        self.analysis_text.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(analysis_frame, command=self.analysis_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.analysis_text.config(yscrollcommand=scrollbar.set)
        
        # Initial message
        self.analysis_text.insert(tk.END, "🎨 Welcome to Kolam Studio!\n\n")
        self.analysis_text.insert(tk.END, "Create beautiful Kolam patterns and analyze their mathematical properties.\n\n")
        self.analysis_text.insert(tk.END, "Features:\n")
        self.analysis_text.insert(tk.END, "• Interactive drawing\n")
        self.analysis_text.insert(tk.END, "• Pattern generation\n")
        self.analysis_text.insert(tk.END, "• Symmetry analysis\n")
        self.analysis_text.insert(tk.END, "• Save/Load designs\n\n")
        self.analysis_text.insert(tk.END, "Start by clicking on the canvas or using pattern tools!")
    
    def show_welcome(self):
        """Show welcome dialog"""
        welcome_msg = """🎨 Welcome to Kolam Design Studio!

This application helps you:
• Create traditional Kolam patterns
• Analyze mathematical properties
• Understand design principles
• Save and share your creations

Perfect for Smart India Hackathon!

Click OK to start designing."""
        
        messagebox.showinfo("Welcome", welcome_msg)
    
    def on_canvas_click(self, event):
        """Handle canvas clicks"""
        if event.inaxes:
            x, y = event.xdata, event.ydata
            self.current_pattern.append([x, y])
            self.update_canvas()
            self.update_analysis_live()
    
    def update_canvas(self):
        """Update the canvas display"""
        self.ax.clear()
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 20)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        
        if self.current_pattern:
            points = np.array(self.current_pattern)
            
            # Draw points
            self.ax.scatter(
                points[:, 0], 
                points[:, 1],
                c=self.selected_color,
                s=60,
                alpha=0.8,
                edgecolors='black',
                linewidth=1
            )
            
            # Connect points if more than 1
            if len(points) > 1:
                self.ax.plot(
                    points[:, 0],
                    points[:, 1],
                    color=self.selected_color,
                    alpha=0.6,
                    linewidth=2
                )
        
        self.ax.set_title(f"Kolam Pattern - {len(self.current_pattern)} points", fontsize=12)
        self.canvas.draw()
    
    def show_grid(self):
        """Show dot grid"""
        grid_size = self.grid_var.get()
        dots = KolamMath.create_dot_grid(grid_size, grid_size, 20/grid_size)
        
        # Add grid dots to pattern
        for dot in dots:
            self.current_pattern.append(dot)
        
        self.update_canvas()
        self.update_analysis_live()
    
    def add_flower_pattern(self):
        """Add flower pattern at center"""
        center = [10, 10]
        flower = KolamMath.create_petal_pattern(center, 3, 6)
        self.current_pattern.extend(flower)
        self.update_canvas()
        self.update_analysis_live()
    
    def add_star_pattern(self):
        """Add star pattern"""
        center = [10, 10]
        star = KolamMath.create_star_pattern(center, 4, 2, 5)
        self.current_pattern.extend(star)
        self.update_canvas()
        self.update_analysis_live()
    
    def add_spiral_pattern(self):
        """Add spiral pattern"""
        center = [10, 10]
        spiral = KolamMath.create_spiral(center, 5, 3)
        self.current_pattern.extend(spiral)
        self.update_canvas()
        self.update_analysis_live()
    
    def add_circle_pattern(self):
        """Add circle pattern"""
        center = [10, 10]
        circle = KolamMath.create_circle_pattern(center, 4, 12)
        self.current_pattern.extend(circle)
        self.update_canvas()
        self.update_analysis_live()
    
    def choose_color(self):
        """Choose custom color"""
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            self.selected_color = color
            self.color_btn.config(bg=color)
    
    def set_color(self, color):
        """Set preset color"""
        self.selected_color = color
        self.color_btn.config(bg=color)
    
    def analyze_pattern(self):
        """Analyze current pattern"""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "No pattern to analyze!")
            return
        
        # Perform analysis
        symmetries = KolamAnalyzer.find_symmetries(self.current_pattern)
        complexity = KolamAnalyzer.calculate_complexity(self.current_pattern)
        
        # Calculate center and spread
        points = np.array(self.current_pattern)
        center = np.mean(points, axis=0)
        distances = [math.sqrt((p[0] - center[0])**2 + (p[1] - center[1])**2) for p in points]
        avg_distance = sum(distances) / len(distances) if distances else 0
        
        # Display results
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "🔍 KOLAM PATTERN ANALYSIS\n")
        self.analysis_text.insert(tk.END, "=" * 30 + "\n\n")
        
        self.analysis_text.insert(tk.END, f"📊 Basic Properties:\n")
        self.analysis_text.insert(tk.END, f"• Points: {len(self.current_pattern)}\n")
        self.analysis_text.insert(tk.END, f"• Center: ({center[0]:.1f}, {center[1]:.1f})\n")
        self.analysis_text.insert(tk.END, f"• Avg Radius: {avg_distance:.1f}\n")
        self.analysis_text.insert(tk.END, f"• Complexity: {complexity}/10\n\n")
        
        self.analysis_text.insert(tk.END, f"🔄 Symmetries Found:\n")
        if symmetries:
            for sym in symmetries:
                self.analysis_text.insert(tk.END, f"✓ {sym}\n")
        else:
            self.analysis_text.insert(tk.END, "• No clear symmetries\n")
        
        self.analysis_text.insert(tk.END, f"\n🎨 Design Classification:\n")
        
        # Classify the design
        if len(symmetries) >= 2:
            classification = "Traditional Kolam"
            score = "Excellent"
        elif len(symmetries) == 1:
            classification = "Semi-Traditional"
            score = "Good"
        else:
            classification = "Modern/Abstract"
            score = "Creative"
        
        self.analysis_text.insert(tk.END, f"• Type: {classification}\n")
        self.analysis_text.insert(tk.END, f"• Score: {score}\n")
        
        # Mathematical principles
        self.analysis_text.insert(tk.END, f"\n📐 Mathematical Principles:\n")
        self.analysis_text.insert(tk.END, f"• Geometric harmony: {len(symmetries) * 20}%\n")
        self.analysis_text.insert(tk.END, f"• Pattern density: {min(100, len(self.current_pattern) * 2)}%\n")
        self.analysis_text.insert(tk.END, f"• Spatial balance: {min(100, complexity * 10)}%\n")
        
        self.analysis_text.insert(tk.END, f"\n⏰ Analysis completed at {datetime.now().strftime('%H:%M:%S')}")
    
    def update_analysis_live(self):
        """Update analysis in real-time"""
        if len(self.current_pattern) > 2:
            complexity = KolamAnalyzer.calculate_complexity(self.current_pattern)
            symmetries = KolamAnalyzer.find_symmetries(self.current_pattern)
            
            # Update just the basic info
            info = f"\n📊 Live Stats:\n"
            info += f"Points: {len(self.current_pattern)}\n"
            info += f"Complexity: {complexity}/10\n"
            info += f"Symmetries: {len(symmetries)}\n"
            
            # Add to end of text
            current_text = self.analysis_text.get(1.0, tk.END)
            if "📊 Live Stats:" in current_text:
                # Replace existing stats
                lines = current_text.split('\n')
                new_lines = []
                skip = False
                for line in lines:
                    if "📊 Live Stats:" in line:
                        skip = True
                    elif skip and line.strip() == "":
                        skip = False
                    elif not skip:
                        new_lines.append(line)
                
                self.analysis_text.delete(1.0, tk.END)
                self.analysis_text.insert(tk.END, '\n'.join(new_lines))
            
            self.analysis_text.insert(tk.END, info)
    
    def save_pattern(self):
        """Save current pattern"""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "No pattern to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                data = {
                    'pattern': self.current_pattern,
                    'color': self.selected_color,
                    'timestamp': datetime.now().isoformat(),
                    'analysis': {
                        'points': len(self.current_pattern),
                        'complexity': KolamAnalyzer.calculate_complexity(self.current_pattern),
                        'symmetries': KolamAnalyzer.find_symmetries(self.current_pattern)
                    }
                }
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                messagebox.showinfo("Success", f"Pattern saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def load_pattern(self):
        """Load pattern from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                self.current_pattern = data['pattern']
                if 'color' in data:
                    self.selected_color = data['color']
                    self.color_btn.config(bg=self.selected_color)
                
                self.update_canvas()
                messagebox.showinfo("Success", f"Pattern loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")
    
    def clear_pattern(self):
        """Clear current pattern"""
        if self.current_pattern:
            result = messagebox.askyesno("Confirm", "Clear current pattern?")
            if result:
                self.current_pattern = []
                self.update_canvas()
                
                self.analysis_text.delete(1.0, tk.END)
                self.analysis_text.insert(tk.END, "Canvas cleared! 🎨\n\n")
                self.analysis_text.insert(tk.END, "Ready for new Kolam design.\n")
                self.analysis_text.insert(tk.END, "Click on canvas or use pattern tools to start.")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = KolamStudio()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")

if __name__ == "__main__":

    main()
