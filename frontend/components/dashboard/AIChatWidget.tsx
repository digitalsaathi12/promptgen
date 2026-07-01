"use client";

import React, { useRef, useEffect, useState } from "react";
import { MessageSquare, Send, ArrowUp, Bot } from "lucide-react";
import { MOCK_CHAT_MESSAGES } from "@/lib/mock-data";
import { ChatMessage } from "@/lib/types";
import { generateChat } from "@/lib/api";

interface AIChatWidgetProps {
  initialMessages?: ChatMessage[];
}

export default function AIChatWidget({ initialMessages }: AIChatWidgetProps) {
  const activeModel = "Gemini";
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages || MOCK_CHAT_MESSAGES);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat thread to bottom on updates
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessageText = input.trim();
    const userMsg: ChatMessage = {
      role: "user",
      text: userMessageText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      // Map history payload
      const historyPayload = messages.map(m => ({
        role: m.role,
        text: m.text
      }));

      const reply = await generateChat({
        message: userMessageText,
        history: historyPayload
      });

      const aiMsg: ChatMessage = {
        role: "ai",
        text: reply,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err: any) {
      console.error("[chat] error:", err);
      const errorMsg: ChatMessage = {
        role: "ai",
        text: "⚠️ System offline. Please check if the Python backend is running on http://localhost:8000.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col bg-white p-5 rounded-2xl border border-gray-100/50 shadow-xs h-full justify-between">
      <div className="space-y-4">
        {/* Header Section */}
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-gray-800 tracking-tight flex items-center gap-1.5">
            <MessageSquare className="h-4.5 w-4.5 text-primary-700" />
            Gemini AI Chat
          </h3>
          <span className="text-[10px] bg-emerald-50 text-emerald-600 px-2 py-0.5 rounded-full font-bold">
            Online
          </span>
        </div>

        {/* Gemini Badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 bg-blue-50 rounded-xl border border-blue-100">
          <span className="h-1.5 w-1.5 rounded-full bg-blue-500" />
          <span className="text-xs font-bold text-blue-700">Gemini 2.5 Flash</span>
        </div>

        {/* Chat Messages scroll area */}
        <div 
          ref={scrollRef}
          className="h-[280px] overflow-y-auto space-y-4 pr-1 custom-scrollbar"
        >
          {messages.map((msg, i) => {
            const isUser = msg.role === "user";
            return (
              <div 
                key={i} 
                className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}
              >
                <div className={`flex items-start gap-2 max-w-[85%]`}>
                  {!isUser && (
                    <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary-100 text-primary-700 shrink-0 text-[10px] font-bold">
                      <Bot className="h-3.5 w-3.5" />
                    </div>
                  )}
                  <div className={`p-3 rounded-2xl text-[11px] font-medium leading-relaxed ${
                    isUser 
                      ? "bg-primary-700 text-white rounded-tr-none" 
                      : "bg-gray-50 text-gray-700 border border-gray-100/50 rounded-tl-none whitespace-pre-line"
                  }`}>
                    {msg.text}
                  </div>
                </div>
                <span className="text-[9px] text-gray-400 font-semibold mt-1 px-1">
                  {msg.timestamp}
                </span>
              </div>
            );
          })}

          {loading && (
            <div className="flex flex-col items-start">
              <div className="flex items-start gap-2 max-w-[85%]">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary-100 text-primary-700 shrink-0 text-[10px] font-bold">
                  <Bot className="h-3.5 w-3.5 animate-bounce" />
                </div>
                <div className="p-3 bg-gray-50 text-gray-400 border border-gray-100/50 rounded-2xl rounded-tl-none text-[11px] font-medium animate-pulse">
                  Gemini is thinking...
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input Message box Pinned at Bottom */}
      <div className="mt-4 pt-3 border-t border-gray-50">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask Gemini anything..."
            className="flex-1 rounded-xl border border-gray-200 px-4 py-2 text-xs outline-hidden focus:border-primary-600 focus:bg-white transition-all duration-200"
          />
          <button
            onClick={handleSend}
            className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-700 hover:bg-primary-800 text-white shadow-xs cursor-pointer hover:scale-105 active:scale-95 transition-all"
            aria-label="Send message"
          >
            <Send className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
