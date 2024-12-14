from google.cloud import vision
import os

# Configurar o caminho para o arquivo JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\cleov\\OneDrive\\Área de Trabalho\\assets\\vision\\turing-lyceum-435603-k1-286d58aceeda.json"

# Cliente Vision API
client = vision.ImageAnnotatorClient()

# Testar OCR em uma imagem
with open("nota_fiscal.jpg", "rb") as image_file:
    content = image_file.read()
image = vision.Image(content=content)

response = client.text_detection(image=image)
print(response.text_annotations[0].description)  # Texto extraído
