from uuid import UUID


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

    errors = dict()

    # Проверка входящего запроса на полное отсутствие полей
    if len(data) == 0:
        return messages_empty_error

    # Проверка входящего запроса на отсутствие некоторых полей
    for request_key in keys:
        if request_key not in data.keys():
            if request_key == 'image_size' and len(data[request_key]) == 0:
                for size_key in size_keys:
                    errors[size_key] = messages_empty_error.get(size_key)
            else:
                errors[request_key] = messages_empty_error.get(request_key)

    # Проверка высоты (ширины) изображения на отсутствие во входящем запросе
    # а также на корректность ввода
    for size_key in size_keys:
        if size_key not in data['image_size'].keys():
            errors[size_key] = messages_empty_error.get(size_key)
        elif data['image_size'].get(size_key) not in range(1, 10000):
            if errors.get(size_key) is None:
                errors[size_key] = messages_incorrect_data_error.get(size_key)

    # Проверка формата сохранения изображения на отсутствие во входящем запросе
    # а также на кооректность указания
    if data.get('save_format') not in formats:
        if errors.get('save_format') is None:
            errors['save_format'] = messages_incorrect_data_error.get('save_format')

    return errors


def check_get_uuid(uuid):
    try:
        UUID(uuid, version=4)
    except ValueError:
        return False

    return True
