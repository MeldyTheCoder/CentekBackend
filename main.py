import os.path
import typing
import fastapi
import uvicorn
import fake
import exceptions
import models
import settings
from routes import users, doctors, patients, meetings
from models import database
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI(
    debug=settings.DEBUG,
    title='Centek Backend',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(meetings.router)


@app.on_event('startup')
async def on_startup():
    await database.connect()

    doctor = await fake.generate_random_doctor()
    print('Admin: ', doctor)

    for _ in range(5):
        await fake.generate_random_patient()

    for _ in range(5):
        await fake.generate_random_meeting(doctor)

    for _ in range(5):
        await fake.generate_random_visit(doctor)


@app.on_event('shutdown')
async def on_shutdown():
    if database.is_connected:
        await database.disconnect()


@app.get(f'/{settings.STATIC_URL}' + '/{file_path:path}', name='Вывод static-файлов для фронтенда')
async def get_static(file_path: str):
    file_path = settings.get_static_file_path(file_path)
    return fastapi.responses.FileResponse(file_path)


@app.get(f'/{settings.MEDIA_URL}' + '/{file_path:path}', name='Вывод media-файлов для фронтенда')
async def get_media(file_path: str):
    file_path = settings.get_media_file_path(file_path)
    return fastapi.responses.FileResponse(file_path)


@app.post(f'/{settings.MEDIA_URL}', name='Загрузка media-файлов')
async def upload_media(
        file: fastapi.UploadFile,
        file_dir: typing.Literal['avatar', 'patients', 'meetings'],
):
    paths = [file_dir or '', file.filename]
    file_path = settings.get_media_file_path(*paths)

    if settings.path_exists(path=file_path):
        raise exceptions.MEDIA_ALREADY_UPLOADED

    with open(file_path, 'wb') as f:
        f.write(file.file.read())

    return {'detail': settings.get_relpath(file_path)}


@app.get('/statistics', name='Статистика по моделям БД')
async def get_database_statistics():
    return dict(
        meetings_count=await models.Meeting.objects.count(),
        patients_count=await models.Patient.objects.count(),
        doctors_count=await models.User.objects.count(),
        visits_count=await models.Visit.objects.count(),
    )


if __name__ == '__main__':
    uvicorn.run(
        host=settings.HOST,
        port=settings.PORT,
        app=app
    )
