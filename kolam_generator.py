import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
import cv2
from PIL import Image, ImageTk
import json
import math
import random
from datetime import datetime

class KolamDesignPrinciples:
    """Core mathematical principles behind Kolam designs"""
    
    @staticmethod
    def generate_dot_grid(rows, cols, spacing=1):
        """Generate a grid of dots as the foundation"""
        dots = []
        for i in range(rows):
            for j in range(cols):
                dots.append((j * spacing, i * spacing))
        return np.array(dots)
    
    @staticmethod
    def create_symmetrical_pattern(center, radius, symmetry_order=4):
        """Create symmetrical patterns around a center point"""
        angles = np.linspace(0, 2*np.pi, symmetry_order, endpoint=False)
        points = []
        for angle in angles:
            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)
            points.append((x, y))
        return points
    
    @staticmethod
    def generate_spiral_pattern(center, max_radius, turns=3):
        """Generate spiral patterns common in Kolams"""
        points = []
        t = np.linspace(0, turns * 2 * np.pi, 100)
        for angle in t:
            radius = max_radius * angle / (turns * 2 * np.pi)
            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)
            points.append((x, y))
        return points
    
    @staticmethod
    def create_mandala_pattern(center, layers=3):
        """Create mandala-style patterns"""
        patterns = []
        for layer in range(1, layers + 1):
            radius = layer * 2
            symmetry = 4 + layer * 2
            layer_pattern = KolamDesignPrinciples.create_symmetrical_pattern(
                center, radius, symmetry
            )
            patterns.extend(layer_pattern)
        return patterns

