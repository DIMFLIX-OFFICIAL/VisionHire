from fastapi import HTTPException, Request, Body
from loader import db
from typing import List, Dict
from loguru import logger
from fastapi.responses import JSONResponse
from database.models import User, Vacancy, Candidate, Role
from .routers import protected
from schemas.recruiter import CreateTask


@protected.post('/get_candidates')
async def get_candidates(request: Request):
    user: User = request.state.user.to_dict()

    if user["role"] == Role.recruiter.value:
        vacancies: List[Vacancy] = await db.get_vacancies(recruiter_username=user["username"])
        results: Dict[int, List[Candidate]] = {}

        for v in vacancies:
            candidates = await db.get_candidates(vacancy_id=v.id)
            results.update({v.id: candidates})

        return results
    
    return HTTPException(status_code=403, detail="Вы не рекрутер")


@protected.post('/get_tasks')
async def get_tasks(request: Request):
    user: User = request.state.user.to_dict()
    allowed_roles = [Role.recruiter, Role.director]

    if user["role"] in allowed_roles:
        tasks = await db.get_tasks(user["username"])
        return {"tasks": [t.to_dict() for t in tasks]}
    else:
        return HTTPException(status_code=403, detail="Ваша роль не позволяет просматривать задания")


@protected.post("/create_task")
async def create_tasks(request: Request, task_data: CreateTask):
    user: User = request.state.user.to_dict()
    creator_username = user["username"]
    title = task_data.title
    description = task_data.description
    receiver_username = creator_username if task_data.receiver_username is None else task_data.receiver_username
    logger.info(f"[{creator_username}] Создается задача: {task_data=}")
    subs: List[int] = await db.get_subs(creator_username)

    if receiver_username not in subs and receiver_username != user["username"]:
        return HTTPException(status_code=403, detail="Вы не можете создать задачу для этого пользователя")
    else:
        await db.create_task(title=title, description=description, creator_username=creator_username, receiver_username=receiver_username)
        return {"message": "Задача успешно создана"}
    
@protected.post("/get_subs")
async def get_subs(request):
    user: User = request.state.user.to_dict()
    creator_username = user["username"]

    await db.get_subs(creator_username)

@protected.post("/update_task")
async def update_task(request: Request, task_id: int):
    user: User = request.state.user.to_dict()

    if user["role"] in [Role.recruiter.value, Role.director.value]:
        await db.update_task(task_id)
    else:
        return HTTPException(status_code=403, detail="Ваша роль не позволяет изменять статус задачи")


@protected.post("/get_data_for_graphs")
async def get_data_for_graphs(request: Request):
    user: User = request.state.user.to_dict()


@protected.post("/get_met_new_candidates")
async def get_met_new_candidates(request: Request):
    data = await request.json()
    date_from = data["date_from"]
    date_to = data["date_to"]
    print(date_from)
    print(date_to)
    user: User = request.state.user.to_dict()
    # if user["role"] == Role.recruiter.value:
    if 1:
        candidates = await db.get_new_condidates_byday(user["username"], date_from, date_to)
        return JSONResponse(candidates)
    # elif user['role'] == Role.director.value:
        # candidates = await db.get_met_new_candidates(date_from, date_to)
    else:
        return HTTPException(status_code=403, detail="Вы не рекрутер")


@protected.post("/get_interviews")
async def get_interviews(request: Request):
    user: User = request.state.user.to_dict()
    if user["role"] == Role.recruiter.value:
        interviews = await db.get_recruiter_interviews(user["username"])
        return interviews
    elif user['role'] == Role.candidate.value:
        interviews = await db.get_candidate_interviews(user["username"])
        return interviews


