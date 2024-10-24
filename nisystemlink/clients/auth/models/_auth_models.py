"""Models utilized for Auth in SystemLink."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class AuthStatement(JsonModel):
    actions: Optional[List[str]] = None
    """
    A list of actions the user is allowed to perform
    """
    resource: Optional[List[str]] = None
    """
    A list of resources the user is allowed to access
    """
    workspace: Optional[str] = Field(None, example="workspace-id")
    """
    The workspace the user is allowed to access
    """


class AuthPolicy(JsonModel):
    statements: Optional[List[AuthStatement]] = None
    """
    A list of statements defining the actions the user can perform on a resource in a workspace
    """


class Statement(JsonModel):
    actions: Optional[List[str]] = None
    """
    A list of actions the user is allowed to perform
    """
    resource: Optional[List[str]] = None
    """
    A list of resources the user is allowed to access
    """
    workspace: Optional[str] = Field(None, example="workspace-id")
    """
    The workspace the user is allowed to access
    """
    description: Optional[str] = None
    """
    A description for this statement
    """


class Policy(JsonModel):
    id: Optional[str] = Field(None, example="policy-id")
    """
    The unique id
    """
    name: Optional[str] = Field(None, example="policy-name")
    """
    The policies's name
    """
    type: Optional[str] = Field(None, example="role")
    """
    The type of the policy
    """
    built_in: Optional[bool] = Field(None, alias="builtIn", example=True)
    """
    Whether the policy is built-in
    """
    user_id: Optional[str] = Field(None, alias="userId", example="user-id")
    """
    The user id
    """
    created: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The created timestamp
    """
    updated: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The last updated timestamp
    """
    deleted: Optional[bool] = Field(None, example=True)
    """
    Whether the policy is deleted or not
    """
    properties: Optional[Dict[str, str]] = Field(None, example={"key1": "value1"})
    """
    A map of key value properties
    """
    statements: Optional[List[Statement]] = None
    """
    A list of statements defining the actions the user can perform on a resource in a workspace
    """
    template_id: Optional[str] = Field(
        None, alias="templateId", example="policy-template-id"
    )
    """
    The id of the policy template. Only set if the policy has been created based on a template and
    does not contain inline statements.
    """
    workspace: Optional[str] = Field(None, example="workspace-id")
    """
    The workspace the policy template applies to. Only set if the policy has been created based on a
    template and does not contain inline statements.
    """


class Key(JsonModel):
    id: Optional[str] = Field(None, example="api-key-id")
    """
    The unique id
    """
    name: Optional[str] = Field(None, example="api-key-name")
    """
    The key's name
    """
    user_id: Optional[str] = Field(None, alias="userId", example="user-id")
    """
    The user id
    """
    created: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The created timestamp
    """
    updated: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The last updated timestamp
    """
    expiry: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The time when the key expires (epoch in milliseconds)
    """
    enabled: Optional[bool] = Field(None, example=True)
    """
    Whether the key is enabled or not
    """
    deleted: Optional[bool] = Field(None, example=True)
    """
    Whether the key is deleted or not
    """
    default_workspace: Optional[str] = Field(
        None, alias="defaultWorkspace", example="workspace-id"
    )
    """
    This field overrides the default workspace when authenticating.
    """
    properties: Optional[Dict[str, str]] = Field(None, example={"key1": "value1"})
    """
    A map of key value properties
    """
    policies: Optional[List[Policy]] = None
    """
    A list of policy definitions including statements and permissions
    """


class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"


class User(JsonModel):
    id: Optional[str] = Field(None, example="user-id")
    """
    The unique id
    """
    first_name: Optional[str] = Field(
        None, alias="firstName", example="user-first-name"
    )
    """
    The user's first name
    """
    last_name: Optional[str] = Field(None, alias="lastName", example="user-last-name")
    """
    The user's last name
    """
    email: Optional[str] = Field(None, example="example@email.com")
    """
    The user's email
    """
    phone: Optional[str] = Field(None, example="555-555-5555")
    """
    The user's contact phone number
    """
    niua_id: Optional[str] = Field(None, alias="niuaId", example="example@email.com")
    """
    The external id (niuaId, SID, login name)
    """
    login: Optional[str] = None
    """
    The login name of the user. This the "username" or equivalent entered when
    the user authenticates with the identity provider.
    """
    accepted_to_s: Optional[bool] = Field(None, alias="acceptedToS", example=True)
    """
    (deprecated) Whether the user accepted the terms of service
    """
    properties: Optional[Dict[str, str]] = Field(None, example={"key1": "value1"})
    """
    A map of key value properties
    """
    keywords: Optional[List[str]] = None
    """
    A list of keywords associated with the user
    """
    created: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The created timestamp
    """
    updated: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The last updated timestamp
    """
    org_id: Optional[str] = Field(None, alias="orgId", example="org-id")
    """
    The id of the organization
    """
    policies: Optional[List[str]] = None
    """
    A list of policy ids to reference existing policies
    """
    status: Optional[Status] = Field(None, example="active")
    """
    The status of the users' registration
    """
    entitlements: Optional[Any] = None
    """
    (deprecated) Features to which the user is entitled within the application.
    """


