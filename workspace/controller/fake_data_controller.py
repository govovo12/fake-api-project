from workspace.utils.fake.fake_helper import (
    fake_username,
    fake_password,
    fake_email,
    fake_product_title,
    fake_product_description,
    fake_product_price,
    fake_cart_quantity,
    fake_cart_date,
)


class FakeDataController:
    """統一管理假資料建構流程，作為 stub/fake 的封裝控制器"""

    @staticmethod
    def get_fake_user_payload() -> dict:
        return {
            "username": fake_username(),
            "password": fake_password(),
            "email": fake_email(),
        }

    @staticmethod
    def get_fake_product_payload() -> dict:
        return {
            "title": fake_product_title(),
            "description": fake_product_description(),
            "price": fake_product_price(),
        }

    @staticmethod
    def get_fake_cart_payload(user_id: int, product_id: int) -> dict:
        return {
            "userId": user_id,
            "date": fake_cart_date(),
            "products": [
                {"productId": product_id, "quantity": fake_cart_quantity()}
            ],
        }

    @staticmethod
    def get_fake_user_cart_bundle() -> dict:
        user = FakeDataController.get_fake_user_payload()
        product = FakeDataController.get_fake_product_payload()
        return {
            "user": user,
            "product": product,
            "cart": FakeDataController.get_fake_cart_payload(
                user_id=1, product_id=1  # 預設為假 ID，之後可替換
            ),
        }
