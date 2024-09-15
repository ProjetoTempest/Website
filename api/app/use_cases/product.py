from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.models import ImagesProducts as ImageProductModel
from app.db.models import Products as ProductModel
from app.schemas.images_products import ImagesProductsResponse
from app.schemas.product import ProductRequest, ProductResponse, ProductUpdate
from app.services.ids import id_generate


class ProductCases:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def add(self, product: ProductRequest) -> dict[str, str]:
        try:
            product_on_db = (
                self.db_session.query(ProductModel)
                .filter_by(title=product.title)
                .first()
            )

            if product_on_db:
                raise HTTPException(
                    status_code=400,
                    detail="Produto já cadastrado"
                )

            product_on_db = ProductModel(
                **product.model_dump(exclude={"images"}),
                id=id_generate()
            )

            self.db_session.add(product_on_db)

            if not product.images:
                self.db_session.commit()
                return {"msg": "Produto cadastrado com sucesso"}

            list_imgs = [
                ImageProductModel(url=img_url, item_id=id, id=id_generate())
                for img_url in product.images
            ]

            self.db_session.add_all(list_imgs)

            product_on_db.images = list_imgs

            self.db_session.commit()

            return {"msg": "Produto cadastrado com sucesso"}

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Internal Server Error: {e}"
            )

    def get(self, product_id: str) -> ProductResponse:
        try:
            product_db = self._product_model_id(product_id)
            product_response = self._assemble_product_response(
                product=product_db
            )

            return product_response

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal Server Error: {e}"
            )

    def get_all(self) -> list[ProductResponse]:
        try:
            product_list = (
                self.db_session.query(ProductModel)
                .options(joinedload(ProductModel.images)).all()
            )

            if not product_list:
                raise HTTPException(
                    status_code=404,
                    detail="Não há nenhum produto cadastrado"
                )

            return self._map_models_to_responses(product_list)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal Server Error: {e}"
            )

    # Fazer a atualização de imagens
    def update(self, product: ProductUpdate) -> dict[str, str]:
        try:
            product_db = self._product_model_id(product.id)

            for field, value in product.dict().items():
                if value:
                    setattr(product_db, field, value)

            self.db_session.commit()

            return {"msg": "Produto atualizado com sucesso"}

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal Server Error: {e}"
            )

    def delete(self, product_id: str) -> dict[str, str]:
        try:
            product_db = self._product_model_id_1(product_id)

            if product_db.images:
                for image in product_db.images:
                    self.db_session.delete(image)

            self.db_session.delete(product_db)
            self.db_session.commit()

            return {"msg": "Produto deletado com sucesso"}

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal Server Error: {e}"
            )

    def _product_model(self, product_title: str) -> ProductModel:
        product_db = (
            self.db_session.query(ProductModel)
            .filter_by(title=product_title)
            .first()
        )

        if not product_db:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        return product_db

    def _product_model_id_1(self, product_id: str) -> ProductModel:
        product_db = (
            self.db_session.query(ProductModel)
            .filter(ProductModel.id == product_id)
            .first()
        )

        if not product_db:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        return product_db

    def _product_model_id(self, product_id: str) -> ProductModel:
        product_db = (
            self.db_session.query(ProductModel)
            .filter(ProductModel.id == product_id)
            .options(joinedload(ProductModel.images))
            .first()
        )

        if not product_db:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        return product_db

    def _map_models_to_responses(
        self, products: list[ProductModel]
    ) -> list[ProductResponse]:
        return [
            self._assemble_product_response(product=product)
            for product in products
        ]

    @staticmethod
    def _assemble_product_response(product: ProductModel) -> ProductResponse:
        if not product.images:
            return ProductResponse(**product.dict())

        return ProductResponse(
            **product.dict(),
            images=[ImagesProductsResponse(**img.dict())
            for img in product.images]
        )
