"use client";

import React, { useState, useRef, useEffect } from "react";
import { MessageSquare, Send, ArrowUp, Bot } from "lucide-react";
import { MOCK_CHAT_MESSAGES } from "@/lib/mock-data";
import { ChatMessage } from "@/lib/types";

interface AIChatWidgetProps {
  initialMessages?: ChatMessage[];
}

export default function AIChatWidget({ initialMessages }: AIChatWidgetProps) {
  const [activeModel, setActiveModel] = useState<"ChatGPT" | "Gemini" | "Claude">("ChatGPT");
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages || MOCK_CHAT_MESSAGES);
  const [input, setInput] = useState("");
  
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat thread to bottom on updates
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg: ChatMessage = {
      role: "user",
      text: input.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    // Simulate AI response stream delay
    setTimeout(() => {
      const aiResponse = getSimulatedResponse(input.trim(), activeModel);
      const aiMsg: ChatMessage = {
        role: "ai",
        text: aiResponse,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, aiMsg]);
    }, 800);
  };

  const getSimulatedResponse = (query: string, model: string): string => {
    const q = query.toLowerCase();
    if (q.includes("restaurant") || q.includes("hotel") || q.includes("food")) {
      return `[Response from ${model} in Hinglish]\n\nयहाँ आपके restaurant के लिए 2 Hooks और Taglines हैं:\n\n1. "भूख लगी है? Direct Sri Ram Dhaba! 🍽️"\n2. "देशी स्वाद, माँ के हाथों जैसा प्यार!"\n\nAd copy के लिए Prompt Library का use करें।`;
    }
    if (q.includes("dentist") || q.includes("clinic") || q.includes("doctor")) {
      return `[Response from ${model}]\n\nFor a dentist clinic in Indore, I recommend targeting localized keywords like 'best dentist in Indore near me' and 'affordable tooth cleaning Vijay Nagar'.`;
    }
    return `[Response from ${model}]\n\nThat is an interesting topic! I can help you compile marketing copies or prompts. Let me know which module (Script, Hooks, or SEO) you would like to construct.`;
  };

  return (
    <div className="flex flex-col bg-white p-5 rounded-2xl border border-gray-100/50 shadow-xs h-full justify-between">
      <div className="space-y-4">
        {/* Header Section */}
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-gray-800 tracking-tight flex items-center gap-1.5">
            <MessageSquare className="h-4.5 w-4.5 text-primary-700" />
            AI Chat (Multi AI)
          </h3>
          <span className="text-[10px] bg-emerald-50 text-emerald-600 px-2 py-0.5 rounded-full font-bold">
            Online
          </span>
        </div>

        {/* Model Selector Tabs */}
        <div className="flex bg-gray-50/70 p-1 rounded-xl border border-gray-100">
          {(["ChatGPT", "Gemini", "Claude"] as const).map((model) => {
            const isSelected = activeModel === model;
            const dotColor = 
              model === "ChatGPT" 
                ? "bg-emerald-500" 
                : model === "Gemini" 
                  ? "bg-blue-500" 
                  : "bg-orange-500";
                  
            return (
              <button
                key={model}
                onClick={() => setActiveModel(model)}
                className={`flex-1 flex items-center justify-center gap-1.5 py-1.5 text-xs font-bold rounded-lg transition-all duration-200 cursor-pointer ${
                  isSelected 
                    ? "bg-white text-gray-800 shadow-2xs border border-gray-100" 
                    : "text-gray-400 hover:text-gray-600"
                }`}
              >
                <span className={`h-1.5 w-1.5 rounded-full ${dotColor}`} />
                {model}
              </button>
            );
          })}
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
            placeholder={`Ask ${activeModel} anything...`}
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
