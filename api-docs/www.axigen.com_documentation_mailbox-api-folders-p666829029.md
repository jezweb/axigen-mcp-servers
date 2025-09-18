---
url: "https://www.axigen.com/documentation/mailbox-api-folders-p666829029"
title: "Mailbox API – Folders | Axigen Documentation"
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

- [List](https://www.axigen.com/documentation/mailbox-api-folders-p666829029#MailboxAPI%E2%80%93Folders-List)
- [List Delta](https://www.axigen.com/documentation/mailbox-api-folders-p666829029#MailboxAPI%E2%80%93Folders-ListDelta)
- [Create](https://www.axigen.com/documentation/mailbox-api-folders-p666829029#MailboxAPI%E2%80%93Folders-Create)
- [Update](https://www.axigen.com/documentation/mailbox-api-folders-p666829029#MailboxAPI%E2%80%93Folders-Update)
- [Delete](https://www.axigen.com/documentation/mailbox-api-folders-p666829029#MailboxAPI%E2%80%93Folders-Delete)
- [Move](https://www.axigen.com/documentation/mailbox-api-folders-p666829029#MailboxAPI%E2%80%93Folders-Move)

## List

|     |
| --- |
| `GET /api/v1/folders/` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `type` | `String` |  | "all", "mails", "events", "tasks", "notes", "contacts" | The folder type<br>**Default value:** "all"<br>**Note:** “public\_container”, “shared\_namespace” and “shared\_container” are not available for this property |
| `accessMode` | `String` |  | "all", "local", "public", "shared" | List only folders matching this access mode<br>**Default value:** "all" |
| `syncTokenOnly` | `Boolean` |  |  | When true, the endpoint should only return the syncToken without the folder list.<br>**Default value:** false |

**Response**

|     |
| --- |
| `{`<br>`    ``syncToken: String,                ` `// A generated token that can be used for synchronization purposes to check if any`<br>`                                      ``// changes occurred since the last interogation`<br>`    ``items: [`<br>`        ``FolderInstance,               ` `// Instance of folder`<br>`        ``...`<br>`    ``]`<br>`}` |

## List Delta

This endpoint is available starting with Axigen 10.6.18.

|     |
| --- |
| `GET /api/v1/folders/delta` |

**Query parameters**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `accessMode` | `String` |  | "all", "local", "public", "shared" | List only folders matching this access mode<br>**Default value:** "all" |
| `syncToken` | `String` |  |  | The synchronization token returned by the previous listing; if missing then an initial round of listing is started (all folders are reported as new items)<br>**Default value:** empty string |

**Response**

|     |
| --- |
| `{`<br>`    ``syncToken: String,              ` `// A generated token that can be used for synchronization purposes to check if any`<br>`                                    ``// changes occurred since the last interogation`<br>`    ``events: [`<br>`        ``{`<br>`          ``eventType: String,        ` `// Describes event type; possible values: [`<br>`                                    ``//     "newFolder",`<br>`                                    ``//     "removedFolder",`<br>`                                    ``//     "changedFolder",`<br>`                                    ``//     "resetContainer",`<br>`                                    ``//     "removeContainer"`<br>`                                    ``// ]`<br>`          ``id: String,               ` `// Folder ID`<br>`          ``containerId: String,      ` `// Owner container ID`<br>`          ``idValidity: Number,       ` `// Folder ID validity (optional)`<br>`                                    ``// Present for "newFolder" and "changedFolder" events`<br>`          ``pathChanged: Boolean,     ` `// Signals changes in folder path (rename or move to other parent folder) (optional)`<br>`                                    ``// Present for "newFolder" and "changedFolder" events`<br>`                                    ``// Always 'false' in case of "newFolder" event`<br>`          ``oldParentId: String,      ` `// Previous parent id (optional)`<br>`                                    ``// Present if pathChanged is 'true'`<br>`          ``syncToken: String,        ` `// Folder content synchronization folder (optional)`<br>`                                    ``// Present for "newFolder" and "changedFolder" events`<br>`          ``name: String,             ` `// Folder name (optional)`<br>`                                    ``// Present for "newFolder" events or if pathChanged is 'true'`<br>`          ``parentId: String,         ` `// Parent folder ID; the container ID (root folder) for top level folders (optional)`<br>`                                    ``// Present for "newFolder" events or if pathChanged is 'true'`<br>`          ``role: String,             ` `// The role of the folder, for special folders (optional)`<br>`                                    ``// Possible values: ["", "inbox", "drafts", "sent", "trash", "junk", "archive", "filtered"]`<br>`                                    ``// Present for "newFolder" events or if pathChanged is 'true'`<br>`          ``ownerUsername: String,    ` `// The username of this folder's owner (optional)`<br>`                                    ``// Present for "newFolder" events or if pathChanged is 'true'`<br>`          ``ownerFullname: String,    ` `// The full name of this folder's owner (optional)`<br>`                                    ``// Present for "newFolder" events or if pathChanged is 'true'`<br>`          ``folderSize: Number,       ` `// The folder size in bytes (optional)`<br>`                                    ``// Present for "newFolder" and "changedFolder" events`<br>`          ``folderType: String,       ` `// The type of items contained in this folder (optional)`<br>`                                    ``// Possible values: [`<br>`                                    ``//     "mails",`<br>`                                    ``//     "events",`<br>`                                    ``//     "tasks",`<br>`                                    ``//     "notes",`<br>`                                    ``//     "contacts",`<br>`                                    ``//     "public_container", // Used only for the "~Public Folders" root folder`<br>`                                    ``//     "shared_namespace", // Used only for the "~Other users' folders" root folder`<br>`                                    ``//     "shared_container"  // Used for the "~Other users' folders/<account name>" account root folders`<br>`                                    ``// ]`<br>`                                    ``// Present for "newFolder" events or if pathChanged is 'true'`<br>`          ``accessMode: String,       ` `// The folder's access mode (optional)`<br>`                                    ``// Possible values: [ "local", "public", "shared" ]`<br>`                                    ``// Present for "newFolder" events or if pathChanged is 'true'`<br>`          ``totalItems: Number,       ` `// The total number of items in this folder (optional)`<br>`                                    ``// Present for "newFolder" and "changedFolder" events`<br>`          ``unreadItems: Number,      ` `// The number of unread items in this folder (optional)`<br>`                                    ``// Present for "newFolder" and "changedFolder" events`<br>`          ``permissions: Array        ` `// Associated allowed permissions list (optional)`<br>`                                    ``// Possible values: [`<br>`                                    ``//     // For all folders:`<br>`                                    ``//     "l", // lookup permission (folder is visible in lists)`<br>`                                    ``//     "r", // read permission (folder can be loaded)`<br>`                                    ``//     "s", // seen permission (items can be marked as seen / unseen)`<br>`                                    ``//     "w", // write flags permission (set or clear flags other than seen and deleted)`<br>`                                    ``//     "i", // insert permission (items can be inserted into this folder)`<br>`                                    ``//     "k", // create sub-folder permission (allows the creation of sub-folders under the current folder)`<br>`                                    ``//     "x", // delete folder permission (allows the deletion of this folder)`<br>`                                    ``//     "t", // mark items as deleted permission (items can be marked as deleted / not deleted)`<br>`                                    ``//     "e", // expunge permission (allow expunge to be performed on this folder)`<br>`                                    ``//     "a"  // acl permission (allows the management of permissions for this folder)`<br>`                                    ``// ]`<br>`                                    ``// Present for "newFolder" events or if pathChanged is 'true'`<br>`        ``}`<br>`        ``...`<br>`    ``]`<br>`}` |

**Notes:**

- Order of events is important, so the client must process folder delta events in the order sent by the server

- “newFolder” event contains all information of a FolderInstance plus ID validity and owning container ID

- If a folder ID validity changes the client must discard any cached content data before the next folder mails synchronization process

- In case of a “resetContainer” event the client must mark for deletion all folders with ‘containerID’ equal with the ‘id’ field of the event (not the ‘containerId’ !) and remove them from the folder tree (but not from content cache!). The folder identified by the event remains in the folder tree! If a ‘newFolder’ event is received for one of these folders, the folder is added in the appropriate place in the folder tree and the deletion mark is removed; the client should keep the cached content data (assuming ID validity has not changed) - treat the ‘newFolder’ event as a regular ‘changedFolder’ event from content point of view. When all synchronization events are processed any remaining folders marked for deletion will be removed from content cache (from folder tree they are already removed)

- In case of a “removeContainer” event the client must remove all folders with ‘containerID’ equal with the ‘id’ field of the event from both folder tree and content cache (as if “removeFolder” events are received for all of them). Also the folder specified in the event will be removed from the folder tree

- Synchronization tokens obtained using one access mode should not be used with another access mode, even though it is not illegal and should give proper response if the scope is enlarged (for example using a ‘local’ synchronization token with an ‘all’ access mode should report only the delta changes for local folders and all public and shared folders reported as “newFolder” events).

- The client should compare the ‘syncToken' field for each “newFolder” or “changedFolder” events with its cached synchronization token in order to decide if content (emails) synchronization is necessary.


## Create

|     |
| --- |
| `POST /api/v1/folders/` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `name` | `String` | \* |  | The new folder name |
| `type` | `String` |  | "mails", "events", "tasks", "notes", "contacts" | The folder type<br>**Default value:** "mails" when `parentId` is not present or when it is equal to the root folder. Otherwise, the default value will be equal to the type of the parent folder.<br>**Note:** “public\_container”, “shared\_namespace” and “shared\_container” are not available for this property<br>**Note:** if the `parentId` is sent and is not the root folder Id, then `type` should not be sent. In this case, if the `type` is sent and does not match the parent folder type, the request will result in a 400 error. |
| `parentId` | `String` |  |  | The parent folder ID<br>**Default value:** the folder container ID (root folder)<br>To create folders in the root folder, you can either omit the parentId property or use the `folderContainerId` provided in [Account Info](https://www.axigen.com/wiki/spaces/DEV/pages/90439990/WMAPI+Account#Get). |

**Response**

If successful, the response will contain an [instance of folder](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#FolderInstance).

## Update

|     |
| --- |
| `PATCH /api/v1/folders/{folderId}` |

**URL parameters**

| **Name** | **Type** | **Description** |
| `folderId` | `String` | The folder id |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `name` | `String` | \* |  | The new folder name |

**Response**

If successful, the response will contain an [instance of folder](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#FolderInstance).

## Delete

Folder deletion takes into account the `deleteToTrash` account setting:

- if `deleteToTrash` is true (which is default), then
  - if the folder is not already in Trash, deleting it will actually move it to Trash

  - otherwise, if the folder already in Trash, it's permanently deleted.
- else
  - the folder is permanently deleted.

|     |
| --- |
| `DELETE /api/v1/folders/{folderId}` |

**URL parameters**

| **Name** | **Type** | **Description** |
| `folderId` | `String` | The folder id |

**Response**

If successful, the response will be empty.

## Move

|     |
| --- |
| `POST /api/v1/folders/{folderId}/move` |

**URL parameters**

| **Name** | **Type** | **Description** |
| `folderId` | `String` | The folder id |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `parentId` | `String` | \* |  | The new parent folder ID; the container ID (root folder) for top level folders. |

**Response**

If successful, the response will contain an [instance of folder](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#FolderInstance).

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

[Mailbox API – Account Filters](https://www.axigen.com/documentation/mailbox-api-account-filters-p666927337) [Mailbox API – Mails](https://www.axigen.com/documentation/mailbox-api-mails-p666992807)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-folders-p666829029#)