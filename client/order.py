class Order:


    def output_order(order_list, visitor):
        """
        Toon de bestelling met behulp van een bezoeker.

        Args:
            order_list (list): Een lijst met items in de bestelling.
            visitor (OrderVisitor): De bezoeker die de bestelling verwerkt.

        """
        for order_item in order_list:
            order_item.accept(visitor)