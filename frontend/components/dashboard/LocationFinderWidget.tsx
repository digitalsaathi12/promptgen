"use client";

import React, { useState } from "react";
import { Search, MapPin, Star } from "lucide-react";
import { MOCK_BUSINESS_RESULTS } from "@/lib/mock-data";
import BusinessResultCard from "./BusinessResultCard";

export default function LocationFinderWidget() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(MOCK_BUSINESS_RESULTS);

  const handleSearch = () => {
    if (query.trim()) {
      console.log("Mock searching location query:", query);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white p-5 rounded-2xl border border-gray-100/50 shadow-xs justify-between">
      <div className="space-y-4">
        {/* Header Title */}
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-gray-800 tracking-tight flex items-center gap-1.5">
            <MapPin className="h-4.5 w-4.5 text-primary-700" />
            Location Finder
          </h3>
          <button className="text-xs font-bold text-primary-700 hover:text-primary-800 transition-colors cursor-pointer">
            View All
          </button>
        </div>

        {/* Search Row */}
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute top-2.5 left-3.5 h-4.5 w-4.5 text-gray-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search any location or business..."
              className="w-full rounded-xl border border-gray-200 bg-gray-50 py-2 pr-4 pl-10 text-xs outline-hidden focus:border-primary-600 focus:bg-white transition-all duration-200"
            />
          </div>
          <button
            onClick={handleSearch}
            className="bg-primary-700 hover:bg-primary-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all duration-200 cursor-pointer shadow-2xs shadow-blue-500/10"
          >
            Search
          </button>
        </div>

        {/* Main Result Card */}
        <div className="space-y-3">
          {results.map((biz, idx) => (
            <BusinessResultCard key={idx} business={biz} />
          ))}
        </div>
      </div>

      {/* Competitors List Pinned at Bottom */}
      <div className="mt-5 border-t border-gray-100 pt-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-[11px] font-bold text-gray-700 uppercase tracking-wider">
            Nearby Competitors (2)
          </span>
          <button className="text-[10px] font-bold text-primary-700 hover:text-primary-800 transition-colors cursor-pointer">
            View All
          </button>
        </div>

        {/* Horizontal scroll list */}
        <div className="flex gap-3 overflow-x-auto pb-2 pr-1 custom-scrollbar">
          {results[0]?.nearby_competitors.map((comp, idx) => (
            <div
              key={idx}
              className="min-w-[190px] flex-1 p-3 bg-gray-50/50 rounded-xl border border-gray-100/30 flex flex-col justify-between"
            >
              <h5 className="text-[11px] font-bold text-gray-700 leading-snug line-clamp-1">
                {comp.business_name}
              </h5>
              <div className="flex items-center gap-1.5 mt-1">
                <div className="flex items-center">
                  <Star className="h-3 w-3 text-amber-400 fill-amber-400" />
                </div>
                <span className="text-[10px] font-bold text-gray-700">
                  {comp.rating}
                </span>
                <span className="text-[10px] text-gray-400 font-medium truncate">
                  {comp.address}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
