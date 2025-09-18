---
url: "https://www.axigen.com/documentation/mailbox-api-conversations-p688750637"
title: "Mailbox API – Conversations | Axigen Documentation"
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

- [List](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-List)
- [Get](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-Get)
- [Get conversation from mail](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-Getconversationfrommail)
- [Update](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-Update)
- [Move](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-Move)
- [Delete](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-Delete)
- [Add Label](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-AddLabel)
- [Remove Label](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-RemoveLabel)
- [Spam Marker](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-SpamMarker)
  - [Mark as Spam](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#MailboxAPI%E2%80%93Conversations-MarkasSpam)

## List

This endpoint returns a list of conversation instances, starting from a specific (requested) folder.

Conversations are cross-folder, covering all folders except for Spam and Trash (and their children).

|     |
| --- |
| `GET /api/v1/conversations` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `folderId` | `String` | \* |  | The folder ID |
| `sort` | `String` |  | "subject", "from", "to", "date", "isUnread", "isFlagged", "importance", "hasAttachments" | The sorting field<br>**Default value:** last provided value or "date" if not yet set |
| `dir` | `String` |  | "ASC", "DESC" | The sorting direction<br>**Default value:** last provided value or "DESC" if not yet set |
| `start` | `Number` |  |  | The starting position<br>**Default value:** 0 |
| `limit` | `Number` |  |  | The maximum number of retrieved items<br>**Default value:** the WebMailData pageSize |
| `activeConversationId` | `String` |  |  | The active conversation ID is used to generate the activeRowIndex property.<br>**Note:** this is used to compute server-side the absolute index in the list for the provided conversation item (used mainly for clients to restore selections etc.) |
| `syncTokenOnly` | `Boolean` |  |  | When true, the endpoint should only return the syncToken without the conversation list.<br>**Default value:** false |

**Response**

|     |
| --- |
| `{`<br>`    ``syncToken: String,         ` `// A generated token that can be used for synchronization purposes to check if any`<br>`                               ``// changes occurred since the last interogation`<br>`    ``totalItems: Number,        ` `// The total number of items in the provided folder`<br>`    ``sortInfo: {`<br>`        ``field: String,         ` `// The current sorting field`<br>`                               ``// Possible values: [`<br>`                               ``//     "subject", "from", "to",`<br>`                               ``//     "date",`<br>`                               ``//     "isUnread", "isFlagged", "importance", "hasAttachments"`<br>`                               ``// ]`<br>`        ``direction: String,     ` `// The current sorting direction`<br>`                               ``// Possible values: ["ASC", "DESC"]`<br>`        ``activeRowIndex: Number ` `// The row index associated with the provided activeConversationId`<br>`    ``},`<br>`    ``items: [`<br>`        ``ConversationInstance,   ` `// Instance of conversation`<br>`        ``...`<br>`    ``]`<br>`}` |

## Get

|     |
| --- |
| `GET /api/v1/conversations/{conversationId}` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `conversationId` | `String` | \* |  | The conversation ID |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `start` | `Number` |  |  | The starting position<br>**Default value:** 0 |
| `limit` | `Number` |  |  | The maximum number of retrieved items<br>**Default value:** the WebMailData pageSize |
| `mailIds` | `Array (mailId)` |  |  | The array of mailIds to be retrieved from the specified conversation.<br>![(warning)](<Base64-Image-Removed>) If sent and not empty, overrides `start`, `limit` |
| ![(question)](<Base64-Image-Removed>)`syncTokenOnly` | `Boolean` |  |  | When true, the endpoint should only return the syncToken without the mail list.<br>**Default value:** false |

**Response**

|     |
| --- |
| `{`<br>`    ``syncToken: String,         ` `// A generated token that can be used for synchronization purposes to check if any`<br>`                               ``// changes occurred since the last interogation`<br>`    ``totalItems: Number,        ` `// The total number of items in the provided conversation`<br>`    ``items: [`<br>`        ``MailInstance,          ` `// Instance of mail`<br>`        ``...`<br>`    ``]`<br>`}` |

## Get conversation from mail

|     |
| --- |
| `GET /api/v1/mails/{mailId}/conversation` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `mailId` | `String` | \* |  | The mail ID |

**Response**

If successful, the response will contain an [instance of conversation](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#ConversationInstance).

## Update

Updating `isUnread` affects all members of the conversation that are not in the Sent or Drafts folders, while updating `isFlagged` affects all members of the conversation.

Conversations are cross-folder, covering all folders except for Spam and Trash (and their children).

|     |
| --- |
| `PATCH /api/v1/conversations/{conversationId}` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `conversationId` | `String` | \* |  | The conversation ID |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `isUnread` | `Boolean` |  |  | The unread / read value |
| `isFlagged` | `Boolean` |  |  | The flagged / not flagged value |

**Response**

If successful, the response will contain an [instance of conversation](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#ConversationInstance).

## Move

This operation affects all members of the conversation that are not in the Sent or Drafts folders.

Conversations are cross-folder, covering all folders except for Spam and Trash (and their children).

|     |
| --- |
| `POST /api/v1/conversations/{conversationId}/move` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `conversationId` | `String` | \* |  | The conversation ID |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `destinationFolderId` | `String` | \* |  | The destination folder ID |

**Response**

If successful, the response will contain an [instance of conversation](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#ConversationInstance).

Conversations can be moved to Spam. In this case, all the mails from the ConversationInstance are moved to Spam and the Conversation data is deleted.

This will result in a 200 OK response with an empty body, signaling that the Conversation doesn’t exist anymore.

## Delete

|     |
| --- |
| `DELETE /api/v1/conversations/{conversationId}` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `conversationId` | `String` | \* |  | The conversation ID |

**Response**

If successful, the response will be empty.

## Add Label

|     |
| --- |
| `POST /api/v1/conversations/{conversationId}/labels` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `conversationId` | `String` | \* |  | The conversation ID |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `labelId` | `String` | \* |  | The label ID |

**Response**

If successful, the response will be empty.

## Remove Label

|     |
| --- |
| `DELETE /api/v1/conversations/{conversationId}/labels/{labelId}` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `conversationId` | `String` | \* |  | The conversation ID |
| `labelId` | `String` | \* |  | The label ID |

**Response**

If successful, the response will be empty.

## Spam Marker

This endpoint is available starting with Axigen 10.5.27.

### Mark as Spam

This operation affects all members of the conversation that are not in the Sent or Drafts folders.

Conversations are cross-folder, covering all folders except for Spam and Trash (and their children).

|     |
| --- |
| `POST /api/v1/conversations/{conversationId}/spam` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `conversationId` | `String` | \* |  | The conversation ID |

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

[Mailbox API – BIMI](https://www.axigen.com/documentation/mailbox-api-bimi-p1444970498) [Mailbox API – Labels](https://www.axigen.com/documentation/mailbox-api-labels-p666960064)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-conversations-p688750637#)