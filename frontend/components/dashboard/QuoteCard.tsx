"use client";

import React from "react";
import { Sparkles } from "lucide-react";

interface QuoteCardProps {
  quote?: string;
  author?: string;
  role?: string;
}

export default function QuoteCard({
  quote = "The best way to predict the future is to invent it. Let your AI Saathi draft your next viral marketing copy, script, or location intelligence prompt to grow 10x faster.",
  author = "Digital Saathi Bot",
  role = "Your Smart AI Assistant"
}: QuoteCardProps) {
  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 via-navy-900 to-slate-950 p-6 text-white border border-slate-800/80 shadow-md h-full flex flex-col justify-between group">
      {/* Decorative ambient background blur lights */}
      <div className="absolute -top-12 -right-12 h-32 w-32 rounded-full bg-blue-500/10 blur-xl group-hover:bg-blue-500/20 transition-all duration-500" />
      <div className="absolute -bottom-12 -left-12 h-32 w-32 rounded-full bg-indigo-500/10 blur-xl group-hover:bg-indigo-500/20 transition-all duration-500" />

      {/* Decorative Quote mark SVG in background */}
      <div className="absolute right-4 bottom-4 opacity-5 pointer-events-none transition-transform duration-500 group-hover:scale-110">
        <svg
          width="120"
          height="120"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M3 21c3 0 7-9 7-13a4 4 0 1 0-8 0c0 4 4.5 9 7 13Z" />
          <path d="M14 21c3 0 7-9 7-13a4 4 0 1 0-8 0c0 4 4.5 9 7 13Z" />
        </svg>
      </div>

      <div className="relative space-y-4">
        {/* Sparkle badge */}
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-xs font-bold text-blue-300">
          <Sparkles className="h-3.5 w-3.5" />
          Tip of the Day
        </div>

        {/* Quote text */}
        <p className="text-xs md:text-sm font-medium italic leading-relaxed text-slate-100 font-serif">
          &ldquo;{quote}&rdquo;
        </p>
      </div>

      {/* Author Details */}
      <div className="relative mt-6 pt-4 border-t border-slate-800/60 flex items-center gap-3">
        {/* Avatar Placeholder */}
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 font-bold text-xs text-white shadow-sm ring-2 ring-slate-800 shrink-0">
          DS
        </div>
        <div>
          <h4 className="text-[11px] font-bold text-slate-200 tracking-wide">
            {author}
          </h4>
          <p className="text-[9px] text-slate-400 font-semibold">
            {role}
          </p>
        </div>
      </div>
    </div>
  );
}
