---
url: "https://www.axigen.com/documentation/mailbox-api-contacts-p666960100"
title: "Mailbox API – Contacts | Axigen Documentation"
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

The Mailbox API is available starting with Axigen X4 (10.4).

- [List](https://www.axigen.com/documentation/mailbox-api-contacts-p666960100#MailboxAPI%E2%80%93Contacts-List)
- [Autocomplete](https://www.axigen.com/documentation/mailbox-api-contacts-p666960100#MailboxAPI%E2%80%93Contacts-Autocomplete)
- [Avatars](https://www.axigen.com/documentation/mailbox-api-contacts-p666960100#MailboxAPI%E2%80%93Contacts-Avatars)
  - [List](https://www.axigen.com/documentation/mailbox-api-contacts-p666960100#MailboxAPI%E2%80%93Contacts-List.1)
- [Contacts Delta](https://www.axigen.com/documentation/mailbox-api-contacts-p666960100#MailboxAPI%E2%80%93Contacts-ContactsDelta)
  - [List Delta](https://www.axigen.com/documentation/mailbox-api-contacts-p666960100#MailboxAPI%E2%80%93Contacts-ListDelta)

## List

|     |
| --- |
| `GET /api/v1/contacts/` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `folderId` | `String` |  |  | The folder ID<br>When missing, all contacts from all contact folders are returned. |
| `sort` | `String` |  | "name", “email” | The sorting field<br>**Default value:** last provided value or "name" if not yet set |
| `dir` | `String` |  | "ASC", "DESC" | The sorting direction<br>**Default value:** last provided value or "DESC" if not yet set |
| `start` | `Number` |  |  | The starting position<br>**Default value:** 0 |
| `limit` | `Number` |  |  | The maximum number of retrieved items<br>**Default value:** the WebMailData pageSize |
| `syncTokenOnly` | `Boolean` |  |  | When true, the endpoint should only return the syncToken without the list of contacts.<br>**Default value:** false |

**Response**

|     |
| --- |
| `{`<br>`    ``syncToken: String,         ` `// A generated token that can be used for synchronization purposes to check if any`<br>`                               ``// changes occurred since the last interogation`<br>`                               ``// Note: when no folderId is provided, the syncToken will be a concatenation of sync tokens`<br>`                               ``// in all contact folders so it shall have variable size`<br>`    ``totalItems: Number,        ` `// The total number of items in the provided folder`<br>`    ``sortInfo: {`<br>`        ``field: String,         ` `// The current sorting field`<br>`                               ``// Possible values: [`<br>`                               ``//     "name", "email"`<br>`                               ``// ]`<br>`        ``direction: String      ` `// The current sorting direction`<br>`                               ``// Possible values: ["ASC", "DESC"]`<br>`    ``},`<br>`    ``items: [`<br>`        ``ContactInstance,       ` `// Instance of contact`<br>`        ``...`<br>`    ``]`<br>`}` |

## Autocomplete

|     |
| --- |
| `GET /api/v1/contacts/autocomplete` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `query` | `String` | \* |  | The search query string |
| `limit` | `Number` |  | 1-50 | Number of results.<br>Default value: 10. |

**Response**

|     |
| --- |
| `{`<br>`    ``totalItems: Number,        ` `// The total number of items returned`<br>`    ``items: [`<br>`        ``ContactInstance,       ` `// Instance of contact`<br>`        ``...`<br>`    ``]`<br>`}` |

## Avatars

Returns avatar images for contacts that match query parameters.

It can be called with one of the following query parameters: `contactEmailAddresses` (for avatar listing based on email addresses) or `contactsIds` (for avatar listing based on contact IDs).

### List

|     |
| --- |
| `POST /api/v1/contacts/avatars/search` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `contactEmailAddresses` | `Array` | \* | Example:

|     |
| --- |
| `contactEmailAddresses: [`<br>`    ``"john.doe@example.com"` `,`<br>`    ``"sarah.jones@example.com"`<br>`]` | | The contact email addresses.<br>The avatar is retrieved from the first contact matching the query parameter (there may be multiple contacts with that email address).<br>Matching is done by searching the provided contact email address as case insensitive substring in the main email address of the contacts (there is no match against “home”, “work”, or other secondary email address types). |
| `contactIds` | `Array` | \* | Example:

|     |
| --- |
| `contactIds: [`<br>`    ``"MTY3Nzk4MDlfNjcxMTQ1MzdfMzAzNwo0"` `,`<br>`    ``"MTY3Nzk4MDlfNjcxMTQ1MzdfMzAzOAo0"`<br>`]` | | The contact IDs.<br>See the `id` field of the [Contact instance](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#ContactInstance) schema definition. |

One of `contactEmailAddresses` or `contactIds` is required.

**Response**

|     |
| --- |
| `{`<br>`    ``items: [`<br>`        ``{`<br>`            ``id: String,           ` `// The contact ID, if found`<br>`            ``email: String,        ` `// The contact email address`<br>`            ``data: String          ` `// The base64 encoded avatar image, if found`<br>`        ``}                 `<br>`        ``...`<br>`    ``]`<br>`}` |

## Contacts Delta

### List Delta

This endpoint lists the modifications occurred in the contacts folder since a previous point defined by a sync token.

|     |
| --- |
| `GET /api/v1/contacts/delta` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `folderId` | `String` |  |  | The folder ID<br>When missing, all contacts from all contact folders are returned. |
| syncToken | String |  |  | The synchronization token returned by the previous listing; if missing then an initial round of listing is started (all contacts are reported as new items) |
| `limit` | `Number` |  |  | The maximum number of retrieved items<br>**Default value:** the WebMailData pageSize |

**Response**

|     |
| --- |
| `{`<br>`    ``syncToken: String,         ` `// A generated token that can be used for synchronization purposes to check if any`<br>`                               ``// changes occurred since the last interogation`<br>`                               ``// Note: when no folderId is provided, the syncToken will be a concatenation of sync tokens`<br>`                               ``// in all contact folders so it shall have variable size`<br>`    ``totalItems: Number,        ` `// The total number of items in the provided folder`<br>`    ``sortInfo: {`<br>`        ``field: String,         ` `// The current sorting field`<br>`                               ``// Possible values: [`<br>`                               ``//     "name", "email"`<br>`                               ``// ]`<br>`        ``direction: String      ` `// The current sorting direction`<br>`                               ``// Possible values: ["ASC", "DESC"]`<br>`    ``},`<br>`    ``moreAvailable: Boolean,                ` `// Whether there are more available items to be synchronized`<br>`    ``newItems: [`<br>`        ``ContactInstance,               ` `// Instance of contact`<br>`        ``...`<br>`    ``],`<br>`    ``replacedItems: [`<br>`        ``ContactInstance,               ` `// Instance of contact`<br>`        ``...`<br>`    ``],`<br>`    ``removedItems: [`<br>`        ``{`<br>`            ``id: String,                              ` `// The mail ID`<br>`            ``folderId: String,                        ` `// The associated folder ID`<br>`        ``},`<br>`        ``...`<br>`    ``]`<br>`}` |

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

[Mailbox API – Labels](https://www.axigen.com/documentation/mailbox-api-labels-p666960064) [Mailbox API – Batch Operations](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-contacts-p666960100#)