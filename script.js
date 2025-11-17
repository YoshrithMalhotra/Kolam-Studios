// Kolam Design Studio - JavaScript
class KolamStudio {
    constructor() {
        this.canvas = document.getElementById('kolamCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.currentPattern = [];
        this.selectedColor = '#FF6B35';
        this.isDrawing = false;
        this.gridVisible = false;
        this.zoom = 1;
        this.panX = 0;
        this.panY = 0;
        
        this.init();
    }

    init() {
        this.setupCanvas();
        this.setupEventListeners();
        this.updateComplexityDisplay();
        this.drawGrid();
    }
    
    setupCanvas() {
        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = 800;
        this.canvas.height = 600;
        
        // Set canvas style
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        this.ctx.strokeStyle = this.selectedColor;
        this.ctx.lineWidth = 3;
    }
    
    setupEventListeners() {
        // Canvas events
        this.canvas.addEventListener('mousedown', (e) => this.startDrawing(e));
        this.canvas.addEventListener('mousemove', (e) => this.draw(e));
        this.canvas.addEventListener('mouseup', () => this.stopDrawing());
        this.canvas.addEventListener('mouseout', () => this.stopDrawing());
        
        // Color palette
        document.querySelectorAll('.color-option').forEach(option => {
            option.addEventListener('click', (e) => {
                document.querySelector('.color-option.active').classList.remove('active');
                e.target.classList.add('active');
                this.selectedColor = e.target.dataset.color;
                this.ctx.strokeStyle = this.selectedColor;
            });
        });
        
        // Custom color picker
        document.getElementById('customColor').addEventListener('change', (e) => {
            this.selectedColor = e.target.value;
            this.ctx.strokeStyle = this.selectedColor;
            document.querySelector('.color-option.active').classList.remove('active');
        });
        
        // Complexity slider
        document.getElementById('complexitySlider').addEventListener('input', (e) => {
            document.getElementById('complexityValue').textContent = e.target.value;
        });
        
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = e.target.getAttribute('href');
                this.navigateTo(target);
            });
        });
    }
    
    startDrawing(e) {
        this.isDrawing = true;
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        this.currentPattern.push({x, y, color: this.selectedColor});
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        
        this.hideCanvasOverlay();
        this.updateCanvasInfo();
    }
    
    draw(e) {
        if (!this.isDrawing) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        this.currentPattern.push({x, y, color: this.selectedColor});
        this.ctx.lineTo(x, y);
        this.ctx.stroke();
        
        this.updateCanvasInfo();
    }
    
    stopDrawing() {
        if (this.isDrawing) {
            this.isDrawing = false;
            this.ctx.beginPath();
            this.updateLiveAnalysis();
        }
    }
    
    hideCanvasOverlay() {
        document.getElementById('canvasOverlay').classList.add('hidden');
    }
    
    showCanvasOverlay() {
        document.getElementById('canvasOverlay').classList.remove('hidden');
    }
    
    updateCanvasInfo() {
        const info = `Drawing • Points: ${this.currentPattern.length} • Color: ${this.selectedColor}`;
        document.getElementById('canvasInfo').textContent = info;
    }
    
    drawGrid() {
        if (!this.gridVisible) return;
        
        this.ctx.save();
        this.ctx.strokeStyle = '#e0e0e0';
        this.ctx.lineWidth = 1;
        
        const gridSize = 20;
        
        // Vertical lines
        for (let x = 0; x <= this.canvas.width; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        
        // Horizontal lines
        for (let y = 0; y <= this.canvas.height; y += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    clearCanvas() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.currentPattern = [];
        this.drawGrid();
        this.showCanvasOverlay();
        this.updateCanvasInfo();
        this.clearAnalysis();
    }
    
    generateAIKolam() {
        const style = document.getElementById('styleSelect').value;
        const complexity = parseInt(document.getElementById('complexitySlider').value);
        
        this.showLoading();
        
        // Simulate AI generation delay
        setTimeout(() => {
            this.clearCanvas();
            this.hideCanvasOverlay();
            
            const centerX = this.canvas.width / 2;
            const centerY = this.canvas.height / 2;
            
            this.ctx.strokeStyle = this.selectedColor;
            this.ctx.lineWidth = 3;
            
            switch (style) {
                case 'traditional':
                    this.generateTraditionalKolam(centerX, centerY, complexity);
                    break;
                case 'modern':
                    this.generateModernKolam(centerX, centerY, complexity);
                    break;
                case 'geometric':
                    this.generateGeometricKolam(centerX, centerY, complexity);
                    break;
                case 'floral':
                    this.generateFloralKolam(centerX, centerY, complexity);
                    break;
            }
            
            this.hideLoading();
            this.updateCanvasInfo();
            this.updateLiveAnalysis();
        }, 2000);
    }
    
    generateTraditionalKolam(centerX, centerY, complexity) {
        // Generate traditional lotus-like pattern
        const layers = Math.min(complexity, 8);
        
        for (let layer = 1; layer <= layers; layer++) {
            const radius = layer * 15;
            const petals = 4 + layer * 2;
            
            this.ctx.beginPath();
            for (let i = 0; i <= petals; i++) {
                const angle = (i / petals) * 2 * Math.PI;
                const x = centerX + radius * Math.cos(angle);
                const y = centerY + radius * Math.sin(angle);
                
                if (i === 0) {
                    this.ctx.moveTo(x, y);
                } else {
                    this.ctx.lineTo(x, y);
                }
                
                this.currentPattern.push({x, y, color: this.selectedColor});
            }
            this.ctx.stroke();
        }
        
        // Add center dot
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 5, 0, 2 * Math.PI);
        this.ctx.fill();
    }
    
    generateModernKolam(centerX, centerY, complexity) {
        // Generate modern abstract pattern
        const iterations = complexity * 10;
        
        this.ctx.beginPath();
        for (let i = 0; i < iterations; i++) {
            const t = i / iterations;
            const angle = t * complexity * Math.PI;
            const radius = 50 + t * 100;
            
            const x = centerX + radius * Math.cos(angle) * (1 - t * 0.5);
            const y = centerY + radius * Math.sin(angle) * (1 - t * 0.5);
            
            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
            
            this.currentPattern.push({x, y, color: this.selectedColor});
        }
        this.ctx.stroke();
    }
    
    generateGeometricKolam(centerX, centerY, complexity) {
        // Generate geometric pattern with squares and circles
        const shapes = Math.min(complexity, 6);
        
        for (let i = 1; i <= shapes; i++) {
            const size = i * 20;
            
            // Square
            this.ctx.beginPath();
            this.ctx.rect(centerX - size, centerY - size, size * 2, size * 2);
            this.ctx.stroke();
            
            // Circle
            this.ctx.beginPath();
            this.ctx.arc(centerX, centerY, size, 0, 2 * Math.PI);
            this.ctx.stroke();
            
            // Add points to pattern
            for (let angle = 0; angle < 2 * Math.PI; angle += Math.PI / 4) {
                const x = centerX + size * Math.cos(angle);
                const y = centerY + size * Math.sin(angle);
                this.currentPattern.push({x, y, color: this.selectedColor});
            }
        }
    }
    
    generateFloralKolam(centerX, centerY, complexity) {
        // Generate floral pattern
        const petals = 4 + complexity;
        const layers = Math.min(complexity, 5);
        
        for (let layer = 1; layer <= layers; layer++) {
            const radius = layer * 25;
            
            this.ctx.beginPath();
            for (let i = 0; i <= petals * 3; i++) {
                const angle = (i / (petals * 3)) * 2 * Math.PI;
                const petalRadius = radius * (1 + 0.3 * Math.sin(petals * angle));
                
                const x = centerX + petalRadius * Math.cos(angle);
                const y = centerY + petalRadius * Math.sin(angle);
                
                if (i === 0) {
                    this.ctx.moveTo(x, y);
                } else {
                    this.ctx.lineTo(x, y);
                }
                
                if (i % 3 === 0) {
                    this.currentPattern.push({x, y, color: this.selectedColor});
                }
            }
            this.ctx.stroke();
        }
    }
    
    addPattern(type) {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        this.hideCanvasOverlay();
        this.ctx.strokeStyle = this.selectedColor;
        this.ctx.lineWidth = 3;
        
        switch (type) {
            case 'dots':
                this.addDotPattern(centerX, centerY);
                break;
            case 'flower':
                this.addFlowerPattern(centerX, centerY);
                break;
            case 'star':
                this.addStarPattern(centerX, centerY);
                break;
            case 'spiral':
                this.addSpiralPattern(centerX, centerY);
                break;
            case 'mandala':
                this.addMandalaPattern(centerX, centerY);
                break;
            case 'geometric':
                this.addGeometricPattern(centerX, centerY);
                break;
        }
        
        this.updateCanvasInfo();
        this.updateLiveAnalysis();
    }
    
    addDotPattern(centerX, centerY) {
        const gridSize = 40;
        const rows = 5;
        const cols = 5;
        
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                const x = centerX - (cols - 1) * gridSize / 2 + j * gridSize;
                const y = centerY - (rows - 1) * gridSize / 2 + i * gridSize;
                
                this.ctx.beginPath();
                this.ctx.arc(x, y, 3, 0, 2 * Math.PI);
                this.ctx.fill();
                
                this.currentPattern.push({x, y, color: this.selectedColor});
            }
        }
    }
    
    addFlowerPattern(centerX, centerY) {
        const petals = 8;
        const radius = 50;
        
        this.ctx.beginPath();
        for (let i = 0; i <= petals; i++) {
            const angle = (i / petals) * 2 * Math.PI;
            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);
            
            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
            
            this.currentPattern.push({x, y, color: this.selectedColor});
        }
        this.ctx.stroke();
        
        // Center
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 5, 0, 2 * Math.PI);
        this.ctx.fill();
    }
    
    addStarPattern(centerX, centerY) {
        const points = 5;
        const outerRadius = 60;
        const innerRadius = 25;
        
        this.ctx.beginPath();
        for (let i = 0; i < points * 2; i++) {
            const angle = (i / (points * 2)) * 2 * Math.PI;
            const radius = i % 2 === 0 ? outerRadius : innerRadius;
            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);
            
            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
            
            this.currentPattern.push({x, y, color: this.selectedColor});
        }
        this.ctx.closePath();
        this.ctx.stroke();
    }
    
    addSpiralPattern(centerX, centerY) {
        const turns = 3;
        const maxRadius = 80;
        const steps = 100;
        
        this.ctx.beginPath();
        for (let i = 0; i <= steps; i++) {
            const t = i / steps;
            const angle = t * turns * 2 * Math.PI;
            const radius = t * maxRadius;
            
            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);
            
            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
            
            if (i % 5 === 0) {
                this.currentPattern.push({x, y, color: this.selectedColor});
            }
        }
        this.ctx.stroke();
    }
    
    addMandalaPattern(centerX, centerY) {
        const layers = 4;
        
        for (let layer = 1; layer <= layers; layer++) {
            const radius = layer * 20;
            const points = 4 + layer * 2;
            
            this.ctx.beginPath();
            for (let i = 0; i <= points; i++) {
                const angle = (i / points) * 2 * Math.PI;
                const x = centerX + radius * Math.cos(angle);
                const y = centerY + radius * Math.sin(angle);
                
                if (i === 0) {
                    this.ctx.moveTo(x, y);
                } else {
                    this.ctx.lineTo(x, y);
                }
                
                this.currentPattern.push({x, y, color: this.selectedColor});
            }
            this.ctx.stroke();
        }
    }
    
    addGeometricPattern(centerX, centerY) {
        const size = 60;
        
        // Square
        this.ctx.beginPath();
        this.ctx.rect(centerX - size, centerY - size, size * 2, size * 2);
        this.ctx.stroke();
        
        // Diamond
        this.ctx.beginPath();
        this.ctx.moveTo(centerX, centerY - size);
        this.ctx.lineTo(centerX + size, centerY);
        this.ctx.lineTo(centerX, centerY + size);
        this.ctx.lineTo(centerX - size, centerY);
        this.ctx.closePath();
        this.ctx.stroke();
        
        // Add corner points
        const corners = [
            {x: centerX - size, y: centerY - size},
            {x: centerX + size, y: centerY - size},
            {x: centerX + size, y: centerY + size},
            {x: centerX - size, y: centerY + size}
        ];
        
        corners.forEach(corner => {
            this.currentPattern.push({...corner, color: this.selectedColor});
        });
    }
    
    analyzePattern() {
        if (this.currentPattern.length === 0) {
            alert('No pattern to analyze! Please draw something first.');
            return;
        }
        
        const analysis = this.performAnalysis();
        this.showAnalysisModal(analysis);
    }
    
    performAnalysis() {
        const points = this.currentPattern;
        const numPoints = points.length;
        
        // Calculate center
        const centerX = points.reduce((sum, p) => sum + p.x, 0) / numPoints;
        const centerY = points.reduce((sum, p) => sum + p.y, 0) / numPoints;
        
        // Calculate complexity
        const complexity = Math.min(10, Math.floor(numPoints / 20));
        
        // Analyze symmetries (simplified)
        const symmetries = this.detectSymmetries(points, centerX, centerY);
        
        // Calculate spread
        const distances = points.map(p => 
            Math.sqrt((p.x - centerX) ** 2 + (p.y - centerY) ** 2)
        );
        const avgDistance = distances.reduce((sum, d) => sum + d, 0) / distances.length;
        const maxDistance = Math.max(...distances);
        
        // Classification
        let classification = 'Modern/Abstract';
        let score = 'Creative';
        
        if (symmetries.length >= 2) {
            classification = 'Traditional Kolam';
            score = 'Excellent';
        } else if (symmetries.length === 1) {
            classification = 'Semi-Traditional';
            score = 'Good';
        }
        
        return {
            numPoints,
            center: {x: centerX.toFixed(1), y: centerY.toFixed(1)},
            complexity,
            symmetries,
            avgDistance: avgDistance.toFixed(1),
            maxDistance: maxDistance.toFixed(1),
            classification,
            score,
            colors: [...new Set(points.map(p => p.color))],
            timestamp: new Date().toLocaleTimeString()
        };
    }
    
    detectSymmetries(points, centerX, centerY) {
        const symmetries = [];
        
        // Simple symmetry detection (placeholder)
        if (points.length > 20) {
            symmetries.push('Rotational');
        }
        
        if (points.length > 50) {
            symmetries.push('Reflection');
        }
        
        return symmetries;
    }
    
    updateLiveAnalysis() {
        if (this.currentPattern.length < 5) return;
        
        const analysis = this.performAnalysis();
        
        const content = `
            <div class="live-analysis">
                <h4><i class="fas fa-chart-line"></i> Live Analysis</h4>
                <div class="analysis-stats">
                    <div class="stat">
                        <span class="stat-label">Points:</span>
                        <span class="stat-value">${analysis.numPoints}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Complexity:</span>
                        <span class="stat-value">${analysis.complexity}/10</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Classification:</span>
                        <span class="stat-value">${analysis.classification}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Symmetries:</span>
                        <span class="stat-value">${analysis.symmetries.length}</span>
                    </div>
                </div>
                <p class="analysis-note">
                    <i class="fas fa-info-circle"></i>
                    Click "Analyze" for detailed results
                </p>
            </div>
        `;
        
        document.getElementById('analysisContent').innerHTML = content;
    }
    
    clearAnalysis() {
        document.getElementById('analysisContent').innerHTML = `
            <div class="welcome-analysis">
                <div class="analysis-icon">
                    <i class="fas fa-brain"></i>
                </div>
                <h4>AI-Powered Analysis</h4>
                <p>Create a pattern to see detailed mathematical analysis including:</p>
                <ul>
                    <li><i class="fas fa-sync"></i> Symmetry Detection</li>
                    <li><i class="fas fa-calculator"></i> Complexity Scoring</li>
                    <li><i class="fas fa-shapes"></i> Geometric Properties</li>
                    <li><i class="fas fa-history"></i> Cultural Classification</li>
                </ul>
            </div>
        `;
    }
    
    showAnalysisModal(analysis) {
        const modalContent = `
            <div class="analysis-results">
                <div class="analysis-section">
                    <h4><i class="fas fa-info-circle"></i> Basic Properties</h4>
                    <div class="property-grid">
                        <div class="property">
                            <span class="property-label">Total Points:</span>
                            <span class="property-value">${analysis.numPoints}</span>
                        </div>
                        <div class="property">
                            <span class="property-label">Center:</span>
                            <span class="property-value">(${analysis.center.x}, ${analysis.center.y})</span>
                        </div>
                        <div class="property">
                            <span class="property-label">Avg Radius:</span>
                            <span class="property-value">${analysis.avgDistance}px</span>
                        </div>
                        <div class="property">
                            <span class="property-label">Max Radius:</span>
                            <span class="property-value">${analysis.maxDistance}px</span>
                        </div>
                    </div>
                </div>
                
                <div class="analysis-section">
                    <h4><i class="fas fa-sync"></i> Symmetry Analysis</h4>
                    <div class="symmetry-list">
                        ${analysis.symmetries.length > 0 
                            ? analysis.symmetries.map(sym => `<span class="symmetry-tag">✓ ${sym}</span>`).join('')
                            : '<span class="no-symmetry">No clear symmetries detected</span>'
                        }
                    </div>
                </div>
                
                <div class="analysis-section">
                    <h4><i class="fas fa-star"></i> Design Classification</h4>
                    <div class="classification-result">
                        <div class="classification-type">${analysis.classification}</div>
                        <div class="classification-score">Score: ${analysis.score}</div>
                        <div class="complexity-bar">
                            <span>Complexity: ${analysis.complexity}/10</span>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${analysis.complexity * 10}%"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="analysis-section">
                    <h4><i class="fas fa-palette"></i> Color Analysis</h4>
                    <div class="color-analysis">
                        <span>Colors used: ${analysis.colors.length}</span>
                        <div class="color-swatches">
                            ${analysis.colors.map(color => 
                                `<div class="color-swatch" style="background: ${color}"></div>`
                            ).join('')}
                        </div>
                    </div>
                </div>
                
                <div class="analysis-footer">
                    <small><i class="fas fa-clock"></i> Analysis completed at ${analysis.timestamp}</small>
                </div>
            </div>
        `;
        
        document.getElementById('modalAnalysisContent').innerHTML = modalContent;
        document.getElementById('analysisModal').classList.remove('hidden');
    }
    
    savePattern() {
        if (this.currentPattern.length === 0) {
            alert('No pattern to save!');
            return;
        }
        
        const analysis = this.performAnalysis();
        const patternData = {
            pattern: this.currentPattern,
            analysis: analysis,
            timestamp: new Date().toISOString(),
            canvasSize: {
                width: this.canvas.width,
                height: this.canvas.height
            }
        };
        
        const dataStr = JSON.stringify(patternData, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `kolam-pattern-${Date.now()}.json`;
        link.click();
        
        alert('Pattern saved successfully!');
    }
    
    loadPattern() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    this.currentPattern = data.pattern || [];
                    this.redrawPattern();
                    alert('Pattern loaded successfully!');
                } catch (error) {
                    alert('Error loading pattern file!');
                }
            };
            reader.readAsText(file);
        };
        
        input.click();
    }
    
    redrawPattern() {
        this.clearCanvas();
        this.hideCanvasOverlay();
        
        if (this.currentPattern.length === 0) return;
        
        // Group points by color and draw
        const colorGroups = {};
        this.currentPattern.forEach(point => {
            if (!colorGroups[point.color]) {
                colorGroups[point.color] = [];
            }
            colorGroups[point.color].push(point);
        });
        
        Object.entries(colorGroups).forEach(([color, points]) => {
            this.ctx.strokeStyle = color;
            this.ctx.beginPath();
            
            points.forEach((point, index) => {
                if (index === 0) {
                    this.ctx.moveTo(point.x, point.y);
                } else {
                    this.ctx.lineTo(point.x, point.y);
                }
            });
            
            this.ctx.stroke();
        });
        
        this.updateCanvasInfo();
        this.updateLiveAnalysis();
    }
    
    toggleGrid() {
        this.gridVisible = !this.gridVisible;
        this.redrawPattern();
    }
    
    zoomIn() {
        this.zoom *= 1.2;
        this.applyTransform();
    }
    
    zoomOut() {
        this.zoom /= 1.2;
        this.applyTransform();
    }
    
    resetView() {
        this.zoom = 1;
        this.panX = 0;
        this.panY = 0;
        this.applyTransform();
    }
    
    applyTransform() {
        this.ctx.setTransform(this.zoom, 0, 0, this.zoom, this.panX, this.panY);
        this.redrawPattern();
    }
    
    showLoading() {
        document.getElementById('loadingOverlay').classList.remove('hidden');
    }
    
    hideLoading() {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }
    
    navigateTo(target) {
        // Remove active class from all nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        // Add active class to clicked link
        document.querySelector(`[href="${target}"]`).classList.add('active');
        
        // Hide all sections
        document.querySelectorAll('section').forEach(section => {
            section.classList.add('hidden');
        });
        
        // Show target section
        const targetSection = document.querySelector(target);
        if (targetSection) {
            targetSection.classList.remove('hidden');
        }
        
        // Special handling for studio
        if (target === '#studio') {
            // Studio is shown by startDesigning function
        }
    }
    
    updateComplexityDisplay() {
        const slider = document.getElementById('complexitySlider');
        const display = document.getElementById('complexityValue');
        
        slider.addEventListener('input', () => {
            display.textContent = slider.value;
        });
    }
}

