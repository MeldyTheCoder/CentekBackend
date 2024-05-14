import enum
from typing import Type, Union, Set, Optional, Dict
import ormar
import random
import pydantic
import sqlalchemy
import databases
import settings
import urllib.request
from datetime import datetime, timedelta
from sqlalchemy_utils import drop_database, create_database, database_exists

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.DATABASE_URL)

# drop_database(settings.DATABASE_URL)
if not database_exists(settings.DATABASE_URL):
    database_inited = False
    create_database(settings.DATABASE_URL)

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

ormar_config = ormar.OrmarConfig(
    metadata=metadata,
    database=database,
)


def get_med_card_expire_date():
    return datetime.now() + timedelta(days=10 * 365)


def get_default_avatar():
    random_seed = random.randint(100, 99999999)
    url = f'https://api.dicebear.com/7.x/miniavs/svg?seed={random_seed}'

    image_save_path, rel_path = settings.get_avatar_save_path(f'{random_seed}.svg')

    urllib.request.urlretrieve(
        url=url,
        filename=image_save_path,
    )

    return rel_path


class GenderChoices(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class VisitStatuses(enum.Enum):
    CLOSED = 'closed'
    OPENED = 'opened'
    PATIENT_NOT_CAME = 'not_came'
    CANCELED = 'canceled'
    RESCHEDULED = 'rescheduled'
    REOPENED = 'reopened'


class MeetingTypes(enum.Enum):
    """
    LABORATORY_TEST: лабораторное исследование
    INSTRUMENTAL_DIAGNOSTICS: инструментальная диагностика
    DRUG_THERAPY: лекарственная терапия
    PHYSIOTHERAPY: физиотерапия
    SURGERY: хирургическое лечение
    """

    LABORATORY_TEST = 'laboratory_test'
    INSTRUMENTAL_DIAGNOSTICS = 'instrumental_diagnostics'
    DRUG_THERAPY = 'drug_therapy'
    PHYSIOTHERAPY = 'physiotherapy'
    SURGERY = 'surgery'


class PartialMixin:
    """
    Mixin для создания сериализаторов без обязательных полей
    для возможности обновления данных без валидации.
    """

    @classmethod
    def get_pydantic_partial(
            cls,
            *,
            include: Union[Set, Dict, None] = None,
            exclude: Union[Set, Dict, None] = None,
    ) -> Type[pydantic.BaseModel]:
        model = cls.get_pydantic(include=include, exclude=exclude)

        new_fields = {
            name: (Optional[model.__annotations__.get(name)], None)
            for name in model.__fields__
        }

        new_model = pydantic.create_model(f"Partial{cls.__name__}", **new_fields)
        return new_model


class Diagnosis(PartialMixin, ormar.Model):
    """
    Модель диагноза БД
    """

    ormar_config = ormar_config.copy(
        tablename='diagnosis'
    )

    id = ormar.BigInteger(
        primary_key=True,
        autoincrement=True,
    )

    name = ormar.String(
        min_length=3,
        max_length=150,
        nullable=False
    )


class Passport(PartialMixin, ormar.Model):
    """
    Модель паспорта пациента БД
    """

    ormar_config = ormar_config.copy(
        tablename='passports'
    )

    id = ormar.BigInteger(
        minimum=1,
        primary_key=True,
        autoincrement=True,
    )

    issued_by = ormar.String(
        max_length=100,
        nullable=False,
    )

    first_name = ormar.String(
        max_length=100,
        nullable=False,
    )

    last_name = ormar.String(
        max_length=100,
        nullable=False
    )

    surname = ormar.String(
        max_length=100,
        nullable=True,
    )

    issued_date = ormar.Date(
        nullable=False
    )

    department_code = ormar.Integer(
        nullable=False,
    )

    gender = ormar.String(
        max_length=10,
        choices=list(GenderChoices),
        nullable=False,
    )

    date_of_birth = ormar.Date(
        nullable=False,
    )

    birth_address = ormar.Text(
        nullable=False,
    )

    series_number = ormar.BigInteger(
        nullable=False,
    )


class InsuranceCompany(PartialMixin, ormar.Model):
    """
    Модель страховой компании пациента БД
    """

    ormar_config = ormar_config.copy(
        tablename='insurance_companies'
    )

    id = ormar.BigInteger(
        minimum=1,
        primary_key=True,
        autoincrement=True,
    )

    name = ormar.String(
        max_length=200,
        nullable=False,
        unique=True,
    )


class InsurancePolicy(PartialMixin, ormar.Model):
    """
    Модель страхового полиса пациента БД
    """

    ormar_config = ormar_config.copy(
        tablename='insurance_policies'
    )

    id = ormar.BigInteger(
        minimum=1,
        primary_key=True,
        autoincrement=True,
    )

    date_created = ormar.Date(
        nullable=False
    )

    date_expires = ormar.Date(
        nullable=False
    )

    number = ormar.BigInteger(
        nullable=False,
        minimum=1,
        unique=True,
    )

    company = ormar.ForeignKey(
        to=InsuranceCompany,
        nullable=False,
        unique=False,
    )


class MedCard(PartialMixin, ormar.Model):
    """
    Модель мед. карты пациента БД
    """

    ormar_config = ormar_config.copy(
        tablename='med_cards'
    )

    id = ormar.BigInteger(
        minimum=1,
        primary_key=True,
        autoincrement=True,
    )

    date_created = ormar.DateTime(
        default=datetime.now
    )

    date_expires = ormar.DateTime(
        nullable=False,
        default=get_med_card_expire_date
    )


class Speciality(PartialMixin, ormar.Model):
    """
    Модель специальности врача БД
    """

    ormar_config = ormar_config.copy(
        tablename='specialties'
    )

    id = ormar.BigInteger(
        minimum=1,
        primary_key=True,
        autoincrement=True,
    )

    name = ormar.String(
        max_length=128,
        nullable=False,
    )


class User(PartialMixin, ormar.Model):
    """
    Модель пользователя (доктора) БД
    """

    ormar_config = ormar_config.copy(
        tablename='users'
    )

    id = ormar.BigInteger(
        minimum=1,
        primary_key=True,
        autoincrement=True,
    )

    photo = ormar.Text(
        default=get_default_avatar,
        nullable=False,
    )

    username = ormar.String(
        max_length=50,
        min_length=3,
        regex=r'^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$',
        nullable=False,
    )

    email = ormar.String(
        max_length=100,
        min_length=5,
        regex=r'^[a-z0-9][a-z0-9-_\.]+@([a-z]|[a-z0-9]?[a-z0-9-]+[a-z0-9])\.[a-z0-9]{2,10}(?:\.[a-z]{2,10})?$',
        nullable=False,
    )

    password = ormar.Text(
        nullable=False,
    )

    first_name = ormar.String(
        max_length=50,
        nullable=False,
    )

    last_name = ormar.String(
        max_length=50,
        nullable=False,
    )

    surname = ormar.String(
        max_length=50,
        nullable=True,
    )

    speciality = ormar.ForeignKey(
        Speciality,
        nullable=False,
        ondelete=ormar.ReferentialAction.RESTRICT,
        onupdate=ormar.ReferentialAction.CASCADE,
    )

    date_joined = ormar.DateTime(
        default=datetime.now,
        nullable=False,
    )

    last_login = ormar.DateTime(
        default=datetime.now,
        nullable=True,
    )


class Patient(PartialMixin, ormar.Model):
    """
    Модель пациента БД
    """

    ormar_config = ormar_config.copy(
        tablename='patients'
    )

    id = ormar.BigInteger(
        minimum=1,
        primary_key=True,
        autoincrement=True,
    )

    first_name = ormar.String(
        max_length=50,
        nullable=False,
    )

    last_name = ormar.String(
        max_length=50,
        nullable=False,
    )

    surname = ormar.String(
        max_length=50,
        nullable=True,
    )

    gender = ormar.String(
        choices=list(GenderChoices),
        max_length=6,
        nullable=False,
        default=GenderChoices.MALE,
    )

    address = ormar.Text(
        nullable=False,
    )

    email = ormar.String(
        max_length=250,
        regex=r"^\S+@\S+\.\S+$",
        nullable=False,
    )

    med_card = ormar.ForeignKey(
        to=MedCard,
        ondelete=ormar.ReferentialAction.RESTRICT,
        onupdate=ormar.ReferentialAction.CASCADE,
        nullable=False,
        unique=True,
    )

    insurance_policy = ormar.ForeignKey(
        to=InsurancePolicy,
        ondelete=ormar.ReferentialAction.RESTRICT,
        onupdate=ormar.ReferentialAction.CASCADE,
        nullable=False,
        unique=True,
    )

    passport = ormar.ForeignKey(
        to=Passport,
        ondelete=ormar.ReferentialAction.RESTRICT,
        onupdate=ormar.ReferentialAction.CASCADE,
        unique=True,
    )

    date_of_birth = ormar.Date()


class Visit(PartialMixin, ormar.Model):
    """"
    Модель посещения пациента в больницу БД
    """

    ormar_config = ormar_config.copy(
        tablename='visits'
    )

    id = ormar.BigInteger(
        minimum=1,
        primary_key=True,
        autoincrement=True,
    )

    date_created = ormar.DateTime(
        default=datetime.now,
        nullable=False
    )

    date_to_visit = ormar.DateTime(
        nullable=False,
    )

    diagnosis = ormar.ForeignKey(
        to=Diagnosis,
        ondelete=ormar.ReferentialAction.RESTRICT,
        onupdate=ormar.ReferentialAction.CASCADE,
    )

    patient = ormar.ForeignKey(
        to=Patient,
        ondelete=ormar.ReferentialAction.RESTRICT,
        onupdate=ormar.ReferentialAction.CASCADE,
        nullable=False,
    )

    doctor = ormar.ForeignKey(
        to=User,
        ondelete=ormar.ReferentialAction.RESTRICT,
        onupdate=ormar.ReferentialAction.CASCADE,
        nullable=False,
    )

    status = ormar.String(
        max_length=50,
        choices=list(VisitStatuses),
        default=VisitStatuses.OPENED,
        nullable=False
    )


class Meeting(PartialMixin, ormar.Model):
    """
    Модель медицинского собрания БД
    """

    ormar_config = ormar_config.copy(
        tablename='meetings'
    )

    id = ormar.BigInteger(
        minimum=1,
        primary_key=True,
        autoincrement=True,
    )

    name = ormar.String(
        max_length=256,
        min_length=10,
        nullable=False,
    )

    date_created = ormar.DateTime(
        default=datetime.now,
        nullable=False,
    )

    type = ormar.String(
        max_length=100,
        choices=list(MeetingTypes),
        nullable=False,
    )

    doctor = ormar.ForeignKey(
        to=User,
        ondelete=ormar.ReferentialAction.SET_NULL,
        onupdate=ormar.ReferentialAction.CASCADE,
        nullable=True,
    )

    patients = ormar.ManyToMany(
        to=Patient,
    )

    data = ormar.JSON(
        nullable=True
    )


# metadata.drop_all(bind=engine)
metadata.create_all(bind=engine)