from products.models import Product

class Featured():
    def __init__(self, request):
        self.session = request.session
        featured = self.session.get('session_key')

        if featured is None:
            featured = {}
            self.session['session_key'] = featured

        self.featured = featured

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.featured:
            self.featured[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 1
            }
        else:
            self.featured[product_id]['quantity'] += 1
        
        self.session['session_key'] = self.featured  
        self.session.modified = True

    
    def get_prods(self):
        products_ids = [int(pid) for pid in self.featured.keys()] 
        products = Product.objects.filter(id__in=products_ids)

        # Add quantity information
        for product in products:
            product.quantity = self.featured[str(product.id)]['quantity']

        return products

    
    def get_total_quantity(self):
        """Returns the total quantity of items in the cart."""
        return len(self.featured)

    
    # def delete(self, product):
    #     product_id = str(product)  

    #     if product_id in self.featured:
    #         del self.featured[product_id]
    #         self.session['featured_session_key'] = self.featured
    #         self.session.modified = True

    def delete(self, product):
        product_id = str(product)

        if product_id in self.featured:
            del self.featured[product_id]
            self.session['session_key'] = self.featured
            self.session.modified = True

    def is_favorited(self, product):
        """Check if the product is in favorites."""
        return str(product.id) in self.featured
