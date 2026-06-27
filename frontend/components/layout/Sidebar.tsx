"use client";

import React from "react";
import { Crown, Check, X, Bot } from "lucide-react";
import { SIDEBAR_ITEMS } from "@/lib/mock-data";
import { SidebarItem } from "@/lib/types";

interface SidebarProps {
  currentTab?: string;
  onTabChange?: (tab: string) => void;
  mobileOpen?: boolean;
  setMobileOpen?: (open: boolean) => void;
}

export default function Sidebar({
  currentTab = "dashboard",
  onTabChange = () => {},
  mobileOpen = false,
  setMobileOpen = () => {}
}: SidebarProps) {
  return (
    <>
      {/* Mobile Drawer Overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-gray-600/40 backdrop-blur-xs lg:hidden transition-opacity duration-300"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Main Sidebar Container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 flex w-[260px] flex-col justify-between border-r border-gray-100 bg-white px-4 py-6 transition-transform duration-300 ease-in-out lg:translate-x-0 ${
          mobileOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Top Section: Logo & Toggle Close */}
        <div>
          <div className="flex items-center justify-between mb-8 px-2">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-700 text-white shadow-md shadow-blue-500/20">
                <Bot className="h-6 w-6" />
              </div>
              <div>
                <h1 className="text-base font-bold text-navy-900 leading-none">
                  The Digital Saathi
                </h1>
                <span className="text-[10px] text-gray-400 font-medium tracking-tight">
                  AI Powered. Result Driven.
                </span>
              </div>
            </div>
            {/* Mobile close button */}
            <button
              className="rounded-lg p-1 text-gray-500 hover:bg-gray-50 lg:hidden"
              onClick={() => setMobileOpen(false)}
              aria-label="Close sidebar menu"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-1 overflow-y-auto max-h-[calc(100vh-340px)] pr-1 custom-scrollbar">
            {SIDEBAR_ITEMS.map((item: SidebarItem) => {
              const Icon = item.icon;
              const isActive = currentTab === item.slug;
              return (
                <button
                  key={item.slug}
                  onClick={() => {
                    onTabChange(item.slug);
                    setMobileOpen(false); // Close on mobile click
                  }}
                  className={`flex w-full items-center gap-3 px-3 py-2.5 text-sm font-medium rounded-xl transition-all duration-200 cursor-pointer ${
                    isActive
                      ? "bg-primary-700 text-white shadow-xs shadow-blue-500/10"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  }`}
                >
                  <Icon
                    className={`h-4.5 w-4.5 ${
                      isActive ? "text-white" : "text-gray-400"
                    }`}
                  />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Bottom Pinned Card: Upgrade to Pro */}
        <div className="mt-6">
          <div className="rounded-2xl bg-blue-50/70 p-4 border border-blue-100/50">
            <div className="flex items-center gap-2 mb-3">
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary-100 text-primary-700">
                <Crown className="h-4 w-4" />
              </div>
              <span className="text-xs font-bold text-primary-900">
                Upgrade to Pro
              </span>
            </div>
            <ul className="space-y-1.5 mb-4 text-[11px] text-gray-600 font-medium">
              {[
                "Unlimited Prompts",
                "Image Generation",
                "Location & Leads",
                "Competitor Analysis",
                "Priority Support"
              ].map((feature, i) => (
                <li key={i} className="flex items-center gap-2">
                  <Check className="h-3 w-3 text-primary-600 stroke-[3]" />
                  {feature}
                </li>
              ))}
            </ul>
            <button className="w-full bg-primary-700 hover:bg-primary-800 text-white text-xs font-bold py-2 rounded-xl transition-all duration-200 shadow-xs shadow-blue-500/10 cursor-pointer">
              Upgrade Now
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
