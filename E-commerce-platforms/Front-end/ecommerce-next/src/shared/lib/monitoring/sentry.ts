import * as Sentry from "@sentry/nextjs";

export function captureError(error: unknown, context?: Record<string, unknown>) {
  if (process.env.NODE_ENV === "production") {
    Sentry.captureException(error, { extra: context });
  } else {
    console.error("[Dev Error]", error, context);
  }
}

export function captureMessage(
  message: string,
  level: Sentry.SeverityLevel = "info",
) {
  if (process.env.NODE_ENV === "production") {
    Sentry.captureMessage(message, level);
  }
}
