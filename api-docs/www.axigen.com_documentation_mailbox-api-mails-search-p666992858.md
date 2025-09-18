---
url: "https://www.axigen.com/documentation/mailbox-api-mails-search-p666992858"
title: "Mailbox API – Mails Search | Axigen Documentation"
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

- [Search](https://www.axigen.com/documentation/mailbox-api-mails-search-p666992858#MailboxAPI%E2%80%93MailsSearch-Search)
- [Mails Search Syntax](https://www.axigen.com/documentation/mailbox-api-mails-search-p666992858#MailboxAPI%E2%80%93MailsSearch-MailsSearchSyntax)
  - [Criteria](https://www.axigen.com/documentation/mailbox-api-mails-search-p666992858#MailboxAPI%E2%80%93MailsSearch-Criteria)
  - [Additional Notes](https://www.axigen.com/documentation/mailbox-api-mails-search-p666992858#MailboxAPI%E2%80%93MailsSearch-AdditionalNotes)

## Search

|     |
| --- |
| `POST /api/v1/mails/search` |

**Request body (JSON)**

| **Name** | **Type** | **Required** | **Values** | **Description** |
| `folderIds` | `Array` | \* | Example:

|     |
| --- |
| `folderIds: [`<br>`    ``"123_456"` `,`<br>`    ``"123_789"`<br>`]` | | The IDs of the folders to search in |
| `query` | `Array` | \* | JSON object list in the following format:

|     |
| --- |
| `[`<br>`    ``{`<br>`        ``field: String, `<br>`        ``value: String, `<br>`        ``negate: Boolean`<br>`    ``},`<br>`    ``...`<br>`]` | | The query should be a JSON array containing all the requested search criteria.<br>See the Search Syntax chapter below for details about criteria. |
| `recursive` | `Boolean` |  |  | Whether the folders specified in the `folderIds` array should be searched recursively. Default value is “false”. |

**Response**

|     |
| --- |
| `{`<br>`    ``folderId: String,        ` `// The temporary search folder ID generated from the search request`<br>`    ``totalItems: Integer   ` `// The number of items in the temporary search folder`<br>`}` |

## Mails Search Syntax

### Criteria

The table below contains the criteria included in the API search implementation, along with their advanced search / quick search mapping.

| **Criterion class** | **Criterion** | **Operators** | **Syntax** |
| **Prefix**<br>**(All languages)** | **Examples** | **Notes** | **Mailbox REST API Examples** |
| Text | From | contains (default)<br>doesn't contain (-) | from: | 1. from:John<br>   <br>2. from:(John Doe)<br>   <br>3. from:(Mihai "John Doe")<br>   <br>4. from:John Doe < [john.doe@example.com](mailto:john.doe@example.com) ><br>   <br>5. from: Mihai "John Doe < [john.doe@example.com](mailto:john.doe@example.com) >"<br>   <br>6. from:-John<br>   <br>7. from:-(John Doe)<br>   <br>8. from:-("John Doe")<br>   <br>9. from: Mihai from: -"john Doe" | Also accepted with a space after ":"<br>When in quotes, exact match will be applied. | |     |
| --- |
| `// 1`<br>`"query"` `: [{` `"field"` `: ` `"from"` `, ` `"value"` `: ` `"\"John\"*"` `, ` `"negate"` `: ` `"no"` `}]`<br>`// 2`<br>`"query"` `: [{` `"field"` `: ` `"from"` `, ` `"value"` `: ` `"\"John\"* \"Doe\"*"` `, ` `"negate"` `: ` `"no"` `} ]`<br>`// 3`<br>`"query"` `: [{` `"field"` `: ` `"from"` `, ` `"value"` `: ` `"\"Mihai\"* \"John Doe\"*"` `, ` `"negate"` `: ` `"no"` `}]`<br>`// 4`<br>`"query"` `: [{` `"field"` `: ` `"from"` `, ` `"value"` `: ` `"John* Doe* \"<john.doe@example.com>\"*"` `, ` `"negate"` `: ` `"no"` `}]`<br>`// 5`<br>`"query"` `: [{` `"field"` `: ` `"from"` `, ` `"value"` `: ` `"\"Mihai\"* \"John Doe <john.doe@example.com>\"*"` `, ` `"negate"` `: ` `"no"` `}]`<br>`// 6`<br>`"query"` `: [{` `"field"` `: ` `"from"` `, ` `"value"` `: ` `"\"John\"*"` `, ` `"negate"` `: ` `"yes"` `}]`<br>`// 9`<br>`"query"` `: [`<br>`        ``{` `"field"` `: ` `"from"` `, ` `"value"` `: ` `"\"Mihai\"*"` `, ` `"negate"` `: ` `"no"` `},`<br>`        ``{` `"field"` `: ` `"from"` `, ` `"value"` `: ` `"\"john Doe\"*"` `, ` `"negate"` `: ` `"yes"` `}`<br>`]` | |
| To | contains (default)<br>doesn't contain (-) | to: | 1. to:John<br>   <br>2. to:(John Doe)<br>   <br>3. to:("John Doe")<br>   <br>4. to:-John<br>   <br>5. to:-(John Doe)<br>   <br>6. to:-("John Doe")<br>   <br>7. to: Mihai "John Doe < [john.doe@example.com](mailto:john.doe@example.com) >"<br>   <br>8. to: Mihai to: -"john Doe" | Also accepted with a space after ":"<br>When in quotes, exact match will be applied. | |     |
| --- |
| `// 1`<br>`"query"` `: [{` `"field"` `: ` `"to"` `, ` `"value"` `: ` `"\"John\"*"` `, ` `"negate"` `: ` `"no"` `}]`<br>`// 4`<br>`"query"` `: [{` `"field"` `: ` `"to"` `, ` `"value"` `: ` `"\"John\"*"` `, ` `"negate"` `: ` `"yes"` `}]` | |
| Subject | contains (default)<br>doesn't contain (-) | subject: | subject:Party<br>subject:(Christmas Party)<br>subject:("Christmas Party")<br>subject:-Party<br>subject:-(Christmas Party)<br>-subject:("Christmas Party") | Also accepted with a space after ":"<br>When in quotes, exact match will be applied. | Same as the "From" criterion API; replace `"field": "from"` with `"field": "subject"` |
| Cc | contains (default)<br>doesn't contain (-) | cc: | cc:John<br>cc:(John Doe)<br>cc:("John Doe")<br>cc:-John<br>cc:-(John Doe)<br>cc:-("John Doe") | Also accepted with a space after ":"<br>When in quotes, exact match will be applied. | Same as the "From" criterion API; replace `"field": "from"` with `"field": "cc"` |
| Bcc | contains (default)<br>doesn't contain (-) | bcc: | bcc:John<br>bcc:(John Doe)<br>bcc:("John Doe")<br>bcc:-John<br>bcc:-(John Doe)<br>bcc:-("John Doe") | Also accepted with a space after ":"<br>When in quotes, exact match will be applied. | Same as the "From" criterion API; replace `"field": "from"` with `"field": "bcc"` |
| Body | contains (default)<br>doesn't contain (-) | body: | body:Party<br>body:(Christmas Party)<br>body:("Christmas Party")<br>body:-Party<br>body:-(Christmas Party)<br>body:-("Christmas Party") | Also accepted with a space after ":"<br>When in quotes, exact match will be applied. | Same as the "From" criterion API; replace `"field": "from"` with `"field": "body"` |
| Any field | contains (default)<br>doesn't contain (-) | N/A | John<br>John Doe <john.doe@ [example.com](http://example.com/) ><br>(Christmas Party)<br>"Christmas Party"<br>-John<br>-(John Doe <john.doe@ [example.com](http://example.com/) >)<br>-(Christmas Party)<br>-"Christmas Party" | Also accepted with a space after ":"<br>When in quotes, exact match will be applied. | Same as the "From" criterion API; replace `"field": "from"` with `"field": "anyfield"` |
| Time | Date | before | before:\[date\] | before:15/12/2019<br>before:(15/12/2019) | Also accepted with a space after ":"<br>Dates are accepted in the format: `dd-mm-yyyy` ( `dd` can also be `d`)<br>"last 7 days" replaces "is from this week"<br>"last 30 days" replaces "is from this month"<br>"before" replaces "is before"<br>"after" replaces "is since" <br>Examples assume today is 14/12/2019<br>The "After" and "Before" dates are exclusive.<br>The date timestamps are treated as UTC, regardless of the client's timezone. | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"before"` `, ` `"value"` `: ` `"15-12-2019"` `, ` `"negate"` `: ` `"no"` `}]` | |
| after | after:\[date\] | after:14/12/2019<br>after:(14/12/2019) | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"after"` `, ` `"value"` `: ` `"14-08-2019"` `, ` `"negate"` `: ` `"no"` `}]` | |
| last 7 days | after:\[date\]<br>before:\[date\] | after:07/12/2019 before:15/12/2019<br>after:(07/12/2019) before:(15/12/2019) | |     |
| --- |
| `"query"` `: [`<br>`        ``{` `"field"` `: ` `"after"` `, ` `"value"` `: ` `"07-12-2020"` `, ` `"negate"` `: ` `"no"` `},`<br>`        ``{` `"field"` `: ` `"before"` `, ` `"value"` `: ` `"15-12-2020"` `, ` `"negate"` `: ` `"no"` `}`<br>`]` | |
| last 30 days | after:14/11/2019 before:15/12/2019<br>after:(14/11/2019) before:(15/12/2019) | |     |
| --- |
| `"query"` `: [`<br>`        ``{` `"field"` `: ` `"after"` `, ` `"value"` `: ` `"14-11-2020"` `, ` `"negate"` `: ` `"no"` `},`<br>`        ``{` `"field"` `: ` `"before"` `, ` `"value"` `: ` `"14-12-2020"` `, ` `"negate"` `: ` `"no"` `}`<br>`]` | |
| between (default) | after:15/08/2019 before:15/12/2019<br>after:(15/08/2019) before:(15/12/2019) | |     |
| --- |
| `"query"` `: [`<br>`        ``{` `"field"` `: ` `"after"` `, ` `"value"` `: ` `"15-08-2020"` `, ` `"negate"` `: ` `"no"` `},`<br>`        ``{` `"field"` `: ` `"before"` `, ` `"value"` `: ` `"15-12-2020"` `, ` `"negate"` `: ` `"no"` `}`<br>`]` | |
| Has attachment | Has attachment | N/A | has: | has:attachment |  | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"hasatt"` `, ` `"negate"` `: ` `"no"` `}] ` `// note that the "value" key is not used` | |
| Read / Unread | Read / Unread | N/A | is: | 1. is:unread<br>   <br>2. is:read | Also accepted with a space after ":"<br>An `is:read` WebMail search translates to a negated `"unread"` API query | |     |
| --- |
| `// 1`<br>`"query"` `: [{` `"field"` `: ` `"unread"` `, ` `"negate"` `: ` `"no"` `}] ` `// note that the "value" key is not used`<br>`// 2`<br>`"query"` `: [{` `"field"` `: ` `"unread"` `, ` `"negate"` `: ` `"yes"` `}] ` `// note that the "value" key is not used` | |
| Folder ID | Search in | All mail | in:anywhere | in:anywhere | Also accepted with a space after ":"<br>The folder name can be in quotes or without quotes.<br>If there's a folder named "mailbox", the current mailbox takes precedence; the folder needs to be added in brackets or quotes to take precedence. | Note that the folder IDs are specified in the fid array, not in the query

|     |
| --- |
| `"folderIds"` `: [`<br>`    ``"<x>_<y1>"` `,    ` `// where x is owner ID and y1 is first folder ID`<br>`    ``"<x>_<y2>"` `,    ` `// where x is owner ID and y2 is second folder ID`<br>`    ``...`<br>`    ``"<x>_<yn>"` `// where x is owner ID and yn is last folder ID`<br>`]` | |
| Current mailbox (default) | N/A | N/A | |     |
| --- |
| `"folderIds"` `: [`<br>`    ``"<x>_<y1>"` `,    ` `// where x is owner ID and y1 is first folder ID`<br>`    ``"<x>_<y2>"` `,    ` `// where x is owner ID and y2 is second folder ID`<br>`    ``...`<br>`    ``"<x>_<yn>"` `// where x is owner ID and yn is last folder ID`<br>`]` | |
| Current mailbox (including Spam and Trash) | in:mailbox | in:mailbox | |     |
| --- |
| `"folderIds"` `: [`<br>`    ``"<x>_<y1>"` `,    ` `// where x is owner ID and y1 is first folder ID`<br>`    ``"<x>_<y2>"` `,    ` `// where x is owner ID and y2 is second folder ID`<br>`    ``...`<br>`    ``"<x>_<yn>"` `,    ` `// where x is owner ID and yn is last folder ID`<br>`    ``"<x>_<ySpam>"` `, ` `// where ySpam is the ID of the Spam folder`<br>`    ``"<x>_<yTrash>"` `// where yTrash is the ID of the Trash folder`<br>`]` | |
| Current folder | in:\[folderName\] | in:Inbox<br>in:(Marketing Materials)<br>in:("Marketing Materials") | |     |
| --- |
| `"folderIds"` `: [`<br>`    ``"<x>_<cf>"` `// where cf is the ID of the current folder`<br>`]` | |
| Custom folders | in:("Inbox", "Marketing Materials") | in:("Inbox", "Marketing Materials") | |     |
| --- |
| `"folderIds"` `: [`<br>`    ``"<x>_<y1>"` `,    ` `// where x is owner ID and y1 is the ID of folder "Inbox"`<br>`    ``"<x>_<y2>"` `,    ` `// where x is owner ID and y2 is the ID of folder "Marketing Materials"`<br>`]` | |
| Size | Size | is less than | smaller:\[size\] | 1. smaller: 2M<br>   <br>2. smaller:800K<br>   <br>3. smaller:1000B<br>   <br>4. smaller:10000 | Also accepted with a space after ":" | |     |
| --- |
| `// 1`<br>`"query"` `: [{` `"field"` `: ` `"smaller"` `, ` `"value"` `: ` `2097152` `, ` `"negate"` `: ` `"no"` `}] ` `// value is in bytes`<br>`// 2`<br>`"query"` `: [{` `"field"` `: ` `"smaller"` `, ` `"value"` `: ` `819200` `, ` `"negate"` `: ` `"no"` `}]  ` `// value is in bytes`<br>`// 3`<br>`"query"` `: [{` `"field"` `: ` `"smaller"` `, ` `"value"` `: ` `1000` `, ` `"negate"` `: ` `"no"` `}]    ` `// value is in bytes`<br>`// 4`<br>`"query"` `: [{` `"field"` `: ` `"smaller"` `, ` `"value"` `: ` `10000` `, ` `"negate"` `: ` `"no"` `}]   ` `// value is in bytes` | |
| is more than | larger:\[size\] | 1. larger: 2M<br>   <br>2. larger:800K<br>   <br>3. larger:1000B<br>   <br>4. larger:10000 | |     |
| --- |
| `// 1`<br>`"query"` `: [{` `"field"` `: ` `"larger"` `, ` `"value"` `: ` `2097152` `, ` `"negate"` `: ` `"no"` `}] ` `// value is in bytes`<br>`// 2`<br>`"query"` `: [{` `"field"` `: ` `"larger"` `, ` `"value"` `: ` `819200` `, ` `"negate"` `: ` `"no"` `}]  ` `// value is in bytes`<br>`// 3`<br>`"query"` `: [{` `"field"` `: ` `"larger"` `, ` `"value"` `: ` `1000` `, ` `"negate"` `: ` `"no"` `}]    ` `// value is in bytes`<br>`// 4`<br>`"query"` `: [{` `"field"` `: ` `"larger"` `, ` `"value"` `: ` `10000` `, ` `"negate"` `: ` `"no"` `}]   ` `// value is in bytes` | |
| Flag | Flag | is follow-up | is: | is:follow-up | Also accepted with a space after ":" | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"flag"` `, ` `"value"` `: ` `"followup"` `, ` `"negate"` `: ` `"no"` `}]` | |
| is not follow-up | is:-follow-up | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"flag"` `, ` `"value"` `: ` `"followup"` `, ` `"negate"` `: ` `"yes"` `}]` | |
| is completed | is:completed | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"flag"` `, ` `"value"` `: ` `"completed"` `, ` `"negate"` `: ` `"no"` `}]` | |
| is not completed | is:-completed | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"flag"` `, ` `"value"` `: ` `"completed"` `, ` `"negate"` `: ` `"yes"` `}]` | |
| Importance | Importance | is high importance | has: | has:high-importance | Also accepted with a space after ":" | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"importance"` `, ` `"value"` `: ` `"high"` `, ` `"negate"` `: ` `"no"` `}]` | |
| is not high importance | has:-high-importance | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"importance"` `, ` `"value"` `: ` `"high"` `, ` `"negate"` `: ` `"yes"` `}]` | |
| is low importance | has:low-importance | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"importance"` `, ` `"value"` `: ` `"normal"` `, ` `"negate"` `: ` `"no"` `}]` | |
| is not low importance | has:-low-importance | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"importance"` `, ` `"value"` `: ` `"normal"` `, ` `"negate"` `: ` `"yes"` `}]` | |
| is normal importance | has:normal-importance | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"importance"` `, ` `"value"` `: ` `"low"` `, ` `"negate"` `: ` `"no"` `}]` | |
| is not normal importance | has:-normal-importance | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"importance"` `, ` `"value"` `: ` `"low"` `, ` `"negate"` `: ` `"yes"` `}]` | |
| Label | Label | has label | label: | label:MyLabelName | Also accepted with a space after ":"<br>The client will translate label name to label id | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"label"` `, ` `"value"` `: ` `"40_71"` `"negate"` `: ` `"no"` `}]` | |
| does not have label | label:-MyOtherLabelName | |     |
| --- |
| `"query"` `: [{` `"field"` `: ` `"label"` `, ` `"value"` `: ` `"40_83"` `"negate"` `: ` `"yes"` `}]` | |

### Additional Notes

- The default operator is `AND`.

- The "-" prefix negates the entire criterion ("-" followed by space is not accepted — i.e. does not have the same behavior)

- Multiple criteria can be combined. Examples:
  - `Christmas Party from:John`

  - `"Christmas Party 2019" from:John`

  - `from:John from:Doe`  → `from:(John Doe)`

  - `from:John subject:Party is:replied after:2019-12-01`

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

[Mailbox API – Mails Create and Send](https://www.axigen.com/documentation/mailbox-api-mails-create-and-send-p666992827) [Mailbox API – Mails Counters](https://www.axigen.com/documentation/mailbox-api-mails-counters-p688750780)

Axigen uses cookies. By using our services, you’re agreeing to our [Cookie Policy](https://www.axigen.com/legal/cookie-policy/). [GOT IT](https://www.axigen.com/documentation/mailbox-api-mails-search-p666992858#)