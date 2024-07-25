import json
import os
import cv2
# import pdfplumber
import fitz
import pdf2image
import PyPDF2
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
import pdfplumber
# import pdftotext
import pytesseract
import numpy as np
from PIL import Image
from ultralytics import YOLO

import onnxruntime as ort

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from paddleocr import PaddleOCR, PPStructure

import base64
import mimetypes
import requests

classes = ['0', '180', '270', '90']

model_dir = os.getenv('MODEL_DIR', os.path.join(os.path.expanduser('~'), '.processpdfdocs', 'models'))

rotation_model = ort.InferenceSession(os.path.join(model_dir, 'rotation_model.onnx'))
rotation_model_input_name = rotation_model.get_inputs()[0].name
rotation_model_output_name = rotation_model.get_outputs()[0].name

config = Cfg.load_config_from_name('vgg_seq2seq')
config['cnn']['pretrained'] = False
config['device'] = "cpu"

detector = Predictor(config)

table_detector = YOLO(os.path.join(model_dir, 'table_detect_model.pt'))
cell_detector = YOLO(os.path.join(model_dir, 'cell_detect_model.pt'))

def is_text_selectable(pdf_path):
    if not pdf_path.lower().endswith('.pdf'):
        print("The file is not a PDF.")
        return False
    
    try:
        pdf_document = fitz.open(pdf_path)
        text_content_threshold = 150
        total_text_length = 0

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text("text")
            total_text_length += len(text.strip())

        if total_text_length <= text_content_threshold:
            return False

        if total_text_length > text_content_threshold:
            common_signature_phrases = ["Digitally signed", "Signature", "Certified by", "Ngày ký:"]
            if any(phrase in text for phrase in common_signature_phrases):
                return False
            return True

    except Exception as e:
        print(f"An error occurred: {e}")
    return False

def generate_html_table(cells_dict):
    cells = list(cells_dict.items())

    # if not cells:
    #     return "<table></table>"

    cells.sort(key=lambda item: item[0][1])
    try:
        rows = []
        current_row = []
        current_y = cells[0][0][1]
    except:
        print('No cell detected')
        return ''
    threshold = 10

    for cell in cells:
        bbox = cell[0]
        if bbox[1] > current_y + threshold:
            rows.append(current_row)
            current_row = []
            current_y = bbox[1]
        current_row.append(cell)
    
    if current_row:
        rows.append(current_row)
    
    for row in rows:
        row.sort(key=lambda item: item[0][0])

    html = "<table>\n"
    for row in rows:
        html += "  <tr>\n"
        for cell in row:
            cell_text = cell[1].replace("\n", "<br>")
            html += f"    <td>{cell_text}</td>\n"
        html += "  </tr>\n"
    html += "</table>"

    return html

