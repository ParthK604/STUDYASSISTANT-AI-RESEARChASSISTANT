"use client";

import { useState } from "react";
import UploadButton from "@/components/UploadButton";

export default function ChatInput({ onSend, onUpload, isSending, isUploading }) {
  const [value, setValue] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    const didSend = await onSend(value);

    if (didSend !== null) {
      setValue("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-3xl border border-white/10 bg-slate-950/90 p-4 shadow-2xl shadow-cyan-950/20 backdrop-blur-xl">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-end">
        <textarea
          value={value}
          onChange={(event) => setValue(event.target.value)}
          rows={3}
          placeholder="Ask StudyAgent anything about your documents, research, or study plan..."
          className="min-h-[88px] flex-1 resize-none rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-100 outline-none transition placeholder:text-slate-500 focus:border-cyan-400/50 focus:ring-2 focus:ring-cyan-400/20"
        />
        <div className="flex items-center gap-3 lg:pb-1">
          <UploadButton onUpload={onUpload} isUploading={isUploading} />
          <button
            type="submit"
            disabled={isSending || !value.trim()}
            className="rounded-full bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSending ? "Sending..." : "Send"}
          </button>
        </div>
      </div>
    </form>
  );
}