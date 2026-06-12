# Roles and Invites

## Workspace roles

- `owner`: full control, ownership-sensitive changes, final governance
- `admin`: invites, providers, operator settings, broad workspace operations
- `editor`: projects, facts, audits, SoV checks, reports, artifacts
- `viewer`: read-only access to projects, reports, and evidence

## Invite lifecycle

1. Admin or owner creates an invite.
2. The platform returns the invite token and metadata.
3. Admin or owner can update, resend, revoke, or reassign the invite.
4. The invited user accepts the invite while authenticated as the matching
   email.
5. The membership is created and audit logs are written.

## Hard rules

- only owners can promote or demote ownership-sensitive roles
- admins can manage standard operator roles
- workspace isolation always applies to downstream projects, reports, artifacts,
  providers, and logs

## Operator guidance

- use `viewer` for clients who only need visibility
- use `editor` for delivery operators
- use `admin` for day-to-day workspace managers
- keep `owner` narrow and intentional
