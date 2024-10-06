import asyncio
import argparse

import uvicorn
from loguru import logger

import config as cfg
from loader import app
from api import account, auth, recruiter, dashboard # Импорт всех хендлеров API
from api.routers import protected, unprotected
from utils.init_db import init_db
from utils.fake_data import filling_fake_data


def run_server():
    app.include_router(unprotected, prefix="/api")
    app.include_router(protected, prefix="/api")
    uvicorn.run(app, host=cfg.API_HOST, port=cfg.API_PORT)


if __name__ == "__main__":
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        logger.info("uvloop installed")
    except Exception:
        logger.warning("uvloop not installed")

    parser = argparse.ArgumentParser(description="Backend VisionHire")
    parser.add_argument('--action', type=str, choices=['init_db', 'fake_fill'])
    parser.add_argument('--users-count', type=int, default=30, help='Количество фейковых пользователей')
    parser.add_argument('--vacancies-count', type=int, default=10, help='Количество фейковых вакансий')
    parser.add_argument('--candidates-count', type=int, default=40, help='Количество фейковых кандидатов')
    parser.add_argument('--tasks-count', type=int, default=13, help='Количество фейковых задач')
    parser.add_argument('--interviews-count', type=int, default=3, help='Количество фейковых интервью')
    args = parser.parse_args()

    if args.action == 'init_db':
        asyncio.run(init_db())
    elif args.action == 'fake_fill':
        asyncio.run(filling_fake_data(args.users_count, args.vacancies_count, args.candidates_count, args.tasks_count, args.interviews_count))
    else:
        run_server()
