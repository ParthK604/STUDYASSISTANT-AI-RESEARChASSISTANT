"use client";

import { useRef } from "react";

const ACCEPTED_TYPES = ".pdf,.docx,.txt,.csv,.xlsx";

export default function UploadButton({ onUpload, isUploading }) {
  const inputRef = useRef(null);

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    await onUpload(file);
    event.target.value = "";
  };

  return (
    <>
      <input ref={inputRef} type="file" accept={ACCEPTED_TYPES} className="hidden" onChange={handleFileChange} />
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        disabled={isUploading}
        className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-slate-100 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isUploading ? "Uploading..." : "Upload"}
      </button>
    </>
  );
}