class KolamAI:
    """AI-powered Kolam pattern recognition and generation"""
    
    def __init__(self):
        self.pattern_database = {
            'traditional': ['lotus', 'peacock', 'geometric', 'floral'],
            'modern': ['abstract', 'fusion', 'digital'],
            'regional': ['tamil', 'andhra', 'karnataka', 'kerala']
        }
        
    def analyze_symmetry(self, points):
        """Analyze symmetry in a given pattern"""
        center = np.mean(points, axis=0)
        symmetries = []
        
        for order in range(2, 9):
            if self._check_rotational_symmetry(points, center, order):
                symmetries.append(f"{order}-fold rotational")
        
        if self._check_reflection_symmetry(points, center):
            symmetries.append("reflection")
            
        return symmetries
    
    def _check_rotational_symmetry(self, points, center, order):
        """Check if pattern has rotational symmetry"""
        angle = 2 * np.pi / order
        tolerance = 0.5
        
        for point in points:
            rotated_point = self._rotate_point(point, center, angle)
            if not self._point_exists_nearby(rotated_point, points, tolerance):
                return False
        return True
    
    def _check_reflection_symmetry(self, points, center):
        """Check if pattern has reflection symmetry"""
        tolerance = 0.5
        for point in points:
            reflected_point = (2 * center[0] - point[0], point[1])
            if not self._point_exists_nearby(reflected_point, points, tolerance):
                return False
        return True
    
    def _rotate_point(self, point, center, angle):
        """Rotate a point around center by given angle"""
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        dx, dy = point[0] - center[0], point[1] - center[1]
        new_x = center[0] + dx * cos_a - dy * sin_a
        new_y = center[1] + dx * sin_a + dy * cos_a
        return (new_x, new_y)
    
    def _point_exists_nearby(self, target, points, tolerance):
        """Check if a point exists within tolerance"""
        for point in points:
            distance = np.sqrt((point[0] - target[0])**2 + (point[1] - target[1])**2)
            if distance <= tolerance:
                return True
        return False
    
    def generate_ai_kolam(self, style='traditional', complexity=5):
        """Generate AI-powered Kolam based on learned patterns"""
        center = (10, 10)
        
        if style == 'traditional':
            return self._generate_traditional_kolam(center, complexity)
        elif style == 'modern':
            return self._generate_modern_kolam(center, complexity)
        else:
            return self._generate_fusion_kolam(center, complexity)
    
    def _generate_traditional_kolam(self, center, complexity):
        """Generate traditional Kolam patterns"""
        patterns = []
        
        # Central mandala
        patterns.extend(KolamDesignPrinciples.create_mandala_pattern(center, complexity))
        
        # Surrounding spirals
        for i in range(4):
            angle = i * np.pi / 2
            spiral_center = (
                center[0] + 8 * np.cos(angle),
                center[1] + 8 * np.sin(angle)
            )
            patterns.extend(KolamDesignPrinciples.generate_spiral_pattern(
                spiral_center, 3, 2
            ))
        
        return patterns
    
    def _generate_modern_kolam(self, center, complexity):
        """Generate modern abstract Kolam patterns"""
        patterns = []
        
        # Fractal-like patterns
        for level in range(complexity):
            radius = 2 + level * 1.5
            sides = 3 + level
            pattern = KolamDesignPrinciples.create_symmetrical_pattern(
                center, radius, sides
            )
            patterns.extend(pattern)
        
        return patterns
    
    def _generate_fusion_kolam(self, center, complexity):
        """Generate fusion of traditional and modern"""
        traditional = self._generate_traditional_kolam(center, complexity // 2)
        modern = self._generate_modern_kolam(center, complexity // 2)
        return traditional + modern

class KolamStudio:
    """Main GUI application for Kolam design and analysis"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 AI Kolam Studio - Smart India Hackathon")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.kolam_ai = KolamAI()
        self.current_pattern = []
        self.drawing_mode = False
        self.selected_color = '#FF6B35'
        
        # Create UI
        self.create_ui()
        
        # Load sample patterns
        self.load_sample_patterns()
    
    def create_ui(self):
        """Create the main user interface"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2C3E50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🎨 AI Kolam Studio", 
            font=('Arial', 24, 'bold'),
            fg='white', 
            bg='#2C3E50'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Discover, Analyze & Create Traditional Indian Kolam Patterns with AI",
            font=('Arial', 12),
            fg='#BDC3C7',
            bg='#2C3E50'
        )
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        self.create_control_panel(main_frame)
        
        # Right panel - Canvas
        self.create_canvas_panel(main_frame)
        
        # Bottom panel - Analysis
        self.create_analysis_panel(main_frame)
    
    def create_control_panel(self, parent):
        """Create the control panel"""
        control_frame = tk.LabelFrame(
            parent, 
            text="🎛️ Design Controls", 
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        control_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # AI Generation Section
        ai_frame = tk.LabelFrame(control_frame, text="🤖 AI Generation", bg='white')
        ai_frame.pack(fill='x', pady=5)
        
        tk.Label(ai_frame, text="Style:", bg='white').pack(anchor='w')
        self.style_var = tk.StringVar(value='traditional')
        style_combo = ttk.Combobox(
            ai_frame, 
            textvariable=self.style_var,
            values=['traditional', 'modern', 'fusion'],
            state='readonly'
        )
        style_combo.pack(fill='x', pady=2)
        
        tk.Label(ai_frame, text="Complexity:", bg='white').pack(anchor='w')
        self.complexity_var = tk.IntVar(value=5)
        complexity_scale = tk.Scale(
            ai_frame, 
            from_=1, 
            to=10, 
            orient='horizontal',
            variable=self.complexity_var,
            bg='white'
        )
        complexity_scale.pack(fill='x', pady=2)
        
        generate_btn = tk.Button(
            ai_frame,
            text="🎨 Generate AI Kolam",
            command=self.generate_ai_kolam,
            bg='#3498DB',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        generate_btn.pack(fill='x', pady=5)
        
        # Manual Design Section
        manual_frame = tk.LabelFrame(control_frame, text="✏️ Manual Design", bg='white')
        manual_frame.pack(fill='x', pady=5)
        
        # Grid controls
        tk.Label(manual_frame, text="Grid Size:", bg='white').pack(anchor='w')
        grid_frame = tk.Frame(manual_frame, bg='white')
        grid_frame.pack(fill='x')
        
        tk.Label(grid_frame, text="Rows:", bg='white').pack(side='left')
        self.rows_var = tk.IntVar(value=10)
        rows_spin = tk.Spinbox(grid_frame, from_=5, to=20, textvariable=self.rows_var, width=5)
        rows_spin.pack(side='left', padx=2)
        
        tk.Label(grid_frame, text="Cols:", bg='white').pack(side='left')
        self.cols_var = tk.IntVar(value=10)
        cols_spin = tk.Spinbox(grid_frame, from_=5, to=20, textvariable=self.cols_var, width=5)
        cols_spin.pack(side='left', padx=2)
        
        # Pattern tools
        pattern_frame = tk.Frame(manual_frame, bg='white')
        pattern_frame.pack(fill='x', pady=5)
        
        tk.Button(
            pattern_frame,
            text="⊕ Add Dots",
            command=self.add_dot_grid,
            bg='#27AE60',
            fg='white'
        ).pack(side='left', padx=2)
        
        tk.Button(
            pattern_frame,
            text="🌀 Spiral",
            command=self.add_spiral,
            bg='#E74C3C',
            fg='white'
        ).pack(side='left', padx=2)
        
        tk.Button(
            pattern_frame,
            text="🔄 Mandala",
            command=self.add_mandala,
            bg='#9B59B6',
            fg='white'
        ).pack(side='left', padx=2)
        
        # Color selection
        color_frame = tk.Frame(manual_frame, bg='white')
        color_frame.pack(fill='x', pady=5)
        
        tk.Label(color_frame, text="Color:", bg='white').pack(side='left')
        self.color_btn = tk.Button(
            color_frame,
            text="🎨",
            command=self.choose_color,
            bg=self.selected_color,
            width=3
        )
        self.color_btn.pack(side='left', padx=5)
        
        # Action buttons
        action_frame = tk.LabelFrame(control_frame, text="⚡ Actions", bg='white')
        action_frame.pack(fill='x', pady=5)
        
        tk.Button(
            action_frame,
            text="🔍 Analyze Pattern",
            command=self.analyze_current_pattern,
            bg='#F39C12',
            fg='white',
            font=('Arial', 10, 'bold')
        ).pack(fill='x', pady=2)
        
        tk.Button(
            action_frame,
            text="💾 Save Design",
            command=self.save_design,
            bg='#16A085',
            fg='white'
        ).pack(fill='x', pady=2)
        
        tk.Button(
            action_frame,
            text="📁 Load Design",
            command=self.load_design,
            bg='#8E44AD',
            fg='white'
        ).pack(fill='x', pady=2)
        
        tk.Button(
            action_frame,
            text="🗑️ Clear Canvas",
            command=self.clear_canvas,
            bg='#E74C3C',
            fg='white'
        ).pack(fill='x', pady=2)
    
    def create_canvas_panel(self, parent):
        """Create the drawing canvas"""
        canvas_frame = tk.LabelFrame(
            parent, 
            text="🎨 Kolam Canvas", 
            font=('Arial', 12, 'bold'),
            bg='white'
        )
        canvas_frame.pack(side='left', fill='both', expand=True)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(-2, 22)
        self.ax.set_ylim(-2, 22)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Click to draw or use AI generation", fontsize=14)
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkinter(self.fig, canvas_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Bind mouse events
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
    
    def create_analysis_panel(self, parent):
        """Create the analysis results panel"""
        analysis_frame = tk.LabelFrame(
            parent, 
            text="📊 Pattern Analysis", 
            font=('Arial', 12, 'bold'),
            bg='white'
        )
        analysis_frame.pack(side='bottom', fill='x', pady=(10, 0))
        
        # Create text widget for analysis results
        self.analysis_text = tk.Text(
            analysis_frame, 
            height=6, 
            bg='#F8F9FA',
            font=('Consolas', 10)
        )
        self.analysis_text.pack(fill='x', padx=10, pady=10)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(analysis_frame, command=self.analysis_text.yview)
        self.analysis_text.config(yscrollcommand=scrollbar.set)
    
    def generate_ai_kolam(self):
        """Generate AI-powered Kolam design"""
        style = self.style_var.get()
        complexity = self.complexity_var.get()
        
        try:
            # Generate pattern using AI
            self.current_pattern = self.kolam_ai.generate_ai_kolam(style, complexity)
            
            # Update canvas
            self.update_canvas()
            
            # Show generation info
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, f"🤖 AI Generated Kolam\n")
            self.analysis_text.insert(tk.END, f"Style: {style.title()}\n")
            self.analysis_text.insert(tk.END, f"Complexity: {complexity}/10\n")
            self.analysis_text.insert(tk.END, f"Points: {len(self.current_pattern)}\n")
            self.analysis_text.insert(tk.END, f"Generated at: {datetime.now().strftime('%H:%M:%S')}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate Kolam: {str(e)}")
    
    def add_dot_grid(self):
        """Add dot grid to current pattern"""
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        
        dots = KolamDesignPrinciples.generate_dot_grid(rows, cols, 2)
        self.current_pattern.extend(dots.tolist())
        self.update_canvas()
    
    def add_spiral(self):
        """Add spiral pattern"""
        center = (10, 10)
        spiral = KolamDesignPrinciples.generate_spiral_pattern(center, 5, 3)
        self.current_pattern.extend(spiral)
        self.update_canvas()
    
    def add_mandala(self):
        """Add mandala pattern"""
        center = (10, 10)
        mandala = KolamDesignPrinciples.create_mandala_pattern(center, 4)
        self.current_pattern.extend(mandala)
        self.update_canvas()
    
    def choose_color(self):
        """Choose drawing color"""
        color = colorchooser.askcolor(title="Choose Kolam Color")[1]
        if color:
            self.selected_color = color
            self.color_btn.config(bg=color)
    
    def on_canvas_click(self, event):
        """Handle canvas click events"""
        if event.inaxes:
            x, y = event.xdata, event.ydata
            self.current_pattern.append((x, y))
            self.update_canvas()
    
    def update_canvas(self):
        """Update the canvas with current pattern"""
        self.ax.clear()
        self.ax.set_xlim(-2, 22)
        self.ax.set_ylim(-2, 22)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        
        if self.current_pattern:
            points = np.array(self.current_pattern)
            self.ax.scatter(points[:, 0], points[:, 1], 
                          c=self.selected_color, s=50, alpha=0.8)
            
            # Connect points to show pattern flow
            if len(points) > 1:
                self.ax.plot(points[:, 0], points[:, 1], 
                           color=self.selected_color, alpha=0.5, linewidth=2)
        
        self.ax.set_title(f"Kolam Pattern ({len(self.current_pattern)} points)", fontsize=14)
        self.canvas.draw()
    
    def analyze_current_pattern(self):
        """Analyze the current pattern for mathematical properties"""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "No pattern to analyze!")
            return
        
        try:
            points = np.array(self.current_pattern)
            
            # Analyze symmetries
            symmetries = self.kolam_ai.analyze_symmetry(points)
            
            # Calculate center and spread
            center = np.mean(points, axis=0)
            distances = np.sqrt(np.sum((points - center)**2, axis=1))
            avg_distance = np.mean(distances)
            
            # Display analysis
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, "🔍 PATTERN ANALYSIS RESULTS\n")
            self.analysis_text.insert(tk.END, "=" * 40 + "\n\n")
            
            self.analysis_text.insert(tk.END, f"📊 Basic Properties:\n")
            self.analysis_text.insert(tk.END, f"  • Total Points: {len(points)}\n")
            self.analysis_text.insert(tk.END, f"  • Center: ({center[0]:.2f}, {center[1]:.2f})\n")
            self.analysis_text.insert(tk.END, f"  • Average Radius: {avg_distance:.2f}\n\n")
            
            self.analysis_text.insert(tk.END, f"🔄 Symmetry Analysis:\n")
            if symmetries:
                for sym in symmetries:
                    self.analysis_text.insert(tk.END, f"  ✓ {sym}\n")
            else:
                self.analysis_text.insert(tk.END, f"  • No clear symmetries detected\n")
            
            self.analysis_text.insert(tk.END, f"\n🎨 Design Principles:\n")
            self.analysis_text.insert(tk.END, f"  • Complexity Score: {min(len(points)//10, 10)}/10\n")
            self.analysis_text.insert(tk.END, f"  • Symmetry Score: {len(symmetries)}/5\n")
            
            # Traditional Kolam classification
            if len(symmetries) >= 2:
                classification = "Traditional Kolam"
            elif len(symmetries) == 1:
                classification = "Semi-Traditional"
            else:
                classification = "Modern/Abstract"
            
            self.analysis_text.insert(tk.END, f"  • Classification: {classification}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    def save_design(self):
        """Save current design to file"""
        if not self.current_pattern:
            messagebox.showwarning("Warning", "No pattern to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                design_data = {
                    'pattern': self.current_pattern,
                    'color': self.selected_color,
                    'timestamp': datetime.now().isoformat(),
                    'metadata': {
                        'points': len(self.current_pattern),
                        'style': self.style_var.get()
                    }
                }
                
                with open(filename, 'w') as f:
                    json.dump(design_data, f, indent=2)
                
                messagebox.showinfo("Success", f"Design saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def load_design(self):
        """Load design from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    design_data = json.load(f)
                
                self.current_pattern = design_data['pattern']
                if 'color' in design_data:
                    self.selected_color = design_data['color']
                    self.color_btn.config(bg=self.selected_color)
                
                self.update_canvas()
                messagebox.showinfo("Success", f"Design loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")
    
    def clear_canvas(self):
        """Clear the current pattern"""
        self.current_pattern = []
        self.update_canvas()
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "Canvas cleared. Ready for new design! 🎨")
    
    def load_sample_patterns(self):
        """Load some sample patterns for demonstration"""
        # This could load from a database of traditional patterns
        pass
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function to run the Kolam Studio"""
    try:
        app = KolamStudio()
        app.run()
    except Exception as e:
        print(f"Error starting Kolam Studio: {e}")

if __name__ == "__main__":
    main()