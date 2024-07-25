from abc import ABC, abstractmethod
from typing import Dict, List, NoReturn, Optional

from luna_sdk.interfaces.repository_i import IRepository
from luna_sdk.schemas import QpuTokenOut
from luna_sdk.schemas.enums.qpu_token_type import QpuTokenTypeEnum


class IQpuTokenRepo(IRepository, ABC):
    @abstractmethod
    def create(
        self,
        name: str,
        provider: str,
        token: str,
        token_type: QpuTokenTypeEnum = QpuTokenTypeEnum.PERSONAL,
        encryption_key: Optional[str] = None,
    ) -> QpuTokenOut:
        """
        Create organization QPU token

        Parameters
        ----------
        name: str
            Name of the QPU token
        provider: ProviderEnum
            Name of provider
        token: str
            Token
        token_type: QpuTokenTypeEnum
            There are two types of QPU tokens: PERSONAL and ORGANIZATION.
            The default value is PERSONAL.
            All users of an organization can use organization QPU tokens.
            User QPU tokens can only be used by the user who created them.
        encryption_key: Optional[str]
            Encryption key to be used for encryption of QPU tokens.
        Returns
        -------
        QpuTokenOut
            QpuToken instances.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        filter_provider: Optional[str] = None,
        name: Optional[str] = None,
        token_type: Optional[QpuTokenTypeEnum] = None,
    ) -> Dict[QpuTokenTypeEnum, List[QpuTokenOut]]:
        """
        Retrieve a list of QPU tokens.

        Parameters
        ----------
        filter_provider: Optional[str]
            The provider for which qpu tokens should be retrieved
        name: Optional[str]
            Name of the QPU token that should be retrieved
        token_type: Optional[QpuTokenTypeEnum]
            If you want to retrieve only user or organization QPU tokens
            otherwise all QPU tokens will be retrieved
        Returns
        -------
        Dict[QpuTokenTypeEnum, List[QpuTokenOut]]
            List of QpuTokenOut instances.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        name: str,
        token_type: QpuTokenTypeEnum = QpuTokenTypeEnum.PERSONAL,
    ) -> QpuTokenOut:
        """
        Retrieve user QPU token by id

        Parameters
        ----------
        name: str
            Name of the QPU token that should be retrieved

        token_type: QpuTokenTypeEnum
            There are two types of QPU tokens: PERSONAL and ORGANIZATION.
            The default value is PERSONAL.
            All users of an organization can use organization QPU tokens.
            User QPU tokens can only be used by the user who created them.

        Returns
        -------
        QpuTokenOut
            QpuToken instance.
        """
        raise NotImplementedError

    @abstractmethod
    def rename(
        self,
        name: str,
        new_name: str,
        token_type: QpuTokenTypeEnum = QpuTokenTypeEnum.PERSONAL,
    ) -> QpuTokenOut:
        """
        Update organization QPU token by id

        Parameters
        ----------
        name: str
            Current name of the QPU token that should be updated
        new_name: str
            The new name

        token_type: QpuTokenTypeEnum
            There are two types of QPU tokens: PERSONAL and ORGANIZATION.
            The default value is PERSONAL.
            All users of an organization can use organization QPU tokens.
            User QPU tokens can only be used by the user who created them.


        Returns
        -------
        QpuTokenOut
            QpuToken instance.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        name: str,
        token_type: QpuTokenTypeEnum = QpuTokenTypeEnum.PERSONAL,
    ) -> None:
        """
        Delete organization QPU token by id

        Parameters
        ----------
        name: str
            Name of the QPU token that should be deleted

        token_type: QpuTokenTypeEnum
            There are two types of QPU tokens: PERSONAL and ORGANIZATION.
            The default value is PERSONAL.
            All users of an organization can use organization QPU tokens.
            User QPU tokens can only be used by the user who created them.

        Returns
        -------
        """
        raise NotImplementedError
