# Email templates

Four ready-to-paste HTML emails. Built with tables and inline styles so they work in Gmail, Apple Mail, and Outlook.

| File | Email | When |
| --- | --- | --- |
| `weekly-bite.html` | The Weekly Bite | Every Thursday |
| `just-opened.html` | Just Opened | When a new place opens |
| `eat-for-less.html` | Eat for Less This Weekend | Some weekends |
| `local-spotlight-sponsored.html` | A Local Spotlight (paid) | At most once a month, opt-in list only |

## Filling them in

Every `{{token}}` is a blank to fill. When you pick an email service (Beehiiv, Kit, Mailchimp), swap the tokens for that service's merge tags. Its own unsubscribe and preferences links replace `{{unsubscribe_url}}` and `{{preferences_url}}`.

Blocks marked `OPTIONAL` in the HTML (deal, sponsor, partner offer) can be deleted when not used.

Rules that must stay:
- `{{mailing_address}}` is required by US law (CAN-SPAM). A P.O. box works.
- Paid content keeps the black SPONSORED tag and never gets a Good or Great label.
- `{{logo_url}}` and every image need full `https://` links. Email can't load files from your computer.
