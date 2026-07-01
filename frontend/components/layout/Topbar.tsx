"use client";

import React, { useState } from "react";
import { Search, Globe, Clock, Bell, ChevronDown, Menu, LogOut, Settings, User } from "lucide-react";

interface TopbarProps {
  onMenuClick: () => void;
}

export default function Topbar({ onMenuClick }: TopbarProps) {
  const [lang, setLang] = useState("English");
  const [langOpen, setLangOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-gray-100 bg-white px-6 shadow-xs">
      {/* Left: Mobile hamburger menu toggle & Search bar */}
      <div className="flex flex-1 items-center gap-4">
        <button
          onClick={onMenuClick}
          className="rounded-lg p-1.5 text-gray-500 hover:bg-gray-50 lg:hidden cursor-pointer"
          aria-label="Open menu drawer"
        >
          <Menu className="h-5.5 w-5.5" />
        </button>

        {/* Search Bar Input */}
        <div className="relative w-full max-w-md hidden sm:block">
          <Search className="absolute top-2.5 left-3.5 h-4.5 w-4.5 text-gray-400" />
          <input
            type="text"
            placeholder="Search prompts, tools, or anything..."
            className="w-full rounded-full border border-gray-200 bg-gray-50 py-2 pr-4 pl-10 text-sm outline-hidden focus:border-primary-600 focus:bg-white transition-all duration-200"
          />
        </div>
      </div>

      {/* Right Side: Options & User Avatar */}
      <div className="flex items-center gap-3 md:gap-4">
        {/* Globe Language Selector */}
        <div className="relative">
          <button
            onClick={() => setLangOpen(!langOpen)}
            onBlur={() => setTimeout(() => setLangOpen(false), 200)}
            className="flex items-center gap-1.5 rounded-lg px-2 py-1.5 text-sm font-medium text-gray-600 hover:bg-gray-50 cursor-pointer"
          >
            <Globe className="h-4.5 w-4.5 text-gray-400" />
            <span className="hidden md:inline">{lang}</span>
            <ChevronDown className="h-4 w-4 text-gray-400" />
          </button>

          {langOpen && (
            <div className="absolute right-0 mt-1 w-32 rounded-xl border border-gray-100 bg-white py-1 shadow-lg ring-1 ring-black/5 z-40">
              {["English", "Hindi", "Hinglish"].map((l) => (
                <button
                  key={l}
                  onClick={() => setLang(l)}
                  className="w-full px-4 py-2 text-left text-xs font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900 cursor-pointer"
                >
                  {l}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* History / Clock Button */}
        <button
          className="rounded-lg p-2 text-gray-500 hover:bg-gray-50 cursor-pointer"
          aria-label="View generation history"
        >
          <Clock className="h-4.5 w-4.5 text-gray-400 hover:text-gray-700 transition-colors" />
        </button>

        {/* Notifications Bell */}
        <button
          className="relative rounded-lg p-2 text-gray-500 hover:bg-gray-50 cursor-pointer"
          aria-label="Open notifications menu"
        >
          <Bell className="h-4.5 w-4.5 text-gray-400 hover:text-gray-700 transition-colors" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-red-500 ring-2 ring-white" />
        </button>

        {/* Divider line */}
        <div className="h-6 w-px bg-gray-100" />

        {/* User Profile Avatar block */}
        <div className="relative">
          <button
            onClick={() => setProfileOpen(!profileOpen)}
            onBlur={() => setTimeout(() => setProfileOpen(false), 200)}
            className="flex items-center gap-2 rounded-lg p-1 text-left hover:bg-gray-50 cursor-pointer"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary-100 font-bold text-primary-700 shadow-sm border border-primary-200">
              A
            </div>
            <div className="hidden md:block pr-1">
              <p className="text-xs font-bold text-gray-700 leading-none">
                Admin User
              </p>
              <span className="text-[10px] text-gray-400 font-medium">
                Enterprise
              </span>
            </div>
            <ChevronDown className="h-3.5 w-3.5 text-gray-400 hidden md:block" />
          </button>

          {profileOpen && (
            <div className="absolute right-0 mt-1 w-48 rounded-2xl border border-gray-100 bg-white p-1.5 shadow-lg ring-1 ring-black/5 z-40">
              <button className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900 cursor-pointer">
                <User className="h-4 w-4 text-gray-400" />
                Profile
              </button>
              <button className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900 cursor-pointer">
                <Settings className="h-4 w-4 text-gray-400" />
                Settings
              </button>
              <div className="my-1 border-t border-gray-50" />
              <button className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium text-red-600 hover:bg-red-50/50 cursor-pointer">
                <LogOut className="h-4 w-4 text-red-400" />
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
