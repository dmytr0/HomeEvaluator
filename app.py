#!/usr/bin/env python3
"""
Home Evaluator Web Application
Flask-based web interface for the Home Evaluator system
"""

from flask import Flask, render_template, request, jsonify
import json
from home_evaluator import HomeEvaluator, House, EvaluationWeights

app = Flask(__name__)

# Global evaluator instance
evaluator = HomeEvaluator()


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/evaluate', methods=['POST'])
def evaluate():
    """Evaluate a single house"""
    try:
        data = request.get_json()
        house_data = data.get('house', {})
        custom_weights = data.get('weights', {})
        custom_params = data.get('custom_params', [])
        
        # Create House object from data
        house = House.from_dict(house_data)
        
        # Apply custom weights
        weights = EvaluationWeights.from_dict(custom_weights)
        custom_evaluator = HomeEvaluator(weights)
        
        # Evaluate
        result = custom_evaluator.evaluate_house(house)
        
        # Add custom parameters evaluation
        if custom_params:
            result['custom_scores'] = evaluate_custom_params(house, custom_params, custom_weights)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/compare', methods=['POST'])
def compare():
    """Compare multiple houses"""
    try:
        data = request.get_json()
        houses_data = data.get('houses', [])
        custom_weights = data.get('weights', {})
        custom_params = data.get('custom_params', [])
        
        # Create House objects
        houses = [House.from_dict(h) for h in houses_data]
        
        # Apply custom weights
        weights = EvaluationWeights.from_dict(custom_weights)
        custom_evaluator = HomeEvaluator(weights)
        
        # Evaluate all houses
        results = custom_evaluator.compare_houses(houses, sort_by='final_score')
        
        # Add custom parameters evaluation
        if custom_params:
            for result in results:
                house_data = result.get('house', {})
                house = House.from_dict(house_data)
                result['custom_scores'] = evaluate_custom_params(house, custom_params, custom_weights)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/weights', methods=['GET'])
def get_weights():
    """Get default weights"""
    try:
        weights = EvaluationWeights()
        return jsonify(weights.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/weights', methods=['POST'])
def save_weights():
    """Save custom weights"""
    try:
        data = request.get_json()
        weights_data = data.get('weights', {})
        weights = EvaluationWeights.from_dict(weights_data)
        return jsonify({'status': 'success', 'weights': weights.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/config', methods=['GET'])
def get_config():
    """Get evaluator configuration"""
    try:
        config = {
            'reference_price': evaluator.REFERENCE_PRICE,
            'reference_area': evaluator.REFERENCE_AREA,
            'reference_year': evaluator.REFERENCE_YEAR,
            'max_distance': evaluator.MAX_DISTANCE,
            'condition_scores': evaluator.CONDITION_SCORES
        }
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/house_template', methods=['GET'])
def get_house_template():
    """Get template for a new house"""
    try:
        template = {
            'name': '',
            'price': 0,
            'area': 0,
            'has_gas': False,
            'has_water': False,
            'has_sewer': False,
            'has_electricity': False,
            'has_heating': False,
            'has_bathroom': False,
            'has_kitchen': False,
            'condition': 'average',
            'location_rating': 5,
            'year_built': None,
            'floors': 1,
            'has_garden': False,
            'has_garage': False,
            'distance_to_city': None
        }
        return jsonify(template)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def evaluate_custom_params(house, custom_params, custom_weights):
    """
    Evaluate custom parameters for a house
    
    Args:
        house: House object
        custom_params: List of custom parameter definitions
        custom_weights: Dictionary of custom weights
    
    Returns:
        Dictionary with custom parameter scores
    """
    custom_scores = {}
    
    for param in custom_params:
        param_name = param.get('name', '')
        param_type = param.get('type', 'bool')
        param_weight = custom_weights.get(f'{param_name}_weight', 5.0)
        
        # Get parameter value from house
        param_value = getattr(house, param_name, None)
        
        # If parameter doesn't exist in house, use default
        if param_value is None and param_name in house.to_dict():
            param_value = house.to_dict()[param_name]
        
        # Calculate score based on type
        if param_type == 'bool':
            # Boolean parameter: 1.0 if True, 0.0 if False
            score = 1.0 if param_value else 0.0
        elif param_type == 'float':
            # Numeric parameter: normalize to 0-1 range
            if param_value is None:
                score = 0.5  # Default score for missing numeric value
            else:
                # For now, just normalize to 0-1 based on some reasonable range
                # This can be customized per parameter
                score = min(1.0, max(0.0, param_value / 100.0))
        elif param_type == 'select':
            # Select parameter: map options to scores
            options = param.get('options', ['low', 'medium', 'high'])
            if param_value in options:
                score = (options.index(param_value) + 1) / len(options)
            else:
                score = 0.5  # Default for unknown option
        else:
            score = 0.5  # Default score
        
        custom_scores[param_name] = {
            'value': param_value,
            'score': score,
            'weight': param_weight,
            'weighted': score * param_weight,
            'type': param_type
        }
    
    return custom_scores


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
