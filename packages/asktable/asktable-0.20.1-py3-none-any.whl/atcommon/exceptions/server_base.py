# Error Design


class UnknownError(Exception):
    code = -1
    message = "Unknown Internal Error"


class ServerBaseError(Exception):
    code = 0
    message = "Base error"


# 1000 - 配置类错误
class ManagementError(ServerBaseError):
    code = 1
    message = "Management Error"


# 2000 - QA对话类错误
class QAError(ServerBaseError):
    code = 2
    message = "Question Answering Error"


# 3000 - 内部错误
class InternalError(ServerBaseError):
    code = 3
    message = "Internal error"


# 5000 - DataSource 自身内部错误
class DataSourceError(ServerBaseError):
    code = 5
    message = "DataSource Error"


################################


class Unauthorized(ManagementError):
    code = 1000
    message = "Unauthorized"


class ResourceAlreadyExists(ManagementError):
    code = 10010
    message = "Resource already exists"


class DataSourceExists(ManagementError):
    code = 10011
    message = "Datasource already exists"


class AuthRolePolicyExists(ManagementError):
    code = 10112
    message = "Auth Role Policy already exists"


class NotFound(ManagementError):
    code = 10040
    message = "Not found"


class DataSourceNotFound(ManagementError):
    code = 10041
    message = "Datasource not found"


class ChatNotFound(ManagementError):
    code = 10042
    message = "Chat not found"


class MessageNotFound(ManagementError):
    code = 10043
    message = "Message not found"


class TenantNotFound(ManagementError):
    code = 10044
    message = "Tenant not found"


class SecureTunnelNotFound(ManagementError):
    code = 10045
    message = "SecureTunnel not found"


class SecureTunnelLinkNotFound(ManagementError):
    code = 10046
    message = "SecureTunnel link not found"


class AuthPolicyNotFound(ManagementError):
    code = 10047
    message = "Auth Policy not found"


class AuthRoleNotFound(ManagementError):
    code = 10048
    message = "Auth Role not found"


class BotNotFound(ManagementError):
    code = 10049
    message = "Bot not found"


class ParameterError(ManagementError):
    code = 1003
    message = "Parameter error"


class DataSourceConfigError(ManagementError):
    code = 1005
    message = "Datasource config error"


class TooManyTablesAdded(ManagementError):
    code = 1006
    message = "Too many tables added"


class DataSourceMetaProcessing(ManagementError):
    code = 1007
    message = "Datasource meta processing"


class DataSourceMetaNotReady(ManagementError):
    code = 1008
    message = "Datasource meta not ready!"


class SecureTunnelConfigError(ManagementError):
    code = 1009
    message = "SecureTunnel config error"


class SecureTunnelInUse(ManagementError):
    code = 1011
    message = "SecureTunnel in use"


class ATSTServerAPIError(ManagementError):
    code = 1012
    message = "ATST Server API error"


class AuthPolicyConfigError(ManagementError):
    code = 1013
    message = "Auth Policy config error"


class AuthRoleConfigError(ManagementError):
    code = 1015
    message = "Auth Role config error"


class AuthRoleVariablesError(ManagementError):
    code = 1018
    message = "Auth Role variables error"


class AuthRolePrivilegesError(ManagementError):
    code = 1019
    message = "Auth Role privileges error"


class BotConfigError(ManagementError):
    code = 1020
    message = "Bot config error"


class ChatConfigError(ManagementError):
    code = 1021
    message = "Chat config error"


################################


class QAErrorNoMatchDataSource(QAError):
    code = 2002
    message = "No match datasource"


class QAErrorInsufficientData(QAError):
    code = 2003
    message = "Insufficient data"


class QAErrorIncompleteQuestion(QAError):
    code = 2004
    message = "Incomplete question"


class QAErrorCannotHandle(QAError):
    code = 2005
    message = "Cannot handle"


class QAErrorNoColumnFound(QAError):
    code = 2006
    message = "No column found"


class QueryPermissionDenied(QAError):
    code = 2008
    message = "Permission denied"


class QAErrorTooManyRows(QAError):
    code = 2007
    message = "Too many rows"


class NoDataFound(QAError):
    """
    查询结果为空
    """

    code = 2009
    message = "No data found"


class NoDataToQuery(QAError):
    """
    没有可供查询的数据
    """

    code = 2010
    message = "No data to query"


class MultipleQuery(QAError):
    """
    多个查询
    当前不支持生成sql时，单次返回多个sql
    """

    code = 2011
    message = "multiple queries in single question"


class PotentialSQLInjection(QAError):
    """
    潜在的SQL注入
    """

    code = 2012
    message = "Potential SQL injection"


####################################


class PromptTooLong(InternalError):
    code = 3001
    message = "Prompt too long"


class InvalidStrucQuery(InternalError):
    code = 3002
    message = "Invalid query syntax"


######################################
class LLMError(InternalError):
    code = 30031
    message = "LLM error"


class LLMBadRequest(LLMError):
    code = 30032
    message = "LLM bad request"


class LLMConnectionError(LLMError):
    code = 30033
    message = "LLM connection error"


# 5000 - DataSource 自身内部错误


class RetrieveMetaError(DataSourceError):
    code = 5001
    message = "Retrieve meta error"


class QueryDataError(DataSourceError):
    code = 5002
    message = "Query data error"


class FileReadError(DataSourceError):
    code = 5003
    message = "File read error"


# 6000 - ExtAPI 错误


class ExtAPIRequestError(ServerBaseError):
    code = 6000
    message = "API Request Error"
