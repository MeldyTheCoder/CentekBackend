import datetime
import typing
import fastapi
import auth
import models
from utils import exclude_none
import serializers
import exceptions


router = fastapi.APIRouter(
    prefix='/patients',
    tags=['Пациенты']
)


async def patient_fetch_params(
        first_name: str = None,
        last_name: str = None,
        surname: str = None,
        gender: models.GenderChoices = None,
        address: str = None,
        email: str = None,
        med_card: int = None,
):
    data_params = {
        'first_name__contains': first_name,
        'last_name__contains': last_name,
        'surname__contains': surname,
        'gender': gender,
        'address__contains': address,
        'email__contains': email,
        'med_card__id': med_card,
    }

    return exclude_none(data_params)


@router.get('/', name='Получение списка и поиск пациентов')
async def get_patients(
        params: typing.Annotated[dict, fastapi.Depends(patient_fetch_params)],
        _: auth.UserType
):
    return await models.Patient.objects.select_all(True).filter(**params).all()


@router.get('/{patient_id}/', name='Получения данных пациента')
async def get_patient(
        patient_id: int,
        _: auth.UserType
):
    patient = await models.Patient.objects.get_or_none(id=patient_id)

    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    return patient


@router.post('/create/', name='Создание пациента')
async def create_patient(
        form_data: serializers.PatientCreateSerializer,
        _: auth.UserType
):
    insurance_company_data = form_data.insurance_policy.company.model_dump(
        exclude={
            'id'
        }
    )

    insurance_policy_data = form_data.insurance_policy.model_dump(
        exclude={
            'id',
            'company',
        }
    )

    passport_data = form_data.passport.model_dump(
        exclude={
            'id'
        }
    )

    form_data_dumped = form_data.model_dump(
        exclude={
            'insurance_policy',
            'passport',
        }
    )

    insurance_company, _ = await models.InsuranceCompany.objects.get_or_create(
        **insurance_company_data,
    )

    med_card = await models.MedCard.objects.create()

    insurance_policy = await models.InsurancePolicy.objects.create(
        **insurance_policy_data,
        company=insurance_company,
    )

    passport = await models.Passport.objects.create(
        **passport_data
    )

    patient = await models.Patient.objects.create(
        **form_data_dumped,
        med_card=med_card,
        insurance_policy=insurance_policy,
        passport=passport,
    )

    return patient


@router.put('/{patient_id}/edit/', name='Редактирование пациента')
async def edit_patient_data(
        patient_id: int,
        form_data: serializers.PatientUpdateSerializer,
        user: auth.UserType,
):
    form_data_dumped = form_data.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True)

    patient = await models.Patient.objects.get_or_none(id=patient_id)
    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    doctor_visits_exists = models.PatientVisit.objects.filter(
        doctor__id=user.id,
        patient__id=patient.id,
    ).exists()
    if not doctor_visits_exists:
        raise exceptions.NOT_DOCTORS_PATIENT

    await patient.update(**form_data_dumped)
    return patient


@router.delete('/{patient_id}/delete', name='Удаление данных пациента')
async def delete_patient_data(
        patient_id: int,
        user: auth.UserType
):
    patient = await models.Patient.objects.get_or_none(id=patient_id)
    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    doctor_visits_exists = models.PatientVisit.objects.filter(
        doctor__id=user.id,
        patient__id=patient.id,
    ).exists()
    if not doctor_visits_exists:
        raise exceptions.NOT_DOCTORS_PATIENT

    await patient.delete()
    return patient


@router.get('/{patient_id}/meetings/', name='Вывод всех мероприятий пациента')
async def get_patient_meetings(
        patient_id: int,
        _: auth.UserType,
        from_date: datetime.date = None,
        to_date: datetime.date = None,
        meeting_type: models.MeetingTypes = None,
):
    patient = await models.Patient.objects.get_or_none(id=patient_id)
    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    filters = exclude_none({
        'patients__id': patient.id,
        'from_date__gte': from_date,
        'to_date__lte': to_date,
        'type': meeting_type,
    })

    meetings = await models.Meeting.objects.filter(
        **filters
    )

    return meetings


@router.get('/{patient_id}/visits', name='Получение списка посещений пациента к докторам')
async def get_patient_visits(
        patient_id: int,
        _: auth.UserType
):
    patient = await models.Patient.objects.get_or_none(id=patient_id)
    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    visits = await models.Visit.objects.filter(
        patient__id=patient.id,
    ).all()

    return visits


@router.post('/{patient_id}/visits/create', name='Создание визита к врачу для пациента')
async def create_patient_visit(
        patient_id: int,
        form_data: serializers.PatientVisitCreateSerializer,
        user: auth.UserType,
):
    diagnosis_data_dumped = form_data.diagnosis.model_dump()

    diagnosis, _ = await models.Diagnosis.objects.get_or_create(**diagnosis_data_dumped)

    form_data_dumped = form_data.model_dump(
        exclude={
            'diagnosis'
        }
    )

    patient = await models.Patient.objects.get_or_none(id=patient_id)
    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    visit = await models.Visit.objects.create(
        **form_data_dumped,
        doctor=user,
        patient=patient,
        diagnosis=diagnosis,
    )

    return visit


@router.delete('/{patient_id}/visits/delete', name='Удаление визита пациента к врачу')
async def delete_patient_visit(
        patient_id: int,
        user: auth.UserType,
        visit_id: int
):
    patient = await models.Patient.objects.get_or_none(id=patient_id)
    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    visit = await models.Visit.objects.get_or_none(
        id=visit_id
    )

    if not visit:
        raise exceptions.VISIT_NOT_FOUND

    elif visit.doctor.id != user.id:
        raise exceptions.DOCTOR_NOT_OWNING_VISIT

    await patient.visits.remove(visit)
    return visit


@router.get('/{patient_id}/diagnosis', name='История диагнозов пациента')
async def get_patient_diagnosis_history(
        patient_id: int,
        _: auth.UserType,
):
    patient = await models.Patient.objects.get_or_none(id=patient_id)
    if not patient:
        raise exceptions.PATIENT_NOT_FOUND

    diagnosis = await models.Diagnosis.objects.filter(
        visits__patient__id=patient.id,
    )

    return diagnosis

