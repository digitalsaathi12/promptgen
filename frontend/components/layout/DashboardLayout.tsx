"use client";

import React, { useState } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

interface DashboardLayoutProps {
  children: React.ReactNode;
  currentTab?: string;
  onTabChange?: (tab: string) => void;
}

export default function DashboardLayout({
  children,
  currentTab = "dashboard",
  onTabChange
}: DashboardLayoutProps) {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50/50">
      {/* Sidebar Frame */}
      <Sidebar
        currentTab={currentTab}
        onTabChange={onTabChange}
        mobileOpen={mobileSidebarOpen}
        setMobileOpen={setMobileSidebarOpen}
      />

      {/* Main Content Grid Frame */}
      <div className="flex flex-col lg:pl-[260px]">
        {/* Topbar frame */}
        <Topbar onMenuClick={() => setMobileSidebarOpen(true)} />

        {/* Content Wrapper */}
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
