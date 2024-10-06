import asyncio
import random
from datetime import datetime, timedelta
from faker import Faker

from database.models import User, Role, Vacancy, Candidate, CandidateStatus, Task, Interview
from loader import oauth2, db_manager
from sqlalchemy.future import select

fake = Faker()


async def create_fake_users(num_users):
    roles = list(Role)
    users = []
    for _ in range(num_users):
        users.append(User(
            username=fake.user_name(),
            name=fake.name(),
            email=fake.email(),
            role=random.choice(roles),
            hashed_password=random.choice([oauth2.get_password_hash(i) for i in ["1234", "1111", "2222", "12345"]]),
            refresh_token=None,
            created_at=datetime.now()
        ))

    async with db_manager.get_session() as session:
        session.add_all(users)
        await session.commit()


async def create_fake_vacancies(num_vacancies):
    async with db_manager.get_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

        for _ in range(num_vacancies):
            vacancy = Vacancy(
                title=fake.job(),
                description=fake.text(max_nb_chars=200),
                location=fake.city(),
                creator_username=random.choice(users).username,
                created_at=datetime.now(),
                status=random.choice([True, False])
            )
            session.add(vacancy)
        await session.commit()


async def create_fake_candidates(num_candidates):
    async with db_manager.get_session() as session:
        result = await session.execute(select(Vacancy))
        vacancies = result.scalars().all()

        for _ in range(num_candidates):
            candidate = Candidate(
                first_name=fake.first_name(),
                family_name=fake.last_name(),
                surname=fake.last_name(),
                phone=fake.phone_number(),
                email=fake.email(),
                city=fake.city(),
                vacancy_id=random.choice(vacancies).id,
                resume_file=fake.file_path(extension='pdf'),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                recruiter_description=fake.text(max_nb_chars=100),
                status=random.choice(list(CandidateStatus))
            )
            session.add(candidate)

        await session.commit()


async def create_fake_tasks(num_tasks):
    async with db_manager.get_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

        for _ in range(num_tasks):
            task = Task(
                title=fake.sentence(nb_words=6),
                description=fake.text(max_nb_chars=200),
                status=random.choice([True, False]),
                creator_username=random.choice(users).username,
                receiver_username=random.choice(users).username,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(task)
        await session.commit()


async def create_fake_interviews(num_interviews):
    async with db_manager.get_session() as session:
        result_users = await session.execute(select(User))
        users = result_users.scalars().all()

        result_candidates = await session.execute(select(Candidate))
        candidates = result_candidates.scalars().all()

        for _ in range(num_interviews):
            interview = Interview(
                recruiter_username=random.choice(users).username,
                candidate_id=random.choice(candidates).id,
                datetime=datetime.now() + timedelta(days=random.randint(1, 30))
            )
            session.add(interview)
        await session.commit()


async def filling_fake_data(users_count=30, vacancies_count=10, candidates_count=40, tasks_count=13, interviews_count=3):
    await create_fake_users(users_count)
    await create_fake_vacancies(vacancies_count)
    await create_fake_candidates(candidates_count)
    await create_fake_tasks(tasks_count)
    await create_fake_interviews(interviews_count)
