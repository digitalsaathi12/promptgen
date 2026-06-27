"use client";

import React from "react";
import { ArrowRight } from "lucide-react";
import { FeatureCardItem } from "@/lib/types";

interface FeatureCardProps {
  card: FeatureCardItem;
  onUseNow?: (slug: string) => void;
}

export default function FeatureCard({ card, onUseNow }: FeatureCardProps) {
  const Icon = card.icon;
  // Resolve slugs from href properties
  const slug = card.href.replace("/", "");

  return (
    <div className="group flex flex-col justify-between p-6 bg-white rounded-2xl border border-gray-100/50 shadow-xs hover:shadow-md hover:border-blue-100 transition-all duration-300 transform hover:-translate-y-1">
      <div className="space-y-4">
        {/* Rounded badge Icon container */}
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50/70 text-primary-700 transition-colors group-hover:bg-primary-700 group-hover:text-white">
          <Icon className="h-5.5 w-5.5" />
        </div>

        {/* Card Title & description */}
        <div className="space-y-1.5">
          <h3 className="text-sm font-bold text-gray-800 tracking-tight group-hover:text-primary-700 transition-colors">
            {card.title}
          </h3>
          <p className="text-xs text-gray-400 font-medium leading-relaxed line-clamp-2">
            {card.description}
          </p>
        </div>
      </div>

      {/* Button action trigger */}
      <button
        onClick={() => onUseNow && onUseNow(slug)}
        className="mt-5 w-full flex items-center justify-center gap-1.5 bg-gray-50 group-hover:bg-primary-700 text-gray-700 group-hover:text-white text-xs font-bold py-2.5 rounded-xl transition-all duration-200 cursor-pointer border border-gray-100/50 group-hover:border-primary-700 shadow-2xs group-hover:shadow-xs shadow-blue-500/10"
      >
        Use Now
        <ArrowRight className="h-3.5 w-3.5 opacity-0 -translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-200" />
      </button>
    </div>
  );
}
