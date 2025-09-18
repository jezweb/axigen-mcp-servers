---
url: "https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827"
title: "Mailbox API – Mails Create and Send | Axigen Documentation"
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

- [Create](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-Create)
- [Replace Draft](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-ReplaceDraft)
- [Send UPDATED](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-SendUpdatedGreen)
  - [Send Mail](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-SendMail)
  - [Send Draft](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-SendDraft)
  - [Undo Send](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-UndoSend)
  - [Scheduled Send](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-ScheduledSend)
  - [Scheduled Send Draft](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-ScheduledSendDraft)
  - [Scheduled Cancel](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-ScheduledCancel)
- [Temporary Attachments](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-TemporaryAttachments)
  - [Create](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-Create.1)
  - [Get](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-Get)
  - [Delete](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-Delete)
  - [Store in Queue](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPI%E2%80%93MailsCreateandSend-StoreinQueue)

## Create

This endpoint allows you to create a new draft email or insert an email into an existing folder.

If `folderId` is specified, the email will be appended to the specified folder, otherwise it will be created as a draft, in the Drafts folder.

|     |
| --- |
| `POST /api/v1/mails` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `folderId` | `String` |  |  | The default value is the ID of the “Drafts” folder |
| `from` | `String` |  |  | The desired value of the `from` header |
| `to` | `String` |  |  | The desired value of the `to` header |
| `cc` | `String` |  |  | The desired value of the `cc` header |
| `bcc` | `String` |  |  | The desired value of the `bcc` header |
| `replyTo` | `String` |  |  | The desired value of the `Reply-To` header |
| `refwType` | `String` |  | "re", "fw" | Whether the mail is a reply or a forward.<br>The mail cannot be both a reply and a forward (“refw” is an invalid value) |
| `refwMailId` | `String` | Required if `refw` is set |  | This field is dependent on `refwType`:<br>- `refwType` missing: `refwMailId` should not be sent<br>  <br>- `refwType` set to "re": `refwMailId` required, the ID of the mail being replied to. This ID is used to automatically generate the `References` and `In-Reply-To` headers for replies.<br>  <br>- `refwType` set to "fw": `refwMailId` required, the ID of the mail being forwarded |
| `subject` | `String` |  |  | The desired value of the `Subject` header |
| `isUnread` | `Boolean` |  |  | The unread / read value |
| `isFlagged` | `Boolean` |  |  | The flagged / not flagged value |
| `importance` | `String` |  |  | "normal", "low", "high"<br>The desired importance. If missing, the importance will default to "normal". |
| `bodyText` | `String` |  |  | The UTF-8 text body, if existing |
| `bodyHtml` | `String` |  |  | The UTF-8 HTML body, if existing |
| `temporaryAttachments` | `Array` |  | JSON object list in the following format:

|     |
| --- |
| `temporaryAttachments: [`<br>`    ``{`<br>`        ``id: Number,                 ` `// The temporary attachment ID`<br>`        ``contentId: String,          ` `// The content ID (cid) of the attachment, if found`<br>`        ``isInline: Boolean           ` `// True if you have referred it in the HTML body by cid`<br>`    ``}`<br>`    ``...`<br>`]` | | The attachments in the attachments queue. |

**Response**

If successful, the response will contain an [instance of mail](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailInstance).

## Replace Draft

This endpoint allows you to replace an existing draft email.

|     |
| --- |
| `PUT /api/v1/drafts/{mailId}` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `mailId` | `String` | \* |  | The draft mail ID |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `from` | `String` |  |  | The desired value of the `from` header |
| `to` | `String` |  |  | The desired value of the `to` header |
| `cc` | `String` |  |  | The desired value of the `cc` header |
| `bcc` | `String` |  |  | The desired value of the `bcc` header |
| `replyTo` | `String` |  |  | The desired value of the `Reply-To` header |
| `refwType` | `String` |  | "re", "fw" | Whether the mail is a reply or a forward.<br>The mail cannot be both a reply and a forward (“refw” is an invalid value) |
| `refwMailId` | `String` | Required if `refw` is set |  | This field is dependent on `refw`:<br>- `refwType` missing: `refwMailId` should not be sent<br>  <br>- `refwType` set to "re": `refwMailId` required, the ID of the mail being replied to. This ID is used to automatically generate the `References` and `In-Reply-To` headers for replies.<br>  <br>- `refwType` set to "fw": `refwMailId` required, the ID of the mail being forwarded |
| `subject` | `String` |  |  | The desired value of the `Subject` header |
| `isUnread` | `Boolean` |  |  | The unread / read value |
| `isFlagged` | `Boolean` |  |  | The flagged / not flagged value |
| `importance` | `String` |  |  | "normal", "low", "high"<br>The desired importance. If missing, the importance will default to "normal". |
| `bodyText` | `String` |  |  | The UTF-8 text body, if existing |
| `bodyHtml` | `String` |  |  | The UTF-8 HTML body, if existing |
| `temporaryAttachments` | `Array` |  | JSON object list in the following format:

