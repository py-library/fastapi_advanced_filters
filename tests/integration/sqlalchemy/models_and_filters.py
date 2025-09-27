import enum
from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, Enum, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.orm import Mapped, declarative_base

from fastapi_filters import (
    AdvancedQSearch,
    BaseFilter,
    FieldCriteria,
    LogicalOperator,
    OperationEnum,
    PaginationEnum,
    QSearch,
    Selectable,
    SortBy,
)

Base = declarative_base()


class GenderEnum(str, enum.Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name: Mapped[str]
    last_name = Column(String)
    age = Column(Integer)
    is_working = Column(Boolean)
    birthday = Column(Date)
    gender = Column(Enum(GenderEnum))
    created_at: Mapped[str]
    titles: Mapped[list[str]] = Column(PG_ARRAY(String), default=[])


USER_PUBLIC_PREFIX = "user_public"
USER_PRIVATE_PREFIX = "user_private"


class Gender(enum.Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"


class UserSimpleFilterExample(BaseFilter):
    class FilterConfig:
        model = User
        prefix = "user"
        fields = "__all__"

        q_search = QSearch(
            model_attrs=[
                User.first_name,
                User.last_name,
            ],
            op=OperationEnum.ILIKE,
            logical_op=LogicalOperator.OR,
        )


class UserSimpleFilterWithCustomFields(BaseFilter):
    class FilterConfig:
        model = User
        prefix = "user"
        fields = ["first_name", "age", "is_working", "birthday"]

        q_search = QSearch(
            model_attrs=[
                User.first_name,
                User.last_name,
            ],
            op=OperationEnum.ILIKE,
            logical_op=LogicalOperator.OR,
        )


class SimpleQ(BaseFilter):
    class FilterConfig:
        q_search = QSearch(
            model_attrs=[User.first_name, User.last_name],
            op=OperationEnum.LIKE,
            logical_op=LogicalOperator.OR,
        )


class AdvancedQ(BaseFilter):
    class FilterConfig:
        q_search = AdvancedQSearch(
            model_attrs_with_op={
                OperationEnum.LIKE: [User.first_name],
                OperationEnum.ILIKE: [User.last_name],
            },
            logical_op=LogicalOperator.OR,
        )


class UserCustomizedFilterExample(BaseFilter):
    user__address__eq: str = "address"

    class FilterConfig:
        model = User
        prefix = "user"
        pagination = PaginationEnum.PAGE_BASED
        default_op = (
            OperationEnum.ILIKE,
            OperationEnum.IN,
            OperationEnum.EQ,
            OperationEnum.LIKE,
        )
        fields = ["first_name", "age", "gender", "is_working", "birthday"]


class UserAdvancedFilterWithRequiredOpExample(BaseFilter):
    class FilterConfig:
        model = User
        pagination = PaginationEnum.OFFSET_BASED
        sort_by = SortBy(
            model_attrs={
                "first_name": User.first_name,
                "age": User.age,
                "created_at": User.created_at,
            },
            alias_as_camelcase=True,
        )

        q_search = QSearch(
            model_attrs=[User.first_name, User.last_name],
            op=OperationEnum.ILIKE,
            logical_op=LogicalOperator.OR,
        )
        select_only = Selectable(
            model_attrs={
                "first_name": User.first_name,
                "age": User.age,
                "is_working": User.is_working,
                "birthday": User.birthday,
            },
            alias_as_camelcase=True,
        )
        fields = [
            FieldCriteria(
                name="first_name",
                field_type=str,
                model_attr=User.first_name,
                op=(
                    OperationEnum.EQ,
                    OperationEnum.NEQ,
                    OperationEnum.LIKE,
                    OperationEnum.ILIKE,
                    OperationEnum.IN,
                    OperationEnum.CONT,
                ),
                prefix=USER_PUBLIC_PREFIX,
            ),
            FieldCriteria(
                name="age",
                field_type=int,
                model_attr=User.age,
                op=(
                    OperationEnum.GTE,
                    OperationEnum.LTE,
                    OperationEnum.GT,
                    OperationEnum.LT,
                    OperationEnum.IN,
                    OperationEnum.NOTIN,
                ),
                prefix=USER_PRIVATE_PREFIX,
                required_op=(
                    OperationEnum.GTE,
                    OperationEnum.LTE,
                    OperationEnum.GT,
                    OperationEnum.LT,
                ),
            ),
        ]


class UserAdvancedFilterExample(BaseFilter):
    class FilterConfig:
        model = User
        pagination = PaginationEnum.OFFSET_BASED
        sort_by = SortBy(
            model_attrs={
                "first_name": User.first_name,
                "age": User.age,
                "created_at": User.created_at,
            },
            alias_as_camelcase=True,
        )

        q_search = AdvancedQSearch(
            model_attrs_with_op={
                OperationEnum.ILIKE: [User.first_name, User.last_name],
                OperationEnum.LIKE: [User.last_name],
            },
            logical_op=LogicalOperator.OR,
        )
        select_only = Selectable(
            model_attrs={
                "first_name": User.first_name,
                "age": User.age,
                "is_working": User.is_working,
                "birthday": User.birthday,
            },
            alias_as_camelcase=True,
        )
        fields = [
            FieldCriteria(
                name="titles",
                field_type=str,
                model_attr=User.titles,
                op=(OperationEnum.CONT, OperationEnum.EQ, OperationEnum.IN),
                prefix=USER_PUBLIC_PREFIX,
            ),
            FieldCriteria(
                name="first_name",
                field_type=str,
                model_attr=User.first_name,
                op=(
                    OperationEnum.EQ,
                    OperationEnum.NEQ,
                    OperationEnum.LIKE,
                    OperationEnum.ILIKE,
                    OperationEnum.IN,
                    OperationEnum.CONT,
                ),
                prefix=USER_PUBLIC_PREFIX,
            ),
            FieldCriteria(
                name="age",
                field_type=int,
                model_attr=User.age,
                op=(
                    OperationEnum.GTE,
                    OperationEnum.LTE,
                    OperationEnum.GT,
                    OperationEnum.LT,
                    OperationEnum.IN,
                    OperationEnum.NOTIN,
                ),
                prefix=USER_PRIVATE_PREFIX,
            ),
            FieldCriteria(
                name="is_working",
                field_type=bool,
                model_attr=User.is_working,
                op=(OperationEnum.ISNULL, OperationEnum.IS),
                prefix=USER_PRIVATE_PREFIX,
            ),
            FieldCriteria(
                name="is_old",
                field_type=bool,
                custom_filter_per_op=lambda _, value: User.age > 65
                if value
                else User.age <= 65,
                op=(OperationEnum.ISNULL, OperationEnum.IS),
                prefix=USER_PRIVATE_PREFIX,
            ),
            FieldCriteria(
                name="is_young",
                field_type=bool,
                custom_filter_per_op=lambda _, value: User.age < 18
                if value
                else User.age >= 18,
                op=(OperationEnum.ISNULL, OperationEnum.IS),
                prefix=USER_PRIVATE_PREFIX,
            ),
            FieldCriteria(
                name="full_name",
                model_attrs_with_logical_op=(
                    (User.first_name, User.last_name),
                    LogicalOperator.AND,
                ),
                field_type=bool,
                op=(OperationEnum.EQ, OperationEnum.NEQ),
                prefix=USER_PRIVATE_PREFIX,
            ),
            FieldCriteria(
                name="birthday",
                field_type=date,
                model_attr=User.birthday,
                op=(
                    OperationEnum.GT,
                    OperationEnum.BTW,
                    OperationEnum.LT,
                    OperationEnum.IN,
                ),
                prefix=USER_PRIVATE_PREFIX,
            ),
            FieldCriteria(
                name="gender",
                field_type=GenderEnum,
                model_attr=User.gender,
                op=(OperationEnum.EQ, OperationEnum.IN, OperationEnum.CONT),
                prefix=USER_PUBLIC_PREFIX,
            ),
            FieldCriteria(
                name="created_at",
                field_type=datetime,
                model_attr=User.created_at,
                op=(
                    OperationEnum.EQ,
                    OperationEnum.GT,
                    OperationEnum.LT,
                    OperationEnum.IN,
                ),
                prefix=USER_PUBLIC_PREFIX,
            ),
        ]
