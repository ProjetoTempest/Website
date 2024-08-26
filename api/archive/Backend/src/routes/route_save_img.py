from fastapi import UploadFile, APIRouter, File, HTTPException, Form
from typing import List, Optional

from ..utils import save_images

routeSaveImg = APIRouter(prefix="/save_img")

# def save_img(ident_img: str, imgs: Optional[List[UploadFile]] = File(None)):
@routeSaveImg.post("/")
async def save_img(ident_img: str = Form(...), imgs: List[UploadFile] = File()):
    print(imgs)

    valid_imgs = []
    for img in imgs:
        if img.filename.endswith(('.jpg', '.png', '.jpeg')):
            valid_imgs.append(img)

    if not valid_imgs:
        print("Nenhum arquivo válido encontrado.")
        raise HTTPException(status_code=400, detail="Sem imagens")
    
    return await save_images.save(images=valid_imgs, ident_img=ident_img)
        