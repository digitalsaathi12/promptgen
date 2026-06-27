import {
  LayoutDashboard,
  BookOpen,
  PenLine,
  FileText,
  Zap,
  Image as ImageIcon,
  MapPin,
  BarChart2,
  MessageSquare,
  Bookmark,
  History,
  Bot,
  Clock,
  TrendingUp
} from "lucide-react";
import { SidebarItem, FeatureCardItem, BusinessResult, ChatMessage, RecentActivity, WhyFeature } from "./types";

export const SIDEBAR_ITEMS: SidebarItem[] = [
  { icon: LayoutDashboard, label: "Dashboard", slug: "dashboard" },
  { icon: BookOpen, label: "Prompt Library", slug: "prompt-library" },
  { icon: PenLine, label: "Prompt Generator", slug: "prompt-generator" },
  { icon: FileText, label: "Script Generator", slug: "script-generator" },
  { icon: Zap, label: "Viral Hooks", slug: "viral-hooks" },
  { icon: ImageIcon, label: "Image Generator", slug: "image-generator" },
  { icon: MapPin, label: "Location Finder", slug: "location-finder" },
  { icon: BarChart2, label: "Competitor Analysis", slug: "competitor-analysis" },
  { icon: MessageSquare, label: "AI Chat (Multi AI)", slug: "ai-chat" },
  { icon: Bookmark, label: "Saved Results", slug: "saved-results" },
  { icon: History, label: "History", slug: "history" }
];

export const FEATURE_CARDS: FeatureCardItem[] = [
  {
    icon: BookOpen,
    title: "Prompt Library",
    description: "1000+ ready prompts for any need.",
    href: "/prompt-library"
  },
  {
    icon: PenLine,
    title: "Prompt Generator",
    description: "Create powerful prompts instantly.",
    href: "/prompt-generator"
  },
  {
    icon: FileText,
    title: "Script Generator",
    description: "Generate blog, reel, video & ad scripts.",
    href: "/script-generator"
  },
  {
    icon: Zap,
    title: "Viral Hooks",
    description: "Get viral hooks for reels, shorts & ads.",
    href: "/viral-hooks"
  },
  {
    icon: ImageIcon,
    title: "Image Generator",
    description: "Generate image prompts or AI images.",
    href: "/image-generator"
  },
  {
    icon: MapPin,
    title: "Location Finder",
    description: "Find business, leads & location details instantly.",
    href: "/location-finder"
  }
];

export const MOCK_BUSINESS_RESULTS: BusinessResult[] = [
  {
    business_name: "Sri Ram Dental Clinic & Orthodontic Center",
    address: "102, Saket Nagar, Opp. High School Road, Indore, Madhya Pradesh, 452001, India",
    phone: "+91 99887 76655",
    website: "https://sriramdentalclinic.in",
    rating: 4.8,
    review_count: 128,
    gmaps_link: "https://www.google.com/maps/search/?api=1&query=22.7246,75.8547",
    coordinates: { lat: "22.7246", lon: "75.8547" },
    category_tags: ["Dental Clinic", "Clinic", "Healthcare"],
    image_url: "https://images.unsplash.com/photo-1629909613654-28e377c37b09?w=300&auto=format&fit=crop&q=60",
    nearby_competitors: [
      {
        business_name: "Indore Smile Dental Care",
        address: "Vijay Nagar Near C21 Mall, Indore",
        rating: 4.5,
        coordinates: { lat: "22.7266", lon: "75.8567" }
      },
      {
        business_name: "Apex Healthcare & Dental Clinic",
        address: "Saket Nagar Lane 4, Indore",
        rating: 4.2,
        coordinates: { lat: "22.7226", lon: "75.8527" }
      }
    ]
  }
];

export const MOCK_CHAT_MESSAGES: ChatMessage[] = [
  {
    role: "user",
    role_type: "user", // backward compat if needed
    text: "Mera ek restaurant business hai, uske liye Hinglish ad copies likhiye.",
    timestamp: "12:44 PM"
  } as any,
  {
    role: "ai",
    text: "नमस्ते! यहाँ आपके restaurant के लिए Hinglish ad copy है:\n\n🔥 **Hook:** 'घर का खाना मिस कर रहे हो? Stop scrolling!'\n👉 **Body:** 'Sri Ram Bhojanalaya में पाइए शुद्ध देशी घी से बनी थाली। स्वाद ऐसा जो माँ के हाथ की याद दिला दे।'\n🚀 **CTA:** 'थाली आर्डर करने के लिए नीचे दिए गए बटन पर अभी क्लिक करें!'",
    timestamp: "12:45 PM"
  }
];

export const MOCK_ACTIVITIES: RecentActivity[] = [
  {
    icon: PenLine,
    title: "Generated prompt for Dental Clinic Ad",
    time: "2 mins ago"
  },
  {
    icon: MapPin,
    title: "Found 10 businesses in Neemuch",
    time: "15 mins ago"
  },
  {
    icon: ImageIcon,
    title: "Generated image prompt for Shoe Poster",
    time: "1 hour ago"
  },
  {
    icon: BarChart2,
    title: "Competitor analysis for competitor.com",
    time: "3 hours ago"
  },
  {
    icon: FileText,
    title: "Generated script for Travel Agency Reel",
    time: "Yesterday"
  }
];

export const WHY_FEATURES: WhyFeature[] = [
  {
    icon: Bot,
    title: "Multi AI Support",
    description: "Works with ChatGPT, Gemini & Claude"
  },
  {
    icon: MapPin,
    title: "Location Intelligence",
    description: "Get location, leads, reviews & competitors"
  },
  {
    icon: Clock,
    title: "Save Time",
    description: "Generate content 10x faster"
  },
  {
    icon: TrendingUp,
    title: "Business Growth",
    description: "Perfect for marketers & agencies"
  }
];
