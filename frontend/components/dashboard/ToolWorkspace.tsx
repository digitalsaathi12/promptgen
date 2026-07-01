"use client";

import React, { useState, useEffect } from "react";
import { generateHooks, generateImagePrompt, generateVideoScript, generateContent, generatePrompt } from "@/lib/api";
import { 
  Sparkles, Copy, Check, RefreshCw, Info, Settings, Play, Download, Bookmark,
  History, MapPin, Star, AlertCircle, HelpCircle, Eye, Trash2, Heart, Award,
  Compass, Laptop, Flame, Video, Image as ImageIcon, Search, ChevronDown, CheckSquare,
  BookOpen
} from "lucide-react";
import LocationFinderWidget from "./LocationFinderWidget";
import AIChatWidget from "./AIChatWidget";
import RecentActivityWidget from "./RecentActivityWidget";

interface ToolWorkspaceProps {
  tab: string;
  onNavigateBack: () => void;
}

export default function ToolWorkspace({ tab, onNavigateBack }: ToolWorkspaceProps) {
  // Global States
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [isFavorited, setIsFavorited] = useState(false);
  const [activeOutputTab, setActiveOutputTab] = useState<string>("Expert Prompt");
  const [result, setResult] = useState<any>(null);
  const [activePreset, setActivePreset] = useState<string>("");
  const [apiError, setApiError] = useState<string | null>(null);

  // Validation state
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  // Tooltip Helper state
  const [activeTooltip, setActiveTooltip] = useState<string | null>(null);

  // 1. PROMPT GENERATOR FIELDS
  const [pBusinessName, setPBusinessName] = useState("Digital Saathi OS");
  const [pIndustry, setPIndustry] = useState("Marketing & SaaS");
  const [pSubIndustry, setPSubIndustry] = useState("AI Tools");
  const [pDescription, setPDescription] = useState("All-in-one AI operating system for Indian entrepreneurs.");
  const [pCategory, setPCategory] = useState("Marketing");
  const [pType, setPType] = useState("Instagram Ad");
  const [pAudience, setPAudience] = useState("Small business owners, local marketers");
  const [pAgeGroup, setPAgeGroup] = useState("25-45");
  const [pLocation, setPLocation] = useState("Indore, Madhya Pradesh");
  const [pLanguage, setPLanguage] = useState("Hinglish");
  const [pGender, setPGender] = useState("All Genders");
  const [pPainPoints, setPPainPoints] = useState("Lack of technical copywriting skills, high cost of agencies");
  const [pGoal, setPGoal] = useState("Generate Leads");
  const [pOffer, setPOffer] = useState("Free 7-Day Trial on our AI Toolkit");
  const [pPlatform, setPPlatform] = useState("Instagram");
  const [pTone, setPTone] = useState("Bold");
  const [pDepth, setPDepth] = useState("Advanced");
  const [pModel, setPModel] = useState("Gemini");
  const [pLength, setPLength] = useState("Medium");
  const [pCreativity, setPCreativity] = useState(7);
  const [pCta, setPCta] = useState(true);
  const [pHashtags, setPHashtags] = useState(true);
  const [pEmojis, setPEmojis] = useState(true);
  const [pSeoKeywords, setPSeoKeywords] = useState(true);
  const [pCompetitor, setPCompetitor] = useState(true);
  const [pMultipleVersions, setPMultipleVersions] = useState(false);
  const [pVariationsCount, setPVariationsCount] = useState(3);

  // 2. SCRIPT GENERATOR FIELDS
  const [sBusinessName, setSBusinessName] = useState("Indore Smiles Dental");
  const [sIndustry, setSIndustry] = useState("Healthcare");
  const [sPlatform, setSPlatform] = useState("Instagram Reel");
  const [sDuration, setSDuration] = useState("30 sec");
  const [sStyle, setSStyle] = useState("Educational");
  const [sHookType, setSHookType] = useState("Pain Point");
  const [sAudience, setSAudience] = useState("People looking for painless tooth implants in Vijay Nagar");
  const [sLanguage, setSLanguage] = useState("Hinglish");
  const [sTone, setSTone] = useState("Warm & Conversational");
  const [sCtaStyle, setSCtaStyle] = useState("Strong");
  const [sVisualStyle, setSVisualStyle] = useState("Talking Head");
  const [sIncludeBreakdown, setSIncludeBreakdown] = useState(true);
  const [sIncludeAngles, setSIncludeAngles] = useState(true);
  const [sIncludeShotList, setSIncludeShotList] = useState(true);
  const [sIncludeVoScript, setSIncludeVoScript] = useState(true);
  const [sIncludeCaption, setSIncludeCaption] = useState(true);
  const [sIncludeHashtags, setSIncludeHashtags] = useState(true);
  const [sIncludeThumbnail, setSIncludeThumbnail] = useState(true);
  const [sIncludeYoutubeDesc, setSIncludeYoutubeDesc] = useState(false);

  // 3. VIRAL HOOK GENERATOR FIELDS
  const [hBusinessName, setHBusinessName] = useState("A1 Gym & Fitness");
  const [hIndustry, setHIndustry] = useState("Fitness & Wellness");
  const [hContentType, setHContentType] = useState("Reel");
  const [hGoal, setHGoal] = useState("Stop Scroll");
  const [hHookType, setHHookType] = useState("Curiosity");
  const [hAudience, setHAudience] = useState("Busy working professionals trying to lose weight");
  const [hLanguage, setHLanguage] = useState("English");
  const [hCount, setHCount] = useState("10");
  const [hLength, setHLength] = useState("Medium");
  const [hCta, setHCta] = useState(true);
  const [hEmojis, setHEmojis] = useState(true);

  // 4. IMAGE GENERATOR FIELDS
  const [iBusinessName, setIBusinessName] = useState("Premium Saffron Chai");
  const [iIndustry, setIIndustry] = useState("Food & Beverage");
  const [iPurpose, setIPurpose] = useState("Social Media");
  const [iStyle, setIStyle] = useState("Cinematic");
  const [iEngine, setIEngine] = useState("FLUX");
  const [iAspect, setIAspect] = useState("16:9");
  const [iResolution, setIResolution] = useState("4K");
  const [iLighting, setILighting] = useState("Golden Hour");
  const [iCamera, setICamera] = useState("DSLR");
  const [iLens, setILens] = useState("50mm");
  const [iColorTheme, setIColorTheme] = useState("Warm orange and earthy brass tones");
  const [iBackground, setIBackground] = useState("Gradient");
  const [iSubject, setISubject] = useState("A steaming ceramic cup of cardamom tea placed next to saffron threads");
  const [iTopic, setITopic] = useState("Traditional Indian Chai Morning Vibe");
  const [iOffer, setIOffer] = useState("Monsoon Special Offer");
  const [iNegative, setINegative] = useState("lowres, bad quality, blurry, text, logo, watermark, artificial colors");
  const [iRefStyle, setIRefStyle] = useState("Commercial Safe");
  const [iHighDetail, setIHighDetail] = useState(true);
  const [iUltraQuality, setIUltraQuality] = useState(true);
  const [iMultiVariations, setIMultiVariations] = useState(false);
  const [iUpscale, setIUpscale] = useState(true);
  const [iRemoveBg, setIRemoveBg] = useState(false);

  // 5. LOCATION FINDER FIELDS
  const [lCategory, setLCategory] = useState("Dentists");
  const [lIndustry, setLIndustry] = useState("Dental Clinics");
  const [lKeyword, setLKeyword] = useState("implants");
  const [lCity, setLCity] = useState("Indore");
  const [lState, setLState] = useState("Madhya Pradesh");
  const [lCountry, setLCountry] = useState("India");
  const [lRadius, setLRadius] = useState("5 KM");
  const [lMinRating, setLMinRating] = useState("4.5+");
  const [lOpenNow, setLOpenNow] = useState(true);
  const [lVerifiedOnly, setLVerifiedOnly] = useState(true);
  const [lHasWebsite, setLHasWebsite] = useState(true);
  const [lHasPhone, setLHasPhone] = useState(true);
  const [lHasEmail, setLHasEmail] = useState(false);
  const [lHasSocial, setLHasSocial] = useState(false);
  const [lMaxResults, setLMaxResults] = useState("25");
  const [lSortBy, setLSortBy] = useState("Highest Rated");

  // Dynamic Suggestion based on Industry Selection
  const [aiSuggestions, setAiSuggestions] = useState<string[]>([]);

  useEffect(() => {
    // Generate AI suggestions when industry changes
    const ind = tab === "prompt-generator" ? pIndustry : 
                tab === "script-generator" ? sIndustry : 
                tab === "viral-hooks" ? hIndustry : 
                tab === "image-generator" ? iIndustry : lIndustry;

    if (ind.toLowerCase().includes("food") || ind.toLowerCase().includes("sweet") || ind.toLowerCase().includes("restaurant")) {
      setAiSuggestions([
        "💡 Focus on sensory copywriting (aroma, texture, taste).",
        "💡 Launch a 'Limited Time Monsoon Offer' campaign.",
        "💡 Visual suggestion: High contrast warm golden hour lighting for food close-ups."
      ]);
    } else if (ind.toLowerCase().includes("health") || ind.toLowerCase().includes("dent")) {
      setAiSuggestions([
        "💡 Emphasize safety protocols, painless treatment, and verified doctor reviews.",
        "💡 Call-to-action preset: 'Book free initial checkup appointment'.",
        "💡 Leverage local keywords 'Best dentist in Indore saket area'."
      ]);
    } else {
      setAiSuggestions([
        "💡 Structure outputs using Direct Response copywriting models.",
        "💡 Exclude aggressive sales language to boost organic reach.",
        "💡 Highlight primary problem solved within the first 3 seconds."
      ]);
    }
  }, [pIndustry, sIndustry, hIndustry, iIndustry, lIndustry, tab]);

  // Load Presets
  const loadPreset = (presetName: string) => {
    setActivePreset(presetName);
    if (tab === "prompt-generator") {
      if (presetName === "sweets") {
        setPBusinessName("Sri Ram Sweets");
        setPIndustry("Food & Restaurant");
        setPSubIndustry("Indian Desserts");
        setPDescription("Serving authentic desi ghee sweets in Indore since 1995.");
        setPCategory("Social Media");
        setPType("Instagram Caption");
        setPAudience("Families, sweet lovers, and festival shoppers");
        setPGoal("Increase Sales");
        setPOffer("Buy 1Kg Kaju Katli, Get 250g Free");
        setPPlatform("Instagram");
        setPTone("Storytelling");
        setPLanguage("Hinglish");
      } else if (presetName === "realestate") {
        setPBusinessName("Indore Prime Realty");
        setPIndustry("Real Estate");
        setPSubIndustry("Residential Housing");
        setPDescription("Modern 2 & 3 BHK luxury apartments in Vijay Nagar.");
        setPCategory("Marketing");
        setPType("Facebook Ad");
        setPAudience("Young families, IT professionals, first-time home buyers");
        setPGoal("Generate Leads");
        setPOffer("Free Site Visit & Spot Booking Gold Coin Gift");
        setPPlatform("Facebook");
        setPTone("Luxury");
        setPLanguage("English");
      }
    } else if (tab === "script-generator") {
      if (presetName === "medical") {
        setSBusinessName("Apex Care Hospital");
        setSIndustry("Healthcare");
        setSPlatform("Instagram Reel");
        setSDuration("45 sec");
        setSStyle("Educational");
        setSHookType("Curiosity");
        setSAudience("People looking for regular health checkups");
        setSTone("Professional & Trustworthy");
        setSCtaStyle("Soft");
      }
    } else if (tab === "image-generator") {
      if (presetName === "ads") {
        setIBusinessName("Smart Running Shoes");
        setIIndustry("Athletic Wear");
        setIPurpose("Facebook Ad");
        setIStyle("Cyberpunk");
        setIEngine("FLUX");
        setIAspect("1:1");
        setIResolution("4K");
        setILighting("Neon");
        setISubject("A high-tech glowing running shoe floating in neon dark rainy street background");
        setIColorTheme("Electric blue and neon magenta");
      }
    }
  };

  // Export handlers
  const exportToTxt = () => {
    if (!result) return;
    const txtContent = typeof result === "string" ? result : JSON.stringify(result, null, 2);
    const element = document.createElement("a");
    const file = new Blob([txtContent], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = `${tab}_brief_output.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const exportToMarkdown = () => {
    if (!result) return;
    const mdHeader = `# The Digital Saathi - AI Brief Engine Export\n\n`;
    const txtContent = typeof result === "string" ? result : JSON.stringify(result, null, 2);
    const element = document.createElement("a");
    const file = new Blob([mdHeader + txtContent], {type: 'text/markdown'});
    element.href = URL.createObjectURL(file);
    element.download = `${tab}_brief_output.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const triggerPrintPDF = () => {
    window.print();
  };

  // Copy result utility
  const handleCopyResult = () => {
    const textToCopy = typeof result === "string" ? result : JSON.stringify(result, null, 2);
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Form Validation
  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    if (tab === "prompt-generator") {
      if (!pBusinessName.trim()) errors.businessName = "Business Name is required";
      if (!pIndustry.trim()) errors.industry = "Industry is required";
      if (!pCategory.trim()) errors.category = "Category is required";
      if (!pType.trim()) errors.type = "Prompt Type is required";
      if (!pAudience.trim()) errors.audience = "Target Audience is required";
      if (!pGoal.trim()) errors.goal = "Goal is required";
      if (!pOffer.trim()) errors.offer = "Offer/Topic is required";
    }
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleBriefSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    setResult(null);
    setApiError(null);

    try {
      // ── PROMPT GENERATOR: calls /api/v1/generate/prompt ──
      if (tab === "prompt-generator") {
        const output = await generatePrompt({
          business: pBusinessName,
          industry: pIndustry,
          sub_industry: pSubIndustry,
          description: pDescription,
          category: pCategory,
          prompt_type: pType,
          audience: pAudience,
          age_group: pAgeGroup,
          location: pLocation,
          language: pLanguage,
          gender: pGender,
          pain_points: pPainPoints,
          goal: pGoal,
          offer: pOffer,
          platform: pPlatform,
          tone: pTone,
          depth: pDepth,
          model: pModel,
          length: pLength,
          creativity: pCreativity,
          cta: pCta,
          hashtags: pHashtags,
          emojis: pEmojis,
          seo_keywords: pSeoKeywords,
          competitor: pCompetitor,
          multiple_versions: pMultipleVersions,
          variations_count: pVariationsCount,
        });

        setResult({
          "Expert Prompt": output.expert_prompt,
          "Optimized Prompt": output.optimized_prompt,
          "Gemini Prompt": output.gemini_prompt,
          "Prompt Explanation": output.explanation,
          "Raw JSON": JSON.stringify(output, null, 2),
        });
        setActiveOutputTab("Expert Prompt");

      // ── VIRAL HOOKS: calls /api/v1/generate/hooks ──
      } else if (tab === "viral-hooks") {
        const resolvedPlatform: "Instagram" | "YouTube" | "Facebook" | "LinkedIn" =
          hContentType === "YouTube" ? "YouTube" :
          hContentType === "Facebook" ? "Facebook" :
          hContentType === "LinkedIn" ? "LinkedIn" : "Instagram";

        const output = await generateHooks({
          niche: `${hIndustry} — ${hBusinessName}`,
          audience: hAudience,
          platform: resolvedPlatform,
          count: parseInt(hCount, 10),
          language: hLanguage,
          hook_type: hHookType,
          goal: hGoal,
          length: hLength,
          cta: hCta,
          emojis: hEmojis,
        });
        // Format the hooks array into readable text for the output panel
        const hooksText = output.hooks
          .map((h: any, i: number) => {
            const ctaLine = h.cta ? `\n   ↳ CTA: ${h.cta}` : "";
            return `${i + 1}. [${h.type.toUpperCase()}] ${h.text}${ctaLine}`;
          })
          .join("\n\n");
        setResult({
          "Hooks Output": `🔥 **${output.hooks.length} VIRAL HOOKS — Powered by Gemini:**\n\n${hooksText}`,
          "Raw JSON": JSON.stringify(output, null, 2),
        });
        setActiveOutputTab("Hooks Output");

      // ── IMAGE PROMPT: calls /api/v1/generate/image-prompt ──
      } else if (tab === "image-generator") {
        const output = await generateImagePrompt({
          subject: iSubject,
          business: iBusinessName,
          industry: iIndustry,
          topic: iTopic,
          offer: iOffer,
          purpose: iPurpose,
          style: iStyle,
          engine: iEngine,
          aspect: iAspect,
          resolution: iResolution,
          lighting: iLighting,
          camera: iCamera,
          lens: iLens,
          color_theme: iColorTheme,
          background: iBackground,
          negative: iNegative,
          ref_style: iRefStyle,
          high_detail: iHighDetail,
          ultra_quality: iUltraQuality,
        });
        setResult({
          "Image Prompt Studio": `🎨 **GEMINI IMAGE PROMPT (${output.suggested_tool}):**\n\n"${output.image_prompt}"`,
          "Negative Prompt": `🚫 **NEGATIVE CONSTRAINTS:**\n\n"${output.negative_prompt}"`,
          "Parameters": `⚙️ **RECOMMENDED TOOL:** ${output.suggested_tool}\n- Aspect Ratio: ${iAspect}\n- Resolution: ${iResolution}\n- Engine: ${iEngine}\n- Background Removal: ${iRemoveBg ? "Active" : "Bypassed"}`,
        });
        setActiveOutputTab("Image Prompt Studio");

      // ── VIDEO SCRIPT: calls /api/v1/generate/video-script ──
      } else if (tab === "script-generator") {
        const durationMap: Record<string, number> = {
          "15 sec": 15, "30 sec": 30, "45 sec": 45,
          "60 sec": 60, "90 sec": 90, "3 min": 180, "5 min": 300
        };
        const seconds = durationMap[sDuration] ?? 30;
        const output = await generateVideoScript({
          business: sBusinessName,
          industry: sIndustry,
          platform: sPlatform,
          duration: sDuration,
          duration_seconds: seconds,
          style: sStyle,
          hook_type: sHookType,
          audience: sAudience,
          language: sLanguage,
          tone: sTone,
          cta_style: sCtaStyle,
          visual_style: sVisualStyle,
          include_breakdown: sIncludeBreakdown,
          include_angles: sIncludeAngles,
          include_shot_list: sIncludeShotList,
          include_vo_script: sIncludeVoScript,
          include_caption: sIncludeCaption,
          include_hashtags: sIncludeHashtags,
          include_thumbnail: sIncludeThumbnail,
          include_youtube_desc: sIncludeYoutubeDesc,
        });
        const scriptResult: Record<string, string> = {
          "Visual Script": `🎬 **HOOK:**\n${output.hook}\n\n📝 **SCRIPT:**\n${output.script}`,
          "CTA": `📣 **CALL TO ACTION:**\n\n${output.cta}`,
        };
        if (output.shot_list?.length) scriptResult["Shot List"] = output.shot_list.join("\n");
        if (output.social_caption) scriptResult["Caption"] = `📱 **SOCIAL CAPTION:**\n\n${output.social_caption}`;
        if (output.hashtags) scriptResult["Hashtags"] = `#️⃣ **HASHTAGS:**\n\n${output.hashtags}`;
        if (output.thumbnail_concept) scriptResult["Thumbnail"] = `🖼️ **THUMBNAIL CONCEPT:**\n\n${output.thumbnail_concept}`;
        if (output.youtube_description) scriptResult["YouTube Desc"] = output.youtube_description;
        scriptResult["Raw JSON"] = JSON.stringify(output, null, 2);
        setResult(scriptResult);
        setActiveOutputTab("Visual Script");

      // ── CONTENT WRITER: falls through to location-finder (local mock) ──
      } else if (tab === "location-finder") {
        setResult({
          "Leads Output":
            `📍 **LOCAL BUSINESS LEADS FOUND IN ${lCity}:**\n\n` +
            `1. **Sri Ram Dental Clinic Saket**\n` +
            `   - Phone: +91 99887 76655 | Rating: 4.8 ⭐\n\n` +
            `2. **Apex Smile Care Vijay Nagar**\n` +
            `   - Phone: +91 98989 88888 | Rating: 4.6 ⭐\n\n` +
            `3. **Indore Orthodontic Center**\n` +
            `   - Phone: +91 95555 44444 | Rating: 4.7 ⭐`,
        });
        setActiveOutputTab("Leads Output");
      }
    } catch (err: any) {
      console.error("[generate] API error:", err);
      setApiError(err?.message ?? "Something went wrong. Make sure the Python backend is running on port 8000.");
    } finally {
      setLoading(false);
      setIsSaved(false);
    }
  };

  // Saved templates logger
  const handleSaveResult = () => {
    setIsSaved(true);
  };

  const handleFavoriteResult = () => {
    setIsFavorited(!isFavorited);
  };

  // Render Tooltip Modal/Bubble
  const toggleTooltip = (fieldId: string) => {
    if (activeTooltip === fieldId) {
      setActiveTooltip(null);
    } else {
      setActiveTooltip(fieldId);
    }
  };

  // Render Form UI based on Tab
  const renderGeneratorForm = () => {
    if (tab === "prompt-generator") {
      return (
        <form onSubmit={handleBriefSubmit} className="space-y-6">
          {/* Presets Row */}
          <div className="flex flex-wrap items-center gap-2 pb-2">
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Presets:</span>
            <button 
              type="button" 
              onClick={() => loadPreset("sweets")}
              className={`px-3 py-1 text-[11px] font-bold rounded-full border transition-all cursor-pointer ${
                activePreset === "sweets" 
                  ? "bg-primary-700 text-white border-primary-700 shadow-xs" 
                  : "bg-white text-gray-600 border-gray-100 hover:bg-gray-50"
              }`}
            >
              Indian Sweets Campaign
            </button>
            <button 
              type="button" 
              onClick={() => loadPreset("realestate")}
              className={`px-3 py-1 text-[11px] font-bold rounded-full border transition-all cursor-pointer ${
                activePreset === "realestate" 
                  ? "bg-primary-700 text-white border-primary-700 shadow-xs" 
                  : "bg-white text-gray-600 border-gray-100 hover:bg-gray-50"
              }`}
            >
              Indore Luxury Real Estate
            </button>
          </div>

          {/* Section 1: Business Fundamentals */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-2">
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-primary-100 text-[10px] font-bold text-primary-700">1</span>
              <h4 className="text-xs font-bold text-gray-800 uppercase tracking-wide">Brand & Business Fundamentals</h4>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-1 relative">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide flex items-center gap-1">
                  Business Name <span className="text-red-500">*</span>
                  <button type="button" onClick={() => toggleTooltip("pBusinessName")} className="text-gray-400 hover:text-primary-700">
                    <Info className="h-3 w-3" />
                  </button>
                </label>
                {activeTooltip === "pBusinessName" && (
                  <div className="absolute z-30 bg-gray-900 text-white text-[9px] p-2 rounded-lg shadow-md -top-10 left-0 w-44 font-semibold">
                    Enter the name of your shop, store, startup, or website.
                  </div>
                )}
                <input
                  type="text"
                  value={pBusinessName}
                  onChange={(e) => setPBusinessName(e.target.value)}
                  className={`w-full rounded-xl border py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium ${
                    validationErrors.businessName ? "border-red-500" : "border-gray-200"
                  }`}
                  required
                />
                {validationErrors.businessName && (
                  <span className="text-[9px] text-red-500 font-bold flex items-center gap-1 mt-1">
                    <AlertCircle className="h-3 w-3" /> {validationErrors.businessName}
                  </span>
                )}
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide flex items-center gap-1">
                  Industry <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={pIndustry}
                  onChange={(e) => setPIndustry(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium"
                  required
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Sub Industry</label>
                <input
                  type="text"
                  value={pSubIndustry}
                  onChange={(e) => setPSubIndustry(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Business Description</label>
              <textarea
                value={pDescription}
                onChange={(e) => setPDescription(e.target.value)}
                rows={2}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium resize-none"
              />
            </div>
          </div>

          {/* Section 2: Prompt Details */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-2">
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-primary-100 text-[10px] font-bold text-primary-700">2</span>
              <h4 className="text-xs font-bold text-gray-800 uppercase tracking-wide">Brief Target & Optimization Goals</h4>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Prompt Category *</label>
                <select
                  value={pCategory}
                  onChange={(e) => setPCategory(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="Marketing">Marketing</option>
                  <option value="SEO">SEO</option>
                  <option value="Sales">Sales</option>
                  <option value="Coding">Coding</option>
                  <option value="Social Media">Social Media</option>
                  <option value="Blog Writing">Blog Writing</option>
                  <option value="Email">Email</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Prompt Type *</label>
                <select
                  value={pType}
                  onChange={(e) => setPType(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="Instagram Ad">Instagram Ad</option>
                  <option value="Facebook Ad">Facebook Ad</option>
                  <option value="Google Ads">Google Ads</option>
                  <option value="Landing Page">Landing Page</option>
                  <option value="Sales Copy">Sales Copy</option>
                  <option value="Cold Email">Cold Email</option>
                  <option value="Instagram Caption">Instagram Caption</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Goal *</label>
                <select
                  value={pGoal}
                  onChange={(e) => setPGoal(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="Increase Sales">Increase Sales</option>
                  <option value="Generate Leads">Generate Leads</option>
                  <option value="Brand Awareness">Brand Awareness</option>
                  <option value="Website Traffic">Website Traffic</option>
                  <option value="Engagement">Engagement</option>
                  <option value="Conversions">Conversions</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Offer / Topic *</label>
                <input
                  type="text"
                  value={pOffer}
                  onChange={(e) => setPOffer(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium"
                  required
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Channel / Platform *</label>
                <select
                  value={pPlatform}
                  onChange={(e) => setPPlatform(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="Instagram">Instagram</option>
                  <option value="Facebook">Facebook</option>
                  <option value="LinkedIn">LinkedIn</option>
                  <option value="YouTube">YouTube</option>
                  <option value="WhatsApp">WhatsApp</option>
                  <option value="Website">Website</option>
                </select>
              </div>
            </div>
          </div>

          {/* Section 3: Target Audience */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-2">
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-primary-100 text-[10px] font-bold text-primary-700">3</span>
              <h4 className="text-xs font-bold text-gray-800 uppercase tracking-wide">Target Audience Profile</h4>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Primary Target Audience *</label>
                <input
                  type="text"
                  value={pAudience}
                  onChange={(e) => setPAudience(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium"
                  required
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Age Group</label>
                <input
                  type="text"
                  value={pAgeGroup}
                  onChange={(e) => setPAgeGroup(e.target.value)}
                  placeholder="e.g. 18-35"
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Geographic Location</label>
                <input
                  type="text"
                  value={pLocation}
                  onChange={(e) => setPLocation(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Gender Targeting</label>
                <select
                  value={pGender}
                  onChange={(e) => setPGender(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="All Genders">All Genders</option>
                  <option value="Male Only">Male Only</option>
                  <option value="Female Only">Female Only</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Customer Pain Points</label>
                <input
                  type="text"
                  value={pPainPoints}
                  onChange={(e) => setPPainPoints(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium"
                />
              </div>
            </div>
          </div>

          {/* Section 4: Style & Presets */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-2">
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-primary-100 text-[10px] font-bold text-primary-700">4</span>
              <h4 className="text-xs font-bold text-gray-800 uppercase tracking-wide">Style & AI Parameters</h4>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Tone Preset *</label>
                <select
                  value={pTone}
                  onChange={(e) => setPTone(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="Professional">Professional</option>
                  <option value="Friendly">Friendly</option>
                  <option value="Luxury">Luxury</option>
                  <option value="Funny">Funny</option>
                  <option value="Bold">Bold</option>
                  <option value="Emotional">Emotional</option>
                  <option value="Storytelling">Storytelling</option>
                  <option value="Educational">Educational</option>
                  <option value="Urgent">Urgent</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Language *</label>
                <select
                  value={pLanguage}
                  onChange={(e) => setPLanguage(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="English">English</option>
                  <option value="Hindi">Hindi (हिंदी)</option>
                  <option value="Hinglish">Hinglish (Hindi + English)</option>
                  <option value="Marathi">Marathi</option>
                  <option value="Gujarati">Gujarati</option>
                  <option value="Tamil">Tamil</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Prompt Depth *</label>
                <select
                  value={pDepth}
                  onChange={(e) => setPDepth(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="Basic">Basic</option>
                  <option value="Standard">Standard</option>
                  <option value="Advanced">Advanced</option>
                  <option value="Expert">Expert</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Target AI Model *</label>
                <select
                  value={pModel}
                  onChange={(e) => setPModel(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="Gemini">Gemini 2.5 Flash</option>
                  <option value="Llama">Llama (Local)</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Output Length *</label>
                <select
                  value={pLength}
                  onChange={(e) => setPLength(e.target.value)}
                  className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 focus:ring-2 focus:ring-primary-500/20 transition-all font-medium cursor-pointer"
                >
                  <option value="Short">Short</option>
                  <option value="Medium">Medium</option>
                  <option value="Long">Long</option>
                  <option value="Very Detailed">Very Detailed</option>
                </select>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between">
                  <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Creativity Level (0-10)</label>
                  <span className="text-xs font-bold text-primary-700">{pCreativity}</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="10"
                  value={pCreativity}
                  onChange={(e) => setPCreativity(parseInt(e.target.value))}
                  className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-700"
                />
              </div>
            </div>
          </div>

          {/* Section 5: Configuration Checkboxes */}
          <div className="space-y-4 bg-gray-50/50 p-4 rounded-2xl border border-gray-100">
            <h4 className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Output Modifiers</h4>
            
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {[
                { label: "Include CTA", val: pCta, set: setPCta },
                { label: "Include Hashtags", val: pHashtags, set: setPHashtags },
                { label: "Include Emojis", val: pEmojis, set: setPEmojis },
                { label: "Include SEO Keywords", val: pSeoKeywords, set: setPSeoKeywords },
                { label: "Competitor Analysis", val: pCompetitor, set: setPCompetitor }
              ].map((item, idx) => (
                <label key={idx} className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                  <input
                    type="checkbox"
                    checked={item.val}
                    onChange={(e) => item.set(e.target.checked)}
                    className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                  />
                  {item.label}
                </label>
              ))}
            </div>

            <div className="border-t border-gray-100 pt-3 flex flex-col sm:flex-row items-start sm:items-center gap-4">
              <label className="flex items-center gap-2 text-xs font-bold text-gray-700 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={pMultipleVersions}
                  onChange={(e) => setPMultipleVersions(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Generate Multiple Versions
              </label>

              {pMultipleVersions && (
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-bold text-gray-500 uppercase">Variations:</span>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={pVariationsCount}
                    onChange={(e) => setPVariationsCount(parseInt(e.target.value))}
                    className="w-14 rounded-lg border border-gray-200 py-1 px-2 text-xs text-center font-bold"
                  />
                </div>
              )}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-primary-700 hover:bg-primary-800 text-white text-xs font-bold py-3 rounded-xl transition-all cursor-pointer shadow-md hover:shadow-lg active:scale-98"
          >
            {loading ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                Compiling AI Brief & Generating Prompts...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4" />
                Formulate Prompt Brief
              </>
            )}
          </button>
        </form>
      );
    }

    if (tab === "script-generator") {
      return (
        <form onSubmit={handleBriefSubmit} className="space-y-6">
          <div className="flex flex-wrap items-center gap-2 pb-2">
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Presets:</span>
            <button 
              type="button" 
              onClick={() => loadPreset("medical")}
              className="px-3 py-1 text-[11px] font-bold rounded-full border bg-white text-gray-600 border-gray-100 hover:bg-gray-50 cursor-pointer"
            >
              Dental Service Reel
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Business Name</label>
              <input
                type="text"
                value={sBusinessName}
                onChange={(e) => setSBusinessName(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Industry</label>
              <input
                type="text"
                value={sIndustry}
                onChange={(e) => setSIndustry(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Target Platform</label>
              <select
                value={sPlatform}
                onChange={(e) => setSPlatform(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium cursor-pointer"
              >
                <option value="Instagram Reel">Instagram Reel</option>
                <option value="YouTube Shorts">YouTube Shorts</option>
                <option value="TikTok">TikTok</option>
                <option value="Facebook">Facebook</option>
                <option value="LinkedIn">LinkedIn</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Video Duration</label>
              <select
                value={sDuration}
                onChange={(e) => setSDuration(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium cursor-pointer"
              >
                <option value="15 sec">15 sec</option>
                <option value="30 sec">30 sec</option>
                <option value="45 sec">45 sec</option>
                <option value="60 sec">60 sec</option>
                <option value="90 sec">90 sec</option>
                <option value="3 Minutes">3 Minutes</option>
                <option value="5 Minutes">5 Minutes</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Script Style</label>
              <select
                value={sStyle}
                onChange={(e) => setSStyle(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium cursor-pointer"
              >
                <option value="Storytelling">Storytelling</option>
                <option value="Educational">Educational</option>
                <option value="Comedy">Comedy</option>
                <option value="Luxury">Luxury</option>
                <option value="Emotional">Emotional</option>
                <option value="Sales">Sales</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Hook Type</label>
              <select
                value={sHookType}
                onChange={(e) => setSHookType(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium cursor-pointer"
              >
                <option value="Curiosity">Curiosity</option>
                <option value="Shock">Shock</option>
                <option value="Pain Point">Pain Point</option>
                <option value="Question">Question</option>
                <option value="Story">Story</option>
                <option value="FOMO">FOMO</option>
                <option value="Offer">Offer</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">CTA Style</label>
              <select
                value={sCtaStyle}
                onChange={(e) => setSCtaStyle(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium cursor-pointer"
              >
                <option value="Soft">Soft</option>
                <option value="Strong">Strong</option>
                <option value="Urgent">Urgent</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Target Audience</label>
              <input
                type="text"
                value={sAudience}
                onChange={(e) => setSAudience(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Language</label>
              <input
                type="text"
                value={sLanguage}
                onChange={(e) => setSLanguage(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Tone</label>
              <input
                type="text"
                value={sTone}
                onChange={(e) => setSTone(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Visual Presentation Style</label>
            <select
              value={sVisualStyle}
              onChange={(e) => setSVisualStyle(e.target.value)}
              className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs outline-hidden focus:border-primary-600 font-medium cursor-pointer"
            >
              <option value="Talking Head">Talking Head (Presenter speaking to camera)</option>
              <option value="B-roll">B-roll (Aesthetic cutaways with background voiceover)</option>
              <option value="Product Showcase">Product Showcase (Detailing physical product features)</option>
              <option value="Voiceover">Voiceover (Dynamic screen recording or slides with narration)</option>
              <option value="Podcast">Podcast (Split screen talk/conversation style)</option>
            </select>
          </div>

          {/* Configuration Checkboxes */}
          <div className="space-y-3 bg-gray-50/50 p-4 rounded-2xl border border-gray-100">
            <h4 className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Include Script Elements</h4>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { label: "Scene Breakdown", val: sIncludeBreakdown, set: setSIncludeBreakdown },
                { label: "Camera Angles", val: sIncludeAngles, set: setSIncludeAngles },
                { label: "Shot List", val: sIncludeShotList, set: setSIncludeShotList },
                { label: "Voiceover Script", val: sIncludeVoScript, set: setSIncludeVoScript },
                { label: "Caption Description", val: sIncludeCaption, set: setSIncludeCaption },
                { label: "Hashtags List", val: sIncludeHashtags, set: setSIncludeHashtags },
                { label: "Thumbnail Title", val: sIncludeThumbnail, set: setSIncludeThumbnail },
                { label: "YouTube Description", val: sIncludeYoutubeDesc, set: setSIncludeYoutubeDesc }
              ].map((item, idx) => (
                <label key={idx} className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                  <input
                    type="checkbox"
                    checked={item.val}
                    onChange={(e) => item.set(e.target.checked)}
                    className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                  />
                  {item.label}
                </label>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-primary-700 hover:bg-primary-800 text-white text-xs font-bold py-3 rounded-xl transition-all cursor-pointer shadow-md"
          >
            {loading ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                Compiling Script & Formatting Angles...
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                Generate 3 Script Variations
              </>
            )}
          </button>
        </form>
      );
    }

    if (tab === "viral-hooks") {
      return (
        <form onSubmit={handleBriefSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Business / Brand</label>
              <input
                type="text"
                value={hBusinessName}
                onChange={(e) => setHBusinessName(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Industry</label>
              <input
                type="text"
                value={hIndustry}
                onChange={(e) => setHIndustry(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Content Type</label>
              <select
                value={hContentType}
                onChange={(e) => setHContentType(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="Reel">Reel / Video</option>
                <option value="YouTube">YouTube</option>
                <option value="Facebook">Facebook</option>
                <option value="LinkedIn">LinkedIn</option>
                <option value="Twitter">Twitter / X Thread</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Scroll Goal</label>
              <select
                value={hGoal}
                onChange={(e) => setHGoal(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="Stop Scroll">Stop Scroll (Hook Rate)</option>
                <option value="Increase Watch Time">Increase Watch Time</option>
                <option value="More Clicks">More Clicks</option>
                <option value="Generate Leads">Generate Leads</option>
                <option value="More Sales">More Sales</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Hook Framework</label>
              <select
                value={hHookType}
                onChange={(e) => setHHookType(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="Curiosity">Curiosity</option>
                <option value="Fear">Fear / Risk</option>
                <option value="Pain">Pain-Point</option>
                <option value="Story">Story / Case Study</option>
                <option value="Question">Question</option>
                <option value="Funny">Funny</option>
                <option value="Luxury">Luxury</option>
                <option value="Controversial">Controversial</option>
                <option value="Emotional">Emotional</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Target Audience</label>
              <input
                type="text"
                value={hAudience}
                onChange={(e) => setHAudience(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Language</label>
              <input
                type="text"
                value={hLanguage}
                onChange={(e) => setHLanguage(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Number of Hooks</label>
              <select
                value={hCount}
                onChange={(e) => setHCount(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="5">5 Hooks</option>
                <option value="10">10 Hooks</option>
                <option value="20">20 Hooks</option>
                <option value="50">50 Hooks (Bulk pack)</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Hook Length</label>
              <select
                value={hLength}
                onChange={(e) => setHLength(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="Short">Short (Punchy)</option>
                <option value="Medium">Medium (Contextual)</option>
                <option value="Long">Long (Detailed/Story)</option>
              </select>
            </div>
          </div>

          <div className="flex gap-4 bg-gray-50/50 p-4 rounded-2xl border border-gray-100">
            <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
              <input
                type="checkbox"
                checked={hCta}
                onChange={(e) => setHCta(e.target.checked)}
                className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
              />
              Include Call to Action
            </label>
            <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
              <input
                type="checkbox"
                checked={hEmojis}
                onChange={(e) => setHEmojis(e.target.checked)}
                className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
              />
              Include Emojis
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-primary-700 hover:bg-primary-800 text-white text-xs font-bold py-3 rounded-xl transition-all cursor-pointer shadow-md"
          >
            {loading ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                Analyzing Virality Signals...
              </>
            ) : (
              <>
                <Flame className="h-4 w-4 animate-pulse" />
                Generate Hook Intelligence Brief
              </>
            )}
          </button>
        </form>
      );
    }

    if (tab === "image-generator") {
      return (
        <form onSubmit={handleBriefSubmit} className="space-y-6">
          <div className="flex flex-wrap items-center gap-2 pb-2">
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Presets:</span>
            <button 
              type="button" 
              onClick={() => loadPreset("ads")}
              className="px-3 py-1 text-[11px] font-bold rounded-full border bg-white text-gray-600 border-gray-100 hover:bg-gray-50 cursor-pointer"
            >
              Shoe Neon Ad Vibe
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Business Name</label>
              <input
                type="text"
                value={iBusinessName}
                onChange={(e) => setIBusinessName(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Industry</label>
              <input
                type="text"
                value={iIndustry}
                onChange={(e) => setIIndustry(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Image Purpose</label>
              <select
                value={iPurpose}
                onChange={(e) => setIPurpose(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="Poster">Poster</option>
                <option value="Banner">Banner</option>
                <option value="Flyer">Flyer</option>
                <option value="Social Media">Social Media Post</option>
                <option value="Logo">Logo</option>
                <option value="Product Photo">Product Photo</option>
                <option value="Packaging">Packaging Design</option>
                <option value="Thumbnail">YouTube Thumbnail</option>
                <option value="Billboard">Billboard</option>
                <option value="Magazine Cover">Magazine Cover</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Visual Style</label>
              <select
                value={iStyle}
                onChange={(e) => setIStyle(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="Photorealistic">Photorealistic</option>
                <option value="3D Cartoon">3D Cartoon</option>
                <option value="Minimal">Minimal</option>
                <option value="Luxury">Luxury</option>
                <option value="Cinematic">Cinematic</option>
                <option value="Anime">Anime</option>
                <option value="Pixar">Pixar / Disney</option>
                <option value="Cyberpunk">Cyberpunk</option>
                <option value="Vector">Vector Graphic</option>
                <option value="Watercolor">Watercolor</option>
                <option value="Sketch">Pencil Sketch</option>
                <option value="Flat Design">Flat Design</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Render Engine Preset</label>
              <select
                value={iEngine}
                onChange={(e) => setIEngine(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="FLUX">FLUX Pro (Highly Recommended)</option>
                <option value="DALL-E">DALL-E 3</option>
                <option value="Stable Diffusion">Stable Diffusion XL</option>
                <option value="Midjourney Style">Midjourney v6</option>
                <option value="Leonardo">Leonardo AI</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Aspect Ratio</label>
              <select
                value={iAspect}
                onChange={(e) => setIAspect(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="1:1">1:1 Square</option>
                <option value="16:9">16:9 Landscape</option>
                <option value="9:16">9:16 Vertical</option>
                <option value="4:5">4:5 Portrait</option>
                <option value="3:2">3:2 Classic</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Resolution</label>
              <select
                value={iResolution}
                onChange={(e) => setIResolution(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="HD">HD</option>
                <option value="2K">2K</option>
                <option value="4K">4K</option>
                <option value="8K">8K Ultra HD</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Lighting Style</label>
              <select
                value={iLighting}
                onChange={(e) => setILighting(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="Studio">Studio Softbox</option>
                <option value="Golden Hour">Golden Hour Natural</option>
                <option value="Soft Light">Soft Ambient Light</option>
                <option value="Dramatic">Dramatic Chiaroscuro</option>
                <option value="Neon">Neon Electric Light</option>
                <option value="Natural">Natural Overcast</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Camera / Lens Angle</label>
              <select
                value={iCamera}
                onChange={(e) => setICamera(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="DSLR">DSLR Standard</option>
                <option value="Sony A7">Sony A7R V Cinema</option>
                <option value="Canon">Canon EOS R5</option>
                <option value="Drone">Drone Aerial Capture</option>
                <option value="Wide Angle">Wide Angle Perspective</option>
                <option value="Macro">Macro Detail Zoom</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Camera Lens Focal Length</label>
              <select
                value={iLens}
                onChange={(e) => setILens(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="35mm">35mm Prime Lens</option>
                <option value="50mm">50mm Portrait Lens</option>
                <option value="85mm">85mm High Detail Lens</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Color Theme</label>
              <input
                type="text"
                value={iColorTheme}
                onChange={(e) => setIColorTheme(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Background Format</label>
              <select
                value={iBackground}
                onChange={(e) => setIBackground(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="Gradient">Gradient Studio Backdrop</option>
                <option value="Transparent">Transparent PNG</option>
                <option value="White">Clean White Backdrop</option>
                <option value="Black">Dramatic Black Backdrop</option>
                <option value="Custom">Custom Styled Background</option>
              </select>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Image Subject Description *</label>
            <textarea
              value={iSubject}
              onChange={(e) => setISubject(e.target.value)}
              rows={2}
              className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 resize-none"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Subject Topic / Vibe</label>
              <input
                type="text"
                value={iTopic}
                onChange={(e) => setITopic(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Special Offer Text Overlay</label>
              <input
                type="text"
                value={iOffer}
                onChange={(e) => setIOffer(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Negative Prompt (Avoid these elements)</label>
            <input
              type="text"
              value={iNegative}
              onChange={(e) => setINegative(e.target.value)}
              className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
            />
          </div>

          {/* Checkboxes */}
          <div className="space-y-3 bg-gray-50/50 p-4 rounded-2xl border border-gray-100">
            <h4 className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Render Qualifiers</h4>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={iHighDetail}
                  onChange={(e) => setIHighDetail(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                High Detail Render
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={iUltraQuality}
                  onChange={(e) => setIUltraQuality(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Ultra Quality Textures
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={iUpscale}
                  onChange={(e) => setIUpscale(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Upscale Image (2x)
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={iRemoveBg}
                  onChange={(e) => setIRemoveBg(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Remove Background
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={iMultiVariations}
                  onChange={(e) => setIMultiVariations(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Generate Variations
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-primary-700 hover:bg-primary-800 text-white text-xs font-bold py-3 rounded-xl transition-all cursor-pointer shadow-md"
          >
            {loading ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                Compiling Studio Parameter Matrix...
              </>
            ) : (
              <>
                <ImageIcon className="h-4 w-4" />
                Compile Render Prompts
              </>
            )}
          </button>
        </form>
      );
    }

    if (tab === "location-finder") {
      return (
        <form onSubmit={handleBriefSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Business Category</label>
              <input
                type="text"
                value={lCategory}
                onChange={(e) => setLCategory(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Industry</label>
              <input
                type="text"
                value={lIndustry}
                onChange={(e) => setLIndustry(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Target Keyword</label>
              <input
                type="text"
                value={lKeyword}
                onChange={(e) => setLKeyword(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">City</label>
              <input
                type="text"
                value={lCity}
                onChange={(e) => setLCity(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">State</label>
              <input
                type="text"
                value={lState}
                onChange={(e) => setLState(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Country</label>
              <input
                type="text"
                value={lCountry}
                onChange={(e) => setLCountry(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Search Radius</label>
              <select
                value={lRadius}
                onChange={(e) => setLRadius(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="1 KM">1 KM</option>
                <option value="3 KM">3 KM</option>
                <option value="5 KM">5 KM</option>
                <option value="10 KM">10 KM</option>
                <option value="25 KM">25 KM</option>
                <option value="50 KM">50 KM</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Minimum Rating</label>
              <select
                value={lMinRating}
                onChange={(e) => setLMinRating(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="3+">3+ Stars</option>
                <option value="4+">4+ Stars</option>
                <option value="4.5+">4.5+ Stars</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Sort Results By</label>
              <select
                value={lSortBy}
                onChange={(e) => setLSortBy(e.target.value)}
                className="w-full rounded-xl border border-gray-200 py-2 px-3 text-xs font-medium outline-hidden focus:border-primary-600 cursor-pointer"
              >
                <option value="Highest Rated">Highest Rated</option>
                <option value="Most Reviews">Most Reviews</option>
                <option value="Nearest">Nearest Location</option>
                <option value="Newest">Newest Listed</option>
              </select>
            </div>
          </div>

          {/* Lead Filters */}
          <div className="space-y-3 bg-gray-50/50 p-4 rounded-2xl border border-gray-100">
            <h4 className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Lead Contact Filters</h4>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={lOpenNow}
                  onChange={(e) => setLOpenNow(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Open Now Only
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={lVerifiedOnly}
                  onChange={(e) => setLVerifiedOnly(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Verified Listings Only
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={lHasWebsite}
                  onChange={(e) => setLHasWebsite(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Has Website
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={lHasPhone}
                  onChange={(e) => setLHasPhone(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Has Phone Number
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={lHasEmail}
                  onChange={(e) => setLHasEmail(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Has Public Email
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={lHasSocial}
                  onChange={(e) => setLHasSocial(e.target.checked)}
                  className="h-4 w-4 rounded-sm border-gray-300 text-primary-700 focus:ring-primary-600 cursor-pointer"
                />
                Has Social Media Links
              </label>
            </div>

            <div className="border-t border-gray-100 pt-3 flex items-center gap-3">
              <span className="text-[10px] font-bold text-gray-500 uppercase">Max Results Limit:</span>
              <select
                value={lMaxResults}
                onChange={(e) => setLMaxResults(e.target.value)}
                className="rounded-lg border border-gray-200 py-1 px-2 text-xs font-bold bg-white cursor-pointer"
              >
                <option value="10">10 results</option>
                <option value="25">25 results</option>
                <option value="50">50 results</option>
                <option value="100">100 results</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-primary-700 hover:bg-primary-800 text-white text-xs font-bold py-3 rounded-xl transition-all cursor-pointer shadow-md"
          >
            {loading ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                Querying OSM & Crawling Local Indices...
              </>
            ) : (
              <>
                <Search className="h-4 w-4" />
                Find Leads & Extract Metadata
              </>
            )}
          </button>
        </form>
      );
    }
  };

  const renderWorkspaceContent = () => {
    switch (tab) {
      case "prompt-library":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-gray-800 tracking-tight flex items-center gap-1.5">
                <BookOpen className="h-4.5 w-4.5 text-primary-700" />
                Prompt Library Templates
              </h3>
              <span className="text-[10px] bg-blue-50 text-primary-700 px-2 py-0.5 rounded-full font-bold">
                1000+ Active Templates
              </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                {
                  title: "Festival Sweets Special Offer",
                  desc: "Generate viral copy for sweets, desserts, and local bakery special events.",
                  category: "Marketing",
                  template: "Write a casual Hinglish post for my sweets shop..."
                },
                {
                  title: "Local Dentist Clinic Lead Gen",
                  desc: "Attract clinic appointments using location-targeted local campaigns.",
                  category: "Leads",
                  template: "Generate 3 local ad templates for dental implants..."
                },
                {
                  title: "Tech Startup Launch Campaign",
                  desc: "Professional B2B copy to announce product features and launches.",
                  category: "SaaS",
                  template: "Act as an expert marketer. Write an introductory email..."
                },
                {
                  title: "Instagram Reel Script Outline",
                  desc: "Hook-Intro-Body-CTA structure optimized for short visual videos.",
                  category: "Social Media",
                  template: "Create a 30s video script for custom products..."
                }
              ].map((item, idx) => (
                <div key={idx} className="p-4 bg-gray-50 border border-gray-100 rounded-xl space-y-3 hover:border-blue-200 transition-colors">
                  <div className="flex justify-between items-center">
                    <span className="text-[9px] bg-white border border-gray-100 font-bold px-2 py-0.5 rounded-full text-gray-500 uppercase">
                      {item.category}
                    </span>
                    <button 
                      onClick={() => handleCopy(item.template)}
                      className="text-gray-400 hover:text-primary-700 cursor-pointer"
                      title="Copy template"
                    >
                      <Copy className="h-3.5 w-3.5" />
                    </button>
                  </div>
                  <h4 className="text-xs font-bold text-gray-800">{item.title}</h4>
                  <p className="text-[11px] text-gray-500 font-medium leading-relaxed">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        );

      case "ai-chat":
        return (
          <div className="h-[480px]">
            <AIChatWidget />
          </div>
        );

      case "saved-results":
        return (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-gray-800 tracking-tight flex items-center gap-1.5">
              <Bookmark className="h-4.5 w-4.5 text-primary-700" />
              Saved Prompts & Marketing Copies
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { title: "Diwali Sweet Post Copy", tool: "Prompt Generator", time: "2 days ago" },
                { title: "Dentist Local Ad Campaign", tool: "Script Generator", time: "3 days ago" },
                { title: "Shoe poster visual prompt", tool: "Image Generator", time: "5 days ago" }
              ].map((item, idx) => (
                <div key={idx} className="p-4 bg-white border border-gray-100 rounded-xl flex items-center justify-between shadow-2xs">
                  <div>
                    <h4 className="text-xs font-bold text-gray-800">{item.title}</h4>
                    <span className="text-[9px] text-gray-400 font-semibold">{item.tool} • {item.time}</span>
                  </div>
                  <button className="text-xs font-bold text-primary-700 hover:underline cursor-pointer">
                    Reuse
                  </button>
                </div>
              ))}
            </div>
          </div>
        );

      case "history":
        return (
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-gray-800 tracking-tight flex items-center gap-1.5">
              <History className="h-4.5 w-4.5 text-primary-700" />
              Activity Log & Generations Audit
            </h3>
            <RecentActivityWidget />
          </div>
        );

      default:
        return (
          <div className="flex flex-col items-center justify-center py-20 text-gray-400 text-center">
            <Info className="h-10 w-10 text-gray-300 stroke-[1.5] mb-2" />
            <h4 className="text-xs font-bold">Module Under Construction</h4>
            <p className="text-[10px] max-w-[250px] leading-normal mt-1">
              This module ({tab}) is successfully registered. Core functionalities are ready for backend binding.
            </p>
          </div>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Back button and page title */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button 
            onClick={onNavigateBack}
            className="flex h-8 w-8 items-center justify-center rounded-xl bg-white border border-gray-100 shadow-2xs hover:bg-gray-50 transition-colors text-gray-600 font-bold text-xs cursor-pointer"
          >
            ←
          </button>
          <div>
            <h2 className="text-base font-bold text-gray-800 capitalize tracking-tight flex items-center gap-2">
              {tab.replace("-", " ")} Brief Studio
              <Award className="h-4 w-4 text-amber-500 fill-amber-100" />
            </h2>
            <p className="text-[10px] text-gray-400 font-semibold tracking-wide">
              The Digital Saathi &bull; Professional AI Formulation Engine
            </p>
          </div>
        </div>

        {/* Saved, Favorited state markers */}
        {result && (
          <div className="flex items-center gap-2">
            <button
              onClick={handleFavoriteResult}
              className={`flex h-8 w-8 items-center justify-center rounded-xl border transition-colors cursor-pointer ${
                isFavorited 
                  ? "bg-red-50 border-red-100 text-red-500" 
                  : "bg-white border-gray-100 text-gray-400 hover:text-red-500"
              }`}
              title="Add to Favorites"
            >
              <Heart className={`h-4 w-4 ${isFavorited ? "fill-red-500 animate-pulse" : ""}`} />
            </button>
            <button
              onClick={handleSaveResult}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all cursor-pointer ${
                isSaved
                  ? "bg-emerald-50 border-emerald-100 text-emerald-600"
                  : "bg-white border-gray-100 text-gray-500 hover:bg-gray-50"
              }`}
            >
              <Bookmark className={`h-3.5 w-3.5 ${isSaved ? "fill-emerald-600" : ""}`} />
              {isSaved ? "Saved" : "Save Template"}
            </button>
          </div>
        )}
      </div>

      {/* Main Grid Wrapper */}
      {tab === "prompt-library" || tab === "ai-chat" || tab === "saved-results" || tab === "history" ? (
        <div className="bg-white border border-gray-100/50 p-6 rounded-3xl shadow-sm">
          {renderWorkspaceContent()}
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Config Forms */}
          <div className="lg:col-span-7 bg-white border border-gray-100/50 p-6 rounded-3xl shadow-sm space-y-6">
            {/* Industry Specific Suggestions */}
            {aiSuggestions.length > 0 && (
              <div className="bg-blue-50/40 border border-blue-100/50 rounded-2xl p-4 space-y-1.5">
                <span className="text-[10px] font-bold text-primary-700 uppercase tracking-wider block">AI Strategic Presets recommendation:</span>
                <ul className="space-y-1">
                  {aiSuggestions.map((sug, i) => (
                    <li key={i} className="text-[10px] text-gray-600 font-semibold leading-relaxed flex items-center gap-1.5">
                      {sug}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {renderGeneratorForm()}
          </div>

          {/* Right Column: AI Output Panel */}
          <div className="lg:col-span-5 flex flex-col justify-between p-6 border border-gray-100 bg-white rounded-3xl shadow-sm min-h-[550px] relative overflow-hidden">
            {/* Glowing active glow border if output is loaded */}
            {result && <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-indigo-600" />}

            <div className="space-y-5">
              <div className="flex items-center justify-between border-b border-gray-50 pb-3">
                <span className="text-[10px] font-extrabold text-gray-400 uppercase tracking-wider">
                  Brief Analytics & Compilations
                </span>

                {result && (
                  <div className="flex gap-2">
                    <button
                      onClick={handleCopyResult}
                      className="flex items-center gap-1 text-[10px] font-bold text-primary-700 bg-blue-50 px-2.5 py-1 rounded-lg hover:bg-blue-100 transition-colors cursor-pointer"
                    >
                      {copied ? (
                        <>
                          <Check className="h-3 w-3 text-emerald-600" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="h-3 w-3" />
                          Copy Active Output
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>

              {loading ? (
                <div className="flex flex-col items-center justify-center py-28 gap-4 text-center">
                  <div className="h-10 w-10 animate-spin rounded-full border-4 border-primary-50 border-t-primary-700" />
                  <div>
                    <h4 className="text-xs font-bold text-gray-700">Calling Gemini AI...</h4>
                    <p className="text-[10px] text-gray-400 font-semibold animate-pulse">Generating real output from Gemini 2.5 Flash...</p>
                  </div>
                </div>
              ) : apiError ? (
                <div className="flex flex-col items-center justify-center py-20 gap-3 text-center px-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-50 text-red-500">
                    <AlertCircle className="h-6 w-6" />
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-red-700">Generation Failed</h4>
                    <p className="text-[11px] text-gray-500 font-medium mt-1 max-w-sm">{apiError}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setApiError(null)}
                    className="text-[10px] font-bold text-primary-700 underline cursor-pointer mt-1"
                  >
                    Dismiss
                  </button>
                </div>
              ) : result ? (
                <div className="space-y-4">
                  {/* Output Tabs Selection */}
                  <div className="flex bg-gray-50/70 p-1 rounded-xl border border-gray-100 overflow-x-auto gap-1 custom-scrollbar">
                    {Object.keys(result).map((key) => {
                      const isSelected = activeOutputTab === key;
                      return (
                        <button
                          key={key}
                          type="button"
                          onClick={() => setActiveOutputTab(key)}
                          className={`flex-1 min-w-[90px] text-center py-1.5 text-[10px] font-bold rounded-lg transition-all duration-200 cursor-pointer whitespace-nowrap px-2.5 ${
                            isSelected 
                              ? "bg-white text-gray-800 shadow-2xs border border-gray-100" 
                              : "text-gray-400 hover:text-gray-600"
                          }`}
                        >
                          {key}
                        </button>
                      );
                    })}
                  </div>

                  {/* Active Output text display */}
                  <div className="p-4 bg-gray-50/50 rounded-2xl border border-gray-50 text-[11px] font-medium whitespace-pre-wrap leading-relaxed text-gray-700 max-h-[420px] overflow-y-auto pr-1 custom-scrollbar">
                    {result[activeOutputTab]}
                  </div>

                  {/* Export Options */}
                  <div className="bg-gray-50 rounded-2xl p-3 border border-gray-100 flex items-center justify-between gap-2">
                    <span className="text-[9px] font-bold text-gray-400 uppercase">Export Brief:</span>
                    <div className="flex gap-1.5">
                      <button 
                        onClick={exportToTxt}
                        className="flex items-center gap-1 text-[9px] font-bold text-gray-600 hover:text-gray-800 bg-white border border-gray-100 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
                      >
                        <Download className="h-3 w-3" />
                        TXT
                      </button>
                      <button 
                        onClick={exportToMarkdown}
                        className="flex items-center gap-1 text-[9px] font-bold text-gray-600 hover:text-gray-800 bg-white border border-gray-100 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
                      >
                        <Download className="h-3 w-3" />
                        Markdown
                      </button>
                      <button 
                        onClick={triggerPrintPDF}
                        className="flex items-center gap-1 text-[9px] font-bold text-gray-600 hover:text-gray-800 bg-white border border-gray-100 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
                      >
                        <Download className="h-3 w-3" />
                        PDF / Print
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-28 text-center text-gray-400 space-y-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50/50 text-primary-700">
                    <Sparkles className="h-6 w-6 animate-pulse" />
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-gray-800">Brief Compilation Engine</h4>
                    <p className="text-[10px] max-w-[260px] leading-relaxed mt-1">
                      Configure your details on the left, then click formulate to compile your brief templates.
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Special layout image preview block if image-generator is loaded */}
            {tab === "image-generator" && result && !loading && (
              <div className="mt-4 p-4 bg-gray-50 border border-gray-100 rounded-2xl space-y-2">
                <span className="text-[9px] font-bold text-gray-400 uppercase block">FLUX Image Output Preview</span>
                <div className="w-full h-44 rounded-xl overflow-hidden bg-gray-100 border border-gray-100">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img 
                    src="https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500&auto=format&fit=crop&q=60" 
                    alt="FLUX tea visual showcase render" 
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
            )}

            <div className="mt-6 pt-3 border-t border-gray-50 flex justify-between items-center text-[9px] text-gray-400 font-semibold">
              <span>Endpoint: POST /api/v1/generators/{tab}/generate</span>
              <span>Access: Authorized Bypass</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
