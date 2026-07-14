"use client";

import { SignOutButton, UserButton } from "@clerk/nextjs";

export default function Navbar() {
  return (
    <header className="border-b border-white/10 bg-slate-950/80 backdrop-blur-xl">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div>
          <p className="text-lg font-semibold tracking-[0.25em] text-cyan-300 uppercase">StudyAgent</p>
          <p className="text-sm text-slate-400">Autonomous research and study assistant</p>
        </div>
        <div className="flex items-center gap-3">
          <UserButton afterSignOutUrl="/sign-in" />
          <SignOutButton>
            <button className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-slate-100 transition hover:bg-white/10">
              Logout
            </button>
          </SignOutButton>
        </div>
      </div>
    </header>
  );
}