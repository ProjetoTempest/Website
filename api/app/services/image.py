# from os import remove
# from os.path import exists

# from fastapi import HTTPException, UploadFile, status
# from fastapi.responses import FileResponse

# from typing import List
# import os
# import shutil
# from random import randint

# IMAGES_PATH = "/api/app/images"  # Troque para o caminho da sua pasta de imagens


# def get_path_image(dir: str, file_name: str):
#     image_dir = f'{IMAGES_PATH}/{dir}/{file_name}.jpg'
#     return image_dir


# def image_path_on_db(dir: str, file_name: str):
#     """
#     Gera a URL Correta que deve ser salva no banco de dados, para uma imagem relacionada a um registro
    
#     Ex: Imagem referente a um evento, foto de perfil relacionada a um usuário
    
#     - Args:
#         - dir:: str: Diretório onde a imagem se encontra
#         - file_name:: str: Nome do arquivo sem extensão
        
#     - Return:
#         - link:: str: Link para aquela imagem
#     """
#     return f"/image?path={get_path_image(dir, file_name)}"


# def upload_image(output: str, file: UploadFile, filename: str):
#     """
#     Salva uma imagem no servidor e retorna seu caminho em caso de sucesso
    
#     Args:
#         output:: str: Indica se o arquivo é para eventos ou clientes
#         file:: UploadFile: Arquivo a ser salvo
#         filename:: str: nome do arquivo sem extensão
    
#     Return: 
#         str: Caminho do arquivo salvo em caso de sucesso,
#     """

#     try:
#         print(file.filename)
#         if file.filename.lower().split('.')[-1] not in ["jpg", "jpeg", "png"]:
#             print("Error ao salvar a imagem")
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato inválido da imagem")
#         # contents = file.read() # Método para leitura assincrona
#         contents = file.file.read()  # método .file para leitura síncrona

#         saved_at = get_path_image(output, filename)
#         print(saved_at)
#         with open(saved_at, "wb") as f:
#             f.write(contents)
#     except:
#         raise


# def get_image_from_URL(image_url: str) -> FileResponse:
#     """
#     Coleta uma imagem do servidor e a envia no formato FileResponse
    
#     - Args:
#         - folder:: str: Indica se o arquivo é para eventos, clientes ou marketing
#         - filename:: str: nome do arquivo sem extensão
        
#     - Returns:
#         - FileResponse:: Imagem Encontrada
#     """

#     if not exists(image_url):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagem não encontrada")

#     return FileResponse(image_url, media_type='image/jpeg')


# def remove_image(folder: str, filename: str):
#     """
#     Coleta uma imagem do servidor e a remove
    
#     - Args:
#         - folder:: str: Indica se o arquivo é para eventos, clientes ou marketing
#         - filename:: str: nome do arquivo sem extensão
        
#     - Returns:
#         - None
#     """

#     image_dir = get_path_image(folder, filename)

#     if not exists(image_dir):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagem não encontrada")

#     remove(image_dir)


# path = "/home/will/Downloads/Website/api/app/images/"


# async def save_img_path(temp_file_name: str, img: UploadFile):
#     try:

#         index = temp_file_name.rfind("/")
#         file_name = temp_file_name[index + 1:]

#         if file_name in os.listdir(path=path):
#             temp = file_name.replace(".png", "").replace(".jpg", "") \
#                 + str(randint(0, 1_000_000)) + ".png"
#             temp_file_name = temp_file_name.replace(file_name, temp)
#             print(temp_file_name)

#         with open(temp_file_name, "wb") as buffer:
#             shutil.copyfileobj(img.file, buffer)
#         return temp_file_name
#     except Exception as e:
#         print(f"Error ao salvar no diretório: {e}")
#         return None


# async def save(images: List[UploadFile], ident_img: str):
#     """
#     Função auxiliar para salvar imagens no diretório especificado.

#     Args:
#     - images (List[UploadFile]): Lista de arquivos de imagem a serem salvos.
#     - ident_img (str): Nome do serviço para criar o nome do arquivo.

#     Returns:
#     - List[str]: Lista de caminhos dos arquivos salvos.
#     """

#     if not os.path.exists(path):
#         os.makedirs(path)

#     saved_image_urls = []

#     if len(images) == 1:
#         temp_file_name = os.path.join(path, ident_img + images[0].filename)
#         saved_path = await save_img_path(
#             temp_file_name=temp_file_name, img=images[0]
#             )
#         if saved_path:
#             return [{"url": saved_path}]
#         else:
#             return []

#     for img in images:
#         temp_file_name = os.path.join(path, ident_img + img.filename)
#         saved_path = await save_img_path(
#             temp_file_name=temp_file_name, img=img
#             )
#         if saved_path:
#             saved_image_urls.append({"url": saved_path})

#     return saved_image_urls

import os
import shutil
from typing import List
from uuid import uuid4
from fastapi import UploadFile

# Defina o caminho do diretório de imagens
IMAGE_PATH = "/home/will/Downloads/Website/api/app/images/"
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

async def save_image(img: UploadFile) -> str:
    try:
        # Certifique-se de que o diretório existe
        os.makedirs(IMAGE_PATH, exist_ok=True)

        # Valide a extensão do arquivo
        _, ext = os.path.splitext(img.filename)
        ext = ext.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Extensão de arquivo não suportada: {ext}")

        # Gere um nome de arquivo único
        unique_name = f"{uuid4().hex}{ext}"
        file_path = os.path.join(IMAGE_PATH, unique_name)

        # Salve o arquivo no sistema
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

        return file_path
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")
        return None

async def save(images: List[UploadFile]) -> List[dict]:
    saved_image_urls = []

    for img in images:
        saved_path = await save_image(img)
        if saved_path:
            saved_image_urls.append({"url": saved_path})
        else:
            print(f"Falha ao salvar a imagem {img.filename}")

    return saved_image_urls
