from faker import Faker
from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime, timedelta

class TestDataGenerator:
    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None):
        self.fake = Faker(locale)
        if seed is not None:
            Faker.seed(seed)
            
    def generate_user(self, include_address: bool = False) -> Dict[str, Any]:
        """Generate random user data"""
        user = {
            'id': self.fake.unique.random_number(digits=6),
            'username': self.fake.user_name(),
            'email': self.fake.email(),
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'phone': self.fake.phone_number(),
            'created_at': self.fake.date_time_this_year().isoformat()
        }
        
        if include_address:
            user['address'] = {
                'street': self.fake.street_address(),
                'city': self.fake.city(),
                'state': self.fake.state(),
                'country': self.fake.country(),
                'postcode': self.fake.postcode()
            }
            
        return user
    
    def generate_product(self) -> Dict[str, Any]:
        """Generate random product data"""
        return {
            'id': self.fake.unique.random_number(digits=6),
            'name': self.fake.catch_phrase(),
            'description': self.fake.text(max_nb_chars=200),
            'price': round(self.fake.random_number(4) / 100, 2),
            'category': self.fake.word(ext_word_list=['Electronics', 'Clothing', 'Books', 'Home', 'Sports']),
            'stock': self.fake.random_int(min=0, max=1000),
            'rating': round(self.fake.random.uniform(1, 5), 1),
            'created_at': self.fake.date_time_this_year().isoformat()
        }
    
    def generate_order(self, num_items: int = None) -> Dict[str, Any]:
        """Generate random order data"""
        if num_items is None:
            num_items = self.fake.random_int(min=1, max=5)
            
        items = []
        total = 0
        
        for _ in range(num_items):
            product = self.generate_product()
            quantity = self.fake.random_int(min=1, max=5)
            item_total = product['price'] * quantity
            
            items.append({
                'product_id': product['id'],
                'product_name': product['name'],
                'quantity': quantity,
                'unit_price': product['price'],
                'total': item_total
            })
            
            total += item_total
        
        return {
            'id': self.fake.unique.random_number(digits=8),
            'user_id': self.fake.unique.random_number(digits=6),
            'items': items,
            'total': round(total, 2),
            'status': self.fake.random_element(['pending', 'processing', 'shipped', 'delivered']),
            'created_at': self.fake.date_time_this_year().isoformat()
        }
    
    def save_test_data(self, data: Any, filename: str) -> str:
        """Save generated test data to a JSON file"""
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
        return filepath
    
    def generate_date_range(self, start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> Dict[str, str]:
        """Generate a random date range within specified bounds"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
            
        date = self.fake.date_time_between(start_date=start_date, end_date=end_date)
        duration = self.fake.random_int(min=1, max=30)
        end = date + timedelta(days=duration)
        
        return {
            'start_date': date.isoformat(),
            'end_date': end.isoformat(),
            'duration_days': duration
        }
    
    def generate_api_response(self, status_code: int = 200) -> Dict[str, Any]:
        """Generate mock API response data"""
        return {
            'status': status_code,
            'timestamp': self.fake.iso8601(),
            'data': {
                'id': self.fake.uuid4(),
                'message': self.fake.sentence(),
                'details': self.fake.paragraph()
            },
            'metadata': {
                'version': f"{self.fake.random_int(1, 5)}.{self.fake.random_int(0, 9)}.{self.fake.random_int(0, 9)}",
                'generated_at': self.fake.iso8601()
            }
        }