def generate_markdown_table(cells_dict):
    cells = list(cells_dict.items())

    if not cells:
        return ""

    cells.sort(key=lambda item: item[0][1])
    rows = []
    current_row = []
    current_y = cells[0][0][1]
    threshold = 10

    for cell in cells:
        bbox = cell[0]
        if bbox[1] > current_y + threshold:
            rows.append(current_row)
            current_row = []
            current_y = bbox[1]
        current_row.append(cell)
    
    if current_row:
        rows.append(current_row)
    
    for row in rows:
        row.sort(key=lambda item: item[0][0])

    num_columns = max(len(row) for row in rows)

    markdown = ""
    
    if rows:
        header_row = rows[0]
        header = "| " + " | ".join([cell[1].replace("\n", "<br>") for cell in header_row]) + " |\n"
        separator = "| " + " | ".join(["---" for _ in header_row]) + " |\n"
        markdown += header + separator

        for row in rows[1:]:
            row_cells = [cell[1].replace("\n", "<br>") for cell in row]
            row_texts = "| " + " | ".join(row_cells) + " |\n"
            if len(row_cells) < num_columns:
                row_texts = row_texts[:-2] + " |" * (num_columns - len(row_cells)) + "\n"
            markdown += row_texts

    return markdown

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def describe_image_with_openai(image_mime_type, base64_image, openai_api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
        Mô tả hình ảnh nhận được.
        Cần sử dụng từ ngữ mạch lạc, các câu văn liên kết tự nhiên với nhau. Chỉ sử dụng ký tự chữ cái thông thường, không sử dụng các ký tự code của markdown hay html.

        Đầu tiên bạn cần xác định xem ảnh này thuộc loại nào trong 4 nhãn sau, tuy nhiên KHÔNG cần ghi nhãn của hình ảnh trong mô tả của bạn: 
        - "Flow": Chứa các bước hay luồng hoạt động của một chương trình hoặc một quy trình, lưu đồ,...
        - "Table": Chứa bảng (table) hay biểu mẫu (form), mẫu đơn,...
        - "Text": Chỉ chứa các đoạn chữ bình thường mà không chứa bảng hay luồng hoạt động.
        - "Image": Là một hình ảnh thông thường, không chứa bảng, luồng hoạt động hay đoạn chữ bình thường
        
        Hãy làm theo chính xác những gì được hướng dẫn với mỗi loại hình ảnh, và không sử dụng hướng dẫn khác cho loại hình ảnh đó:

        - Loại 1: Nếu hình ảnh thuộc nhãn "Flow", hãy mô tả ngắn gọn nhưng chính xác từng bước trong quy trình hoặc luồng đó. Hãy chắc chắn rằng bạn mô tả các bước theo đúng thứ tự của các bước trong luồng hoặc quy trình. Nếu quy trình hay luồng có nhiều bước, hãy sử dụng các từ sao cho phù hợp và tự nhiên nhất để giúp người đọc theo dõi. Sử dụng kí tự xuống dòng như '\n' hay '\n\n' nếu cần thiết.
        
        - Loại 2: Nếu hình ảnh thuộc nhãn "Table", hãy định hình vị trí của bảng, sau đó tái cấu trúc lại bảng trong hình ảnh dưới dạng bảng markdown, đồng thời tuyệt đối không sử dụng thêm từ ngữ mô tả nào khác cho hình ảnh có chứa bảng, chỉ cần đưa ra bảng ở định dạng markdown. Với các ô trong bảng với nội dung nhiều dòng, hãy sử dụng kí tự xuống dòng của markdown như <br> để phân biệt các dòng trong ô đó. Nếu trong hình ảnh vừa có bảng vừa có một phần nhỏ text, hãy viết lại phần text đó đúng vị trí của nó so với vị trí của bảng, không cần sử dụng markdown hay html.
        
        - Loại 3: Nếu hình ảnh thuộc nhãn "Text", hãy OCR hình ảnh đó và trả về kết quả OCR dưới dạng văn bản thông thường, giữ nguyên cấu trúc ban đầu của đoạn chữ trong ảnh, không cần sử dụng markdown hay html.

        - Loại 4: Nếu hình ảnh thuộc nhãn "Image", hãy mô tả ngắn gọn nhưng chính xác về nội dung của hình ảnh đó, bao gồm các chi tiết quan trọng như đối tượng, bối cảnh, màu sắc chủ đạo, vân vân, đồng thời nói lên ý nghĩa của bức hình
        
        Nếu có thể trình bày kĩ hơn về các bước trong luồng hoặc quy trình hoạt động, hãy sử dụng các từ ngữ mạch lạc, các câu văn liên kết tự nhiên với nhau. Tuy nhiên tuyệt đối không được sử dụng từ ngữ để trình bày các bảng, với các bảng chỉ được cung cấp bảng dưới dạng markdown.
        Nếu có các tên chức danh, tên vị trí, tên tổ chức, tên sản phẩm, tên dịch vụ, tên công nghệ, vân vân, hãy sử dụng chúng trong ngoặc kép để nhấn mạnh, ví dụ: Sau khi nhấn vào nút "Đăng nhập", hệ thống sẽ chuyển hướng đến trang "Đăng nhập" để yêu cầu nhập tên đăng nhập và mật khẩu.
        Các mô tả bạn đưa ra để mô tả các bước, các luồng phải rõ ràng, mạch lạc, liên kết với nhau như một đoạn văn nói, đoạn giải thích, đoạn hướng dẫn, vân vân, sao cho người đọc có thể hiểu rõ nội dung hình ảnh mà không cần xem hình ảnh đó.
        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{image_mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def text_extraction(element):
    line_text = element.get_text()

    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    format_per_line = list(set(line_formats))
    
    return (line_text, format_per_line)

def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    
    return table

def table_converter(table):
    table_string = ''
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else '' if item is None else item for item in row]
        table_string += ('|' + '|'.join(cleaned_row) + '|\n')
        if row_num == 0:
            separator_row = '|'.join(['---'] * len(cleaned_row))
            table_string += ('|' + separator_row + '|\n')
    table_string = table_string[:-1]
    return table_string

def is_element_inside_any_table(element, page ,tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for table in tables:
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False

def find_table_for_element(element, page ,tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for i, table in enumerate(tables):
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return i
    return None  

def crop_image(element, pageObj):
    [image_left, image_top, image_right, image_bottom] = [element.x0,element.y0,element.x1,element.y1] 
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

def convert_to_images(input_file,):
    images = pdf2image.convert_from_path(input_file)
    image = images[0]
    output_file = 'PDF_image.png'
    image.save(output_file, 'PNG')

# def image_to_text(image_path):
#     image_mime_type, _ = mimetypes.guess_type(image_path)
#     base64_image = encode_image(image_path)

#     text = describe_image_with_openai(image_mime_type, base64_image, openai_api_key)
#     return text

def has_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return len(text.strip()) > 30

def extract_table_from_pdf(pdf_path, openai_api_key):
    # with open(pdf_path, "rb") as f:
    #     pdf = pdftotext.PDF(f, physical=True)

    # pdf_return = []

    # for i, page in enumerate(pdf):
    #     pdf_return.append(page)
    #     pdf_return.append("\n\n")
    #     print(f"Page {i + 1}...\n")
    #     # pdf_return.append('#' * 100)

    # return pdf_return

    extracted_content = []

    pdfFileObj = open(pdf_path, 'rb')
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)

    text_per_page = {}
    image_flag = False

    for pagenum, page in enumerate(extract_pages(pdf_path)):

        pageObj = pdfReaded.pages[pagenum]
        page_text = []
        line_format = []
        text_from_images = []
        text_from_tables = []
        page_content = []
        table_in_page= -1
        pdf = pdfplumber.open(pdf_path)
        page_tables = pdf.pages[pagenum]
        tables = page_tables.find_tables()
        if len(tables)!=0:
            table_in_page = 0

        for table_num in range(len(tables)):
            table = extract_table(pdf_path, pagenum, table_num)
            table_string = table_converter(table)
            text_from_tables.append(table_string)

        page_elements = [(element.y1, element) for element in page._objs]
        page_elements.sort(key=lambda a: a[0], reverse=True)


        for i,component in enumerate(page_elements):
            element = component[1]

            if table_in_page == -1:
                pass
            else:
                if is_element_inside_any_table(element, page ,tables):
                    table_found = find_table_for_element(element,page ,tables)
                    if table_found == table_in_page and table_found != None:    
                        page_content.append(text_from_tables[table_in_page])
                        page_text.append('table')
                        line_format.append('table')
                        table_in_page+=1
                    continue

            if not is_element_inside_any_table(element,page,tables):

                if isinstance(element, LTTextContainer):
                    (line_text, format_per_line) = text_extraction(element)
                    page_text.append(line_text)
                    line_format.append(format_per_line)
                    page_content.append(line_text)


                if isinstance(element, LTFigure):
                    crop_image(element, pageObj)
                    convert_to_images(f'cropped_image.pdf')
                    # image_text = image_to_text(f'PDF_image.png')
                    # image_mime_type, _ = mimetypes.guess_type(f'PDF_image.png')
                    if not has_text(f'PDF_image.png'):
                        image_text = ''
                    else:
                        image_mime_type, _ = mimetypes.guess_type(f'PDF_image.png')
                        base64_image = encode_image(f'PDF_image.png')

                        image_text = describe_image_with_openai(image_mime_type, base64_image, openai_api_key=openai_api_key)
                    text_from_images.append(image_text)
                    page_content.append(image_text)
                    page_text.append('image')
                    line_format.append('image')
                    image_flag = True


        dctkey = 'Page_'+str(pagenum)
        text_per_page[dctkey]= [page_text, line_format, text_from_images,text_from_tables, page_content]

        extracted_content.append(''.join(page_content))
        extracted_content.append("\n")

        # pdfFileObj.close()
        # os.remove('cropped_image.pdf')
        # os.remove('PDF_image.png')

    return extracted_content

def ocr_pdf_to_text_and_html(pdf_path, temp_image_converted_path, openai_api_key):

    results = []

    if not is_text_selectable(pdf_path):
        if pdf_path.lower().endswith('.pdf'):
            images = pdf2image.convert_from_path(pdf_path)
            # table_detector = YOLO('/home/ivirse/chienlm/yolo_table_detect/runs/detect/table_detect/weights/best.pt')
            # cell_detector = YOLO('/home/ivirse/chienlm/yolo_cell_detect/runs/detect/table_cell_detect/weights/best.pt')
            structure_engine = PPStructure(table=False, ocr=False, show_log=True)

            for i, image in enumerate(images):
                print(type(image))
                print("Page: ", i + 1)
                a_page_output = []

                # cv2_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                try:    
                    resized_img = image.resize((480, 480))
                    rotation_result = rotation_model.run([rotation_model_output_name], {rotation_model_input_name: np.array([resized_img], dtype=np.float32)/255.0})
                    rotation_angle = int(classes[np.argmax(rotation_result[0])])
                    if rotation_angle==0:
                        rotated_image = image
                    elif rotation_angle==180:
                        rotated_image = image.rotate(180)
                    elif rotation_angle==270:
                        rotated_image = image.rotate(270, expand=True)
                    else:
                        rotated_image = image.rotate(90, expand=True)
                    cv2_img = cv2.cvtColor(np.array(rotated_image), cv2.COLOR_RGB2BGR)
                    pdf_file_name = os.path.basename(pdf_path)
                    pdf_file_name = os.path.splitext(pdf_file_name)[0]
                    # image_path = os.path.join(temp_image_converted_path, f'{pdf_file_name}_{i}.jpg')
                    # cv2.imwrite(image_path, cv2_img)
                    # try:


                    paddle_structure_results = structure_engine(cv2_img)

                    # table_detect_results = table_detector.predict(cv2_img, conf=0.6)
                    table_bboxes = [line['bbox'] for line in paddle_structure_results if line['type'] == 'table']

                    table_regions = []
                    rotate_times = 0
                    # for result in table_detect_results[0].boxes.cpu().xyxy.numpy():
                    for i, result in enumerate(table_bboxes):

                        x1, y1, x2, y2 = result
                        # overlaps_figure = any((x1 < fx2 and x2 > fx1 and y1 < fy2 and y2 > fy1) for fx1, fy1, fx2, fy2 in figure_regions)
                        # if overlaps_figure:
                        #     continue
                        table_regions.append((x1, y1, x2, y2))
                        only_table_image = cv2_img[int(y1):int(y2), int(x1):int(x2)]

                        paddle = PaddleOCR(
                                            enable_mkldnn=True, 
                                            # use_tensorrt=False, 
                                            use_angle_cls=False, 
                                            lang="vi", 
                                            use_gpu=True,
                                            # gpu_mem=4096,
                                        )

                        cell_detect_results = cell_detector.predict(only_table_image)
                        cell_and_its_text = {}

                        for cell_result in cell_detect_results[0].boxes.cpu().xyxy.numpy():
                            cx1, cy1, cx2, cy2 = cell_result
                            cell_image = only_table_image[int(cy1):int(cy2), int(cx1):int(cx2)]
                            if cell_image is None:
                                continue
                            try:
                                paddle_result = paddle.ocr(cell_image, cls=False, det=True)
                                paddle_result = paddle_result[:][:][0]
                                boxes = []
                                for line in paddle_result:
                                    line = line[0]
                                    boxes.append([[int(line[0][0]), int(line[0][1])], [int(line[2][0]), int(line[2][1])]])
                            except SystemExit as e:
                                print("Caught SystemExit:", e)
                                continue
                            except Exception as e:
                                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                                print(e)
                                continue

                            EXPEND = 5
                            for box in boxes:
                                box[0][0] -= EXPEND
                                box[0][1] -= EXPEND
                                box[1][0] += EXPEND
                                box[1][1] += EXPEND

                            texts = []
                            for box in boxes:
                                cropped_image = cell_image[box[0][1]:box[1][1], box[0][0]:box[1][0]]
                                try:
                                    cropped_image = Image.fromarray(cropped_image)
                                    rec_result = detector.predict(cropped_image)
                                    text = rec_result
                                    texts.append(text)
                                except Exception as e:
                                    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                                    continue

                            cell_and_its_text[(cx1, cy1, cx2, cy2)] = '\n'.join(texts)

                        # html_table = generate_html_table(cell_and_its_text)
                        # print(cell_and_its_text)
                        html_table = generate_markdown_table(cell_and_its_text)
                        a_page_output.append(((x1, y1, x2, y2), html_table, 'table'))

                    figure_regions = []

                    figure_bboxes = [line['bbox'] for line in paddle_structure_results if line['type'] == 'figure']
                    for i, bbox in enumerate(figure_bboxes):
                        x1, y1, x2, y2 = bbox
                        overlaps_table = any((x1 < tx2 and x2 > tx1 and y1 < ty2 and y2 > ty1) for tx1, ty1, tx2, ty2 in table_regions)
                        if overlaps_table:
                            continue
                        figure_regions.append((x1, y1, x2, y2))
                        figure_img = cv2_img[int(y1):int(y2), int(x1):int(x2)]
                        figure_img_path = os.path.join(temp_image_converted_path, f'{pdf_file_name}_{i}_figure.jpg')
                        cv2.imwrite(figure_img_path, figure_img)

                        image_mime_type, _ = mimetypes.guess_type(figure_img_path)
                        base64_image = encode_image(figure_img_path)

                        content = describe_image_with_openai(image_mime_type, base64_image, openai_api_key)
                        a_page_output.append(((x1, y1, x2, y2), content, 'figure'))
                    
                    # except:
                    #     print("Exception")
                    #     continue
                    paddle = PaddleOCR(
                                        enable_mkldnn=True, 
                                        # use_tensorrt=False, 
                                        use_angle_cls=False, 
                                        lang="vi", 
                                        use_gpu=True,
                                        # gpu_mem=4096,
                                    )
                    try:
                        ocr_result = paddle.ocr(cv2_img, cls=False, det=True)
                        ocr_result = ocr_result[:][:][0]
                        text_boxes = []
                        for line in ocr_result:
                            line = line[0]
                            text_boxes.append([[int(line[0][0]), int(line[0][1])], [int(line[2][0]), int(line[2][1])]])
                    except SystemExit as e:
                        print("Caught SystemExit:", e)
                        continue
                    except:
                        continue
                    EXPEND = 5
                    for box in text_boxes:
                        box[0][0] -= EXPEND
                        box[0][1] -= EXPEND
                        box[1][0] += EXPEND
                        box[1][1] += EXPEND

                    for box in text_boxes:
                        x1, y1, x2, y2 = box[0][0], box[0][1], box[1][0], box[1][1]
                        overlaps_table = any((x1 < tx2 and x2 > tx1 and y1 < ty2 and y2 > ty1) for tx1, ty1, tx2, ty2 in table_regions)
                        overlaps_figure = any((x1 < fx2 and x2 > fx1 and y1 < fy2 and y2 > fy1) for fx1, fy1, fx2, fy2 in figure_regions)
                        if overlaps_table or overlaps_figure:
                            continue

                        cropped_image = cv2_img[box[0][1]:box[1][1], box[0][0]:box[1][0]]
                        try:
                            cropped_image = Image.fromarray(cropped_image)
                            rec_result = detector.predict(cropped_image)
                            text = rec_result
                            a_page_output.append(((box[0][0], box[0][1], box[1][0], box[1][1]), text, 'text'))
                        except Exception as e:
                            continue

                    a_page_output.sort(key=lambda item: (item[0][1], item[0][0]))
                    final_page_output = "\n".join([item[1] for item in a_page_output])
                    results.append(final_page_output)
                except SystemExit as e:
                    print("Caught SystemExit:", e)
                    continue
                except Exception as e:
                    print(e)
                    continue
    return results