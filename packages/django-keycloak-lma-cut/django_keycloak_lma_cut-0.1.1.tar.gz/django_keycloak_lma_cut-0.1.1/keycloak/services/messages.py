from django.conf import settings

EXPIRED_SIGNATURE_ERROR = {
    'ru-ru': 'Ошибка аутентификации (истек срок действия токена)',
    'en-us': 'Failed to authenticate due to an expired access token',
}
JWT_CLAIMS_ERROR = {
    'ru-ru': 'Ошибка аутентификации (не прошла проверка требований к токену)',
    'en-us': 'Failed to authenticate due to failing claim checks',
}
JWT_ERROR = {
    'ru-ru': 'Ошибка аутентификации (некорректный токен)',
    'en-us': 'Failed to authenticate due to a malformed access token',
}
REFRESH_TOKEN_ERROR = {
    'ru-ru': 'URL недоступен / истек срок действия токена / некорректный токен',
    'en-us': 'URL is unreachable or refresh_token has expired or invalid token',
}
REMOTE_REFRESH_TOKEN_ERROR = {
    'ru-ru': 'URL недоступен / доступ ограничен / истек срок действия токена / некорректный токен',
    'en-us': 'URL is unreachable or access restriction or access_token has expired or invalid token',
}
MISMATCH_CLIENT_ERROR = {
    'ru-ru': 'Несоответствие ID клиента в токене и приложении',
    'en-us': 'The client in the token does not match the client in the application',
}
ABSENCE_USER_GROUP_ERROR = {
    'ru-ru': 'Токен не содержит группу доступа к приложению',
    'en-us': 'The token does not contain a user_group with access to the Client',
}
FAIL_AUTHENTICATION_ERROR = {
    'ru-ru': 'Не удалось пройти аутентификацию. Обратитесь к администратору',
    'en-us': 'Failed to authenticate',
}

OBJ_ID_NOT_FOUND = {
    'ru-ru': 'Не найден объект с id:',
    'en-us': 'There is no object with id:',
}
OIDC_PROFILE_NOT_FOUND = {
    'ru-ru': 'Отсутствует профиль пользователя с sub:',
    'en-us': 'There is no user profile with sub:',
}


def list_id_to_str(id_data) -> str:
    if type(id_data) not in (list, set, tuple):
        return id_data

    return ", ".join(str(id_obj) for id_obj in id_data)


def get_backend_message(backend, message):
    return f"{backend}: {message}"


def get_backend_message_with_error(backend, message, error):
    return f"{backend}: {message}: {error}"


def get_message(message):
    if hasattr(settings, 'KEYCLOAK_MESSAGE_LANGUAGE'):
        language = settings.KEYCLOAK_MESSAGE_LANGUAGE
    else:
        language = 'en-us'

    if type(message) != dict:
        return message

    message_in_language = message.get(language)
    if message_in_language:
        return message_in_language

    return ''


def obj_id_not_found(obj_id, message=get_message(OBJ_ID_NOT_FOUND)):
    return f"{message} {list_id_to_str(obj_id)}"
