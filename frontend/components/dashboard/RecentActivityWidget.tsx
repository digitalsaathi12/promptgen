"use client";

import React from "react";
import { History, ArrowRight } from "lucide-react";
import { MOCK_ACTIVITIES } from "@/lib/mock-data";
import { RecentActivity } from "@/lib/types";

interface RecentActivityWidgetProps {
  activities?: RecentActivity[];
}

export default function RecentActivityWidget({ activities = MOCK_ACTIVITIES }: RecentActivityWidgetProps) {
  return (
    <div className="flex flex-col bg-white p-5 rounded-2xl border border-gray-100/50 shadow-xs h-full justify-between">
      <div className="space-y-4">
        {/* Header Title */}
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-gray-800 tracking-tight flex items-center gap-1.5">
            <History className="h-4.5 w-4.5 text-primary-700" />
            Recent Activity
          </h3>
          <button className="text-xs font-bold text-primary-700 hover:text-primary-800 transition-colors cursor-pointer">
            View All
          </button>
        </div>

        {/* Activity Items List */}
        <div className="space-y-4 max-h-[300px] overflow-y-auto pr-1 custom-scrollbar">
          {activities.map((act, i) => {
            const Icon = act.icon;
            return (
              <div key={i} className="flex items-center justify-between gap-3 group">
                <div className="flex items-center gap-3">
                  {/* Circular icon indicator */}
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50/50 text-primary-700 group-hover:bg-primary-100 transition-colors shrink-0">
                    <Icon className="h-4.5 w-4.5" />
                  </div>
                  <div>
                    <p className="text-[11px] font-bold text-gray-700 leading-snug line-clamp-2">
                      {act.title}
                    </p>
                    <span className="text-[9px] text-gray-400 font-semibold">
                      {act.time}
                    </span>
                  </div>
                </div>

                {/* Arrow indicator */}
                <button 
                  className="rounded-lg p-1 text-gray-300 hover:text-primary-600 hover:bg-gray-50/50 transition-colors shrink-0 cursor-pointer"
                  aria-label="View activity detail"
                >
                  <ArrowRight className="h-3.5 w-3.5" />
                </button>
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Bottom spacer or details */}
      <div className="mt-4 pt-3 border-t border-gray-50 flex items-center justify-between text-[10px] text-gray-400 font-semibold">
        <span>Total Logs: {activities.length}</span>
        <span>Filter: All</span>
      </div>
    </div>
  );
}
