from sqlalchemy import BigInteger, Boolean, Column, String

from utils.models import BaseModel


class UserDB(BaseModel):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    image = Column(String, nullable=True)
    username = Column(String(150), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    second_last_name = Column(String(50), nullable=True)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)

    async def has_perm(self, perm):
        return True
        from models import Permission

        if self.is_staff:
            return True

        groups = (await self.get_groups()).all()
        groups_id = [group.id for group in groups]

        permission = (
            await Permission.where_async(
                codename=perm,
                deleted=None,
                group_permissions___group_id__in=groups_id,
                group_permissions___deleted=None,
            )
        ).first()

        if permission:
            return True

        return False
