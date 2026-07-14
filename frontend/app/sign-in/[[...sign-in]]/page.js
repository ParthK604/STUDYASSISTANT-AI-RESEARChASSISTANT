import { SignIn } from "@clerk/nextjs";

export default function Page() {
  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-10">
      <div className="w-full max-w-md rounded-[2rem] border border-white/10 bg-slate-950/80 p-6 shadow-2xl shadow-cyan-950/20 backdrop-blur-xl sm:p-8">
        <div className="mb-6 text-center">
          <p className="text-2xl font-semibold tracking-[0.22em] text-cyan-300 uppercase">StudyAgent</p>
          <p className="mt-2 text-sm text-slate-400">Sign in to continue your research workspace.</p>
        </div>
        <SignIn routing="path" path="/sign-in" signUpUrl="/sign-up" afterSignInUrl="/dashboard" />
      </div>
    </div>
  );
}