import json
import re
import sys

def extract_latex_from_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    latex_expressions = []
    
    for item in data:
        if item.get('type') == 'expression' and 'latex' in item:
            latex_expressions.append(item['latex'])
    
    content = '\n'.join(latex_expressions)
    
    content = re.sub(r'\\\\', r'\\', content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_latex.py <input_json_file> <output_text_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        extract_latex_from_json(input_file, output_file)
        print(f"LaTeX expressions extracted to {output_file}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
    except json.JSONDecodeError:
        print(f"Error: '{input_file}' is not a valid JSON file")
    except Exception as e:
        print(f"Error: {e}")