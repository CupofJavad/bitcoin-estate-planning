import NextAuth from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const authOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        try {
          // Login to FastAPI backend
          const loginResponse = await fetch(`${API_URL}/api/v1/auth/jwt/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
              username: credentials.email,
              password: credentials.password,
            }),
          })

          if (!loginResponse.ok) {
            const errorText = await loginResponse.text()
            console.error('Login failed:', errorText)
            return null
          }

          // Check if response has content before parsing
          const loginText = await loginResponse.text()
          if (!loginText || loginText.trim() === '') {
            console.error('Login response is empty')
            return null
          }

          let loginData
          try {
            loginData = JSON.parse(loginText)
          } catch (e) {
            console.error('Failed to parse login response:', loginText)
            return null
          }

          // Get user info
          const userResponse = await fetch(`${API_URL}/api/v1/auth/users/me`, {
            headers: {
              Authorization: `Bearer ${loginData.access_token}`,
            },
          })

          if (!userResponse.ok) {
            const errorText = await userResponse.text()
            console.error('Get user failed:', errorText)
            return null
          }

          // Check if response has content before parsing
          const userText = await userResponse.text()
          if (!userText || userText.trim() === '') {
            console.error('User response is empty')
            return null
          }

          let user
          try {
            user = JSON.parse(userText)
          } catch (e) {
            console.error('Failed to parse user response:', userText)
            return null
          }

          return {
            id: user.id.toString(),
            email: user.email,
            name: user.full_name || user.email,
            accessToken: loginData.access_token,
          }
        } catch (error) {
          console.error('Auth error:', error)
          return null
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.accessToken
        token.id = user.id
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.accessToken = token.accessToken as string
        session.user.id = token.id as string
      }
      return session
    },
  },
  pages: {
    signIn: '/login',
    error: '/login', // Redirect errors to login
  },
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  secret: process.env.NEXTAUTH_SECRET,
  debug: process.env.NODE_ENV === 'development',
  // Ensure proper error handling for session fetching
  events: {
    async signIn({ user }) {
      console.log('Sign in event:', { user: user?.email })
    },
    async signOut() {
      console.log('Sign out event')
    },
  },
}

const { handlers } = NextAuth(authOptions)

export const { GET, POST } = handlers

