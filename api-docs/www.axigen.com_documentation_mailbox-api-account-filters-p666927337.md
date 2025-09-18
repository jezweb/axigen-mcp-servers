---
url: "https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337"
title: "Mailbox API – Account Filters | Axigen Documentation"
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

- [Get](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Get)
- [Update](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Update)
- [Whitelist](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Whitelist)
  - [List](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-List)
  - [Create](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Create)
  - [Update](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Update.1)
  - [Delete](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Delete)
- [Blacklist](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Blacklist)
  - [List](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-List.1)
  - [Create](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Create.1)
  - [Update](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Update.2)
  - [Delete](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Delete.1)
- [Filters - on/off](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-Filters-on/off)
  - [List Presets](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-ListPresets)
  - [Get Preset](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-GetPreset)
  - [Choose Preset](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-ChoosePreset)
  - [List Filters](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-ListFilters)
  - [Update Filter](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#MailboxAPI%E2%80%93AccountFilters-UpdateFilter)

## Get

|     |
| --- |
| `GET /api/v1/account/avas` |

**Response**

|     |
| --- |
| `{`<br>`    ``whitelistIncludeAddressBook: Boolean   ` `// Whether the addresses in the address book are automatically`<br>`                                           ``// included in the Whitelist`<br>`    ``blacklistExcludeAddressBook: Boolean   ` `// Whether the addresses not in the address book are automatically`<br>`                                           ``// included in the Blacklist           `<br>`}` |

## Update

|     |
| --- |
| `PATCH /api/v1/account/avas` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `whitelistIncludeAddressBook` | `Boolean` |  |  | Whether the addresses in the address book are automatically included in the Whitelist<br>**Default value:** true |
| `blacklistExcludeAddressBook` | `Boolean` |  |  | Whether the addresses not in the address book are automatically excluded from the Blacklist<br>**Default value:** true |

**Response**

|     |
| --- |
| `{`<br>`    ``whitelistIncludeAddressBook: Boolean   ` `// Whether the addresses in the address book are automatically`<br>`                                           ``// included in the Whitelist`<br>`    ``blacklistExcludeAddressBook: Boolean   ` `// Whether the addresses not in the address book are automatically`<br>`                                           ``// excluded from the Blacklist           `<br>`}` |

## Whitelist

### List

|     |
| --- |
| `GET /api/v1/account/avas/whitelist` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `start` | `Number` |  |  | The starting position<br>**Default value:** 0 |
| `limit` | `Number` |  |  | The maximum number of retrieved items<br>**Default value:** the WebMailData pageSize |

**Response**

|     |
| --- |
| `{`<br>`    ``totalItems: Number,           ` `// The total number of items in whitelist`<br>`    ``items: [`<br>`        ``{`<br>`            ``id: String,               ` `// The whitelisted email address ID`<br>`            ``emailAddress: String,     ` `// The whitelisted email address        `<br>`        ``},`<br>`        ``...`<br>`    ``]`<br>`}` |

### Create

|     |
| --- |
| `POST /api/v1/account/avas/whitelist` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `emailAddress` | `String` | \* |  | The email address to whitelist |

**Response**

|     |
| --- |
| `{`<br>`    ``id: String,               ` `// The whitelisted email address ID`<br>`    ``emailAddress: String,     ` `// The whitelisted email address        `<br>`}` |

### Update

|     |
| --- |
| `PUT /api/v1/account/avas/whitelist/{id}` |

**URL parameters**

| **Name** | **Type** | **Description** |
| `id` | `String` | The whitelisted email address ID |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `emailAddress` | `String` | \* |  | The new email address |

**Response**

|     |
| --- |
| `{`<br>`    ``id: String,               ` `// The whitelisted email address ID`<br>`    ``emailAddress: String,     ` `// The whitelisted email address        `<br>`}` |

### Delete

|     |
| --- |
| `DELETE /api/v1/account/avas/whitelist/{id}` |

**URL parameters**

| **Name** | **Type** | **Description** |
| `id` | `String` | The whitelisted email address ID |

**Response**

If successful, the response will be empty.

## Blacklist

### List

|     |
| --- |
| `GET /api/v1/account/avas/blacklist` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `start` | `Number` |  |  | The starting position<br>**Default value:** 0 |
| `limit` | `Number` |  |  | The maximum number of retrieved items<br>**Default value:** the WebMailData pageSize |

**Response**

|     |
| --- |
| `{`<br>`    ``totalItems: Number,           ` `// The total number of items in blacklist`<br>`    ``items: [`<br>`        ``{`<br>`            ``id: String,               ` `// The blacklisted email address ID`<br>`            ``emailAddress: String,     ` `// The blacklisted email address        `<br>`        ``},`<br>`        ``...`<br>`    ``]`<br>`}` |

### Create

|     |
| --- |
| `POST /api/v1/account/avas/blacklist` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `emailAddress` | `String` | \* |  | The email address to blacklist |

**Response**

|     |
| --- |
| `{`<br>`    ``id: String,               ` `// The blacklisted email address ID`<br>`    ``emailAddress: String,     ` `// The blacklisted email address        `<br>`}` |

### Update

|     |
| --- |
| `PUT /api/v1/account/avas/blacklist/{id}` |

**URL parameters**

| **Name** | **Type** | **Description** |
| `id` | `String` | The blacklisted email address ID |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `emailAddress` | `String` | \* |  | The new email address |

**Response**

|     |
| --- |
| `{`<br>`    ``id: String,               ` `// The blacklisted email address ID`<br>`    ``emailAddress: String,     ` `// The blacklisted email address        `<br>`}` |

### Delete

|     |
| --- |
| `DELETE /api/v1/account/avas/blacklist/{id}` |

**URL parameters**

| **Name** | **Type** | **Description** |
| `id` | `String` | The blacklisted email address ID |

**Response**

If successful, the response will be empty.

## Filters - on/off

### List Presets

|     |
| --- |
| `GET /api/v1/account/avas/filters/onoff/presets` |

**Response**

|     |
| --- |
| `{`<br>`    ``items: [`<br>`        ``name: String,           ` `// Name of the filter`<br>`        ``...`<br>`    ``]`<br>`}` |

### Get Preset

|     |
| --- |
| `GET /api/v1/account/avas/filters/onoff/preset` |

**Response**

|     |
| --- |
| `{`<br>`    ``preset: String    ` `// The current state of the filter preset`<br>`                      ``// Possible values: [ `<br>`                      ``//   "off",`<br>`                      ``//   "strong",`<br>`                      ``//   "weak",`<br>`                      ``//   "custom"    // when the current state of the filters does not match any of the other presets`<br>`                      ``// ]`<br>`}` |

### Choose Preset

|     |
| --- |
| `POST /api/v1/account/avas/filters/onoff/preset` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Description** |
| `preset` | `String` | true | Possible values are: “off”, “strong”, “weak”. |

**Response**

If successful, the response will be empty.

### List Filters

|     |
| --- |
| `GET /api/v1/account/avas/filters/onoff` |

**Response**

|     |
| --- |
| `{`<br>`    ``items: [`<br>`        ``{`<br>`            ``id: Number,                 ` `// Filter identification number`<br>`            ``name: String,               ` `// Name of the filter`<br>`            ``enabled: Boolean    ` `// State of the filter`<br>`        ``},`<br>`        ``...`<br>`    ``]`<br>`}` |

### Update Filter

|     |
| --- |
| `PATCH /api/v1/account/avas/filters/onoff/{id}` |

**URL parameters**

| **Name** | **Type** | **Required** | **Description** |
| `id` | `Number` | true | Filter id to be updated |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Description** |
| `enabled` | `Boolean` | true | Possible values are: “true”, “false”. |

**Response**

If successful, the response will be empty.

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

[Mailbox API – Account Security](https://www.axigen.com/documentation/mailbox-api-account-security-p1602977833) [Mailbox API – Folders](https://www.axigen.com/documentation/mailbox-api-folders-p666829029)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337#)