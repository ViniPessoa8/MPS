from flask import Blueprint, request, abort
from ..util.constants import SALE_STATES
from ..util.errors import error_resp, InvalidRequest, CouldNotFindProductOwner
from ..db.auth import check_auth
from ..db.user import get_product_owner
from ..db.sale import (
    check_cart_exists,
    check_sale_exists_seller,
    add_product_cart,
    add_product_new_cart,
    get_sale_by_buyer,
    update_sale_info,
    get_cart_info,
    remove_product_from_cart
)

bp = Blueprint('sale', __name__, url_prefix='/sale')

@bp.route('/cart', methods=['POST'])
def add_to_cart():
    params = request.json
    auth   = request.headers.get('Authorization')
    result = None

    buyer = check_auth(auth)
    if buyer == None:
        abort(403)
    
    try:
        if (
            params == None or
            not 'product_id' in params or
            not 'quantity'   in params
        ):
            raise InvalidRequest
        
        cart = check_cart_exists(buyer_id=buyer['id'])

        if cart != None:
            result = add_product_cart(product_id=params['product_id'], quantity=params['quantity'], cart_id=cart['id'])
        else:
            seller = get_product_owner(product_id=params['product_id'])
            if 'error' in seller:
                raise CouldNotFindProductOwner
            
            result = add_product_new_cart(buyer_id=buyer['id'], product_id=params['product_id'], quantity=params['quantity'], seller_id=seller['id'])

        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/cart', methods=['DELETE'])
def remove_from_cart():
    params = request.args
    auth   = request.headers.get('Authorization')
    result = None

    user = check_auth(auth)
    if user == None:
        abort(403)
    
    try:
        if params == None or not 'product_id' in params:
            raise InvalidRequest
        
        cart = check_cart_exists(buyer_id=user['id'])
        if cart == None:
            raise InvalidRequest

        result = remove_product_from_cart(product_id=params['product_id'], cart_id=cart['id'])
    
        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/cart', methods=['GET'])
def get_cart():
    auth   = request.headers.get('Authorization')
    result = None

    user = check_auth(auth)
    if user == None:
        abort(403)
    
    try:
        cart = check_cart_exists(buyer_id=user['id'])
        if cart == None:
            raise InvalidRequest

        result = get_cart_info(cart_id=cart['id'])

        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/buy', methods=['GET'])
def request_sale():
    auth = request.headers.get('Authorization')

    user = check_auth(auth)
    if user == None:
        abort(403)

    try:
        sale = get_sale_by_buyer(buyer_id=user['id'])

        if sale == None or sale['status'] != SALE_STATES['CART']:
            raise InvalidRequest
        
        result = update_sale_info(sale_id=sale['id'], status=SALE_STATES['WAITING_CONFIRMATION'])

        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/confirm_request', methods=['GET'])
def confirm_request():
    params = request.args
    auth   = request.headers.get('Authorization')
    result = None

    seller = check_auth(auth)
    if seller == None:
        abort(403)
    
    try:
        if params == None or not 'sale_id' in params:
            raise InvalidRequest
        
        sale = check_sale_exists_seller(seller_id=seller['id'], sale_id=params['sale_id'])
        if sale == None:
            raise InvalidRequest

        result = update_sale_info(sale_id=sale['id'], status=SALE_STATES['WAITING_DELIVERY'])
    
        return result
    except BaseException as e:
        return error_resp(e)