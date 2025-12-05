from product.model.product import Product


class ProductRepository:
    def find_by_id(self, product_id: int) -> Product | None:
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def exists_by_id(self, product_id: int) -> bool:
        return Product.objects.filter(id=product_id).exists()
