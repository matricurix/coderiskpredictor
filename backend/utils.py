import ast
import re
from radon.complexity import cc_visit
from radon.metrics import mi_visit

def extract_features(code):
    """Extract numerical features from code for ML model"""
    try:
        tree = ast.parse(code)
        
        # Basic metrics
        lines = code.split('\n')
        num_lines = len([l for l in lines if l.strip()])
        
        # Count various elements
        num_functions = sum(1 for _ in ast.walk(tree) if isinstance(_, ast.FunctionDef))
        num_classes = sum(1 for _ in ast.walk(tree) if isinstance(_, ast.ClassDef))
        num_loops = sum(1 for _ in ast.walk(tree) if isinstance(_, (ast.For, ast.While)))
        num_ifs = sum(1 for _ in ast.walk(tree) if isinstance(_, ast.If))
        
        # Function parameters
        max_params = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                num_params = len(node.args.args)
                max_params = max(max_params, num_params)
        
        # Nesting depth
        max_depth = calculate_max_depth(tree)
        
        # Complexity metrics
        try:
            complexity = sum(block.complexity for block in cc_visit(code))
        except:
            complexity = 0
        
        try:
            maintainability = mi_visit(code, True)
        except:
            maintainability = 100
        
        # Additional metrics
        num_comments = len(re.findall(r'#.*$', code, re.MULTILINE))
        avg_line_length = sum(len(l) for l in lines) / max(len(lines), 1)
        
        return {
            'num_lines': num_lines,
            'num_functions': num_functions,
            'num_classes': num_classes,
            'num_loops': num_loops,
            'num_ifs': num_ifs,
            'max_params': max_params,
            'max_depth': max_depth,
            'complexity': complexity,
            'maintainability': maintainability,
            'num_comments': num_comments,
            'avg_line_length': avg_line_length
        }
    except:
        return None

def calculate_max_depth(node, depth=0):
    """Calculate maximum nesting depth"""
    max_d = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.For, ast.While, ast.If, ast.With)):
            child_depth = calculate_max_depth(child, depth + 1)
            max_d = max(max_d, child_depth)
        else:
            child_depth = calculate_max_depth(child, depth)
            max_d = max(max_d, child_depth)
    return max_d