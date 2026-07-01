"use client";

import React from "react";

interface WelcomeBannerProps {
  userName?: string;
}

export default function WelcomeBanner() {
  return (
    <div className="relative overflow-hidden rounded-3xl bg-linear-to-r from-blue-700 via-blue-800 to-indigo-900 p-8 md:p-10 text-white shadow-xl">
      {/* Decorative vector sparkle/star indicators in the corners */}
      <div className="absolute top-6 right-8 text-blue-200/25 pointer-events-none text-2xl select-none">✨</div>
      <div className="absolute bottom-6 left-8 text-blue-200/20 pointer-events-none text-xl select-none">✨</div>

      <div className="flex flex-col md:flex-row items-center justify-between gap-8 relative z-10">
        {/* Left text column */}
        <div className="space-y-3 max-w-xl text-center md:text-left">
          <span className="text-xs font-semibold uppercase tracking-wider text-blue-200/80">
            Welcome to
          </span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">
            The Digital Saathi ✨
          </h2>
          <p className="text-sm md:text-base font-normal text-blue-100/90 leading-relaxed">
            All-in-one AI Toolkit for Prompts, Content, Images, Location Data & Business Growth. 
            Optimize campaigns instantly in English, Hindi, and Hinglish.
          </p>
        </div>

        {/* Right Mascot column */}
        <div className="flex items-center gap-4 flex-col sm:flex-row">
          {/* Speech Bubble */}
          <div className="relative bg-white text-gray-800 text-xs font-bold px-4 py-3 rounded-2xl shadow-lg border border-blue-100 max-w-[200px] text-center sm:text-left animate-bounce duration-1000">
            Hello! I'm your AI Saathi. How can I help you today?
            {/* Speech bubble pointer */}
            <div className="absolute bottom-[-6px] left-1/2 -translate-x-1/2 sm:left-auto sm:right-[-6px] sm:top-1/2 sm:bottom-auto sm:-translate-y-1/2 w-3 h-3 bg-white rotate-45 border-r border-b border-blue-50" />
          </div>

          {/* SVG Robot Mascot Illustration */}
          <div className="w-24 h-24 flex items-center justify-center rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 shadow-inner">
            <svg
              className="h-16 w-16 text-blue-100"
              viewBox="0 0 64 64"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              {/* Head body */}
              <rect x="14" y="16" width="36" height="28" rx="8" fill="#ffffff" />
              <rect x="14" y="16" width="36" height="28" rx="8" stroke="#3b82f6" strokeWidth="2" />
              {/* Screen eyes face area */}
              <rect x="20" y="22" width="24" height="12" rx="4" fill="#1e3a8a" />
              {/* Eyes */}
              <circle cx="26" cy="28" r="3" fill="#60a5fa" />
              <circle cx="38" cy="28" r="3" fill="#60a5fa" />
              {/* Ears */}
              <rect x="8" y="24" width="6" height="12" rx="3" fill="#93c5fd" />
              <rect x="50" y="24" width="6" height="12" rx="3" fill="#93c5fd" />
              {/* Antenna */}
              <line x1="32" y1="16" x2="32" y2="8" stroke="#ffffff" strokeWidth="3" />
              <circle cx="32" cy="7" r="4" fill="#f59e0b" />
              {/* Mouth line */}
              <path d="M28 39H36" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
