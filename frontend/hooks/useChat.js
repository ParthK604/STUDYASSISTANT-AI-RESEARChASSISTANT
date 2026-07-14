"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { getConversation, queryAgent, uploadDocument } from "@/lib/api";

export function useChat(userId) {
  const [messages, setMessages] = useState([]);
  const [isLoadingConversation, setIsLoadingConversation] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");
  const toastTimer = useRef(null);

  const clearToastLater = useCallback((value) => {
    setToast(value);
    window.clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(() => setToast(""), 2600);
  }, []);

  const normalizedMessages = useMemo(
    () =>
      messages.map((message, index) => ({
        id: message.id || `${message.role}-${index}-${message.content.slice(0, 12)}`,
        ...message,
      })),
    [messages]
  );

  const fetchConversation = useCallback(async () => {
    if (!userId) return;

    setIsLoadingConversation(true);
    setError("");

    try {
      const data = await getConversation(userId);
      const items = Array.isArray(data) ? data : data?.messages || [];
      setMessages(
        items.map((message) => ({
          role: message.role,
          content: message.content,
          created_at: message.created_at,
        }))
      );
    } catch (err) {
      setError(err.message || "Unable to load conversation.");
      clearToastLater("Backend unavailable while loading conversation.");
    } finally {
      setIsLoadingConversation(false);
    }
  }, [clearToastLater, userId]);

  useEffect(() => {
    fetchConversation();
    return () => window.clearTimeout(toastTimer.current);
  }, [fetchConversation]);

  const sendMessage = useCallback(
    async (question) => {
      const trimmed = question.trim();

      if (!trimmed) {
        clearToastLater("Message cannot be empty.");
        return null;
      }

      const userMessage = {
        role: "user",
        content: trimmed,
        created_at: new Date().toISOString(),
      };

      setMessages((current) => [...current, userMessage]);
      setIsSending(true);
      setError("");

      try {
        const result = await queryAgent({ userId, question: trimmed });
        const answer = typeof result === "string" ? result : result?.answer || "";

        setMessages((current) => [
          ...current,
          {
            role: "assistant",
            content: answer,
            created_at: new Date().toISOString(),
          },
        ]);

        return answer;
      } catch (err) {
        setError(err.message || "Failed to send message.");
        clearToastLater("Unable to reach the backend.");
        setMessages((current) => current.slice(0, -1));
        return null;
      } finally {
        setIsSending(false);
      }
    },
    [clearToastLater, userId]
  );

  const uploadFile = useCallback(
    async (file) => {
      if (!file) return false;

      setIsUploading(true);
      setError("");

      try {
        await uploadDocument({ userId, file });
        clearToastLater("Document uploaded successfully.");
        return true;
      } catch (err) {
        setError(err.message || "Upload failed.");
        clearToastLater("Upload failed.");
        return false;
      } finally {
        setIsUploading(false);
      }
    },
    [clearToastLater, userId]
  );

  return {
    messages: normalizedMessages,
    isLoadingConversation,
    isSending,
    isUploading,
    error,
    toast,
    fetchConversation,
    sendMessage,
    uploadFile,
  };
}