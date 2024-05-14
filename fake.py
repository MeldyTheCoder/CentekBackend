import random
import auth
import faker
from datetime import timedelta, datetime
import models

fake = faker.Faker(locale='ru')


async def generate_random_doctor():
    first_name, last_name, surname = fake.first_name(), fake.last_name(), None
    email = fake.email(domain='mail.ru')
    username = 'admin'
    speciality_name = random.choice([
        'Лор-эндокринолог',
        'Терапевт',
        'Мед-сестра/Мед-брат',
        'Психиатр-нарколог',
        'Рентгенолаборант',
        'Медицинский регистратор',
        'Санитар',
        'Врач-кардиолог'
    ])

    user_exists = await models.User.objects.get_or_none(
        username=username
    )

    if user_exists:
        return user_exists

    speciality, _ = await models.Speciality.objects.get_or_create(
        name=speciality_name
    )

    return await models.User.objects.create(
        first_name=first_name,
        last_name=last_name,
        surname=surname,
        email=email,
        username=username,
        speciality=speciality,
        password=auth.create_password_hash('12345678')
    )


async def generate_random_patient():
    email = fake.email(domain='mail.ru')
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
    series_number = random.randint(1000_000000, 9999_999999)
    issued_date = (date_of_birth + timedelta(days=365 * 14))
    first_name, last_name, surname = fake.first_name(), fake.last_name(), None
    department_code = random.randint(100_000, 999_999)
    gender = random.choice(['male', 'female'])
    birth_address = fake.address()

    date_created = fake.date_between(start_date=date_of_birth, end_date=issued_date)
    date_expires = (date_created + timedelta(days=365 * 10))
    policy_number = random.randint(1_000_000, 9_999_999)

    company_name = fake.company()

    passport = await models.Passport.objects.create(
        date_of_birth=date_of_birth,
        series_number=series_number,
        issued_date=issued_date,
        issued_by='УМВД РОССИИ ПО ТВЕРСКОЙ ОБЛАСТИ',
        first_name=first_name,
        last_name=last_name,
        surname=surname,
        department_code=department_code,
        gender=gender,
        birth_address=birth_address,
    )

    insurance_company, _ = await models.InsuranceCompany.objects.get_or_create(
        name=company_name,
    )

    insurance_policy = await models.InsurancePolicy.objects.create(
        date_created=date_created,
        date_expires=date_expires,
        number=policy_number,
        company=insurance_company,
    )

    med_card = await models.MedCard.objects.create()

    patient = await models.Patient.objects.create(
        first_name=first_name,
        last_name=last_name,
        surname=surname,
        date_of_birth=date_of_birth,
        insurance_policy=insurance_policy,
        med_card=med_card,
        passport=passport,
        gender=gender,
        address=birth_address,
        email=email,
    )

    return patient


async def generate_random_meeting(
        doctor: models.User,
):
    patients = await models.Patient.objects.all()

    meeting_type = random.choice(list(models.MeetingTypes))
    name = fake.sentence(nb_words=4)

    meeting = await models.Meeting.objects.create(
        type=meeting_type,
        name=name,
        doctor=doctor,
    )

    for patient in patients:
        await meeting.patients.add(patient)

    return meeting


async def generate_random_visit(
        doctor: models.User,
):
    patients = await models.Patient.objects.all()
    patient = random.choice(patients)

    diagnosis_name = random.choice([
        'Вегетососудистая дистония',
        'Гарднереллез',
        'Микоплазмоз',
        'Уреаплазмоз',
        'Дисбактериоз',
        'Остеохондроз',
        'Песок в почках',
        'Авитаминоз',
    ])

    diagnosis, _ = await models.Diagnosis.objects.get_or_create(
        name=diagnosis_name
    )
    date_to_visit = (datetime.now() + timedelta(days=10))
    status = random.choice(list(models.VisitStatuses))

    return await models.Visit.objects.create(
        doctor=doctor,
        patient=patient,
        diagnosis=diagnosis,
        date_to_visit=date_to_visit,
        status=status
    )



