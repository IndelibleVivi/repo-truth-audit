# Complete the application's unsubscribe workflow

The event library looks complete, but the attached TypeScript application cannot use it to stop wildcard subscriptions while continuing to receive its ordinary named events. Please investigate and fix the library within this disposable workspace, and verify the application can complete that workflow. Preserve the existing supported uses and type checking.

The original library source and README are at the workspace root. The application and pinned installed dependencies are in `consumer/`; its README gives the reproduction command. Carry any required change through the source and the actual local package consumed by the application. Do not publish, contact upstream, or install into a user-global environment. Give a concise explanation of what changed and the decisive checks.
