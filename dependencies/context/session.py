from sqlalchemy_mixins.session import SessionMixin

from dependencies.context.exception import ExceptionContext
from dependencies.context.user import UserContext


async def close_session(db):
    # UserContext.set_user(None)
    # SessionMixin.set_session(None)
    if ExceptionContext.exceptions:
        await db.rollback()
    else:
        try:
            await db.commit()
        except:
            await db.rollback()
            raise
    await db.close()
