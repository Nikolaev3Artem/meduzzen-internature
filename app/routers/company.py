from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.schemas.company import CompanyCreate, CompanyGet, CompanyUpdate
from app.services.auth_jwt import get_active_user
from app.services.company import CompanyService

router = APIRouter(prefix="/company", tags=["Company"])


@router.post("/", response_model=CompanyGet, status_code=status.HTTP_201_CREATED)
async def company_create(
    company: CompanyCreate,
    session: AsyncSession = Depends(get_session),
    company_service: CompanyService = Depends(CompanyService),
    user: User = Depends(get_active_user),
) -> CompanyGet:
    return await company_service.company_create(
        company=company, session=session, user=user
    )


@router.get("/", response_model=list[CompanyGet])
async def company_list(
    limit: int,
    offset: int,
    session: AsyncSession = Depends(get_session),
    company_service: CompanyService = Depends(CompanyService),
    user: User = Depends(get_active_user),
) -> list[CompanyGet]:
    return await company_service.companies_list(
        limit=limit, offset=offset, session=session
    )


@router.get("/{company_id}", response_model=CompanyGet)
async def company_get(
    company_id: UUID,
    session: AsyncSession = Depends(get_session),
    company_service: CompanyService = Depends(CompanyService),
    user: User = Depends(get_active_user),
) -> CompanyGet:
    return await company_service.company_get(id=company_id, session=session)


@router.patch("/{company_id}", response_model=CompanyUpdate)
async def company_update(
    company_id: UUID,
    company_data: CompanyUpdate,
    session: AsyncSession = Depends(get_session),
    company_service: CompanyService = Depends(CompanyService),
    user: User = Depends(get_active_user),
):
    return await company_service.company_update(
        company_id=company_id, company_data=company_data, session=session, user=user
    )


@router.patch("/{company_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def company_deactivate(
    company_id: UUID,
    session: AsyncSession = Depends(get_session),
    company_service: CompanyService = Depends(CompanyService),
    user: User = Depends(get_active_user),
) -> None:
    return await company_service.company_deactivate(
        company_id=company_id, session=session, user=user
    )
