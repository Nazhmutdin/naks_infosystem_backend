from dishka import Provider, Scope, provide, from_context
from naks_library.committer import SqlAlchemyCommitter
from naks_library.common.get_many_stmt_creator import IGetManyStmtCreator, StandartSqlAlchemyGetManyStmtCreator
from fastapi import Request

from app.application.interfaces.gateways import PersonalGateway, PersonalNaksCertificationGateway, NdtGateway, AcstGateway
from app.application.interactors import (
    CreatePersonalInteractor,
    UpdatePersonalInteractor,
    GetPersonalInteractor,
    SelectPersonalInteractor,
    DeletePersonalInteractor,
    CreatePersonalNaksCertificationInteractor,
    UpdatePersonalNaksCertificationInteractor,
    GetPersonalNaksCertificationInteractor,
    GetCertainPersonalNaksCertificationsInteractor,
    SelectPersonalNaksCertificationInteractor,
    DeletePersonalNaksCertificationInteractor,
    CreateNdtInteractor,
    UpdateNdtInteractor,
    GetNdtInteractor,
    GetCertainPersonalNdtsInteractor,
    SelectNdtInteractor,
    DeleteNdtInteractor,
    GetAcstInteractor,
    CreateAcstInteractor,
    UpdateAcstInteractor,
    DeleteAcstInteractor,
    SelectAcstInteractor
)
from app.infrastructure.database.mappers import PersonalMapper, PersonalNaksCertificationMapper, NdtMapper, AcstMapper
from app.application.common.select_stmt_creator_configs import (
    PersonalSelectStmtCreatorConfig, 
    PersonalNaksCertificationSelectStmtCreatorConfig, 
    NdtSelectStmtCreatorConfig,
    AcstSelectStmtCreatorConfig
)


type PersonalGetManyStmtCreator = IGetManyStmtCreator
type PersonalNaksCertificationGetManyStmtCreator = IGetManyStmtCreator
type NdtGetManyStmtCreator = IGetManyStmtCreator
type AcstGetManyStmtCreator = IGetManyStmtCreator


