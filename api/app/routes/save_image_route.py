from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from typing import List

from app.services.image import save

router = APIRouter(prefix="/images")


@router.post("/upload-images")
async def upload_images(
    images: List[UploadFile] = File(...)
):
    """
    Rota para receber uma ou várias imagens e salvá-las no servidor.

    Args:
    - images (List[UploadFile]): Lista de arquivos de imagem enviados.
    - ident_img (str): Identificador opcional para prefixar nos nomes dos arquivos.

    Returns:
    - JSONResponse: URLs ou caminhos das imagens salvas.
    """
    if not images:
        raise HTTPException(status_code=400, detail="Nenhuma imagem enviada.")

    saved_image_urls = await save(images)

    if not saved_image_urls:
        raise HTTPException(status_code=500, detail="Falha ao salvar as imagens.")

    return JSONResponse(content={"images": saved_image_urls})
