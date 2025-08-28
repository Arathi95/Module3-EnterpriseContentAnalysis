

import json
from datetime import datetime

class CostTracker:
    def __init__(self, usage_file='usage_data.json'):
        self.usage_file = usage_file
        self.usage_data = self._load_usage_data()
        self.daily_limit = 50.0
        self.monthly_limit = 200.0
        self.input_cost_per_million = 0.50
        self.output_cost_per_million = 1.50

    def _load_usage_data(self):
        try:
            with open(self.usage_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_usage_data(self):
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage_data, f, indent=4)

    def record_usage(self, input_tokens, output_tokens):
        today = datetime.now().strftime('%Y-%m-%d')
        month = datetime.now().strftime('%Y-%m')
        
        cost = (input_tokens / 1_000_000) * self.input_cost_per_million + \
               (output_tokens / 1_000_000) * self.output_cost_per_million

        if today not in self.usage_data:
            self.usage_data[today] = {'tokens': 0, 'cost': 0.0}
        
        self.usage_data[today]['tokens'] += input_tokens + output_tokens
        self.usage_data[today]['cost'] += cost
        
        self._save_usage_data()

    def get_daily_usage(self):
        today = datetime.now().strftime('%Y-%m-%d')
        return self.usage_data.get(today, {'tokens': 0, 'cost': 0.0})

    def get_monthly_usage(self):
        month = datetime.now().strftime('%Y-%m')
        monthly_tokens = 0
        monthly_cost = 0.0
        for date, data in self.usage_data.items():
            if date.startswith(month):
                monthly_tokens += data['tokens']
                monthly_cost += data['cost']
        return {'tokens': monthly_tokens, 'cost': monthly_cost}

    def can_afford_analysis(self, input_tokens, output_tokens):
        daily_usage = self.get_daily_usage()
        monthly_usage = self.get_monthly_usage()
        
        estimated_cost = (input_tokens / 1_000_000) * self.input_cost_per_million + \
                         (output_tokens / 1_000_000) * self.output_cost_per_million

        if daily_usage['cost'] + estimated_cost > self.daily_limit:
            return False, "daily limit exceeded"
        if monthly_usage['cost'] + estimated_cost > self.monthly_limit:
            return False, "monthly limit exceeded"
        
        return True, "ok"

