---
url: "https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397"
title: "Mailbox API – Account Settings | Axigen Documentation"
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

- [Settings](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-Settings)
  - [Get](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-Get)
  - [Update](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-Update)
- [WebMail UI Settings](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-WebMailUISettings)
  - [Get](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-Get.1)
  - [Update](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-Update.1)
  - [Delete](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-Delete)
- [Client UI Settings](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-ClientUISettings)
  - [Get](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-Get.2)
  - [Update](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-Update.2)
  - [Delete](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#MailboxAPI%E2%80%93AccountSettings-Delete.1)

## Settings

### Get

|     |
| --- |
| `GET /api/v1/account/settings` |

**Response**

|     |
| --- |
| `{`<br>`    ``archivingPolicy: String,                ` `// Possible values: [ `<br>`                                            ``//   "none",`<br>`                                            ``//   "folderPerYear",`<br>`                                            ``//   "folderPerMonth",`<br>`                                            ``//   "subfolderPerMonth"`<br>`                                            ``// ]`<br>`    ``conversationView: Boolean,              ` `// Whether the conversation view is enabled for the current account`<br>`    ``theme: String,                           ` `// Possible values: [`<br>`                                            ``//  "ocean",`<br>`                                            ``//  "breeze",`<br>`                                            ``//  "neutral"`<br>`                                            ``//],`<br>`    ``deleteToTrash: Boolean,                 ` `// The item will be permanently deleted or will end up in Trash`<br>`    ``confirmMailDelete: Boolean,             ` `// Confirm before the item is deleted`<br>`    ``autoAddRecipients: Boolean,             ` `// Automatically add recipients from sent emails to Collected Addresses`<br>`    ``purgeTrashOnLogout: Boolean,            ` `// Purge the Trash folder on logout`<br>`    ``purgeSpamOnLogout: Boolean,             ` `// Purge the Spam folder on logout`<br>`    ``bodyHtmlFilteringLevel: Number,         ` `// Possible values: [0,1,2,3]`<br>`    ``language: String,                       ` `// Possible values: ["ar","bg","ca","cs","da","de","el","en","es","et","fa",`<br>`                                            ``//  "fi","fr","he","hi","hr","hu","id","is","it","ja","ko","lt","lv","mk","nl",`<br>`                                            ``//  "no","pl","pt","ro","ru","sk","sl","sr","sv","th","tr","tk","uk","vi","zh-cn","zh-tw"]`<br>`    ``timezone: String,                       ` `// The default time zone                         `<br>`    ``dateFormat: String,                     ` `// Possible values: ["MM-DD-YYYY", "MM-DD-YY", "MM-D-YYYY", "MM-D-YY", "M-DD-YY", `<br>`                                            ``//  "M-D-YYYY", "M-D-YY", "MM/DD/YYYY", "MM/DD/YY", "MM/DD/YY","MM/D/YYYY", "MM/D/YY", `<br>`                                            ``//  "M/DD/YYYY", "M/DD/YY", "M/D/YYY", "M/D/YY", "MM.DD.YYYY", "MM.DD.YY", "MM.D.YYYY", `<br>`                                            ``//  "MM.D.YY","M.DD.YYYY", "M.D.YY", "DD-MM-YYYY", "DD-MM-YY", "DD-M-YYYY", "DD-M-YY", `<br>`                                            ``//  "D-MM-YYYY", "D-MM-YY", "D-M-YYYY", "D-M-YY","DD/MM/YYYY", "DD/MM/YY", "DD/M/YYYY", `<br>`                                            ``//  "DD/M/YY", "D/MM/YYYY", "D/MM/YY", "D/M/YYYY", "D/M/YY", "DD.MM.YYYY", "DD.MM.YY",`<br>`                                            ``//  "DD.M.YY", "D.MM.YYYY", "D.MM.YY", "D.M.YYYY", "D.M.YY", "YYYY-MM-DD", "YYYY-MM-D", `<br>`                                            ``//  "YYYY-M-DD", "YYYY-M-D", "YY-MM-DD","YY-MM-D", "YY-M-DD", "YY-M-D", "YYYY/MM/DD", `<br>`                                            ``//  "YYYY/MM/D", "YYYY/M/DD", "YYYY/M/D", "YY/MM/DD", "YY/MM/D", "YY/M/D","YYYY.MM.DD", `<br>`                                            ``//  "YYYY.MM.D", "YYYY.M.DD", "YYYY.M.D", "YY.MM.DD", "YY.MM.D", "YY.M.DD", "YY.M.D"]`<br>`    ``timeFormat: String,                     ` `// Possible values: ["h:mm A.M.", "h:mm A.M.", "hh:mm AM", "hh:mm A.M.", "h.mm AM", `<br>`                                            ``//  "h.mm A.M.", "hh.mm AM", hh.mm A.M.", "h:mm", "hh:mm", "h.mm",`<br>`                                            ``//  "hh:mm", "h.mm", "hh.mm", "h"h" mm"min"", "hh"h" mm"min""]`<br>`    ``weekStartDay: Number,                   ` `// Possible values: [0-6]`<br>`                                            ``// Represents every day of the week`<br>`    ``workingDays: Number,                    ` `// Possible values [1-127]`<br>`                                            ``// For each day a multipe of 2 is assigned; to select more days, their sum will be set `<br>`                                            ``// (sunday 1, monday 2, tuesday 4, wednesday 8, thrusday 16, friday 32, saturday 64        `<br>`    ``startWorkingTime: String,               ` `// Possible values: hh:mm::ss`<br>`    ``endWorkingTime: String,                 ` `// Possible values: hh:mm::ss`<br>`    ``calendarType: String,                   ` `// Possible values: [`<br>`                                            ``//  "gregorian",`<br>`                                            ``//  "persian"`<br>`                                            ``// ]              `<br>`    ``receipts:`<br>`    ``{`<br>`        ``sendReadReceipts: String,           ` `// Possible values: [ `<br>`                                            ``//   "ask",`<br>`                                            ``//   "always",`<br>`                                            ``//   "never"`<br>`                                            ``// ]`<br>`        ``requestReadReceipts: Boolean,       ` `// Whether a read receiept is requested when sending an email`<br>`        ``requestDeliveryReceipts: Boolean    ` `// Whether a delivery receiept is requested when sending an email`<br>`    ``}`<br>`}` |

### Update

|     |
| --- |
| `PATCH /api/v1/account/settings` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `archivingPolicy` | `String` |  | `"none"`, `"folderPerYear"`, `"folderPerMonth"`, `"subfolderPerMonth"` | The new archiving policy type |
| `conversationView` | `Boolean` |  |  | The new option for the Conversation View |
| `theme` | `String` |  | `"neutral"`, `"breeze"`, `"ocean"` | The new option for theme |
| `deleteToTrash` | `Boolean` |  |  | The new option for delete to trash |
| `confirmMailDelete` | `Boolean` |  |  | The new option for confirm mail delete |
| `autoAddRecipients` | `Boolean` |  |  | The new option for auto add recipients |
| `purgeTrashOnLogout` | `Boolean` |  |  | The new option for purge trash message selector |
| `purgeSpamOnLogout` | `Boolean` |  |  | The new option for purge spam message selector |
| `bodyHtmlFilteringLevel` | `Number` |  | `[0-3]` | The new option for html filter level |
| `language` | `String` |  | `"ar"`, `"bg"`, `"ca"`, `"cs"`, `"da"`, `"de"`, `"el"`, `"en"`, `"es"`, `"et"`, `"fa"`, `"fi"`, `"fr"`, `"he"`, `"hi"`, `"hr"`, `"hu"`, `"id"`, `"is"`, `"it"`, `"ja"`, `"ko"`, `"lt"`, `"lv"`, `"mk"`, `"nl"`, `"no"`, `"pl"`, `"pt"`, `"ro"`, `"ru"`, `"sk"`, `"sl"`, `"sr"`, `"sv"`, `"th"`, `"tr"`, `"tk"`, `"uk"`, `"vi"`, `"zh-cn"`, `"zh-tw"` | The new option for language |
| `timezone` | `String` |  |  | The new option for timezone |
| `dateFormat` | `String` |  | `"MM-DD-YYYY"`, `"MM-DD-YY"`, `"MM-D-YYYY"`, `"MM-D-YY"`, `"M-DD-YY"`, `"M-D-YYYY"`, `"M-D-YY"`, `"MM/DD/YYYY"`, `"MM/DD/YY"`, `"MM/DD/YY"`,<br>`"MM/D/YYYY"`, `"MM/D/YY"`, `"M/DD/YYYY"`, `"M/DD/YY"`, `"M/D/YYY"`, `"M/D/YY"`, `"MM.DD.YYYY"`, `"MM.DD.YY"`, `"MM.D.YYYY"`, `"MM.D.YY"`,<br>`"M.DD.YYYY"`, `"M.D.YY"`, `"DD-MM-YYYY"`, `"DD-MM-YY"`, `"DD-M-YYYY"`, `"DD-M-YY"`, `"D-MM-YYYY"`, `"D-MM-YY"`, `"D-M-YYYY"`, `"D-M-YY"`,<br>`"DD/MM/YYYY"`, `"DD/MM/YY"`, `"DD/M/YYYY"`, `"DD/M/YY"`, `"D/MM/YYYY"`, `"D/MM/YY"`, `"D/M/YYYY"`, `"D/M/YY"`, `"DD.MM.YYYY"`, `"DD.MM.YY"`,<br>`"DD.M.YY"`, `"D.MM.YYYY"`, `"D.MM.YY"`, `"D.M.YYYY"`, `"D.M.YY"`, `"YYYY-MM-DD"`, `"YYYY-MM-D"`, `"YYYY-M-DD"`, `"YYYY-M-D"`, `"YY-MM-DD"`,<br>`"YY-MM-D"`, `"YY-M-DD"`, `"YY-M-D"`, `"YYYY/MM/DD"`, `"YYYY/MM/D"`, `"YYYY/M/DD"`, `"YYYY/M/D"`, `"YY/MM/DD"`, `"YY/MM/D"`, `"YY/M/D"`,<br>`"YYYY.MM.DD"`, `"YYYY.MM.D"`, `"YYYY.M.DD"`, `"YYYY.M.D"`, `"YY.MM.DD"`, `"YY.MM.D"`, `"YY.M.DD"`, `"YY.M.D"` | The new option for date format |
| `timeFormat` | `String` |  | `"h:mm A.M."`, `"h:mm A.M."`, `"hh:mm AM"`, `"hh:mm A.M."`, `"h.mm AM"`, `"h.mm A.M."`, `"hh.mm AM"`, `"hh.mm A.M."`, `"h:mm"`, `"hh:mm"`, `"h.mm"`,<br>`"hh:mm"`, `"h.mm"`, `"hh.mm"`, `"h"h" mm"min""`, `"hh"h" mm"min""` | The new option for time format |
| `weekStartDays` | `Number` |  | `[0-6]` | The new option for week start days |
| `workingDays` | `Number` |  | `[1-127]` | The new option for working days |
| `startWorkingTime` | `String` |  |  | The new option for start working time |
| `endWorkingTime` | `String` |  |  | The new option for end working time |
| `calendarType` | `String` |  | `"persian"`, `"gregorian"` | The new option for calendar type |
| `receipts` | `Object` |  | |     |
| --- |
| `receipts:`<br>`{`<br>`    ``sendReadReceipts: String,           ` `// Possible values: [ `<br>`                                        ``//   "ask",`<br>`                                        ``//   "always",`<br>`                                        ``//   "never"`<br>`                                        ``// ]`<br>`    ``requestReadReceipts: Boolean,       ` `// Whether a read receiept is requested when sending an email`<br>`    ``requestDeliveryReceipts: Boolean    ` `// Whether a delivery receiept is requested when sending an email`<br>`}` | |  |
| `receipts.sendReadReceipts` | `String` |  | `"ask"`, `"always"`, `"never"` | The new option for sending read receipts |
| `receipts.requestReadReceipts` | `Boolean` |  |  | The new option for requesting read receipts |
| `receipts.requestDeliveryReceipts` | `Boolean` |  |  | The new option for requesting delivery receipts |

**Response**

If successful, the response will be empty.

## WebMail UI Settings

For Axigen WebMail frontend-specific settings and configurations.

The UI Settings endpoints are available starting with Axigen X5 (10.5).

### Get

|     |
| --- |
| `GET /api/v1/account/settings/ui` |

**Response**

|     |
| --- |
| `{`<br>`    ``uiSettings: String ` `// any data previously set for the current account`<br>`}` |

### Update

|     |
| --- |
| `POST /api/v1/account/settings/ui` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `uiSettings` | `String` | \* | Any string up to 8192 bytes | The frontend settings to be saved for the current account |

**Response**

If successful, the response will be empty.

### Delete

This will reset the settings to an empty string.

|     |
| --- |
| `DELETE /api/v1/account/settings/ui` |

**Response**

If successful, the response will be empty.

## Client UI Settings

For custom frontend-specific settings and configurations

The UI Settings endpoints are available starting with Axigen X5 (10.5).

### Get

|     |
| --- |
| `GET /api/v1/account/settings/client` |

**Response**

|     |
| --- |
| `{`<br>`    ``clientSettings: String ` `// any data previously set for the current account`<br>`}` |

### Update

|     |
| --- |
| `POST /api/v1/account/settings/client` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `clientSettings` | `String` | \* | Any string up to 8192 bytes | The frontend settings to be saved for the current account |

**Response**

If successful, the response will be empty.

### Delete

This will reset the settings to an empty string.

|     |
| --- |
| `DELETE /api/v1/account/settings/client` |

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

[Mailbox API – Account](https://www.axigen.com/documentation/mailbox-api-account-p666828978) [Mailbox API – Account Security](https://www.axigen.com/documentation/mailbox-api-account-security-p1602977833)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-account-settings-p891191397#)