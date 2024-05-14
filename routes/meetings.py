import fastapi

import auth
import models
import serializers
import utils
from datetime import datetime
from typing import Annotated
import exceptions

router = fastapi.APIRouter(
    prefix='/meetings',
    tags=['Мероприятия']
)


async def meetings_fetch_params(
        name: str = None,
        from_date: datetime = None,
        to_date: datetime = None,
        doctor_first_name: str = None,
        doctor_surname: str = None,
        doctor_last_name: str = None,
        meeting_type: models.MeetingTypes = None,
):
    data_params = {
        'name__contains': name,
        'doctor__first_name__contains': doctor_first_name,
        'doctor__last_name__contains': doctor_last_name,
        'doctor__surname__contains': doctor_surname,
        'type': meeting_type,
        'date_created__lte': from_date,
        'date_created__gte': to_date,
    }

    return utils.exclude_none(data_params)


@router.get('/', name='Получение списка и поиск мероприятий')
async def get_meetings(
        params: Annotated[dict, fastapi.Depends(meetings_fetch_params)],
        _: auth.UserType,
):
    return await models.Meeting.objects.select_all(True).filter(**params).all()


@router.post('/create', name='Создание мероприятия')
async def create_meeting(form_data: serializers.MeetingCreateSerializer, user: auth.UserType):
    form_data_dumped = form_data.model_dump()

    meeting, is_created = await models.Meeting.objects.get_or_create(
        **form_data_dumped,
        doctor=user,
    )

    if not is_created:
        raise exceptions.MEETING_ALREADY_EXISTS

    return meeting


@router.put('/{meeting_id}/update', name='Редактирование данных мероприятия')
async def edit_meeting_data(
        meeting_id: int,
        form_data: serializers.PatientUpdateSerializer,
        user: auth.UserType
):
    form_data_dumped = form_data.model_dump(
        exclude_none=True,
        exclude_unset=True,
        exclude_defaults=True,
    )

    meeting = await models.Meeting.objects.get_or_none(id=meeting_id)
    if not meeting:
        raise exceptions.MEETING_NOT_FOUND

    if not meeting.doctor.id == user.id:
        raise exceptions.DOCTOR_NOT_OWNING_MEETING

    await meeting.update(**form_data_dumped)
    return meeting


@router.get('/{meeting_id}', name='Получение данных мероприятия')
async def get_meeting_data(meeting_id: int, _: auth.UserType):
    meeting = await models.Meeting.objects.get_or_none(id=meeting_id)

    if not meeting:
        raise exceptions.MEETING_NOT_FOUND

    return meeting


@router.delete('/{meeting_id}/delete', name='Удаление данных мероприятия')
async def delete_meeting_data(meeting_id: int, user: auth.UserType):
    meeting = await models.Meeting.objects.get_or_none(id=meeting_id)

    if not meeting:
        raise exceptions.MEETING_NOT_FOUND

    if not meeting.doctor.id == user.id:
        raise exceptions.DOCTOR_NOT_OWNING_MEETING

    await meeting.delete()
    return meeting


@router.get('/{meeting_id}/patients', deprecated=True, name='Вывод списка пациентов мероприятия')
async def get_meeting_patients(meeting_id: int, _: auth.UserType):
    """
    Список мероприятий в данный момент можно получить сразу
    через GET /{meeting_id}/.
    """

    meeting = await models.Meeting.objects.get_or_none(id=meeting_id)

    if not meeting:
        raise exceptions.MEETING_NOT_FOUND

    return meeting.patients


@router.post('/{meeting_id}/patients/add', name='Добавление пациента к мероприятию')
async def add_patient_to_meeting(meeting_id: int, patient_id: int, user: auth.UserType):
    meeting = await models.Meeting.objects.get_or_none(id=meeting_id)
    if not meeting:
        raise exceptions.MEETING_NOT_FOUND

    if not meeting.doctor.id == user.id:
        raise exceptions.DOCTOR_NOT_OWNING_MEETING

    patient = await models.Patient.objects.get_or_none(id=patient_id)
    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    if patient in meeting.patients:
        raise exceptions.PATIENT_ALREADY_IN_MEETING

    await meeting.patients.add(patient)
    return meeting


@router.delete('/{meeting_id}/patients/delete', name='Удаление пациента из мероприятия')
async def delete_patient_from_meeting(meeting_id: int, patient_id: int, user: auth.UserType):
    meeting = await models.Meeting.objects.get_or_none(id=meeting_id)
    if not meeting:
        raise exceptions.MEETING_NOT_FOUND

    if not meeting.doctor.id == user.id:
        raise exceptions.DOCTOR_NOT_OWNING_MEETING

    patient = await models.Patient.objects.get_or_none(id=patient_id)
    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    if patient not in meeting.patients:
        raise exceptions.PATIENT_NOT_IN_MEETING

    await meeting.patients.remove(patient)
    return meeting


