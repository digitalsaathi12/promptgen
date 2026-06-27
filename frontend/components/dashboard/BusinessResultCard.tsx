"use client";

import React from "react";
import { MapPin, Phone, Globe, Star, ExternalLink, ShieldCheck } from "lucide-react";
import { BusinessResult } from "@/lib/types";

interface BusinessResultCardProps {
  business: BusinessResult;
}

export default function BusinessResultCard({ business }: BusinessResultCardProps) {
  // Helper to render rating stars
  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    for (let i = 0; i < 5; i++) {
      stars.push(
        <Star
          key={i}
          className={`h-3.5 w-3.5 ${
            i < fullStars
              ? "text-amber-400 fill-amber-400"
              : "text-gray-200 fill-gray-200"
          }`}
        />
      );
    }
    return stars;
  };

  return (
    <div className="flex flex-col md:flex-row gap-5 p-5 bg-gray-50/50 rounded-2xl border border-gray-100/30">
      {/* Left Column: Details */}
      <div className="flex-1 space-y-4">
        {/* Name and Verified Badge */}
        <div>
          <div className="flex items-start gap-2">
            <h4 className="text-sm font-bold text-gray-800 tracking-tight leading-snug">
              {business.business_name}
            </h4>
            <ShieldCheck className="h-4.5 w-4.5 text-blue-500 fill-blue-50 shrink-0" />
          </div>
          {/* Stars Row */}
          <div className="flex items-center gap-1.5 mt-1">
            <div className="flex items-center">{renderStars(business.rating)}</div>
            <span className="text-[11px] font-bold text-gray-700">
              {business.rating}
            </span>
            <span className="text-[11px] text-gray-400 font-medium">
              ({business.review_count} Reviews)
            </span>
          </div>
        </div>

        {/* Info Rows */}
        <div className="space-y-2 text-[11px] font-medium text-gray-600">
          <div className="flex items-start gap-2">
            <MapPin className="h-3.5 w-3.5 text-gray-400 shrink-0 mt-0.5" />
            <span>{business.address}</span>
          </div>

          {business.phone && (
            <div className="flex items-center gap-2">
              <Phone className="h-3.5 w-3.5 text-gray-400 shrink-0" />
              <span>{business.phone}</span>
            </div>
          )}

          {business.website && (
            <div className="flex items-center gap-2">
              <Globe className="h-3.5 w-3.5 text-gray-400 shrink-0" />
              <a
                href={business.website}
                target="_blank"
                rel="noreferrer"
                className="text-primary-700 hover:underline hover:text-primary-800 transition-colors"
              >
                {business.website.replace("https://", "").replace("www.", "")}
              </a>
            </div>
          )}
        </div>

        {/* Tags and External links */}
        <div className="flex flex-wrap items-center gap-2 pt-1.5">
          {business.category_tags.map((tag, idx) => (
            <span
              key={idx}
              className="px-2.5 py-1 text-[10px] font-bold text-gray-500 bg-white rounded-full border border-gray-100"
            >
              {tag}
            </span>
          ))}

          <a
            href={business.gmaps_link}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-[10px] font-bold text-primary-700 hover:text-primary-800 px-2 py-1 hover:bg-blue-50/50 rounded-lg transition-colors ml-auto"
          >
            Open in Google Maps
            <ExternalLink className="h-3 w-3" />
          </a>
        </div>
      </div>

      {/* Right Column: Image Thumbnail */}
      {business.image_url && (
        <div className="w-full md:w-32 h-32 md:h-auto rounded-xl overflow-hidden shrink-0 bg-gray-100 border border-gray-100">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={business.image_url}
            alt={business.business_name}
            className="w-full h-full object-cover"
          />
        </div>
      )}
    </div>
  );
}
