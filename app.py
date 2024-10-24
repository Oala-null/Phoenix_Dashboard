from flask import Flask, render_template
import os
import glob
import shutil

app = Flask(__name__)

# Define the base directory of your project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Since files are already in the static directory, we'll just define the paths for verification
GRAPH_FILES = [
    'expense_flow_sankey.html',
    'vendor_comparison_chart.html',
    'vendor_repetition_rate_comparison.html',
    'vendor_metrics_dashboard.html'
]

IMAGE_FILES = [
    'Anomoly_Detection_Heatmap.jpg',
    'Correlation_Matrix.jpg',
    'Payment_Trend.jpg',
    'Top_Vendors_By_anomoly.jpg'
]

def verify_files():
    """Verify that all required files exist in the static directories"""
    try:
        # Verify directories exist
        graphs_dir = os.path.join('static', 'graphs')
        images_dir = os.path.join('static', 'images')
        os.makedirs(graphs_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)
        
        # Verify graph files
        missing_graphs = []
        for file in GRAPH_FILES:
            file_path = os.path.join(graphs_dir, file)
            if not os.path.exists(file_path):
                missing_graphs.append(file)
        
        # Verify image files
        missing_images = []
        for file in IMAGE_FILES:
            file_path = os.path.join(images_dir, file)
            if not os.path.exists(file_path):
                missing_images.append(file)
        
        # Report any missing files
        if missing_graphs or missing_images:
            print("\nMissing files:")
            if missing_graphs:
                print("Graphs:", missing_graphs)
            if missing_images:
                print("Images:", missing_images)
            return False
        
        print("All files verified successfully!")
        return True
    
    except Exception as e:
        print(f"Error verifying files: {str(e)}")
        return False

def get_plotly_graphs():
    """Load all HTML files from the graphs directory"""
    graphs_dir = os.path.join('static', 'graphs')
    graphs = []
    
    try:
        for file in GRAPH_FILES:
            file_path = os.path.join(graphs_dir, file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    display_name = file.replace('.html', '').replace('_', ' ').title()
                    graphs.append({
                        'name': display_name,
                        'content': f.read()
                    })
    except Exception as e:
        print(f"Error loading graphs: {str(e)}")
        return []
    
    return graphs

def get_images():
    """Get all JPG files from the images directory"""
    images_dir = os.path.join('static', 'images')
    images = []
    
    try:
        for file in IMAGE_FILES:
            if os.path.exists(os.path.join(images_dir, file)):
                display_name = file.replace('.jpg', '').replace('_', ' ').title()
                images.append({
                    'file': file,
                    'name': display_name
                })
    except Exception as e:
        print(f"Error loading images: {str(e)}")
        return []
    
    return images

@app.route('/')
def index():
    graphs = get_plotly_graphs()
    images = get_images()
    return render_template('index.html', graphs=graphs, images=images)

if __name__ == '__main__':
    print("\nVerifying files...")
    if verify_files():
        print("\nStarting Flask server...")
        app.run(debug=True)
    else:
        print("\nERROR: Some required files are missing. Please check the file paths.")