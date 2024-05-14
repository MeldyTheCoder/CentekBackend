import fastapi
from fastapi import APIRouter
from typing import Annotated
import auth
import models
import serializers
import utils
import exceptions


router = APIRouter(
    prefix='/doctors',
    tags=['Докторы']
)


async def doctor_fetch_params(
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        surname: str = None,
        speciality: str = None,
):
    data_params = {
        'username__contains': username,
        'first_name__contains': first_name,
        'last_name__contains': last_name,
        'surname__contains': surname,
        'speciality__name__contains': speciality
    }

    return utils.exclude_none(data_params)


@router.get('/', name='Получение списка и поиск докторов')
async def get_doctors(params: Annotated[dict, fastapi.Depends(doctor_fetch_params)],  _: auth.UserType):
    return await models.User.objects.select_all(True).filter(**params).all()


@router.get('/meetings', name='Вывод списка мероприятий авторизованного доктора')
async def get_authorized_doctor_meetings(user: auth.UserType):
    meetings = await models.Meeting.objects.select_all(True).filter(
        doctor__id=user.id,
    ).all()

    return meetings


@router.get('/visits', name='Вывод списка посещений пациентов авторизованного доктора')
async def get_authorized_doctor_meetings(user: auth.UserType):
    visits = await models.Visit.objects.select_all(True).filter(
        doctor__id=user.id,
    ).all()

    return visits


@router.get('/specialities', name='Вывод всех специальностей докторов')
async def get_specialities():
    specialities = await models.Speciality.objects.select_all(True).all()
    return specialities


@router.get('/patients/', name='Вывод списка пациентов авторизованного доктора')
async def get_doctor_patients(user: auth.UserType):
    patients: list[models.Patient] = await models.Patient.objects.select_all(True).filter(
        visits__doctor__id=user.id
    ).all()

    return patients


@router.get('/{doctor_id}/', name='Получение данных конкретного доктора')
async def get_doctor(doctor_id: int,  _: auth.UserType):
    doctor = await models.User.objects.select_all(True).get_or_none(id=doctor_id)

    if not doctor:
        raise exceptions.DOCTOR_NOT_FOUND

    return doctor


@router.get('/{doctor_id}/meetings/', name='Вывод списка всех мероприятий доктора')
async def get_doctor_meetings(doctor_id: int, _: auth.UserType):
    doctor: models.User = await models.User.objects.get_or_none(id=doctor_id)

    if not doctor:
        raise exceptions.DOCTOR_NOT_FOUND

    meetings: list[models.Meeting] = await models.Meeting.objects.select_all(True).filter(doctor__id=doctor.id).all()
    return meetings


@router.get('/{doctor_id}/patients/', name='Вывод списка пациентов доктора')
async def get_doctor_patients(doctor_id: int, _: auth.UserType):
    doctor: models.User = await models.User.objects.get_or_none(id=doctor_id)

    if not doctor:
        raise exceptions.DOCTOR_NOT_FOUND

    patients: list[models.Patient] = await models.Patient.objects.select_all(True).filter(
        visits__doctor__id=doctor.id
    ).all()

    return patients
