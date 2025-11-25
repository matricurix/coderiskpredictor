import pandas as pd
import random

def generate_training_data():
    """Generate synthetic code smell dataset with more diversity"""
    
    samples = []
    
    # Long Method samples (SMELL) - High confidence
    long_methods = [
        """def process_user_data(user_id, name, email, age, address):
    user = get_user(user_id)
    if user:
        validate_email(email)
        validate_age(age)
        update_database(user_id, name, email)
        send_notification(email)
        log_activity(user_id)
        calculate_metrics(user)
        generate_report(user)
        update_cache(user_id)
        trigger_webhook(user)
        cleanup_old_data()
        process_analytics(user)
        sync_external_systems(user)
        update_search_index(user)
        invalidate_cache(user_id)
        send_welcome_email(email)
        create_audit_log(user_id)
        update_statistics()
        refresh_recommendations(user)
    return user""",
        
        """def calculate_invoice(items, tax_rate, discount, shipping):
    total = 0
    for item in items:
        price = item.price
        quantity = item.quantity
        subtotal = price * quantity
        total += subtotal
    tax = total * tax_rate
    total_with_tax = total + tax
    discount_amount = total_with_tax * discount
    final_total = total_with_tax - discount_amount
    shipping_cost = calculate_shipping(items)
    grand_total = final_total + shipping_cost
    apply_loyalty_discount(grand_total)
    check_minimum_order(grand_total)
    validate_payment_method()
    process_payment(grand_total)
    send_confirmation_email()
    update_inventory(items)
    generate_invoice_pdf()
    log_transaction(grand_total)
    return grand_total""",
    ]
    
    for code in long_methods:
        samples.append({
            'code': code,
            'smell_type': 'long_method',
            'has_smell': 1,
            'severity': 'high'
        })
    
    # Borderline long methods (AMBIGUOUS - sometimes smell, sometimes not)
    borderline_long = [
        """def process_order(order):
    validate_order(order)
    check_inventory(order)
    calculate_total(order)
    apply_discount(order)
    process_payment(order)
    send_confirmation(order)
    update_inventory(order)
    log_transaction(order)
    return order""",
        
        """def generate_report(data):
    filtered = filter_data(data)
    sorted_data = sort_data(filtered)
    grouped = group_by_category(sorted_data)
    calculated = calculate_metrics(grouped)
    formatted = format_output(calculated)
    return formatted"""
    ]
    
    for code in borderline_long:
        samples.append({
            'code': code,
            'smell_type': 'borderline',
            'has_smell': random.choice([0, 1]),
            'severity': 'medium'
        })
    
    # Too Many Parameters samples (SMELL)
    many_params = [
        """def create_user(name, email, password, age, country, city, zipcode, phone, address):
    return User(name, email, password, age, country, city, zipcode, phone, address)""",
        
        """def send_email(to, from_addr, subject, body, cc, bcc, priority, attachments, reply_to):
    email = Email(to, from_addr, subject, body)
    return email.send()""",
        
        """def process_payment(card_number, cvv, expiry, amount, currency, customer_id, order_id, billing_address):
    payment = Payment(card_number, cvv, expiry, amount)
    return payment.process()""",
    ]
    
    for code in many_params:
        samples.append({
            'code': code,
            'smell_type': 'too_many_parameters',
            'has_smell': 1,
            'severity': 'high'
        })
    
    # Acceptable parameter counts (NO SMELL)
    acceptable_params = [
        """def create_user(name, email, password):
    return User(name, email, password)""",
        
        """def calculate_price(base, tax, discount):
    return base * (1 + tax) * (1 - discount)""",
        
        """def send_notification(user_id, message):
    notification = Notification(user_id, message)
    return notification.send()"""
    ]
    
    for code in acceptable_params:
        samples.append({
            'code': code,
            'smell_type': 'none',
            'has_smell': 0,
            'severity': 'none'
        })
    
    # Deep Nesting samples (SMELL)
    deep_nesting = [
        """def validate_input(data):
    if data:
        if data.user:
            if data.user.age:
                if data.user.age > 18:
                    if data.user.verified:
                        if data.user.email:
                            return True
    return False""",
        
        """def process_order(order):
    if order:
        if order.items:
            for item in order.items:
                if item.available:
                    if item.price > 0:
                        if item.quantity > 0:
                            if check_stock(item):
                                add_to_cart(item)""",
    ]
    
    for code in deep_nesting:
        samples.append({
            'code': code,
            'smell_type': 'deep_nesting',
            'has_smell': 1,
            'severity': 'high'
        })
    
    # Moderate nesting (NO SMELL)
    moderate_nesting = [
        """def validate_user(user):
    if not user:
        return False
    if not user.email:
        return False
    if user.age < 18:
        return False
    return True""",
        
        """def process_item(item):
    if item.available:
        if item.price > 0:
            return add_to_cart(item)
    return None"""
    ]
    
    for code in moderate_nesting:
        samples.append({
            'code': code,
            'smell_type': 'none',
            'has_smell': 0,
            'severity': 'none'
        })
    
    # God Class samples (SMELL)
    god_classes = [
        """class UserManager:
    def create_user(self): pass
    def update_user(self): pass
    def delete_user(self): pass
    def validate_user(self): pass
    def send_email(self): pass
    def log_activity(self): pass
    def calculate_metrics(self): pass
    def generate_report(self): pass
    def export_data(self): pass
    def import_data(self): pass
    def sync_database(self): pass
    def backup_data(self): pass
    def restore_data(self): pass
    def archive_user(self): pass""",
    ]
    
    for code in god_classes:
        samples.append({
            'code': code,
            'smell_type': 'god_class',
            'has_smell': 1,
            'severity': 'high'
        })
    
    # Well-designed classes (NO SMELL)
    good_classes = [
        """class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def validate(self):
        return self.email and '@' in self.email
    
    def to_dict(self):
        return {'name': self.name, 'email': self.email}""",
        
        """class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b"""
    ]
    
    for code in good_classes:
        samples.append({
            'code': code,
            'smell_type': 'none',
            'has_smell': 0,
            'severity': 'none'
        })
    
    # Clean Code samples (NO SMELL) - More variety
    clean_code = [
        "def calculate_total(items):\n    return sum(item.price * item.quantity for item in items)",
        
        "def get_user_by_id(user_id):\n    return database.query(User).filter_by(id=user_id).first()",
        
        "def format_date(date):\n    return date.strftime('%Y-%m-%d')",
        
        "def is_valid_age(age):\n    return 0 < age < 150",
        
        "def calculate_discount(price, percentage):\n    return price * (percentage / 100)",
        
        "def is_empty(value):\n    return value is None or len(value) == 0",
        
        # Add 30 more clean samples
        "def find_max(numbers):\n    return max(numbers) if numbers else None",
        "def is_even(number):\n    return number % 2 == 0",
        "def reverse_string(text):\n    return text[::-1]",
        "def square(x):\n    return x * x",
        "def get_first(items):\n    return items[0] if items else None",
        "def concat(a, b):\n    return str(a) + str(b)",
        "def is_positive(num):\n    return num > 0",
        "def average(numbers):\n    return sum(numbers) / len(numbers)",
        "def capitalize_name(name):\n    return name.title()",
        "def get_length(items):\n    return len(items)",
        "def multiply_by_two(x):\n    return x * 2",
        "def is_none(value):\n    return value is None",
        "def join_strings(strings):\n    return ' '.join(strings)",
        "def get_last(items):\n    return items[-1] if items else None",
        "def count_items(items):\n    return len(items)",
        "def add_tax(price):\n    return price * 1.1",
        "def remove_spaces(text):\n    return text.strip()",
        "def to_lowercase(text):\n    return text.lower()",
        "def is_digit(char):\n    return char.isdigit()",
        "def abs_value(num):\n    return abs(num)",
        "def round_number(num):\n    return round(num, 2)",
        "def split_text(text):\n    return text.split()",
        "def contains(items, value):\n    return value in items",
        "def get_min(numbers):\n    return min(numbers)",
        "def format_price(amount):\n    return f'${amount:.2f}'",
        "def is_alpha(char):\n    return char.isalpha()",
        "def negate(value):\n    return not value",
        "def increment(num):\n    return num + 1",
        "def decrement(num):\n    return num - 1",
        "def get_type(obj):\n    return type(obj).__name__",
    ]
    
    for code in clean_code:
        samples.append({
            'code': code,
            'smell_type': 'none',
            'has_smell': 0,
            'severity': 'none'
        })
    
    # Create variations with noise
    expanded_samples = []
    
    # Base samples
    expanded_samples.extend(samples)
    
    # Create variations with substitutions
    word_variations = {
        'user': ['customer', 'account', 'person', 'member', 'client'],
        'order': ['purchase', 'transaction', 'sale', 'booking'],
        'data': ['info', 'details', 'record', 'entity'],
        'email': ['mail', 'message', 'notification'],
        'process': ['handle', 'execute', 'perform'],
        'calculate': ['compute', 'determine', 'evaluate'],
        'validate': ['verify', 'check', 'confirm'],
    }
    
    # Generate 12 variations of each sample
    for _ in range(12):
        for sample in samples:
            code_var = sample['code']
            
            # Apply random word substitutions
            for original, replacements in word_variations.items():
                if original in code_var.lower():
                    replacement = random.choice(replacements)
                    code_var = code_var.replace(original, replacement)
                    code_var = code_var.replace(original.capitalize(), replacement.capitalize())
            
            expanded_samples.append({
                'code': code_var,
                'smell_type': sample['smell_type'],
                'has_smell': sample['has_smell'],
                'severity': sample['severity']
            })
    
    # Add some intentionally mislabeled samples (noise) - 5%
    num_noise = int(len(expanded_samples) * 0.05)
    if num_noise > 0:
        noise_indices = random.sample(range(len(expanded_samples)), num_noise)
        
        for idx in noise_indices:
            expanded_samples[idx]['has_smell'] = 1 - expanded_samples[idx]['has_smell']
    
    df = pd.DataFrame(expanded_samples)
    return df

# Generate and save dataset
if __name__ == "__main__":
    import os
    
    if not os.path.exists('data'):
        os.makedirs('data')
    
    print("🔄 Generating improved training dataset...")
    df = generate_training_data()
    df.to_csv('data/code_samples.csv', index=False)
    
    print(f"\n✅ Generated {len(df)} training samples")
    print("\n📊 Distribution:")
    print(df['smell_type'].value_counts())
    print("\n🎯 Label Distribution:")
    print(f"   Has Smell: {sum(df['has_smell'])} ({sum(df['has_smell'])/len(df)*100:.1f}%)")
    print(f"   Clean Code: {len(df) - sum(df['has_smell'])} ({(len(df)-sum(df['has_smell']))/len(df)*100:.1f}%)")
    print("\n💾 Saved to: data/code_samples.csv")
    print("\n⚠️  Note: Dataset includes 5% label noise for realistic accuracy")