import { LucideIcon } from "lucide-react";

export interface SidebarItem {
  icon: any; // LucideIcon component reference
  label: string;
  slug: string;
}

export interface FeatureCardItem {
  icon: any;
  title: string;
  description: string;
  href: string;
}

export interface Coordinate {
  lat: string;
  lon: string;
}

export interface CompetitorItem {
  business_name: string;
  address: string;
  rating: number;
  coordinates: Coordinate;
}

export interface BusinessResult {
  business_name: string;
  address: string;
  phone?: string;
  website?: string;
  rating: number;
  review_count: number;
  gmaps_link: string;
  coordinates: Coordinate;
  category_tags: string[];
  image_url?: string;
  nearby_competitors: CompetitorItem[];
}

export interface ChatMessage {
  role: "user" | "ai";
  text: string;
  timestamp: string;
}

export interface RecentActivity {
  icon: any;
  title: string;
  time: string;
}

export interface WhyFeature {
  icon: any;
  title: string;
  description: string;
}
