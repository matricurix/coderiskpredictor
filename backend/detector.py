import ast
import re

class RuleBasedDetector:
    """Rule-based code smell detection"""
    
    def detect_all(self, code):
        """Run all detection rules"""
        smells = []
        smells.extend(self.detect_long_method(code))
        smells.extend(self.detect_too_many_parameters(code))
        smells.extend(self.detect_deep_nesting(code))
        smells.extend(self.detect_god_class(code))
        smells.extend(self.detect_magic_numbers(code))
        return smells
    
    def detect_long_method(self, code):
        """Detect methods longer than threshold"""
        smells = []
        lines = code.split('\n')
        current_function = None
        function_start = 0
        
        for idx, line in enumerate(lines):
            trimmed = line.strip()
            
            # Detect function definition
            if trimmed.startswith('def '):
                # Check previous function
                if current_function and (idx - function_start) > 25:
                    smells.append({
                        'type': 'Long Method',
                        'severity': 'high' if (idx - function_start) > 40 else 'medium',
                        'line': function_start + 1,
                        'description': f"Method '{current_function}' has {idx - function_start} lines. Methods should be under 25 lines.",
                        'suggestion': 'Break this method into smaller, focused functions. Each function should do one thing well.'
                    })
                
                # Start tracking new function
                match = re.match(r'def\s+(\w+)', trimmed)
                if match:
                    current_function = match.group(1)
                    function_start = idx
        
        # Check last function
        if current_function and (len(lines) - function_start) > 25:
            smells.append({
                'type': 'Long Method',
                'severity': 'high' if (len(lines) - function_start) > 40 else 'medium',
                'line': function_start + 1,
                'description': f"Method '{current_function}' has {len(lines) - function_start} lines. Methods should be under 25 lines.",
                'suggestion': 'Break this method into smaller, focused functions. Each function should do one thing well.'
            })
        
        return smells
    
    def detect_too_many_parameters(self, code):
        """Detect functions with too many parameters"""
        smells = []
        lines = code.split('\n')
        
        for idx, line in enumerate(lines):
            match = re.match(r'\s*def\s+(\w+)\((.*?)\):', line)
            if match:
                func_name = match.group(1)
                params_str = match.group(2)
                params = [p.strip() for p in params_str.split(',') if p.strip() and p.strip() != 'self']
                
                if len(params) > 5:
                    smells.append({
                        'type': 'Too Many Parameters',
                        'severity': 'high' if len(params) > 7 else 'medium',
                        'line': idx + 1,
                        'description': f"Function '{func_name}' has {len(params)} parameters. Keep it under 5 for better readability.",
                        'suggestion': 'Consider grouping related parameters into a configuration object or dataclass.'
                    })
        
        return smells
    
    def detect_deep_nesting(self, code):
        """Detect deeply nested code blocks"""
        smells = []
        lines = code.split('\n')
        
        for idx, line in enumerate(lines):
            if not line.strip():
                continue
            
            # Calculate indentation level
            indent = len(line) - len(line.lstrip())
            nesting_level = indent // 4
            
            if nesting_level >= 4:
                smells.append({
                    'type': 'Deep Nesting',
                    'severity': 'high' if nesting_level >= 5 else 'medium',
                    'line': idx + 1,
                    'description': f"Code has {nesting_level} levels of nesting. This makes it hard to understand and test.",
                    'suggestion': 'Use early returns, extract methods, or use guard clauses to reduce nesting.'
                })
        
        return smells
    
    def detect_god_class(self, code):
        """Detect classes with too many methods"""
        smells = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    num_methods = len(methods)
                    
                    if num_methods > 10:
                        smells.append({
                            'type': 'God Class',
                            'severity': 'high' if num_methods > 15 else 'medium',
                            'line': node.lineno,
                            'description': f"Class '{node.name}' has {num_methods} methods. It likely has too many responsibilities.",
                            'suggestion': 'Apply Single Responsibility Principle. Split this class into smaller, focused classes.'
                        })
        except:
            pass
        
        return smells
    
    def detect_magic_numbers(self, code):
        """Detect magic numbers in code"""
        smells = []
        lines = code.split('\n')
        
        for idx, line in enumerate(lines):
            # Skip function/class definitions
            if 'def ' in line or 'class ' in line:
                continue
            
            # Find numbers with 2+ digits
            matches = re.finditer(r'\b(\d{2,})\b', line)
            for match in matches:
                number = match.group(1)
                # Skip common numbers
                if number in ['100', '1000', '0']:
                    continue
                
                smells.append({
                    'type': 'Magic Number',
                    'severity': 'low',
                    'line': idx + 1,
                    'description': f"Magic number '{number}' found. What does it represent?",
                    'suggestion': 'Replace with a named constant to explain its purpose.'
                })
        
        return smells