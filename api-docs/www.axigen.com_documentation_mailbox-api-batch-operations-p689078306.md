---
url: "https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306"
title: "Mailbox API – Batch Operations | Axigen Documentation"
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

- [Mail Batch Operations](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-MailBatchOperations)
  - [Copy](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-Copy)
  - [Move](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-Move)
  - [Delete](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-Delete)
  - [Update](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-Update)
  - [Add Label](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-AddLabel)
  - [Remove Label](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-RemoveLabel)
- [Conversations Batch Operations](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-ConversationsBatchOperations)
  - [Move](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-Move.1)
  - [Delete](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-Delete.1)
  - [Update](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-Update.1)
  - [Add Label](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-AddLabel.1)
  - [Remove Label](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#MailboxAPI%E2%80%93BatchOperations-RemoveLabel.1)

## Mail Batch Operations

### Copy

|     |
| --- |
| `POST /api/v1/batch/mails/copy` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `destinationFolderId` | `String` | \* |  | The destination folder ID |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The mail IDs to be copied |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number               ` `// number of IDs including the starting ID`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

**Response**

Depending on the size of the batch, the batch operation will be executed either synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

### Move

|     |
| --- |
| `POST /api/v1/batch/mails/move` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `destinationFolderId` | `String` | \* |  | The destination folder ID |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The mail IDs to be moved |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number               ` `// number of IDs including the starting ID`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

### Delete

|     |
| --- |
| `POST /api/v1/batch/mails/delete` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The mail IDs to be deleted |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number               ` `// number of IDs including the starting ID`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

### Update

|     |
| --- |
| `POST /api/v1/batch/mails/update` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `isUnread` | `Boolean` | \* |  | The unread / read value |
| `isFlagged` | `Boolean` | \* |  | The flagged / not flagged value |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The mail IDs to be updated |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number               ` `// number of IDs including the starting ID`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

One of `isUnread` or `isFlagged` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

### Add Label

|     |
| --- |
| `POST /api/v1/batch/mails/labels/add` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `labelId` | `String` | \* |  | The label ID |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The mail IDs to which the label should be added |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number               ` `// number of IDs including the starting ID`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

### Remove Label

|     |
| --- |
| `POST /api/v1/batch/mails/labels/remove` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `labelId` | `String` | \* |  | The label ID |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The mail IDs from which the label should be removed |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number               ` `// number of IDs including the starting ID`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

## Conversations Batch Operations

### Move

|     |
| --- |
| `POST /api/v1/batch/conversations/move` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `destinationFolderId` | `String` | \* |  | The destination folder ID |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The conversation IDs to be moved |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number,              ` `// number of IDs including the starting ID,`<br>`        ``sourceFolderId: String      ` `// the source folder ID where the starting ID resides`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

### Delete

|     |
| --- |
| `POST /api/v1/batch/conversations/delete` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The conversation IDs to be deleted |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number,              ` `// number of IDs including the starting ID`<br>`        ``sourceFolderId: String      ` `// the source folder ID where the starting ID resides`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

### Update

|     |
| --- |
| `POST /api/v1/batch/conversations/update` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `isUnread` | `Boolean` | \* |  | The unread / read value |
| `isFlagged` | `Boolean` | \* |  | The flagged / not flagged value |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The conversation IDs to be updated |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number,              ` `// number of IDs including the starting ID`<br>`        ``sourceFolderId: String      ` `// the source folder ID where the starting ID resides`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

One of `isUnread` or `isFlagged` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

### Add Label

|     |
| --- |
| `POST /api/v1/batch/conversations/labels/add` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `labelId` | `String` | \* |  | The label ID |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The conversation IDs to which the label should be added |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number,              ` `// number of IDs including the starting ID`<br>`        ``sourceFolderId: String      ` `// the source folder ID where the starting ID resides`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

### Remove Label

|     |
| --- |
| `POST /api/v1/batch/conversations/labels/remove` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `labelId` | `String` | \* |  | The label ID |
| `ids` | `Array` | \* | |     |
| --- |
| `ids: [`<br>`    ``"ODVfMTIxXzE"` `,`<br>`    ``"ODVfMTIxXzT"`<br>`]` | | The conversation IDs from which the label should be removed |
| `ranges` | `Array` | \* | |     |
| --- |
| `ranges: [`<br>`    ``{`<br>`        ``start: String,              ` `// starting ID`<br>`        ``limit: Number,              ` `// number of IDs including the starting ID`<br>`        ``sourceFolderId: String      ` `// the source folder ID where the starting ID resides`<br>`    ``},`<br>`    ``...`<br>`]` | | The list for ranges to be copied |
| `sortInfo` | `Object` | \*<br>(when using ranges) | |     |
| --- |
| `sortInfo: {`<br>`    ``field: String,          ` `// The current sorting field`<br>`                            ``// Possible values: [`<br>`                            ``//     "subject", "from", "to",`<br>`                            ``//     "date",`<br>`                            ``//     "size",`<br>`                            ``//     "isUnread", "isFlagged", "importance", "hasAttachments",`<br>`                            ``//     "folderName"`<br>`                            ``// ]`<br>`    ``direction: String,      ` `// The current sorting direction`<br>`                            ``// Possible values: ["ASC", "DESC"]`<br>`}` | | Sorting information to be used for range calculation |

One of `ids` or `ranges` is required.

**Response**

Depending on the size of the batch, the batch operation will be either executed synchronously or asynchronously.

**Synchronous Response**

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number,               ` `//  Floating number between 0-100 expressing the progress in percentages        `<br>`}` |

**Asynchronous Response**

In case the batch is processed asynchronously, the end point will reply with HTTP status code: 201 Created.

|     |
| --- |
| `{`<br>`    ``batchOperationDetails: {        ` `// List of original IDs for which the batch operation failed`<br>`        ``failedItems: [              `<br>`            ``String,          `<br>`            ``...`<br>`        ``]`<br>`    ``},`<br>`    ``jobKey: String,                 ` `// The job key which can be used to return the status of the batch operation`<br>`    ``status: String,                 ` `// The current state of batch operation`<br>`                                    ``// Possible values: [ `<br>`                                    ``//   "inProgress",`<br>`                                    ``//   "completed"`<br>`                                    ``// ]`<br>`    ``progress: Number                ` `//  Floating number between 0-100 expressing the progress in percentages`<br>`}` |

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

[Mailbox API – Contacts](https://www.axigen.com/documentation/mailbox-api-contacts-p666960100) [Mailbox API – Undo](https://www.axigen.com/documentation/mailbox-api-undo-p688783382)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-batch-operations-p689078306#)