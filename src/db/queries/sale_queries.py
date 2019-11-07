from datetime import date

def qr_check_cart_exists(buyer_id):
    return f"SELECT * FROM sales WHERE (buyer_id='{buyer_id}' and status=1)"

def qr_create_cart(buyer_id, seller_id):
    return f"INSERT INTO sales(buyer_id, seller_id, date, status) \
    VALUES ({buyer_id}, {seller_id}, '{date.today()}', 1);"

def qr_add_to_cart(product_id, quantity, cart_id):
    return f"INSERT INTO sales_has_product(sales_id, product_id, quantity) \
    VALUES ({cart_id}, {product_id}, '{quantity}');"
    
def qr_get_sale_by_buyer(buyer_id):
    return f"SELECT * FROM sales WHERE buyer_id='{buyer_id}';"

def qr_update_sale_info(sale_id, status):
    return f"UPDATE sales SET status={status} WHERE id={sale_id};"

def qr_get_sale_product(product_id, cart_id):
    return f"SELECT * FROM sales_has_product WHERE (sales_id={cart_id} and product_id={product_id});"

def qr_update_sale_product(product_id, quantity, cart_id):
    return f"UPDATE sales_has_product SET quantity={quantity} WHERE (sales_id={cart_id} and product_id={product_id});"