"use client";

import { useEffect, useRef } from "react";
import ChatMessage from "@/components/ChatMessage";
import ChatInput from "@/components/ChatInput";
import TypingIndicator from "@/components/TypingIndicator";
import { useChat } from "@/hooks/useChat";

export default function ChatWindow({ userId }) {
  const { messages, isLoadingConversation, isSending, isUploading, toast, sendMessage, uploadFile } = useChat(userId);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length, isSending]);

  return (
    <div className="flex min-h-0 flex-1 flex-col gap-4">
      {toast ? (
        <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/10 px-4 py-3 text-sm text-cyan-200">
          {toast}
        </div>
      ) : null}

      <div className="flex min-h-0 flex-1 flex-col rounded-[2rem] border border-white/10 bg-slate-950/70 shadow-2xl shadow-cyan-950/10 backdrop-blur-xl">
        <div className="flex-1 space-y-4 overflow-y-auto px-4 py-5 sm:px-6">
          {isLoadingConversation ? (
            <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300">Loading conversation...</div>
          ) : messages.length === 0 ? (
            <div className="flex min-h-[40vh] items-center justify-center rounded-3xl border border-dashed border-white/10 bg-white/[0.03] px-6 text-center text-sm text-slate-400">
              Start the conversation by asking a question or uploading a document.
            </div>
          ) : (
            messages.map((message, index) => <ChatMessage key={message.id || index} role={message.role} content={message.content} />)
          )}
          {isSending ? <TypingIndicator /> : null}
          <div ref={bottomRef} />
        </div>
        <div className="border-t border-white/10 p-4 sm:p-6">
          <ChatInput onSend={sendMessage} onUpload={uploadFile} isSending={isSending} isUploading={isUploading} />
        </div>
      </div>
    </div>
  );
}