|     |
| --- |
| `temporaryAttachments: [`<br>`    ``{`<br>`        ``id: Number,                 ` `// The temporary attachment ID`<br>`        ``contentId: String,          ` `// The content ID (cid) of the attachment, if found`<br>`        ``isInline: Boolean           ` `// True if you have referred it in the HTML body by cid`<br>`    ``}`<br>`    ``...`<br>`]` | | The attachments in the attachments queue. |

**Response**

If successful, the response will contain an [instance of mail](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailInstance).

## Send UPDATED

### Send Mail

This endpoint allows you to send an email which is not yet saved to Drafts.

It will also save a copy to Sent according to the user preference.

|     |
| --- |
| `POST /api/v1/mails/send` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `from` | `String` |  |  | The desired value of the `from` header |
| `to` | `String` |  |  | The desired value of the `to` header |
| `cc` | `String` |  |  | The desired value of the `cc` header |
| `bcc` | `String` |  |  | The desired value of the `bcc` header |
| `replyTo` | `String` |  |  | The desired value of the `Reply-To` header |
| `refwType` | `String` |  | "re", "fw" | Whether the mail is a reply or a forward.<br>The mail cannot be both a reply and a forward (“refw” is an invalid value) |
| `refwMailId` | `String` | Required if `refw` is set |  | This field is dependent on `refwType`:<br>- `refwType` missing: `refwMailId` should not be sent<br>  <br>- `refwType` set to "re": `refwMailId` required, the ID of the mail being replied to. This ID is used to automatically generate the `References` and `In-Reply-To` headers for replies.<br>  <br>- `refwType` set to "fw": `refwMailId` required, the ID of the mail being forwarded |
| `subject` | `String` |  |  | The desired value of the `Subject` header |
| `importance` | `String` |  |  | "normal", "low", "high"<br>The desired importance. If missing, the importance will default to "normal". |
| `requestReadReceipt` | `Boolean` |  |  | Whether to request a read receipt |
| `requestDeliveryReceipt` | `Boolean` |  |  | Whether to request a delivery receipt |
| `bodyText` | `String` |  |  | The UTF-8 text body, if existing |
| `bodyHtml` | `String` |  |  | The UTF-8 HTML body, if existing |
| `temporaryAttachments` | `Array` |  | JSON object list in the following format:

|     |
| --- |
| `temporaryAttachments: [`<br>`    ``{`<br>`        ``id: Number,                 ` `// The temporary attachment ID`<br>`        ``contentId: String,          ` `// The content ID (cid) of the attachment, if found`<br>`        ``isInline: Boolean           ` `// True if you have referred it in the HTML body by cid`<br>`    ``}`<br>`    ``...`<br>`]` | | The attachments in the attachments queue. |

**Response**

If successful, the response will be empty.

Starting with Axigen X5 (10.5), as part of the planned support for the Undo Send functionality, if successful, the server response will be as documented below.

|     |
| --- |
| `{`<br>`    ``mailId: String,          ` `// The ID of the mail saved to the Sent folder (only present if the mail was actually saved to Sent)`<br>`    ``processingId: Number     ` `// The ID of the mail in the processing queue, on its way to delivery`<br>`}` |

### Send Draft

This endpoint allows you to send an existing draft email.

If this is preceded by opening the draft for editing, on send you should first save it to drafts and then call this endpoint with the draft mail ID.

This endpoint will also delete the draft upon sending and will save a copy to Sent according to the user preference.

|     |
| --- |
| `POST /api/v1/drafts/{mailId}/send` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `mailId` | `String` | \* |  | The draft mail ID |

**Response**

If successful, the response will be empty.

Starting with Axigen X5 (10.5), as part of the planned support for the Undo Send functionality, if successful, the server response will be as documented below.

|     |
| --- |
| `{`<br>`    ``mailId: String,          ` `// The ID of the mail saved to the Sent folder (only present if the mail was actually saved to Sent)`<br>`    ``processingId: Number     ` `// The ID of the mail in the processing queue, on its way to delivery`<br>`}` |

