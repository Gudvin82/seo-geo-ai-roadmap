# Roles and Invites

## Workspace roles

- `owner`: полный контроль, workspace governance, изменение ролей
- `admin`: может приглашать пользователей, управлять providers, смотреть logs
- `editor`: может создавать проекты, facts и audit runs
- `viewer`: может просматривать проекты, reports и artifacts

## Invite flow

1. Admin или owner создает invite.
1. Платформа возвращает invite token.
1. Приглашенный пользователь принимает invite, будучи залогинен под тем же email.
1. Membership создается, а audit logs обновляются.
