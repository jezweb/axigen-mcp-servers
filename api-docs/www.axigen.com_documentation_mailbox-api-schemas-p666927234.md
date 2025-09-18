---
url: "https://www.axigen.com/documentation/mailbox-api-schemas-p666927234"
title: "Mailbox API – Schemas | Axigen Documentation"
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

- [Folder Instance](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailboxAPI%E2%80%93Schemas-FolderInstance)
- [Mail Instance](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailboxAPI%E2%80%93Schemas-MailInstance)
- [Conversation Instance](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailboxAPI%E2%80%93Schemas-ConversationInstance)
- [Attachment Instance](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailboxAPI%E2%80%93Schemas-AttachmentInstance)
- [Contact Instance](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailboxAPI%E2%80%93Schemas-ContactInstance)
- [Label Instance](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailboxAPI%E2%80%93Schemas-LabelInstance)
- [MessagePart Instance](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailboxAPI%E2%80%93Schemas-MessagePartInstance)
- [MessagePartData Instance](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#MailboxAPI%E2%80%93Schemas-MessagePartDataInstance)

## Folder Instance

|     |
| --- |
| `{`<br>`    ``id: String,               ` `// The folder ID`<br>`    ``name: String,             ` `// The folder name`<br>`    ``parentId: String,         ` `// The parent folder ID; the container ID (root folder) for top level folders`<br>`    ``role: String,             ` `// The role of the folder, for special folders`<br>`                              ``// Possible values: ["", "inbox", "drafts", "sent", "trash", "junk", "archive", "filtered"]`<br>`    ``ownerUsername: String,    ` `// The username of this folder's owner`<br>`    ``ownerFullname: String,    ` `// The full name of this folder's owner`<br>`    ``folderSize: Number,       ` `// The folder size in bytes`<br>`    ``folderType: String,       ` `// The type of items contained in this folder`<br>`                              ``// Possible values: [`<br>`                              ``//     "mails",`<br>`                              ``//     "events",`<br>`                              ``//     "tasks",`<br>`                              ``//     "notes",`<br>`                              ``//     "contacts",`<br>`                              ``//     "public_container", // Used only for the "~Public Folders" root folder`<br>`                              ``//     "shared_namespace", // Used only for the "~Other users' folders" root folder`<br>`                              ``//     "shared_container"  // Used for the "~Other users' folders/<account name>" account root folders`<br>`                              ``// ]`<br>`    ``accessMode: String,       ` `// The folder's access mode`<br>`                              ``// Possible values: [ "local", "public", "shared" ]`<br>`    ``totalItems: Number,       ` `// The total number of items in this folder`<br>`    ``unreadItems: Number,      ` `// The number of unread items in this folder`<br>`    ``permissions: Array        ` `// Associated allowed permissions list`<br>`                              ``// Possible values: [`<br>`                              ``//     // For all folders:`<br>`                              ``//     "l", // lookup permission (folder is visible in lists)`<br>`                              ``//     "r", // read permission (folder can be loaded)`<br>`                              ``//     "s", // seen permission (items can be marked as seen / unseen)`<br>`                              ``//     "w", // write flags permission (set or clear flags other than seen and deleted)`<br>`                              ``//     "i", // insert permission (items can be inserted into this folder)`<br>`                              ``//     "k", // create sub-folder permission (allows the creation of sub-folders under the current folder)`<br>`                              ``//     "x", // delete folder permission (allows the deletion of this folder)`<br>`                              ``//     "t", // mark items as deleted permission (items can be marked as deleted / not deleted)`<br>`                              ``//     "e", // expunge permission (allow expunge to be performed on this folder)`<br>`                              ``//     "a"  // acl permission (allows the management of permissions for this folder)`<br>`                              ``// ]`<br>`}` |

## Mail Instance

|     |
| --- |
| `{`<br>`    ``id: String,                              ` `// The mail ID`<br>`    ``folderId: String,                        ` `// The associated folder ID`<br>`    ``size: Number,                            ` `// The mail size in bytes`<br>`    ``from` `: String,                            ` `// The From header`<br>`    ``to: String,                              ` `// The To header`<br>`    ``cc: String,                              ` `// The Cc header`<br>`    ``bcc: String,                             ` `// The Bcc header if present`<br>`    ``replyTo: String,                         ` `// The Reply-To header if present, otherwise the From header value`<br>`    ``replyToAll: String,                      ` `// The merged To and Cc headers`<br>`    ``sender: String,                          ` `// The Sender header`<br>`    ``messageId: String,                       ` `// The Message-Id header`<br>`    ``subject: String,                         ` `// The Subject header`<br>`    ``snippet: String,                         ` `// A text snippet of the mail body`<br>`    ``date: String,                            ` `// The date the mail was actually received, sent or saved by the server as timestamp (UTC)`<br>`                                             ``// Note: this is not the "Date" header of the mail but the internal server date which is more accurate`<br>`    ``isUnread: Boolean,                       ` `// The read flag value`<br>`    ``isFlagged: Boolean,                      ` `// The followup flag value`<br>`    ``isDraft: Boolean,                        ` `// Whether the mail is a draft`<br>`    ``refwFlags: ` `""` `| ` `"re"` `| ` `"fw"` `| ` `"refw"` `,    ` `// The replied / forwarded mail flag`<br>`    ``refwType: ` `""` `| ` `"re"` `| ` `"fw"` `,              ` `// Used for Drafts only! Whether the mail is a reply or a forward. The mail cannot be both a reply and a forward (“refw” is an invalid value)`<br>`    ``refwMailId: String,                      ` `// Used for Drafts only! Set only if refwType is either "re" or "fw".`<br>`    ``isDeleted: Boolean,                      ` `// The deleted flag value`<br>`                                             ``// Note: this flag is only set by IMAP clients (in IMAP mails can be marked as deleted`<br>`                                             ``// but will still be returned until expunged)`<br>`    ``hasAttachments: Boolean,                 ` `// The attachment flag value`<br>`    ``isItip: Boolean,                         ` `// The calendar flag value`<br>`    ``returnReceipt: Boolean,                  ` `// True if the mail carries a disposition notification header`<br>`    ``importance: ` `"normal"` `| ` `"low"` `| ` `"high"` `,   ` `// The "Importance" header value`<br>`    ``originalFolderId: String,                ` `// The original folder ID when searching`<br>`    ``originalMailId: String,                  ` `// The original mail ID when searching`<br>`    ``attachments: [`<br>`        ``AttachmentInstance,                  ` `// Instance of attachment`<br>`        ``...`<br>`    ``],`<br>`    ``labelIds: [`<br>`        ``labelId: String,                     ` `// Label id`<br>`        ``...`<br>`    ``],`<br>`    ``bimiLocation: String                     ` `// Available from Axigen X6 (10.6) `<br>`                                             ``// BIMI Location; if not empty, used by the client to request the BIMI indicator (SVG logotype)`<br>`}` |

## Conversation Instance

|     |
| --- |
| `{`<br>`    ``id: String,                              ` `// The conversation ID`<br>`    ``subject: String,                         ` `// Subject of the first mail in the conversation`<br>`    ``snippet: String,                         ` `// Snippet for the last mail in the conversation that belongs to the requested folder`<br>`    ``date: String,                            ` `// UTC datestamp of the last mail in the conversation that belongs to the requested folder`<br>`                                             ``// Note: this is not the "Date" header of the mail but the internal server date which is more accurate`<br>`    ``isUnread: Boolean,                       ` `// The conversation read flag`<br>`    ``isFlagged: Boolean,                      ` `// The conversation followup flag`<br>`    ``refwFlags: ` `""` `| ` `"re"` `| ` `"fw"` `| ` `"refw"` `,    ` `// The conversation replied / forwarded flag`<br>`    ``hasAttachments: Boolean,                 ` `// Whether any mails in the conversation have attachments`<br>`    ``importance: ` `"normal"` `| ` `"low"` `| ` `"high"` `,   ` `// The greatest "Importance" header value of the mails in the conversation`<br>`    `<br>`    ``labelIds: [                              ` `// The list for label IDs used in the conversation`<br>`        ``String,`<br>`        ``...`<br>`    ``],`<br>`    ``attachments: [`<br>`        ``AttachmentInstance,                  ` `// Instance of attachment`<br>`        ``...`<br>`    ``],`<br>`    ``participants: [                          ` `// All "From" full email addresses, including the name part, in all emails in the conversation, `<br>`                                             ``// deduped by email address (email address part)`<br>`        ``{`<br>`            ``fullEmailAddress,`<br>`            ``isMe,`<br>`            ``hasUnreadMessages`<br>`        ``},`<br>`        ``...`<br>`    ``],`<br>`    `<br>`    ``myRecipients: [                          ` `// All the recipients (full email addresses, including the name part) in the emails the current user has sent, `<br>`                                             ``// deduped by email address (email address part)`<br>`        ``{`<br>`            ``fullEmailAddress,`<br>`            ``isMe,`<br>`            ``isTo,`<br>`            ``isCc,`<br>`            ``isBcc`<br>`        ``},`<br>`        ``...`<br>`    ``],`<br>`    ``hasDrafts: Boolean,                      ` `// True if there is at least one draft in the conversation, false otherwise `<br>`    ``mailCount: String,                       ` `// The number of mails in the conversation`<br>`    ``mails: [`<br>`        ``{`<br>`            ``mailId: String,                  ` `// The mail ID`<br>`            ``normalizedMessageId: String,     ` `// The mail's normalized MessageId header value`<br>`            ``folderId: String,                ` `// The associated folder ID`<br>`            ``isUnread: Boolean,               ` `// The read flag value`<br>`            ``isFlagged: Boolean,              ` `// The followup flag value`<br>`            ``isDraft: Boolean,                ` `// Whether the email is a draft`<br>`            ``originalFolderId: String,        ` `// The original folder ID when searching`<br>`            ``originalMailId: String           ` `// The original mail ID when searching`<br>`        ``},`<br>`        ``...`<br>`    ``]`<br>`}` |

## Attachment Instance

|     |
| --- |
| `{`<br>`    ``id: Number,                      ` `// The attachment ID`<br>`    ``mailId: String,                  ` `// The associated mail ID`<br>`    ``name: String,                    ` `// The name of the attachment`<br>`    ``contentId: String                ` `// The content ID (cid) of the attachment, if found`<br>`    ``contentType: String,             ` `// The content type of the attachment`<br>`    ``size: Number,                    ` `// The attachment size in bytes`<br>`    ``isInline: Boolean                ` `// True if it's an inline attachment; `<br>`                                     ``// Note: this is not related to the Content-Disposition property; `<br>`                                     ``// it's set to true only for attachments in multipart/related messages `<br>`                                     ``// that are referenced in the body using a cid`<br>`}` |

## Contact Instance

|     |
| --- |
| `{`<br>`    ``id: String,                  ` `// The contact ID`<br>`    ``folderId: String,            ` `// The associated folder ID`<br>`    ``isDistributionList: Boolean, ` `// True if this item is a distribution list`<br>`    ``name: String,                ` `// The contact's full name`<br>`    ``email: String,               ` `// The defined email address`<br>`                                 ``// Note: this field can be either the email, business email or home email (in this order)`<br>`                                 ``// depending on which one is actually defined`<br>`    ``firstName: String,           ` `// The contact's first name`<br>`    ``lastName: String,            ` `// The contact's last name`<br>`    ``nickName: String,            ` `// The contact's nick name`<br>`    ``reversedName: String         ` `// The contact's reversed full name`<br>`}` |

## Label Instance

|     |
| --- |
| `{`<br>`    ``id:   String,    ` `// The label ID`<br>`    ``name: String     ` `// The label name`<br>`}` |

## MessagePart Instance

|     |
| --- |
| `{`<br>`    ``contentType: String,          ` `// The value of the Content-Type header (e.g. "multipart/alternative", "text/html")`<br>`    ``id: Number,                   ` `// The id of the message part`<br>`    ``parts:[                       ` `// List of nested message parts`<br>`        ``MessagePartInstance,       `<br>`        ``...`<br>`    ``],`<br>`    ``headers:[                     ` `// List of headers of the message part`<br>`        ``{`<br>`            ``name: String,         ` `// The name of the part header (e.g. "Content-Id", "Content-Disposition", "Content-Type")`<br>`            ``value: String         ` `// The raw value of the part header (e.g. "<cid_b1@cid_b1>\n", "inline;\n\tfilename=\"b1_png.png\"\n", "image/png;\n\tname=\"b1_png.png\"\n")`<br>`        ``},`<br>`        ``...`<br>`    ``],`<br>`    ``filename: String,             ` `// Present only if the message part is an attachment. Retrieved from Content-Disposition's "filename" attribute or "name" attributes, in this order`<br>`    ``estimatedSize: Number         ` `// The approximate body part size in bytes (the actual size can depend on the encoding overhead)`<br>`}` |

## MessagePartData Instance

|     |
| --- |
| `{`<br>`    ``id: Number,                   ` `// The id of the message part`<br>`    ``data: String                  ` `// The base64 encoded body part content`<br>`    ``isTruncated: Boolean,         ` `// HTML parts bigger than 2 MB in size are returned truncated.`<br>`                                  ``// The full decoded body can be retrieved using a separate endpoint. `<br>`    ``hasExternalImages: Boolean,   ` `// Whether the email body contains external images`<br>`    ``quotedOffset: Number,         ` `// The raw offset of the start of the first quoted part identified`<br>`    ``quotedPartsOffsets:[`<br>`          ``{`<br>`          ``Number,                 ` `// start of quoted part`<br>`          ``Number                  ` `// end of quoted part`<br>`          ``},`<br>`          ``...`<br>`    ``]`<br>`}` |

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

[Mailbox API – Authentication and Authorization](https://www.axigen.com/documentation/mailbox-api-authentication-and-authorization-p773357577) [Mailbox API – Versioning](https://www.axigen.com/documentation/mailbox-api-versioning-p723157025)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-schemas-p666927234#)