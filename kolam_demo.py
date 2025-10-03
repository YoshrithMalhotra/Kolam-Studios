import matplotlib.pyplot as plt
import numpy as np
import math

class KolamDemo:
    """Demo of Kolam mathematical principles"""
    
    def __init__(self):
        self.fig, self.axes = plt.subplots(2, 3, figsize=(15, 10))
        self.fig.suptitle('🎨 Kolam Design Principles - Mathematical Analysis', fontsize=16, fontweight='bold')
        
    def create_dot_grid(self, rows=8, cols=8):
        """Create traditional dot grid"""
        dots = []
        for i in range(rows):
            for j in range(cols):
                dots.append([j, i])
        return np.array(dots)
    
    def create_flower_kolam(self):
        """Create traditional flower Kolam"""
        center = [4, 4]
        points = []
        
        # Central flower with 8 petals
        for i in range(8):
            angle = 2 * math.pi * i / 8
            for r in [1, 2, 3]:
                x = center[0] + r * math.cos(angle)
                y = center[1] + r * math.sin(angle)
                points.append([x, y])
        
        # Add center point
        points.append(center)
        
        return np.array(points)
    
    def create_geometric_kolam(self):
        """Create geometric pattern"""
        points = []
        center = [4, 4]
        
        # Create concentric squares
        for size in [1, 2, 3]:
            # Square corners
            corners = [
                [center[0] - size, center[1] - size],
                [center[0] + size, center[1] - size],
                [center[0] + size, center[1] + size],
                [center[0] - size, center[1] + size]
            ]
            points.extend(corners)
            
            # Square edges
            for i in range(4):
                start = corners[i]
                end = corners[(i + 1) % 4]
                for t in np.linspace(0, 1, 5):
                    x = start[0] + t * (end[0] - start[0])
                    y = start[1] + t * (end[1] - start[1])
                    points.append([x, y])
        
        return np.array(points)
    
    def create_spiral_kolam(self):
        """Create spiral pattern"""
        points = []
        center = [4, 4]
        
        # Archimedean spiral
        for t in np.linspace(0, 6 * math.pi, 100):
            r = 0.3 * t
            x = center[0] + r * math.cos(t)
            y = center[1] + r * math.sin(t)
            if 0 <= x <= 8 and 0 <= y <= 8:
                points.append([x, y])
        
        return np.array(points)
    
    def create_mandala_kolam(self):
        """Create mandala-style Kolam"""
        points = []
        center = [4, 4]
        
        # Multiple layers with different symmetries
        for layer in range(1, 4):
            radius = layer * 1.5
            n_points = 4 + layer * 2
            
            for i in range(n_points):
                angle = 2 * math.pi * i / n_points
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                points.append([x, y])
        
        # Add center
        points.append(center)
        
        return np.array(points)
    
    def analyze_symmetry(self, points):
        """Analyze symmetry of pattern"""
        center = np.mean(points, axis=0)
        symmetries = []
        
        # Check rotational symmetries
        for n in range(2, 9):
            if self.has_rotational_symmetry(points, center, n):
                symmetries.append(f"{n}-fold")
        
        return symmetries
    
    def has_rotational_symmetry(self, points, center, n):
        """Check if pattern has n-fold rotational symmetry"""
        angle = 2 * math.pi / n
        tolerance = 0.3
        
        for point in points:
            # Rotate point
            dx, dy = point[0] - center[0], point[1] - center[1]
            new_x = center[0] + dx * math.cos(angle) - dy * math.sin(angle)
            new_y = center[1] + dx * math.sin(angle) + dy * math.cos(angle)
            
            # Check if rotated point exists
            found = False
            for orig_point in points:
                dist = math.sqrt((orig_point[0] - new_x)**2 + (orig_point[1] - new_y)**2)
                if dist < tolerance:
                    found = True
                    break
            
            if not found:
                return False
        
        return True
    
    def plot_pattern(self, ax, points, title, color='red'):
        """Plot a Kolam pattern"""
        ax.scatter(points[:, 0], points[:, 1], c=color, s=50, alpha=0.8)
        
        # Connect points to show flow
        if len(points) > 1:
            ax.plot(points[:, 0], points[:, 1], color=color, alpha=0.5, linewidth=1)
        
        ax.set_xlim(-1, 9)
        ax.set_ylim(-1, 9)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(title, fontweight='bold')
        
        # Add analysis
        symmetries = self.analyze_symmetry(points)
        complexity = min(10, len(points) // 5)
        
        info_text = f"Points: {len(points)}\n"
        info_text += f"Complexity: {complexity}/10\n"
        if symmetries:
            info_text += f"Symmetry: {', '.join(symmetries[:2])}"
        else:
            info_text += "Symmetry: None detected"
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def create_demo(self):
        """Create complete demo"""
        # 1. Dot Grid Foundation
        dots = self.create_dot_grid(8, 8)
        self.plot_pattern(self.axes[0, 0], dots, "1. Dot Grid Foundation", 'blue')
        
        # 2. Flower Kolam
        flower = self.create_flower_kolam()
        self.plot_pattern(self.axes[0, 1], flower, "2. Traditional Flower Kolam", 'red')
        
        # 3. Geometric Pattern
        geometric = self.create_geometric_kolam()
        self.plot_pattern(self.axes[0, 2], geometric, "3. Geometric Pattern", 'green')
        
        # 4. Spiral Pattern
        spiral = self.create_spiral_kolam()
        self.plot_pattern(self.axes[1, 0], spiral, "4. Spiral Pattern", 'purple')
        
        # 5. Mandala Pattern
        mandala = self.create_mandala_kolam()
        self.plot_pattern(self.axes[1, 1], mandala, "5. Mandala Pattern", 'orange')
        
        # 6. Combined Pattern
        combined = np.vstack([flower[:10], geometric[:15], spiral[::5]])
        self.plot_pattern(self.axes[1, 2], combined, "6. AI-Generated Fusion", 'darkred')
        
        plt.tight_layout()
        
        # Add innovation text
        innovation_text = """
🚀 INNOVATION FOR SMART INDIA HACKATHON:

1. AI Pattern Recognition: Automatically identify traditional Kolam elements
2. Mathematical Analysis: Real-time symmetry and complexity calculation  
3. Interactive Design: Click-and-draw with pattern assistance
4. Cultural Preservation: Digital archive of regional Kolam styles
5. Educational Tool: Learn geometry through traditional art
6. Mobile App Ready: Touch-friendly interface for tablets
7. 3D Visualization: Export patterns for 3D printing and AR
8. Community Platform: Share and rate Kolam designs
        """
        
        plt.figtext(0.02, 0.02, innovation_text, fontsize=10, 
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.show()

def main():
    """Run the Kolam demo"""
    print("🎨 Kolam Design Principles Demo")
    print("=" * 40)
    print("Generating mathematical analysis of traditional Kolam patterns...")
    
    demo = KolamDemo()
    demo.create_demo()
    
    print("\n✅ Demo complete!")
    print("\nKey Innovations:")
    print("• Mathematical pattern analysis")
    print("• AI-powered design generation") 
    print("• Interactive drawing interface")
    print("• Cultural preservation through digitization")
    print("• Educational geometry learning")

if __name__ == "__main__":
    main()