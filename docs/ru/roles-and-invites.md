# Roles and Invites

## Workspace roles

- `owner`: полный контроль, ownership-sensitive changes, финальный governance
- `admin`: invites, providers, operator settings, широкие workspace-операции
- `editor`: projects, facts, audits, SoV checks, reports, artifacts
- `viewer`: read-only доступ к projects, reports и evidence

## Invite lifecycle

1. Admin или owner создает invite.
2. Платформа возвращает invite token и metadata.
3. Admin или owner может обновить, resend, revoke или reassignment invite.
4. Приглашенный пользователь принимает invite, будучи авторизованным под
   нужным email.
5. Membership создается, а audit logs пополняются.

## Жесткие правила

- только owner может менять ownership-sensitive roles
- admin управляет стандартными operator roles
- workspace isolation всегда распространяется на projects, reports, artifacts,
  providers и logs

## Operator guidance

- `viewer` для клиентов, которым нужна только прозрачность
- `editor` для delivery-операторов
- `admin` для ежедневных workspace-менеджеров
- `owner` держите узким и осознанным
