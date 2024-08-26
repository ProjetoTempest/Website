from fastapi import UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from os.path import exists
from os import remove


IMAGES_PATH = "/api/app/images" # Troque para o caminho da sua pasta de imagens

def get_path_image(dir:str, file_name:str):
    image_dir = f'{IMAGES_PATH}/{dir}/{file_name}.jpg'
    return image_dir

def image_path_on_db(dir:str, file_name: str):
    """
    Gera a URL Correta que deve ser salva no banco de dados, para uma imagem relacionada a um registro
    
    Ex: Imagem referente a um evento, foto de perfil relacionada a um usuário
    
    - Args:
        - dir:: str: Diretório onde a imagem se encontra
        - file_name:: str: Nome do arquivo sem extensão
        
    - Return:
        - link:: str: Link para aquela imagem
    """
    return f"/image?path={get_path_image(dir,file_name)}"

def  upload_image(output: str, file: UploadFile, filename: str):
    """
    Salva uma imagem no servidor e retorna seu caminho em caso de sucesso
    
    Args:
        output:: str: Indica se o arquivo é para eventos ou clientes
        file:: UploadFile: Arquivo a ser salvo
        filename:: str: nome do arquivo sem extensão
    
    Return: 
        str: Caminho do arquivo salvo em caso de sucesso,
    """
    

    try:
        print(file.filename)
        if not file.filename.lower().split('.')[-1] in ["jpg", "jpeg", "png"]:
            print("Error ao salvar a imagem")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato inválido da imagem")
        #contents = file.read() # Método para leitura assincrona
        contents = file.file.read() # método .file para leitura síncrona
        
        saved_at = get_path_image(output,filename)
        print(saved_at)
        with open(saved_at, "wb") as f:
            f.write(contents)
    except:
        raise
    
def get_image_from_URL(image_url: str) -> FileResponse:
    """
    Coleta uma imagem do servidor e a envia no formato FileResponse
    
    - Args:
        - folder:: str: Indica se o arquivo é para eventos, clientes ou marketing
        - filename:: str: nome do arquivo sem extensão
        
    - Returns:
        - FileResponse:: Imagem Encontrada
    """

    if not exists(image_url):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagem não encontrada")
        
    return FileResponse(image_url, media_type='image/jpeg')


def remove_image(folder: str, filename: str):
    """
    Coleta uma imagem do servidor e a remove
    
    - Args:
        - folder:: str: Indica se o arquivo é para eventos, clientes ou marketing
        - filename:: str: nome do arquivo sem extensão
        
    - Returns:
        - None
    """
    
    image_dir = get_path_image(folder, filename)
    
    if not exists(image_dir):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagem não encontrada")
        
    remove(image_dir)
    
