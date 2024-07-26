from typing import List
from fastapi import UploadFile
import os
import shutil
from random import randint

path = "/home/will/Documentos/project_tempest/Website/Backend/imagens/"


async def save_img_path(temp_file_name: str, img: UploadFile):
    try:

        index = temp_file_name.rfind("/")
        file_name = temp_file_name[index+1:]

        if file_name in os.listdir(path=path):
            temp = file_name.replace(".png", "").replace(".jpg", "") \
                + str(randint(0, 1_000_000)) + ".png"
            temp_file_name = temp_file_name.replace(file_name, temp)
            print(temp_file_name)

        with open(temp_file_name, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        return temp_file_name
    except Exception as e:
        print(f"Error ao salvar no diretório: {e}")
        return None


async def save(images: List[UploadFile], ident_img: str):
    """
    Função auxiliar para salvar imagens no diretório especificado.

    Args:
    - images (List[UploadFile]): Lista de arquivos de imagem a serem salvos.
    - ident_img (str): Nome do serviço para criar o nome do arquivo.

    Returns:
    - List[str]: Lista de caminhos dos arquivos salvos.
    """

    if not os.path.exists(path):
        os.makedirs(path)

    saved_image_urls = []

    if len(images) == 1:
        temp_file_name = os.path.join(path, ident_img + images[0].filename)
        saved_path = await save_img_path(temp_file_name=temp_file_name, img=images[0])
        if saved_path:
            return saved_path
        else:
            return []

    for img in images:
        temp_file_name = os.path.join(path, ident_img + img.filename)
        saved_path = await save_img_path(temp_file_name=temp_file_name, img=img)
        if saved_path:
            saved_image_urls.append(saved_path)

    return saved_image_urls
