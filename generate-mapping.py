import os
import json
import argparse
import sys

def is_media_file(filename):
    """Check if a file is a media file based on its extension."""
    media_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.mp4', '.webm', '.ogg']
    return any(filename.lower().endswith(ext) for ext in media_extensions)

def is_hidden(path):
    """Check if a file or directory is hidden (starts with a dot)."""
    return os.path.basename(path).startswith('.')

def scan_directory(path):
    """Recursively scan a directory and return its structure, ignoring hidden files and folders."""
    name = os.path.basename(path)
    
    if is_hidden(path):
        return None
    
    if os.path.isfile(path):
        if is_media_file(name):
            return {
                'name': name,
                'type': 'image' if name.lower().split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif', 'svg'] else 'video'
            }
        else:
            return {
                'name': name,
                'type': 'file',
                'children': []
            }
    
    children = []
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if not is_hidden(item_path):
                result = scan_directory(item_path)
                if result:
                    children.append(result)
    except PermissionError:
        print(f"Warning: Permission denied to access {path}")
    except Exception as e:
        print(f"Warning: Error scanning {path}: {e}")
    
    return {
        'name': name,
        'type': 'folder',
        'children': children
    }

def generate_media_files_json(root_path, output_file):
    """Generate the mapping.json file."""
    structure = scan_directory(root_path)
    
    with open(output_file, 'w') as f:
        json.dump(structure, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Generate a JSON file of media files in a directory, ignoring hidden files and folders.")
    parser.add_argument("root_directory", help="Path to the root directory to scan")
    parser.add_argument("-o", "--output", default="mapping.json", help="Output JSON file name (default: mapping.json)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.root_directory):
        print(f"Error: The specified directory '{args.root_directory}' does not exist.")
        sys.exit(1)
    
    try:
        generate_media_files_json(args.root_directory, args.output)
        print(f"Generated {args.output}")
    except Exception as e:
        print(f"Error generating JSON file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
