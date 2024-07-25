def check_valid_param(param_value, param_name, valid_values=None, valid_type=None):
    if valid_type:
        if not isinstance(param_value, valid_type):
            raise ValueError(f'{param_name} must be of type {valid_type}.')
        
    if valid_values:
        if param_value not in valid_values:
            raise ValueError(f'{param_name} must be one of {", ".join(valid_values)}.')