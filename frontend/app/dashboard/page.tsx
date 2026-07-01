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
      {/* ── Work-in-Progress tabs ── */}
      {(currentTab === "prompt-library" || currentTab === "location-finder") ? (
        <div className="flex flex-col items-center justify-center min-h-[70vh] animate-fade-in text-center px-6">
          {/* Animated icon ring */}
          <div className="relative mb-8">
            <div className="h-24 w-24 rounded-full bg-primary-50 flex items-center justify-center">
              <span className="text-5xl">🚧</span>
            </div>
            <span className="absolute -top-1 -right-1 flex h-5 w-5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-400 opacity-75"></span>
              <span className="relative inline-flex h-5 w-5 rounded-full bg-primary-600"></span>
            </span>
          </div>

          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            {currentTab === "prompt-library" ? "Prompt Library" : "Location Finder"}
          </h2>
          <p className="text-base font-semibold text-primary-600 mb-3 uppercase tracking-wider">
            Work in Progress
          </p>
          <p className="text-gray-500 max-w-md mb-8 leading-relaxed">
            {currentTab === "prompt-library"
              ? "We're building a curated library of 1000+ ready-to-use prompts across every category. It'll be ready soon!"
              : "The Location Finder with Google Maps integration and lead extraction is under active development. Stay tuned!"}
          </p>

          {/* Progress bar */}
          <div className="w-64 h-2 bg-gray-100 rounded-full overflow-hidden mb-6">
            <div
              className="h-full bg-gradient-to-r from-primary-500 to-primary-700 rounded-full"
              style={{ width: currentTab === "prompt-library" ? "45%" : "30%" }}
            />
          </div>
          <p className="text-xs text-gray-400 mb-8">
            {currentTab === "prompt-library" ? "45%" : "30%"} complete
          </p>

          <button
            onClick={handleNavigateBack}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-700 text-white text-sm font-semibold hover:bg-primary-800 transition-colors shadow-md shadow-blue-500/20"
          >
            ← Back to Dashboard
          </button>
        </div>

      /* ── All other non-dashboard tabs go to ToolWorkspace ── */
      ) : currentTab !== "dashboard" ? (
        <div className="animate-fade-in">
          <ToolWorkspace tab={currentTab} onNavigateBack={handleNavigateBack} />
        </div>
      ) : (
        <div className="space-y-8 animate-fade-in">
          {/* Top Hero Welcome Section */}
          <WelcomeBanner />

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
