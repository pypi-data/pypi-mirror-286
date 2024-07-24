import os
from .download_models import download_models

class Processor:
    def __init__(self, model_dir='~/.processpdfdocs/models', openai_api_key=None):
        assert openai_api_key is not None, "OpenAI API key is required"
        self.model_dir = os.path.expanduser(model_dir)
        self.openai_api_key = openai_api_key

        self.temp_image_converted_path = './temp_image_converted'
        if not os.path.exists(self.temp_image_converted_path):
            os.makedirs(self.temp_image_converted_path)

        self._check_and_download_models()
        self._import_utils()

    def _check_and_download_models(self):
        required_models = ['rotation_model.onnx', 'table_detect_model.pt', 'cell_detect_model.pt']
        for model in required_models:
            if not os.path.exists(os.path.join(self.model_dir, model)):
                print(f"Model {model} not found. Downloading...")
                download_models(self.model_dir)
                break

    def _import_utils(self):
        global is_text_selectable, ocr_pdf_to_text_and_html, extract_table_from_pdf
        from .utils import is_text_selectable, ocr_pdf_to_text_and_html, extract_table_from_pdf

    def process_pdf(self, pdf_path):
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"The file {pdf_path} does not exist.")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError("The provided file is not a PDF.")
        
        if not is_text_selectable(pdf_path):
            extracted_text = ocr_pdf_to_text_and_html(pdf_path, temp_image_converted_path=self.temp_image_converted_path, openai_api_key=self.openai_api_key)
            texts = "\n".join(extracted_text)
        else:
            extracted_text = extract_table_from_pdf(pdf_path, openai_api_key=self.openai_api_key)
            texts = "\n".join(extracted_text)

        return texts