class ApplicationProvider(Provider):
    request = from_context(provides=Request, scope=Scope.REQUEST)
    
    @provide(scope=Scope.APP)
    async def provide_personal_get_many_stmt_creator(self) -> PersonalGetManyStmtCreator:
        return StandartSqlAlchemyGetManyStmtCreator(
            filters_map=PersonalSelectStmtCreatorConfig.filters_map,
            select_attrs=PersonalSelectStmtCreatorConfig.select_attrs,
            select_from_attrs=PersonalSelectStmtCreatorConfig.select_from_attrs,
            order_by_attrs=PersonalSelectStmtCreatorConfig.order_by_attrs
        )
    

    @provide(scope=Scope.APP)
    async def provide_personal_naks_certification_get_many_stmt_creator(self) -> PersonalNaksCertificationGetManyStmtCreator:
        return StandartSqlAlchemyGetManyStmtCreator(
            filters_map=PersonalNaksCertificationSelectStmtCreatorConfig.filters_map,
            select_attrs=PersonalNaksCertificationSelectStmtCreatorConfig.select_attrs,
            select_from_attrs=PersonalNaksCertificationSelectStmtCreatorConfig.select_from_attrs,
            order_by_attrs=PersonalNaksCertificationSelectStmtCreatorConfig.order_by_attrs
        )
    

    @provide(scope=Scope.APP)
    async def provide_ndt_get_many_stmt_creator(self) -> NdtGetManyStmtCreator:
        return StandartSqlAlchemyGetManyStmtCreator(
            filters_map=NdtSelectStmtCreatorConfig.filters_map,
            select_attrs=NdtSelectStmtCreatorConfig.select_attrs,
            select_from_attrs=NdtSelectStmtCreatorConfig.select_from_attrs,
            order_by_attrs=NdtSelectStmtCreatorConfig.order_by_attrs
        )
    

    @provide(scope=Scope.APP)
    async def provide_acst_get_many_stmt_creator(self) -> AcstGetManyStmtCreator:
        return StandartSqlAlchemyGetManyStmtCreator(
            filters_map=AcstSelectStmtCreatorConfig.filters_map,
            select_attrs=AcstSelectStmtCreatorConfig.select_attrs,
            select_from_attrs=AcstSelectStmtCreatorConfig.select_from_attrs,
            order_by_attrs=AcstSelectStmtCreatorConfig.order_by_attrs
        )
    

    @provide(scope=Scope.REQUEST)
    async def provide_personal_gateway(
        self,
        committer: SqlAlchemyCommitter,
    ) -> PersonalGateway:
        return PersonalMapper(committer.session)
    
    
    @provide(scope=Scope.REQUEST)
    async def provide_personal_naks_certification_gateway(
        self,
        committer: SqlAlchemyCommitter,
    ) -> PersonalNaksCertificationGateway:
        return PersonalNaksCertificationMapper(committer.session)
    
    
    @provide(scope=Scope.REQUEST)
    async def provide_ndt_gateway(
        self,
        committer: SqlAlchemyCommitter,
    ) -> NdtGateway:
        return NdtMapper(committer.session)
    
    
    @provide(scope=Scope.REQUEST)
    async def provide_acst_gateway(
        self,
        committer: SqlAlchemyCommitter,
    ) -> AcstGateway:
        return AcstMapper(committer.session)


    @provide(scope=Scope.REQUEST)
    async def provide_create_personal_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        personal_gateway: PersonalGateway
    ) -> CreatePersonalInteractor:

        return CreatePersonalInteractor(
            gateway=personal_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_personal_data_interactor(
        self, 
        personal_gateway: PersonalGateway
    ) -> GetPersonalInteractor:

        return GetPersonalInteractor(
            gateway=personal_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_select_personal_interactor(
        self, 
        create_stmt: PersonalGetManyStmtCreator,
        personal_gateway: PersonalGateway
    ) -> SelectPersonalInteractor:

        return SelectPersonalInteractor(
            create_stmt=create_stmt,
            gateway=personal_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_update_personal_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        personal_gateway: PersonalGateway
    ) -> UpdatePersonalInteractor:

        return UpdatePersonalInteractor(
            gateway=personal_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_delete_personal_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        personal_gateway: PersonalGateway
    ) -> DeletePersonalInteractor:

        return DeletePersonalInteractor(
            gateway=personal_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_create_personal_naks_certification_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        personal_naks_certification_gateway: PersonalNaksCertificationGateway
    ) -> CreatePersonalNaksCertificationInteractor:

        return CreatePersonalNaksCertificationInteractor(
            gateway=personal_naks_certification_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_personal_naks_certification_data_interactor(
        self, 
        personal_naks_certification_gateway: PersonalNaksCertificationGateway
    ) -> GetPersonalNaksCertificationInteractor:

        return GetPersonalNaksCertificationInteractor(
            gateway=personal_naks_certification_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_certain_personal_naks_certifications_data_interactor(
        self, 
        personal_naks_certification_gateway: PersonalNaksCertificationGateway
    ) -> GetCertainPersonalNaksCertificationsInteractor:

        return GetCertainPersonalNaksCertificationsInteractor(
            gateway=personal_naks_certification_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_select_personal_naks_certification_interactor(
        self, 
        create_stmt: PersonalNaksCertificationGetManyStmtCreator,
        personal_naks_certification_gateway: PersonalNaksCertificationGateway
    ) -> SelectPersonalNaksCertificationInteractor:

        return SelectPersonalNaksCertificationInteractor(
            create_stmt=create_stmt,
            gateway=personal_naks_certification_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_update_personal_naks_certification_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        personal_naks_certification_gateway: PersonalNaksCertificationGateway
    ) -> UpdatePersonalNaksCertificationInteractor:

        return UpdatePersonalNaksCertificationInteractor(
            gateway=personal_naks_certification_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_delete_personal_naks_certification_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        personal_naks_certification_gateway: PersonalNaksCertificationGateway
    ) -> DeletePersonalNaksCertificationInteractor:

        return DeletePersonalNaksCertificationInteractor(
            gateway=personal_naks_certification_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_create_ndt_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        ndt_gateway: NdtGateway
    ) -> CreateNdtInteractor:

        return CreateNdtInteractor(
            gateway=ndt_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_ndt_data_interactor(
        self, 
        ndt_gateway: NdtGateway
    ) -> GetNdtInteractor:

        return GetNdtInteractor(
            gateway=ndt_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_certain_personal_ndts_data_interactor(
        self, 
        ndt_gateway: NdtGateway
    ) -> GetCertainPersonalNdtsInteractor:

        return GetCertainPersonalNdtsInteractor(
            gateway=ndt_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_select_ndt_interactor(
        self, 
        create_stmt: NdtGetManyStmtCreator,
        ndt_gateway: NdtGateway
    ) -> SelectNdtInteractor:

        return SelectNdtInteractor(
            create_stmt=create_stmt,
            gateway=ndt_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_update_ndt_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        ndt_gateway: NdtGateway
    ) -> UpdateNdtInteractor:

        return UpdateNdtInteractor(
            gateway=ndt_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_delete_ndt_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        ndt_gateway: NdtGateway
    ) -> DeleteNdtInteractor:

        return DeleteNdtInteractor(
            gateway=ndt_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_create_acst_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        acst_gateway: AcstGateway
    ) -> CreateAcstInteractor:

        return CreateAcstInteractor(
            gateway=acst_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_acst_data_interactor(
        self, 
        acst_gateway: AcstGateway
    ) -> GetAcstInteractor:

        return GetNdtInteractor(
            gateway=acst_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_select_acst_interactor(
        self, 
        create_stmt: AcstGetManyStmtCreator,
        acst_gateway: AcstGateway
    ) -> SelectAcstInteractor:

        return SelectAcstInteractor(
            create_stmt=create_stmt,
            gateway=acst_gateway
        )


    @provide(scope=Scope.REQUEST)
    async def provide_update_acst_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        acst_gateway: AcstGateway
    ) -> UpdateAcstInteractor:

        return UpdateAcstInteractor(
            gateway=acst_gateway,
            committer=committer
        )


    @provide(scope=Scope.REQUEST)
    async def provide_delete_acst_interactor(
        self, 
        committer: SqlAlchemyCommitter,
        acst_gateway: AcstGateway
    ) -> DeleteAcstInteractor:

        return DeleteAcstInteractor(
            gateway=acst_gateway,
            committer=committer
        )
