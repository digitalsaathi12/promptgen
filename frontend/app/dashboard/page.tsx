"use client";

import React, { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import WelcomeBanner from "@/components/dashboard/WelcomeBanner";
import FeatureCardGrid from "@/components/dashboard/FeatureCardGrid";
import LocationFinderWidget from "@/components/dashboard/LocationFinderWidget";
import AIChatWidget from "@/components/dashboard/AIChatWidget";
import RecentActivityWidget from "@/components/dashboard/RecentActivityWidget";
import WhySection from "@/components/dashboard/WhySection";
import QuoteCard from "@/components/dashboard/QuoteCard";
import ToolWorkspace from "@/components/dashboard/ToolWorkspace";

export default function DashboardPage() {
  const [currentTab, setCurrentTab] = useState("dashboard");

  const handleTabChange = (tab: string) => {
    setCurrentTab(tab);
  };

  const handleUseNow = (slug: string) => {
    setCurrentTab(slug);
  };

  const handleNavigateBack = () => {
    setCurrentTab("dashboard");
  };

  return (
    <DashboardLayout currentTab={currentTab} onTabChange={handleTabChange}>
      {currentTab !== "dashboard" ? (
        <div className="animate-fade-in">
          <ToolWorkspace tab={currentTab} onNavigateBack={handleNavigateBack} />
        </div>
      ) : (
        <div className="space-y-8 animate-fade-in">
          {/* Top Hero Welcome Section */}
          <WelcomeBanner userName="Krishna" />

          {/* Feature Tools Grid */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-gray-800 tracking-tight">
                AI Tools & Generators
              </h2>
              <span className="text-[10px] text-gray-400 font-bold uppercase tracking-wider">
                6 Modules Active
              </span>
            </div>
            <FeatureCardGrid onUseNow={handleUseNow} />
          </div>

          {/* Dynamic Interactive Widgets Row */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Location intelligence */}
            <div className="lg:col-span-1 min-h-[480px]">
              <LocationFinderWidget />
            </div>

            {/* Multi-AI Chat Panel */}
            <div className="lg:col-span-1 min-h-[480px]">
              <AIChatWidget />
            </div>

            {/* Activity Logs & History audit */}
            <div className="lg:col-span-1 min-h-[480px]">
              <RecentActivityWidget />
            </div>
          </div>

          {/* Bottom Benefits Highlights & Quote Details */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* 4 Core Value Propositions Grid */}
            <div className="lg:col-span-2">
              <WhySection />
            </div>

            {/* Premium Dark-navy Quote Tip widget */}
            <div className="lg:col-span-1">
              <QuoteCard />
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}
