from uuid import UUID

"""
    Функция для проверки корректности данных во входящем запросе на изменение
    размеров изображения
    
    Входные данные:
        data - входные данных изображения, отаправленные в теле входящего запроса
    
    Возвращаемый результат:
        errors - описание выявленных ошибок указания данных в теле входящего запроса
"""


def check_post_request(data):
    keys = ['image', 'image_size', 'save_format']
    size_keys = ['h', 'w']
    formats = ['jpeg', 'png']

    messages_empty_error = {
        'image': "Не выбрано изображение",
        'h': "Не указан размер высоты изображения",
        'w': "Не указан размер ширины изображения",
        'save_format': "Не выбран формат сохранения изображения"
    }

    messages_incorrect_data_error = {
        'h': "Указаный размер высоты изображения не соответсвует допустимому диапазону",
        'w': "Указаный размер ширины изображения не соответсвует допустимому диапазону",
        'save_format': "Указан неверный формат сохранения изображения"
    }

    messages_incorrect_type_error = {
        'h': "Указаный размер высоты изображения не является целочисленным числом",
        'w': "Указаный размер ширины изображения не является целочисленным числом",
    }

    errors = dict()

    # Проверка входящего запроса на полное отсутствие полей
    if len(data) == 0:
        return messages_empty_error

    # Проверка входящего запроса на отсутствие некоторых полей
    for request_key in keys:
        if request_key not in data.keys():
            if request_key == 'image_size' and len(data[request_key]) == 0:
                for size_key in size_keys:
                    errors[size_key] = messages_empty_error[size_key]
            else:
                errors[request_key] = messages_empty_error[request_key]

    # Проверка высоты (ширины) изображения на отсутствие во входящем запросе
    # а также на корректность ввода
    for size_key in size_keys:
        if size_key not in data['image_size'].keys():
            errors[size_key] = messages_empty_error[size_key]
        elif type(data['image_size'][size_key]) != int:
            errors[size_key] = messages_incorrect_type_error[size_key]
        elif data['image_size'][size_key] not in range(1, 10000):
            errors[size_key] = messages_incorrect_data_error[size_key]

    # Проверка формата сохранения изображения на отсутствие во входящем запросе
    # а также на кооректность указания
    if errors.get('save_format') is None:
        if data['save_format'] not in formats:
            errors['save_format'] = messages_incorrect_data_error['save_format']

    return errors


"""
    Функция для проверки корректности уникального идентификатора
    
    Входные данные:
        uuid - уникальный идентификатор
    
    Возвращаемый результат:
        True (если идентификатор корректный)
        False (если идентификатор некорректный) 
"""


def check_get_uuid(uuid):
    try:
        UUID(uuid, version=4)
    except ValueError:
        return False

    return True
