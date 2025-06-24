from sqlalchemy import Column, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .meta import Base


class User(Base):
    __tablename__ = "user" # noqa

    uid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = Column(String)
    reports: Mapped[list["Report"]] = relationship("Report", back_populates="user")
    is_subscribed: Mapped[bool] = Column(Boolean, default=True)


class Report(Base):
    __tablename__ = "report" # noqa

    id: Mapped[str] = Column(Integer, primary_key=True, autoincrement=True)
    user_uid = mapped_column(ForeignKey("user.uid"))
    user: Mapped["User"] = relationship("User", back_populates="reports", uselist=False)
    progress: Mapped[str] = Column(String, default="")
    plans: Mapped[str] = Column(String, default="")
    problems: Mapped[str] = Column(String, default="")


