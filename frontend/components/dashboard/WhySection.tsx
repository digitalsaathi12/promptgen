"use client";

import React from "react";
import { WHY_FEATURES } from "@/lib/mock-data";
import { WhyFeature } from "@/lib/types";

interface WhySectionProps {
  features?: WhyFeature[];
}

export default function WhySection({ features = WHY_FEATURES }: WhySectionProps) {
  return (
    <div className="bg-white p-6 md:p-8 rounded-2xl border border-gray-100/50 shadow-sm">
      <div className="space-y-6">
        {/* Section Header */}
        <div className="space-y-1">
          <h2 className="text-base font-bold text-gray-800 tracking-tight">
            Why The Digital Saathi?
          </h2>
          <p className="text-xs text-gray-500 font-medium">
            Empowering your business with state-of-the-art AI tooling and location intelligence.
          </p>
        </div>

        {/* Benefits Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, i) => {
            const Icon = feature.icon;
            return (
              <div 
                key={i} 
                className="group flex flex-col p-5 rounded-xl bg-gray-50/50 border border-gray-100 hover:border-blue-100 hover:bg-white hover:shadow-xs transition-all duration-300 transform hover:-translate-y-0.5"
              >
                {/* Icon Wrapper */}
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-primary-700 transition-colors group-hover:bg-primary-700 group-hover:text-white mb-4 shrink-0">
                  <Icon className="h-5 w-5" />
                </div>
                {/* Text Content */}
                <div className="space-y-1">
                  <h3 className="text-sm font-bold text-gray-800 group-hover:text-primary-700 transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-xs text-gray-500 font-medium leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
