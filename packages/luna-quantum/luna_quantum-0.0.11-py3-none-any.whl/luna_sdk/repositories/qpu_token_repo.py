import json
import os
from typing import Dict, List, Optional

from httpx import Response

from luna_sdk.exceptions.encryption_exception import EncryptionNotSetException
from luna_sdk.interfaces.qpu_token_repo_i import IQpuTokenRepo
from luna_sdk.schemas import QpuTokenOut
from luna_sdk.schemas.create import QpuTokenIn
from luna_sdk.schemas.enums.qpu_token_type import QpuTokenTypeEnum


class QpuTokenRepo(IQpuTokenRepo):
    @property
    def _endpoint(self) -> str:
        return "/qpu-tokens"

    def _get_endpoint_by_type(
        self, token_type: Optional[QpuTokenTypeEnum] = None
    ) -> str:
        if token_type is None:
            return f"{self._endpoint}"
        elif token_type == QpuTokenTypeEnum.PERSONAL:
            return f"{self._endpoint}/users"
        else:
            return f"{self._endpoint}/organization"

    def _get_by_name(self, name: str, token_type: QpuTokenTypeEnum) -> QpuTokenOut:
        response: Response = self._client.get(
            f"{self._get_endpoint_by_type(token_type)}/by_name/{name}"
        )
        response.raise_for_status()

        qpu_token_data = response.json()
        return QpuTokenOut.model_validate(qpu_token_data)

    def create(
        self,
        name: str,
        provider: str,
        token: str,
        token_type: QpuTokenTypeEnum = QpuTokenTypeEnum.PERSONAL,
        encryption_key: Optional[str] = None,
    ) -> QpuTokenOut:
        """
        Create user QPU token

        Parameters
        ----------
        name: str
            Name of the QPU token
        provider: str
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
            QpuTokenOut instances.
        """
        encryption_key = encryption_key or os.environ.get("LUNA_ENCRYPTION_KEY")
        if encryption_key is None:
            raise EncryptionNotSetException
        qpu_token = QpuTokenIn(
            name=name,
            provider=provider,
            token=token,
            encryption_key=encryption_key,
        )

        response: Response = self._client.post(
            self._get_endpoint_by_type(token_type), content=qpu_token.model_dump_json()
        )
        response.raise_for_status()
        qpu_token_data = response.json()
        return QpuTokenOut.model_validate(qpu_token_data)

    def get_all(
        self,
        filter_provider: Optional[str] = None,
        name: Optional[str] = None,
        token_type: Optional[QpuTokenTypeEnum] = None,
    ) -> Dict[QpuTokenTypeEnum, List[QpuTokenOut]]:
        """
        Retrieve list of user QPU tokens.

        Parameters
        ----------
        filter_provider: Optional[str]
            The provider for which qpu tokens should be retrieved
        name: Optional[str]
            Name of the QPU token that should be retrieved
        token_type: Optional[QpuTokenTypeEnum]
            If you want to retrieve only user or organization QPU tokens
            otherwise all QPU tokens will be retrieved
        token_type: QpuTokenTypeEnum
            There are two types of QPU tokens: PERSONAL and ORGANIZATION.
            The default value is PERSONAL.
            All users of an organization can use organization QPU tokens.
            User QPU tokens can only be used by the user who created them.

        Returns
        -------
        Dict[QpuTokenTypeEnum, List[QpuTokenOut]]
            List of QpuTokenOut instances.
        """
        params = {}
        if filter_provider:
            params["filter_provider"] = filter_provider

        if name:
            params["name"] = name

        response = self._client.get(self._get_endpoint_by_type(), params=params)
        response.raise_for_status()

        to_return: Dict[QpuTokenTypeEnum, List[QpuTokenOut]] = {}
        for key, value in response.json().items():
            to_return[QpuTokenTypeEnum(key)] = [
                QpuTokenOut.model_validate(item) for item in value
            ]

        return to_return

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
            QpuTokenOut instance.
        """

        qpu_token: QpuTokenOut = self._get_by_name(name, token_type)

        return qpu_token

    def rename(
        self,
        name: str,
        new_name: str,
        token_type: QpuTokenTypeEnum = QpuTokenTypeEnum.PERSONAL,
    ) -> QpuTokenOut:
        """
        Update user QPU token by id

        Parameters
        ----------
        name: str
            Name of the QPU token that should be updated
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
            QpuTokenOut instance.
        """
        qpu_token_update_data = {"name": new_name}

        token: QpuTokenOut = self.get(name, token_type)

        response = self._client.put(
            f"{self._get_endpoint_by_type(token_type)}/{token.id}",
            content=json.dumps(qpu_token_update_data),
        )
        response.raise_for_status()

        qpu_token_data = response.json()
        return QpuTokenOut.model_validate(qpu_token_data)

    def delete(
        self,
        name: str,
        token_type: QpuTokenTypeEnum = QpuTokenTypeEnum.PERSONAL,
    ) -> None:
        """
        Delete organization QPU token by name

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
        token: QpuTokenOut = self.get(name, token_type)

        response = self._client.delete(
            f"{self._get_endpoint_by_type(token_type)}/{token.id}"
        )
        response.raise_for_status()
