import json
import requests

def create_discount(points):
    price_rule = create_price_rule(points)
    if 'errors' in price_rule: return False
    price_rule_id = str(price_rule['price_rule']['id'])
    # CREATE DISCOUNT CODE
    d = '''{
      "discount_code": {
        "price_rule_id":'''+price_rule_id+''',
        "code":'''+price_rule_id+''',
        "usage_count": 0
      }
    }
    '''
    discount_data = json.loads(d)
    discount_code = requests.post('https://be-a-rocks.myshopify.com/admin/price_rules/'+price_rule_id+'/discount_codes.json',auth=('a0e37f75c491b58c9a16d57ea285bbda', '5cd41b5c4af088a4ee2e943ca371d26e'),json=discount_data)
    d_code = discount_code.json()
    if 'errors' not in d_code:
        return price_rule_id
    else:
        return False

def create_price_rule(points):
    # CREATE PRICE RULE
    p = '''{
          "price_rule": {
            "title": "POINTS REDEEMED",
            "target_type": "line_item",
            "target_selection": "all",
            "allocation_method": "across",
            "value_type": "fixed_amount",
            "value": -'''+points+''',
            "once_per_customer": true,
            "usage_limit": null,
            "customer_selection": "all",
            "prerequisite_subtotal_range": null,
            "prerequisite_shipping_price_range": null,
            "starts_at": "2017-07-05T16:20:03Z",
            "ends_at": null
          }
        }'''
    price_data = json.loads(p)
    new_price_rule = requests.post('https://be-a-rocks.myshopify.com/admin/price_rules.json', auth=('a0e37f75c491b58c9a16d57ea285bbda', '5cd41b5c4af088a4ee2e943ca371d26e'),json=price_data)
    return new_price_rule.json()
