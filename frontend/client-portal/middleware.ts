import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  // Check if the request is for a protected route
  const { pathname } = request.nextUrl
  
  // Public routes that don't require authentication
  const publicRoutes = [
    "/login",
    "/register",
    "/api/auth",
    "/_next",
    "/favicon.ico",
  ]
  
  // Check if the current path is a public route
  const isPublicRoute = publicRoutes.some(route => pathname.startsWith(route))
  
  if (isPublicRoute) {
    return NextResponse.next()
  }
  
  // For protected routes, we'll check authentication in the page components
  // The actual auth check happens via useSession hook in ProtectedRoute component
  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico|login|register).*)"],
}

