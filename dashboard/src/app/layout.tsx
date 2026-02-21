import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Athena - Executive Dashboard',
  description: 'Proactive Program Management',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-slate-900 text-slate-100 min-h-screen flex flex-col`}>
        <nav className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between shadow-lg">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
              Project Athena
            </h1>
          </div>
          <div className="flex gap-6">
            <Link href="/" className="hover:text-blue-400 transition-colors">Health Overview</Link>
            <Link href="/chat" className="hover:text-blue-400 transition-colors">Chat Interface</Link>
            <Link href="/god-mode" className="text-red-400 hover:text-red-300 transition-colors font-medium">God Mode</Link>
          </div>
        </nav>
        <main className="flex-1 p-8 max-w-7xl mx-auto w-full">
          {children}
        </main>
      </body>
    </html>
  )
}
