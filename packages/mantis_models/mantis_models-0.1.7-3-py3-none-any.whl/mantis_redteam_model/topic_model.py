# -*- coding: utf-8 -*-
from enum import Enum
from typing import Dict

from mantis_redteam_model.infrastructure import InfrastructureTypeName


class Topic:
    def to_dict(self) -> Dict:
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }


#######################################
#           ATTACK_SESSION            #
#######################################


class AttackSessionInfos(Topic):
    def __init__(
        self,
        source: str,
        username: str,
        type: str,
        identifier: str,
        privilege_level: int,
    ) -> None:
        self.source = source
        self.username = username
        self.type = type
        self.identifier = identifier
        self.privilege_level = privilege_level


class AttackSession(Topic):
    def __init__(
        self,
        host_ip: str,
        attack_session: AttackSessionInfos,
        parent_identifier: str = "",
        direct_access: bool = False,
    ) -> None:
        self.host_ip = host_ip
        self.attack_session = attack_session
        self.parent_identifier = parent_identifier
        self.direct_access = direct_access

    def to_dict(self) -> Dict:
        return {
            "host_ip": self.host_ip,
            "attack_session": self.attack_session.to_dict(),
            "parent_identifier": self.parent_identifier,
            "direct_access": self.direct_access,
        }


#######################################
#             CREDENTIAL              #
#######################################


class Hash(Topic):
    def __init__(self, content: str, hash_type: str = "") -> None:
        self.content = content
        self.hash_type = hash_type


class Credential(Topic):
    def __init__(
        self,
        username: str,
        password: str = "",
        type: str = "",
        mail: str = "",
        hash: Hash = None,
    ) -> None:
        self.username = username
        self.password = password
        self.type = type
        self.mail = mail
        self.hash = hash

    def to_dict(self) -> Dict:
        cred_dict = {
            "username": self.username,
            "password": self.password,
            "type": self.type,
            "mail": self.mail,
        }

        if self.hash:
            cred_dict["hash"] = self.hash.to_dict()
        return cred_dict


#######################################
#                FILE                 #
#######################################


class FileInfos(Topic):
    def __init__(self, path: str, name: str = "") -> None:
        self.path = path
        self.name = name


class File(Topic):
    def __init__(self, host_ip: str, file: FileInfos) -> None:
        self.host_ip = host_ip
        self.file = file

    def to_dict(self) -> Dict:
        return {"host_ip": self.host_ip, "file": self.file.to_dict()}


#######################################
#                HOST                 #
#######################################


class HostInfos(Topic):
    def __init__(self, hostname: str, netbios_name: str = "") -> None:
        self.hostname = hostname
        self.netbios_name = netbios_name


class Roles(Topic):
    def __init__(self, name: str) -> None:
        self.name = name


class Host(Topic):
    def __init__(self, host_ip: str, host: HostInfos, roles: Roles = None) -> None:
        self.host_ip = host_ip
        self.host = host
        self.roles = roles or []

    def to_dict(self) -> Dict:
        return {
            "host_ip": self.host_ip,
            "host": self.host.to_dict(),
            "roles": [role.to_dict() for role in self.roles],
        }


#######################################
#             INFRASTRUCTURE          #
#######################################


class Infrastructure(Topic):
    def __init__(
        self,
        public_ip: str,
        private_ip: str = "",
        domain_name: str = "",
        type: str = "",
    ) -> None:
        self.public_ip = public_ip
        self.private_ip = private_ip
        self.domain_name = domain_name
        self.type = InfrastructureTypeName(value=type).value


#######################################
#               NETWORK               #
#######################################


class NetworkInterface(Topic):
    def __init__(
        self, ip: str, mac: str = "", subnet: str = "", internet_access: bool = True
    ) -> None:
        self.ip = ip
        self.mac = mac
        self.subnet = subnet
        self.internet_access = internet_access


class Ports(Topic):
    def __init__(self, number: int, type: str, status: str = "") -> None:
        self.number = number
        self.type = type
        self.status = status


class Network(Topic):
    def __init__(
        self, network_interface: NetworkInterface, ports: Ports = None
    ) -> None:
        self.network_interface = network_interface
        self.ports = ports or []

    def to_dict(self) -> Dict:
        return {
            "network_interface": self.network_interface.to_dict(),
            "ports": [port.to_dict() for port in self.ports],
        }


#######################################
#               PAYLOAD               #
#######################################


class PayloadType(str, Enum):
    beacon = "beacon"
    unknown = "unknown"


class PayloadOs(str, Enum):
    linux = "linux"
    windows = "windows"
    unknown = "unknown"


class Payload(Topic):
    def __init__(self, name: str, url: str, payload_type: str, payload_os: str) -> None:
        self.name = name
        self.url = url
        self.payload_type = PayloadType(value=payload_type).value
        self.payload_os = PayloadOs(value=payload_os).value


#######################################
#               SERVICE               #
#######################################


class ServiceInfos(Topic):
    def __init__(
        self,
        product: str,
        vendor: str = "",
        version: str = "",
        language: str = "",
        status: str = "",
    ) -> None:
        self.product = product
        self.vendor = vendor
        self.version = version
        self.language = language
        self.status = status


class Service(Topic):
    def __init__(
        self,
        network_interface: NetworkInterface,
        service: ServiceInfos,
        ports: Ports = None,
        credentials: Credential = None,
    ) -> None:
        self.network_interface = network_interface
        self.service = service
        self.ports = ports or []
        self.credentials = credentials or []

    def to_dict(self) -> Dict:
        return {
            "network_interface": self.network_interface.to_dict(),
            "service": self.service.to_dict(),
            "ports": [port.to_dict() for port in self.ports],
            "credentials": [cred.to_dict() for cred in self.credentials],
        }


#######################################
#               SOFTWARE              #
#######################################


class SoftwareInfos(Topic):
    def __init__(
        self,
        product: str = "",
        vendor: str = "",
        version: str = "",
        language: str = "",
        status: str = "",
        architecture: str = "",
        path: str = "",
        category: str = "",
    ) -> None:
        if not category and not product:
            raise ValueError("If category is not specified, product must be specified.")
        self.product = product
        self.vendor = vendor
        self.version = version
        self.language = language
        self.status = status
        self.architecture = architecture
        self.path = path
        self.category = category


class Software(Topic):
    def __init__(
        self, host_ip: str, software: SoftwareInfos, credentials: Credential = None
    ) -> None:
        self.host_ip = host_ip
        self.software = software
        self.credentials = credentials or []

    def to_dict(self) -> Dict:
        return {
            "host_ip": self.host_ip,
            "software": self.software.to_dict(),
            "credentials": [cred.to_dict() for cred in self.credentials],
        }
