---
url: "https://www.axigen.com/documentation/mailbox-api-authentication-and-authorization-p773357577"
title: "Mailbox API – Authentication and Authorization | Axigen Documentation"
---

[Mail Server, Calendaring & Collaboration](https://www.axigen.com/ "Mail Server, Calendaring & Collaboration")

- [Resources](https://www.axigen.com/mail-server/resources/)
- [Documentation](https://www.axigen.com/documentation/)
- [Knowledge Base](https://www.axigen.com/knowledgebase/)
- [Community](https://www.axigen.com/community/)
- [Customers](https://www.axigen.com/customers/)
- [Blog](https://www.axigen.com/mail-server/articles/)
- Menu

Close


- [Mail Server](https://www.axigen.com/)  - [For Service Providers](https://www.axigen.com/mail-server/isp/)
  - [FOR MSPs](https://www.axigen.com/mail-server/msp/)
  - [Cloud Native Mail Server](https://www.axigen.com/cloud-native-mail-server/)
  - [For Businesses](https://www.axigen.com/mail-server/business/)
  - [Free Mail Server](https://www.axigen.com/mail-server/free/)
  - [Features, Platforms & Roadmap](https://www.axigen.com/mail-server/features/)

- [Downloads](https://www.axigen.com/mail-server/download/)  - [Downloads](https://www.axigen.com/mail-server/download/)
  - [Outlook Connector](https://www.axigen.com/mail-server/outlook-connector/)
  - [Additional Modules](https://www.axigen.com/mail-server/additional-modules/)
  - [Automation Tools](https://www.axigen.com/mail-server/scripts/)

- [Support](https://www.axigen.com/support/)  - [Support Services](https://www.axigen.com/support/)
  - [SP Support](https://www.axigen.com/support/service-providers/)
  - [Channel Support](https://www.axigen.com/support/channel/)
  - [Business Support](https://www.axigen.com/support/business/)
  - [Get Support](https://www.axigen.com/support/contact/)

- [Resources](https://www.axigen.com/mail-server/resources/)  - [Documentation](https://www.axigen.com/documentation/)
  - [Knowledge Base](https://www.axigen.com/knowledgebase/)
  - [Community](https://www.axigen.com/community/)
  - [Release History](https://www.axigen.com/new-features/)
  - [Customers](https://www.axigen.com/customers/)
  - [Blog](https://www.axigen.com/mail-server/articles/)

- [Purchase](https://www.axigen.com/buy/)  - [Buy Online](https://www.axigen.com/buy/)
  - [Renew Support](https://www.axigen.com/buy/#renew)
  - [Locate a Partner](https://www.axigen.com/mail-server/locate-partner/)
  - [EDU / GOV Programs](https://www.axigen.com/mail-server/edu-gov-programs/)
  - [License Registration](https://www.axigen.com/mail-server/register/)

- [Partners](https://www.axigen.com/partners/)  - [Partnership Program](https://www.axigen.com/partners/)
  - [Apply Online](https://www.axigen.com/partners/#signup)
  - [Partner Login](https://www.axigen.com/partners/#login)

- [About us](https://www.axigen.com/about-us/)  - [Company](https://www.axigen.com/about-us/)
  - [Careers](https://www.axigen.com/about-us/careers/)
  - [Press Room](https://www.axigen.com/press/)
  - [Contact](https://www.axigen.com/about-us/contact/)

Updated: April 24, 2025

## Auth Methods

The Axigen Mailbox API supports the following authentication and authorization methods:

- **OAuth 2.0 with OpenID Connect** – for both browser based applications and mobile / native apps

- **Basic Authentication** – in case OAuth 2.0 and OpenID Connect is not available

- **Cookie Authentication** \- for browser based clients


Note that using OAuth 2.0 and OpenID Connect is strongly recommended as it is the most secure option.

2-Step Verification and Catpcha are supported in the following scenarios:

- when using OAuth 2.0 and OpenID Connect if enabled by the Authorization Server;

- when using Cookie based authentication.


## Login

|     |
| --- |
| `POST /api/v1/login` |

**Request Headers**

| **Name** | **Required** | **Values** | **Description** |
| `Authorization` | \* | `"Basic <username>:<password>", "Bearer <token>"` | “Basic” – used to authenticate against internal user authentication mechanism when OAuth 2.0 and OpenID Connect are not available<br>“Bearer” – used to authenticate against an external authentication provider (such as OAuth 2.0 and OpenID Connect) |

**Response**

When successful, the endpoint returns the following JSON structure:

|     |
| --- |
| `{`<br>`    ``sessid: String     ` `// new session ID for the current session`<br>`}` |

All subsequent API calls must use the same authentication method and include the session ID in the `X-Axigen-Session` header.

**Important:** If you start with Basic Auth, **all subsequent API calls must also include the same Basic Auth header**.

Alternatively, you can switch to using cookies **only if the login endpoint sets them** and your client stores them correctly.

Note that when using bearer token authorization, the username is unknown to Axigen until the token is validated against the external authentication provider.

In case the user can't be authenticated (i.e. wrong authentication credentials, invalid token, expired token, unknown user), the endpoint will respond with `401 Unauthorized`.

## Cookie Login NEW

|     |
| --- |
| `POST /api/v1/login/cookie` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `username` | `String` | \* |  | The username including the domain name when the user does not belong to the primary domain or no primary domain is set |
| `password` | `String` | \* |  | The account password |
| `captchaText` | `String` |  |  | The value of the captcha text |
| `captchaId` | `String` |  |  | The captcha id |
| `rememberLogin` | `Boolean` |  |  | The value set based on user choice |

**Response**

When successful, the endpoint returns the following JSON structure:

|     |
| --- |
| `{`<br>`    ``sessid: String     ` `// new session ID for the current session`<br>`}` |

Additionally, the response will also include the following headers when applicable:

| **Name** | **Type** | **Present** | **Values** | **Description** |
| `Set-Cookie` | `String` | \* |  | The Cookie to be used in all subsequent requests |
| `X-Axigen-2FA` | `String` |  | `required`, `mandatory` | The value is set to `required` when the a second step is required as part of the 2-Step Verification<br>The value is set to `mandatory` when setting up 2-Step Verification must be performed before continuing |

All subsequent API calls must use Cookie and include the session id as query parameter `_h=<sessid>`.

In case the user can not be authenticated (i.e. wrong authentication credentials, invalid captcha, unknown user), the endpoint will reply back with `401 Unauthorized`.

## Cookie Login with 2-Step Verification NEW

When 2-Step Verification is administratively enabled and active (i.e. the Cookie Login endpoint includes a `X-Axigen-2FA` header set to `required`), the API client must use this endpoint to complete the 2-Step Verification.

The API client should call the [List Account Security Methods](https://www.axigen.com/documentation/mailbox-api-account-security-p1602977833#ListMethods) endpoint with `scope=2fa` to obtain the list of available methods. When using either an `email` or `sms` method, a `totpToken` must be obtained by calling [Send Token](https://www.axigen.com/documentation/mailbox-api-account-security-p1602977833#SendToken).

Alternatively, a `recoveryCode` can be used to complete the 2-Step Verification. Recovery codes are generated automatically when activating the 2-Step Verification. They can also be regenerated by calling [Regenerate Recovery Codes](https://www.axigen.com/documentation/mailbox-api-account-security-p1602977833#RegenerateRecoveryCodes).

|     |
| --- |
| `POST /api/v1/login/2fa` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `methodId` | `String` | \* |  | The method id used for |
| `totpToken` | `String` | \* |  | The TOTP code |
| `recoveryCode` | `String` | \* |  | One of the recovery codes received when activating 2-Step Verification or after manually regenerating the recovery codes. |

Either of `methodId` and `totpToken` or `recoveryCode` is required.

**Response**

If successful, the response will be empty.

## Captcha NEW

This API is only available when using cookie login.

### Get Status

|     |
| --- |
| `GET /api/v1/captha/status` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `username` | `String` | \* |  | The username (including the domain name) for which the captcha requirement should be checked. |

**Response**

When successful, the endpoint returns the following JSON structure:

|     |
| --- |
| `{`<br>`    ``isRequired: Boolean     ` `// whether the captcha is required for the specified username`<br>`}` |

### Get Captcha

|     |
| --- |
| `GET /api/v1/captha` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `username` | `String` | \* |  | The username (including the domain name) for which the captcha requirement should be checked. |
| `t` | `String` |  |  | Typically set to the current timestamp. This is used to work around browser level caching of the captcha image. |

**Response**

When successful, the endpoint returns the captcha image as PNG in case captcha is required.

Additionally, the response will also include the following headers when applicable:

| **Name** | **Type** | **Present** | **Values** | **Description** |
| `X-Captcha-Id` | `String` | \* |  | The captcha id to be sent when calling cookie login. |

- [Mailbox API – Authentication and Authorization](https://www.axigen.com/documentation/mailbox-api-authentication-and-authorization-p773357577)
- [Mailbox API – Schemas](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234)
- [Mailbox API – Versioning](https://www.axigen.com/documentation/mailbox-api-versioning-p723157025)
- [Mailbox API – Account](https://www.axigen.com/documentation/mailbox-api-account-p666828978)
- [Mailbox API – Account Settings](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397)
- [Mailbox API – Account Security](https://www.axigen.com/documentation/mailbox-api-account-security-p1602977833)
- [Mailbox API – Account Filters](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337)
- [Mailbox API – Folders](https://www.axigen.com/documentation/mailbox-api-folders-p666829029)
- [Mailbox API – Mails](https://www.axigen.com/documentation/mailbox-api-mails-p666992807)
- [Mailbox API – Mails Create and Send](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827)
- [Mailbox API – Mails Search](https://www.axigen.com/documentation/mailbox-api-mails-search-p666992858)
- [Mailbox API – Mails Counters](https://www.axigen.com/documentation/mailbox-api-mails-counters-p688750780)
- [Mailbox API – BIMI](https://www.axigen.com/documentation/mailbox-api-bimi-p1444970498)
- [Mailbox API – Conversations](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637)
- [Mailbox API – Labels](https://www.axigen.com/documentation/mailbox-api-labels-p666960064)
- [Mailbox API – Contacts](https://www.axigen.com/documentation/mailbox-api-contacts-p666960100)
- [Mailbox API – Batch Operations](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306)
- [Mailbox API – Undo](https://www.axigen.com/documentation/mailbox-api-undo-p688783382)
- [Mailbox API – Error Handling](https://www.axigen.com/documentation/mailbox-api-error-handling-p683540544)

[Mailbox API – Schemas](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-authentication-and-authorization-p773357577#)