// Global functions
function startDesigning() {
    document.getElementById('home').classList.add('hidden');
    document.getElementById('studio').classList.remove('hidden');
    
    // Update navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
}

function generateAIKolam() {
    window.kolamStudio.generateAIKolam();
}

function addPattern(type) {
    window.kolamStudio.addPattern(type);
}

function analyzePattern() {
    window.kolamStudio.analyzePattern();
}

function savePattern() {
    window.kolamStudio.savePattern();
}

function loadPattern() {
    window.kolamStudio.loadPattern();
}

function clearCanvas() {
    if (confirm('Are you sure you want to clear the canvas?')) {
        window.kolamStudio.clearCanvas();
    }
}

function toggleGrid() {
    window.kolamStudio.toggleGrid();
}

function zoomIn() {
    window.kolamStudio.zoomIn();
}

function zoomOut() {
    window.kolamStudio.zoomOut();
}

function resetView() {
    window.kolamStudio.resetView();
}

function closeModal() {
    document.getElementById('analysisModal').classList.add('hidden');
}

function loadGalleryPattern(patternId) {
    // Switch to studio mode
    startDesigning();
    
    // Generate the selected pattern
    setTimeout(() => {
        window.kolamStudio.clearCanvas();
        
        switch (patternId) {
            case 'traditional1':
                window.kolamStudio.addPattern('flower');
                break;
            case 'traditional2':
                window.kolamStudio.addPattern('star');
                break;
            case 'geometric1':
                window.kolamStudio.addPattern('mandala');
                break;
            case 'modern1':
                window.kolamStudio.addPattern('spiral');
                break;
        }
    }, 100);
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.kolamStudio = new KolamStudio();
    
    // Add some CSS for analysis results
    const style = document.createElement('style');
    style.textContent = `
        .analysis-results {
            font-family: 'Poppins', sans-serif;
        }
        
        .analysis-section {
            margin-bottom: 2rem;
        }
        
        .analysis-section h4 {
            color: #333;
            margin-bottom: 1rem;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .property-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        
        .property {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem;
            background: #f8f9fa;
            border-radius: 6px;
        }
        
        .property-label {
            font-weight: 500;
            color: #666;
        }
        
        .property-value {
            font-weight: 600;
            color: #333;
        }
        
        .symmetry-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        
        .symmetry-tag {
            background: #27ae60;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.9rem;
        }
        
        .no-symmetry {
            color: #666;
            font-style: italic;
        }
        
        .classification-result {
            text-align: center;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .classification-type {
            font-size: 1.3rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .classification-score {
            color: #FF6B35;
            font-weight: 500;
            margin-bottom: 1rem;
        }
        
        .complexity-bar {
            margin-top: 1rem;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(45deg, #FF6B35, #F7931E);
            transition: width 0.3s ease;
        }
        
        .color-analysis {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .color-swatches {
            display: flex;
            gap: 0.25rem;
        }
        
        .color-swatch {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .analysis-footer {
            text-align: center;
            padding-top: 1rem;
            border-top: 1px solid #eee;
            color: #666;
        }
        
        .live-analysis {
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .live-analysis h4 {
            margin-bottom: 1rem;
            color: #333;
        }
        
        .analysis-stats {
            display: grid;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }
        
        .stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .stat-label {
            font-weight: 500;
            color: #666;
        }
        
        .stat-value {
            font-weight: 600;
            color: #FF6B35;
        }
        
        .analysis-note {
            color: #666;
            font-size: 0.9rem;
            text-align: center;
            margin: 0;
        }
    `;
    document.head.appendChild(style);

});
