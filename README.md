The task was:
"task 2:
Write small service class with methods
get(user_id) → UserDTO
add(user: UserDTO)

signatures can be changed if you think it's needed for better implementation

UserDTO - pydantic model
users are stored in db.
assume you have method get_async_session, which returns AsyncSession sqlalchemy object to interact with db

write tests for that class.

add notes with argumentation for choosen implementation."

1. `git clone https://github.com/marbleyung/prostopay_testtask.git`
2. `cd ${repo}`
3. `pip install -r req.txt`
4. `pytest test_service.py -v`
