import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Navbar from "@/components/Navbar";
import ChatWindow from "@/components/ChatWindow";

export default async function DashboardPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="mx-auto flex w-full max-w-7xl flex-1 px-4 py-4 sm:px-6 lg:px-8 lg:py-6">
        <ChatWindow userId={userId} />
      </main>
    </div>
  );
}