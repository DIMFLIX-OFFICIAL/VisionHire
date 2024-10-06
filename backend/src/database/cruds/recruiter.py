from datetime import datetime
from typing import List, Dict

from sqlalchemy.future import select
from sqlalchemy import extract, func, text
from collections import defaultdict

from ..db import DatabaseManager
from ..models import Candidate, Interview, Task, Vacancy, CandidateStatus, Hierarchy


class RecruiterCRUD:
    db_manager: DatabaseManager

    async def create_vacancy(
        self,
        title: str,
        description: str,
        location: str,
        recruiter_username: str,
        created_at: str,
    ) -> Vacancy:
        async with self.db_manager.get_session() as session:
            new_vacancies = Vacancy(
                title=title,
                description=description,
                location=location,
                recruiter_username=recruiter_username,
                created_at=created_at,
            )

            session.add(new_vacancies)
            await session.commit()
            await session.refresh(new_vacancies)
            return new_vacancies

    async def get_vacancies(self, recruiter_username: str) -> List[Vacancy]:
        '''все вакансии созданные рекрутером'''
        async with self.db_manager.get_session() as session:
            result = await session.execute(
                select(Vacancy).where(Vacancy.creator_username == recruiter_username)
            )
            vacancies = result.scalars().all()
            return vacancies

    async def get_subs_vacancies(self, user_id: str) -> List[Vacancy]:
        '''все вакансии созданные подчиненными'''
        subs = await self.get_subs(user_id)
        async with self.db_manager.get_session() as session:

            result = await session.execute(
                select(Vacancy).where(Vacancy.creator_username == 1)
            )
            vacancies = result.scalars().all()
            return vacancies
        
    async def create_interview(
        self, recruiter_username: str, candidate_id: int, interview_datetime: datetime
    ) -> Interview:
        async with self.db_manager.get_session() as session:
            new_interview = Interview(
                recruiter_username=recruiter_username,
                candidate_id=candidate_id,
                datetime=interview_datetime,
            )

            session.add(new_interview)
            await session.commit()
            await session.refresh(new_interview)
            return new_interview

    async def get_candidate_interviews(self, username: str) -> List[Interview]:
        async with self.db_manager.get_session() as session:

            result = await session.execute(
                select(Interview).where(Interview.candidate_id == username)
            )
            interviews = result.scalars().all()
            return interviews
        
    async def get_receiver_interviews(self, username: str) -> List[Interview]:
        async with self.db_manager.get_session() as session:

            result = await session.execute(
                select(Interview).where(Interview.recruiter == username)
            )
            interviews = result.scalars().all()
            return interviews

    async def get_candidates(self, vacancy_id: int) -> List[Candidate]:
        '''все кандидаты по конкретной вакансии'''
        async with self.db_manager.get_session() as session:
            result = await session.execute(
                select(Candidate).where(Candidate.vacancy_id == vacancy_id)
            )
            candidates = result.scalars().all()
            return candidates

    async def get_tasks(self, username: str) -> List[Task]:
        '''все задачи конкретного пользователя, включая задачи созданные руководителями'''
        async with self.db_manager.get_session() as session:
            usr_tasks: List[Task] = await session.execute(
                select(Task).where(Task.receiver_username == username)
            )
            return usr_tasks.scalars().all()

    async def create_task(self, title: str, description: str, creator_username: int, receiver_username: int) -> List[Task]:
        async with self.db_manager.get_session() as session:
            session.add(
                Task(title=title, description=description, creator_username=creator_username, receiver_username=receiver_username)
            )
            await session.commit()
    
    async def update_task(self, id_task: int) -> List[Task]:
        async with self.db_manager.get_session() as session:
            update_record = await session.query(Task).filter(Task.id == id_task).first()
            update_record.status = not update_record.status
            await session.commit()

    async def get_new_candidates(self, username: str) -> int:
        '''число всех новых кандидатов для метрики'''
        async with self.db_manager.get_session() as session:
            result = await session.execute(
                select(func.count()).where(Candidate.status == CandidateStatus.expected)
            )
            return result.scalar()
        

    async def get_new_condidates_bymonth(self, username: str) -> List[Task]:
        '''новые кандидаты по месяцам для метрики'''
        async with self.db_manager.get_session() as session:
            results = (
                await session.query(
                    extract('year', Candidate.created_at).label('year'),
                    extract('month', Candidate.created_at).label('month'),
                    func.count(Candidate.id).label('count')
                )
                .group_by('year', 'month')
                .order_by('year', 'month')
                .all()
            )

            data = defaultdict(lambda: defaultdict(int))
            months_map = {
                1: "Январь",
                2: "Февраль",
                3: "Март",
                4: "Апрель",
                5: "Май",
                6: "Июнь",
                7: "Июль",
                8: "Август",
                9: "Сентябрь",
                10: "Октябрь",
                11: "Ноябрь",
                12: "Декабрь"
            }

            for year, month, count in results:
                month_name = months_map[month]
                data[year][month_name] = count

            return data

    async def get_new_condidates_byday(self, username: str, date_from:str, date_to:str) -> Dict[str, int]:
        '''новые кандидаты по дням для метрики'''
        async with self.db_manager.get_session() as session:

            results = await session.execute(text(f"SELECT created_at, COUNT(id) FROM candidates where created_at BETWEEN {date_from} AND {date_to} AND vacancy_id IN (SELECT id FROM vacancies WHERE recruiter_username = {username}) GROUP BY created_at"))
            results = results.fetchall()
            data = defaultdict()

            for day, count in results:
                data[day] = count

            return data


    async def get_accepted_condidates_byday(self, username: str) -> List[Task]:
        '''принятые кандидаты по дням для метрики'''
        async with self.db_manager.get_session() as session:

            results = await session.query(Candidate.updated_at, func.count(Candidate.id).label('count')).group_by('updated_at')

            data = defaultdict()

            for day, count in results:
                data[day] = count

            return data


    async def get_accepted_condidates_bymonth(self, username: str) -> List[Task]:
        '''принятые кандидаты по месяцам для метрики'''
        async with self.db_manager.get_session() as session:
            results = (
                await session.query(
                    extract('year', Candidate.updated_at).label('year'),
                    extract('month', Candidate.updated_at).label('month'),
                    func.count(Candidate.id).label('count')
                )
                .group_by('year', 'month')
                .order_by('year', 'month')
                .all()
            )

            data = defaultdict(lambda: defaultdict(int))
            months_map = {
                1: "Январь",
                2: "Февраль",
                3: "Март",
                4: "Апрель",
                5: "Май",
                6: "Июнь",
                7: "Июль",
                8: "Август",
                9: "Сентябрь",
                10: "Октябрь",
                11: "Ноябрь",
                12: "Декабрь"
            }

            for year, month, count in results:
                month_name = months_map[month]
                data[year][month_name] = count

            return data

    async def get_subs(self, user_id: int) -> List[int]:
        '''список id подчиненных для назначения задач'''
        async with self.db_manager.get_session() as session:
            result = await session.execute(
                select(Hierarchy.sub_username).where(Hierarchy.super_username == user_id)
            )
            subs = result.scalars().all()
            return subs
        

    async def get_vacancy_time(self, username: int) -> int:
        '''время существования вакансий'''
        # async with self.db_manager.get_session() as session:
            
        #     results = await session.query(Vacancy.id, )

        #     time_work = result.scalar()
        #     return time_work