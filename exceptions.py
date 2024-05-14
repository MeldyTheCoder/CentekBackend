import fastapi


DOCTOR_NOT_FOUND = fastapi.HTTPException(
    status_code=404,
    detail='Запрашиваемый Вами врач не найден!'
)

PATIENT_NOT_FOUND = fastapi.HTTPException(
    status_code=404,
    detail='Запрашиваемый Вами пациент не найден!'
)

PATIENT_ALREADY_EXISTS = fastapi.HTTPException(
    status_code=400,
    detail='Данный пациент уже существует!'
)

MEETING_ALREADY_EXISTS = fastapi.HTTPException(
    status_code=400,
    detail='Данное мероприятие уже существует!'
)

MEETING_NOT_FOUND = fastapi.HTTPException(
    status_code=404,
    detail='Запрашиваемое Вами мероприятие не было найдено!'
)

PATIENT_ALREADY_IN_MEETING = fastapi.HTTPException(
    status_code=400,
    detail='Данный пациент уже находится в данном мероприятии.'
)

PATIENT_NOT_IN_MEETING = fastapi.HTTPException(
    status_code=400,
    detail='Данный пациент не находится в данном мероприятии.'
)

USER_ALREADY_REGISTERED_EXCEPTION = fastapi.HTTPException(
    detail='Данный пользователь уже зарегистрирован!',
    status_code=403,
)

USER_IS_NOT_REGISTERED_EXCEPTION = fastapi.HTTPException(
    detail='Данный пользователь не зарегистрирован',
    status_code=403,
)

INCORRECT_LOGIN_DATA_EXCEPTION = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
    detail='Неверные данные для входа.'
)

INCORRECT_REGISTRATION_DATA_EXCEPTION = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
    detail='Неверные данные для регистрации.'
)

DOCTOR_NOT_OWNING_MEETING = fastapi.HTTPException(
    status_code=400,
    detail='Вы не можете редактировать данное мероприятие, т.к вы не являетесь его организатором.'
)

NOT_DOCTORS_PATIENT = fastapi.HTTPException(
    status_code=400,
    detail='Данный доктор не работал с данным пациентом.'
)

VISIT_NOT_FOUND = fastapi.HTTPException(
    status_code=404,
    detail='Запрашиваемый Вами визит к врачу не найден!'
)

DOCTOR_NOT_OWNING_VISIT = fastapi.HTTPException(
    status_code=400,
    detail='Данный визит пациента к врачу проводится другим врачем.'
)

MEDIA_ALREADY_UPLOADED = fastapi.HTTPException(
    status_code=400,
    detail='Медиа-файл с данным названием уже был загружен в хранилище.'
)

NOT_A_DIR = fastapi.HTTPException(
    status_code=400,
    detail='Указанный путь сохранения должен быть директорией.'
)

PASSWORD_INVALID = fastapi.HTTPException(
    status_code=400,
    detail='Неверно введен старый пароль!'
)
