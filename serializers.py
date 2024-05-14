import models
from pydantic import BaseModel


class UserPasswordChangeSerializer(BaseModel):
    old_password: str
    new_password: str


UserRegistrationModel = models.User.get_pydantic(
    include={
        'username',
        'password',
        'email',
        'first_name',
        'last_name',
        'surname',
        'speciality__name',
    }
)

UserLoginModel = models.User.get_pydantic(
    include={
        'username',
        'password',
    }
)

UserFetchSerializer = models.User.get_pydantic(
    include={
        'username',
        'first_name',
        'last_name',
        'surname',
        'id',
        'speciality__name',
    }
)

UserUpdateSerializer = models.User.get_pydantic_partial(
    include={
        'first_name',
        'last_name',
        'surname',
    }
)

PatientCreateSerializer = models.Patient.get_pydantic(
    exclude={
        'id',
        'med_card',
        'insurance_policy__id',
        'insurance_policy__company__id'
        'visits',
        'meetings',
        'passport__id',
        'visits',
    }
)

PatientUpdateSerializer = models.Patient.get_pydantic_partial(
    exclude={
        'id',
        'med_card__id',
        'insurance_policy__id',
        'visits',
        'meetings',
    }
)

PatientPassportCreateSerializer = models.Passport.get_pydantic(
    exclude={
        'id',
    }
)

PatientPassportUpdateSerializer = models.Passport.get_pydantic_partial(
    exclude={
        'id',
        'user',
    }
)

MeetingCreateSerializer = models.Meeting.get_pydantic(
    exclude={
        'id',
        'patients',
        'date_created',
        'doctor',
    }
)

MeetingUpdateSerializer = models.Meeting.get_pydantic_partial(
    exclude={
        'id',
        'date_created',
        'patients',
    }
)

SpecialityCreateSerializer = models.Speciality.get_pydantic(
    exclude={
        'id',
    }
)

SpecialityUpdateSerializer = models.Speciality.get_pydantic_partial(
    exclude={
        'id',
    }
)

InsuranceCompanyCreateSerializer = models.InsuranceCompany.get_pydantic(
    exclude={
        'id',
    }
)

InsuranceCompanyUpdateSerializer = models.InsuranceCompany.get_pydantic_partial(
    exclude={
        'id'
    }
)

DiagnosisCreateSerializer = models.Diagnosis.get_pydantic(
    exclude={
        'id',
    }
)

DiagnosisUpdateSerializer = models.Diagnosis.get_pydantic(
    exclude={
        'id',
    }
)

PatientVisitCreateSerializer = models.Visit.get_pydantic(
    exclude={
        'id',
        'date_created',
        'doctor',
        'patient',
        'diagnosis__id',
        'diagnosis__visits',
    }
)

PatientVisitUpdateSerializer = models.Visit.get_pydantic_partial(
    exclude={
        'id',
        'date_created',
        'doctor',
        'patient',
    }
)
