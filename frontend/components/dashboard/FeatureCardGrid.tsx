"use client";

import React from "react";
import { FEATURE_CARDS } from "@/lib/mock-data";
import FeatureCard from "./FeatureCard";

interface FeatureCardGridProps {
  onUseNow?: (slug: string) => void;
}

export default function FeatureCardGrid({ onUseNow }: FeatureCardGridProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 py-2">
      {FEATURE_CARDS.map((card, idx) => (
        <FeatureCard key={idx} card={card} onUseNow={onUseNow} />
      ))}
    </div>
  );
}