class Org(JsonModel):
    id: Optional[str] = Field(None, example="org-id")
    """
    The unique id
    """
    name: Optional[str] = Field(None, example="org-name")
    """
    The name of the organization
    """
    owner_id: Optional[str] = Field(None, alias="ownerId", example="user-id")
    """
    The userId of the organization owner
    """


class Workspace(JsonModel):
    id: Optional[str] = Field(None, example="workspace-id")
    """
    The unique id
    """
    name: Optional[str] = Field(None, example="workspace-name")
    """
    The workspace name
    """
    enabled: Optional[bool] = Field(None, example=True)
    """
    Whether the workspace is enabled or not
    """
    default: Optional[bool] = Field(None, example=True)
    """
    Whether the workspace is the default. The default workspace is used when callers omit a \
workspace id
    """


class Error(JsonModel):
    name: Optional[str] = None
    """
    String error code
    """
    code: Optional[int] = None
    """
    Numeric error code
    """
    resource_type: Optional[str] = Field(None, alias="resourceType")
    """
    Type of resource associated with the error
    """
    resource_id: Optional[str] = Field(None, alias="resourceId")
    """
    Identifier of the resource associated with the error
    """
    message: Optional[str] = None
    """
    Complete error message
    """
    args: Optional[List[str]] = None
    """
    Positional argument values for the error code
    """
    inner_errors: Optional[List[Error]] = Field(None, alias="innerErrors")


class UserPolicy(JsonModel):
    id: Optional[str] = Field(None, example="policy-id")
    """
    The identifier of a policy
    """
    name: Optional[str] = Field(None, example="policy-name")
    """
    The policy name
    """
    template_id: Optional[str] = Field(
        None, alias="templateId", example="policy-template-id"
    )
    """
    The identifier of a policy template
    """
    workspace_id: Optional[str] = Field(
        None, alias="workspaceId", example="workspace-id"
    )
    """
    The identifier of a workspace
    """


class UserPolicyTemplate(JsonModel):
    id: Optional[str] = Field(None, example="policy-template-id")
    """
    The identifier of a policy template
    """
    name: Optional[str] = Field(None, example="policy-template-name")
    """
    The policy template name
    """


class PolicyTemplate(JsonModel):
    id: Optional[str] = Field(None, example="policy-template-id")
    """
    The unique id
    """
    name: Optional[str] = Field(None, example="policy-template-name")
    """
    The policy template's name
    """
    type: Optional[str] = Field(None, example="user")
    """
    The type of the policy template
    """
    built_in: Optional[bool] = Field(None, alias="builtIn", example=True)
    """
    Whether the policy template is built-in
    """
    user_id: Optional[str] = Field(None, alias="userId", example="user-id")
    """
    The user id
    """
    created: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The created timestamp
    """
    updated: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The last updated timestamp
    """
    deleted: Optional[bool] = Field(None, example=True)
    """
    Whether the policy is deleted or not
    """
    properties: Optional[Dict[str, str]] = Field(None, example={"key1": "value1"})
    """
    A map of key value properties
    """
    statements: Optional[List[Statement]] = None
    """
    A list of statements defining the actions the user can perform on a resource
    """


class AuthInfo(JsonModel):
    """Information about the authenticated caller."""

    user: Optional[User]
    """Details of authenticated caller"""
    org: Optional[Org]
    """Organization of authenticated caller"""
    workspaces: Optional[List[Workspace]]
    """List of workspaces the authenticated caller has access"""
    policies: Optional[List[AuthPolicy]]
    """List of policies for the authenticated caller"""
    properties: Optional[Dict[str, str]] = Field(None, example={"key1": "value1"})
    """A map of key value properties"""
