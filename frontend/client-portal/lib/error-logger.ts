/**
 * Advanced Error Logging System
 * Captures detailed error information for debugging and analysis
 */

export interface ErrorLog {
  timestamp: string;
  level: 'error' | 'warning' | 'info' | 'debug';
  message: string;
  error?: {
    name: string;
    message: string;
    stack?: string;
  };
  context: {
    url: string;
    userAgent: string;
    userId?: string;
    sessionId?: string;
    action?: string;
    component?: string;
    [key: string]: any;
  };
  request?: {
    method: string;
    url: string;
    headers?: Record<string, string>;
    body?: any;
  };
  response?: {
    status: number;
    statusText: string;
    headers?: Record<string, string>;
    body?: any;
  };
  metadata?: Record<string, any>;
}

class ErrorLogger {
  private logs: ErrorLog[] = [];
  private maxLogs = 1000;
  private enabled = true;

  /**
   * Log an error with full context
   */
  logError(
    message: string,
    error?: Error,
    context?: Partial<ErrorLog['context']>,
    request?: ErrorLog['request'],
    response?: ErrorLog['response']
  ): void {
    if (!this.enabled) return;

    const log: ErrorLog = {
      timestamp: new Date().toISOString(),
      level: 'error',
      message,
      error: error
        ? {
            name: error.name,
            message: error.message,
            stack: error.stack,
          }
        : undefined,
      context: {
        url: typeof window !== 'undefined' ? window.location.href : 'server',
        userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'server',
        ...context,
      },
      request,
      response,
    };

    this.logs.push(log);
    if (this.logs.length > this.maxLogs) {
      this.logs.shift();
    }

    // Console output
    console.error('🔴 Error Logged:', {
      message,
      error: error?.message,
      context,
      request,
      response,
    });

    // Send to backend if available
    this.sendToBackend(log).catch((err) => {
      console.error('Failed to send error log to backend:', err);
    });
  }

  /**
   * Log a warning
   */
  logWarning(
    message: string,
    context?: Partial<ErrorLog['context']>,
    metadata?: Record<string, any>
  ): void {
    if (!this.enabled) return;

    const log: ErrorLog = {
      timestamp: new Date().toISOString(),
      level: 'warning',
      message,
      context: {
        url: typeof window !== 'undefined' ? window.location.href : 'server',
        userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'server',
        ...context,
      },
      metadata,
    };

    this.logs.push(log);
    console.warn('🟡 Warning Logged:', { message, context, metadata });
  }

  /**
   * Log info
   */
  logInfo(
    message: string,
    context?: Partial<ErrorLog['context']>,
    metadata?: Record<string, any>
  ): void {
    if (!this.enabled) return;

    const log: ErrorLog = {
      timestamp: new Date().toISOString(),
      level: 'info',
      message,
      context: {
        url: typeof window !== 'undefined' ? window.location.href : 'server',
        userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'server',
        ...context,
      },
      metadata,
    };

    this.logs.push(log);
    console.info('🔵 Info Logged:', { message, context, metadata });
  }

  /**
   * Send error log to backend
   */
  private async sendToBackend(log: ErrorLog): Promise<void> {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      await fetch(`${apiUrl}/api/v1/logs/error`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(log),
      });
    } catch (error) {
      // Silently fail - don't break the app if logging fails
    }
  }

  /**
   * Get all logs
   */
  getLogs(): ErrorLog[] {
    return [...this.logs];
  }

  /**
   * Get logs by level
   */
  getLogsByLevel(level: ErrorLog['level']): ErrorLog[] {
    return this.logs.filter((log) => log.level === level);
  }

  /**
   * Clear all logs
   */
  clearLogs(): void {
    this.logs = [];
  }

  /**
   * Export logs as JSON
   */
  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }

  /**
   * Enable/disable logging
   */
  setEnabled(enabled: boolean): void {
    this.enabled = enabled;
  }
}

// Global error logger instance
export const errorLogger = new ErrorLogger();

// Global error handler
if (typeof window !== 'undefined') {
  // Catch unhandled errors
  window.addEventListener('error', (event) => {
    errorLogger.logError(
      'Unhandled error',
      event.error || new Error(event.message),
      {
        action: 'unhandled_error',
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
      }
    );
  });

  // Catch unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    errorLogger.logError(
      'Unhandled promise rejection',
      event.reason instanceof Error ? event.reason : new Error(String(event.reason)),
      {
        action: 'unhandled_rejection',
      }
    );
  });
}

