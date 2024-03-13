class OrderVisitor:
    def visit_order(self, order_string):
        print("Processing order using OrderVisitor:")
        print(order_string)

    def visit_order_details(self, order_details):
        print("Processing order details:")
        print(order_details)