### Undo Send

This endpoint allows you to stop the server from delivering a mail in the processing queue. Can be successfully used after a maximum of 10 seconds after the mail was sent.

If the mail is a reply/forward, after undo, the source mail will lose their respective Replied/Answered flag (This happens even when the source mail had the flag set before the reply was sent!).

If `mailId` is specified, the corresponding email will be moved to the Drafts folder. It is intended to be used with the response from the [Send](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPIMailsCreateandSend-Send) and [Send Draft](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#MailboxAPIMailsCreateandSend-SendDraft) endpoints.

If `mailId` is not specified or something goes wrong when moving, a draft will be built based on the mail removed from the processing queue. In this case, the original BCC information will not be available anymore.

|     |
| --- |
| `POST /api/v1/mails/send/undo` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `processingId` | `Number` | \* |  | Id of the mail in the processing queue for which to undo send |
| `mailId` | `String` |  |  | Id of the mail to move to drafts |

**Response**

|     |
| --- |
| `{`<br>`    ``mailId: String    ` `// The ID of the mail in Drafts (either by move or created from the one removed from the processing queue)`<br>`}` |

If the draft creation fails, the endpoint execution will be successful but the `mailId` in the response will not be returned.

### Scheduled Send

This endpoint allows you to schedule delivery of an email which is not yet saved to Drafts, at a desired timestamp in the future

It will also save a copy to the Scheduled folder to facilitate user interaction

The user can choose to delete the mail, in which case, it will also be unscheduled

Upon first delivery attempt, the mail is automatically moved from the user’s Scheduled folder to the Sent folder, or permanently deleted (according to the user’s saveToSent configuration)

|     |
| --- |
| `POST /api/v1/mails/send/schedule` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `deliveryTime` | `Number` | \* | unix timestamp as unsigned 64 bit int (seconds)<br>e.g. we use `"deliveryTime" : 1680171858` for delivering at<br>Thu Mar 30 2023 12:24:18 GMT+0200 (Central European Summer Time) | Timestamp when the mail should be delivered (up to 1 year into the future) |
| `from` | `String` |  |  | The desired value of the `from` header |
| `to` | `String` |  |  | The desired value of the `to` header |
| `cc` | `String` |  |  | The desired value of the `cc` header |
| `bcc` | `String` |  |  | The desired value of the `bcc` header |
| `replyTo` | `String` |  |  | The desired value of the `Reply-To` header |
| `refwType` | `String` |  | "re", "fw" | Whether the mail is a reply or a forward.<br>The mail cannot be both a reply and a forward (“refw” is an invalid value) |
| `refwMailId` | `String` | Required if `refw` is set |  | This field is dependent on `refwType`:<br>- `refwType` missing: `refwMailId` should not be sent<br>  <br>- `refwType` set to "re": `refwMailId` required, the ID of the mail being replied to. This ID is used to automatically generate the `References` and `In-Reply-To` headers for replies.<br>  <br>- `refwType` set to "fw": `refwMailId` required, the ID of the mail being forwarded |
| `subject` | `String` |  |  | The desired value of the `Subject` header |
| `importance` | `String` |  |  | "normal", "low", "high"<br>The desired importance. If missing, the importance will default to "normal". |
| `requestReadReceipt` | `Boolean` |  |  | Whether to request a read receipt |
| `requestDeliveryReceipt` | `Boolean` |  |  | Whether to request a delivery receipt |
| `bodyText` | `String` |  |  | The UTF-8 text body, if existing |
| `bodyHtml` | `String` |  |  | The UTF-8 HTML body, if existing |
| `temporaryAttachments` | `Array` |  | JSON object list in the following format:

|     |
| --- |
| `temporaryAttachments: [`<br>`    ``{`<br>`        ``id: Number,                 ` `// The temporary attachment ID`<br>`        ``contentId: String,          ` `// The content ID (cid) of the attachment, if found`<br>`        ``isInline: Boolean           ` `// True if you have referred it in the HTML body by cid`<br>`    ``}`<br>`    ``...`<br>`]` | | The attachments in the attachments queue. |

**Response**

If successful, the response will contain the mail id of the mail saved to the Scheduled folder

|     |
| --- |
| `{`<br>`    ``mailId: String,          ` `// The ID of the mail saved to the Scheduled folder`<br>`}` |

### Scheduled Send Draft

This endpoint allows you to schedule delivery of an existing draft mail, at a desired timestamp in the future

If this is preceded by opening the draft for editing, on send you should first save it to drafts and then call this endpoint with the draft mail ID

It will move the draft to the Scheduled folder to facilitate user interaction

The user can choose to delete the mail, in which case, it will also be unscheduled

Upon first delivery attempt, the mail is automatically moved from the user’s Scheduled folder to the Sent folder, or permanently deleted (according to the user’s saveToSent configuration)

|     |
| --- |
| `POST /api/v1/drafts/{mailId}/send/schedule` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `mailId` | `String` | \* |  | The draft mail ID |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `deliveryTime` | `Number` | \* | unix timestamp as unsigned 64 bit int (seconds)<br>e.g. we use `"deliveryTime" : 1680171858` for delivering at<br>Thu Mar 30 2023 12:24:18 GMT+0200 (Central European Summer Time) | Timestamp when the mail should be delivered (up to 1 year into the future) |

**Response**

If successful, the response will contain the mail id of the mail saved to the Scheduled folder

|     |
| --- |
| `{`<br>`    ``mailId: String,          ` `// The ID of the mail saved to the Scheduled folder`<br>`}` |

### Scheduled Cancel

This endpoint allows you to cancel delivery of a previously scheduled mail

It will move the targeted mail from the Scheduled folder to the Drafts folder

|     |
| --- |
| `DELETE /api/v1/mails/send/schedule/{mailId}` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `mailId` | `String` | \* |  | The scheduled mail ID |

**Response**

If successful, the response will contain the mail id of the mail saved to the Drafts folder

|     |
| --- |
| `{`<br>`    ``mailId: String,          ` `// The ID of the mail saved to the Drafts folder`<br>`}` |

## Temporary Attachments

Axigen uses an attachments queue for attachment uploads.

1\. To attach a file to a message as a regular attachment:

a. Use the “Create” endpoint to upload the file

b. Pass the `temporaryAttachments` array to the “Send” or “Save” endpoint.

2\. To attach a file to a message as an inline attachment:

a. Use the “Create” endpoint to upload the file

b. Generate a unique `contentId` and refer it as a `cid` source for the corresponding inline image in your email body.

This will ensure that your mail body will contain a valid reference for each inline attachment.

c. Pass the `temporaryAttachments` array (including the `contentId` and the `isInline` property set to `true`) to the “Send” or “Save” endpoint.

3\. When forwarding an email or opening a draft for editing:

a. Add the existing attachments to the internal queue by calling the “Store” endpoint

b. Update your email body and attachments list to point to the internal queue attachments instead of the original ones (both inline and regular attachments).

### Create

|     |
| --- |
| `POST /api/v1/temporaryAttachments` |

**Request body**

Include the attachment as a `multipart/form-data` HTTP body part.

**Response**

|     |
| --- |
| `{`<br>`    ``items: [`<br>`        ``{`<br>`            ``id: Number,               ` `// The temporary attachment ID`<br>`            ``name: String,             ` `// The name of the attachment`<br>`            ``contentType: String,      ` `// The content type of the attachment`<br>`            ``size: Number              ` `// The attachment size in bytes`<br>`        ``},`<br>`        ``...`<br>`    ``]`<br>`}` |

### Get

|     |
| --- |
| `GET /api/v1/temporaryAttachments/{temporaryAttachmentId}` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `temporaryAttachmentId` | `String` | \* |  | The temporary attachment ID |

**Response**

The temporary attachment.

### Delete

|     |
| --- |
| `DELETE /api/v1/temporaryAttachments/{temporaryAttachmentId}` |

**URL parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `temporaryAttachmentId` | `String` | \* |  | The temporary attachment ID |

**Response**

If successful, the response will be empty.

### Store in Queue

This endpoint allows you to store an email’s attachments in the internal queue.

|     |
| --- |
| `POST /api/v1/temporaryAttachments/store` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `mailId` | `String` | \* |  | The mail ID whose attachments you want to store. |

**Response**

|     |
| --- |
| `{`<br>`    ``items: [`<br>`        ``AttachmentInstance,          ` `// Instance of attachment`<br>`        ``...`<br>`    ``]`<br>`}` |

The IDs of the temporary attachments are not related to the original mail; they are internal queue unique identifiers.

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

[Mailbox API – Mails](https://www.axigen.com/documentation/mailbox-api-mails-p666992807) [Mailbox API – Mails Search](https://www.axigen.com/documentation/mailbox-api-mails-search-p666992858)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827#)