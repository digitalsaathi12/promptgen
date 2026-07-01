/**
 * api.ts — Frontend API client for The Digital Saathi
 *
 * All requests go to the Python FastAPI backend at NEXT_PUBLIC_API_URL.
 * The backend holds the GEMINI_API_KEY — the frontend never touches it.
 *
 * Base URL: http://localhost:8000/api/v1  (local dev)
 *           Set NEXT_PUBLIC_API_URL in .env.local to override for production.
 */

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

// ---------------------------------------------------------------------------
// Shared fetch wrapper
// ---------------------------------------------------------------------------

async function post<TBody, TResponse>(
  path: string,
  body: TBody
): Promise<TResponse> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await res.json();

  if (!res.ok) {
    let message = `Request failed with status ${res.status}`;
    if (data) {
      if (typeof data.detail === "object" && data.detail !== null) {
        message = data.detail.message ?? JSON.stringify(data.detail);
      } else if (typeof data.detail === "string") {
        message = data.detail;
      } else if (data.error?.message) {
        message = data.error.message;
      }
    }
    throw new Error(message);
  }

  return data as TResponse;
}

// ---------------------------------------------------------------------------
// 1. Viral Hooks Generator
// ---------------------------------------------------------------------------

export type HookPlatform = "Instagram" | "YouTube" | "Facebook" | "LinkedIn";
export type HookType = "pain" | "curiosity" | "question" | "shock" | "story" | "future";

export interface HookInput {
  niche: string;
  audience: string;
  platform: HookPlatform;
  count?: number;
  language?: string;
  hook_type?: string;
  goal?: string;
  length?: string;
  cta?: boolean;
  emojis?: boolean;
}

export interface Hook {
  type: HookType;
  text: string;
  cta?: string;
}

export interface HookOutput {
  hooks: Hook[];
}

export async function generateHooks(input: HookInput): Promise<HookOutput> {
  const data = await post<HookInput, { output: HookOutput }>("/generate/hooks", input);
  return data.output;
}

// ---------------------------------------------------------------------------
// 2. Image Prompt Generator
// ---------------------------------------------------------------------------

export interface ImagePromptInput {
  subject: string;
  business?: string;
  industry?: string;
  topic?: string;
  offer?: string;
  purpose?: string;
  style?: string;
  engine?: string;
  aspect?: string;
  resolution?: string;
  lighting?: string;
  camera?: string;
  lens?: string;
  color_theme?: string;
  background?: string;
  negative?: string;
  ref_style?: string;
  high_detail?: boolean;
  ultra_quality?: boolean;
}

export type SuggestedTool = "Midjourney" | "DALL-E" | "Stable Diffusion";

export interface ImagePromptOutput {
  image_prompt: string;
  negative_prompt: string;
  suggested_tool: SuggestedTool;
}

export async function generateImagePrompt(input: ImagePromptInput): Promise<ImagePromptOutput> {
  const data = await post<ImagePromptInput, { output: ImagePromptOutput }>(
    "/generate/image-prompt",
    input
  );
  return data.output;
}

// ---------------------------------------------------------------------------
// 3. Video Script Generator
// ---------------------------------------------------------------------------

export interface VideoScriptInput {
  business: string;
  industry?: string;
  platform?: string;
  duration?: string;
  duration_seconds?: number;
  style?: string;
  hook_type?: string;
  audience?: string;
  language?: string;
  tone?: string;
  cta_style?: string;
  visual_style?: string;
  include_breakdown?: boolean;
  include_angles?: boolean;
  include_shot_list?: boolean;
  include_vo_script?: boolean;
  include_caption?: boolean;
  include_hashtags?: boolean;
  include_thumbnail?: boolean;
  include_youtube_desc?: boolean;
}

export interface VideoScriptOutput {
  hook: string;
  script: string;
  cta: string;
  scene_breakdown?: any[];
  camera_angles?: any[];
  shot_list?: string[];
  social_caption?: string;
  hashtags?: string;
  thumbnail_concept?: string;
  youtube_description?: string;
}

export async function generateVideoScript(input: VideoScriptInput): Promise<VideoScriptOutput> {
  const data = await post<VideoScriptInput, { output: VideoScriptOutput }>(
    "/generate/video-script",
    input
  );
  return data.output;
}

// ---------------------------------------------------------------------------
// 4. Content Writer
// ---------------------------------------------------------------------------

export type ContentFormat = "caption" | "ad" | "blog";

export interface ContentWriterInput {
  business: string;
  industry?: string;
  goal: string;
  format: ContentFormat;
  language?: string;
  tone?: string;
  audience?: string;
  platform?: string;
  offer?: string;
  include_emojis?: boolean;
  include_hashtags?: boolean;
}

export interface CaptionOutput {
  captions: string[];
}

export interface AdOutput {
  headline: string;
  primary_text: string;
  cta: string;
}

export interface BlogOutput {
  title: string;
  meta_description: string;
  body: string;
}

export type ContentWriterOutput = CaptionOutput | AdOutput | BlogOutput;

export async function generateContent(input: ContentWriterInput): Promise<ContentWriterOutput> {
  const data = await post<ContentWriterInput, { output: ContentWriterOutput }>(
    "/generate/content-writer",
    input
  );
  return data.output;
}

// ---------------------------------------------------------------------------
// 5. AI Chat
// ---------------------------------------------------------------------------

export interface ChatMessageItem {
  role: "user" | "ai";
  text: string;
}

export interface ChatInput {
  message: string;
  history?: ChatMessageItem[];
}

export async function generateChat(input: ChatInput): Promise<string> {
  const data = await post<ChatInput, { output: string }>("/generate/chat", input);
  return data.output;
}

// ---------------------------------------------------------------------------
// 6. Prompt Generator
// ---------------------------------------------------------------------------

export interface PromptGeneratorInput {
  business: string;
  industry: string;
  sub_industry?: string;
  description?: string;
  category: string;
  prompt_type: string;
  audience: string;
  age_group?: string;
  location?: string;
  language?: string;
  gender?: string;
  pain_points?: string;
  goal: string;
  offer: string;
  platform: string;
  tone?: string;
  depth?: string;
  model?: string;
  length?: string;
  creativity?: number;
  cta?: boolean;
  hashtags?: boolean;
  emojis?: boolean;
  seo_keywords?: boolean;
  competitor?: boolean;
  multiple_versions?: boolean;
  variations_count?: number;
}

export interface PromptGeneratorOutput {
  expert_prompt: string;
  optimized_prompt: string;
  gemini_prompt: string;
  explanation: string;
}

export async function generatePrompt(input: PromptGeneratorInput): Promise<PromptGeneratorOutput> {
  const data = await post<PromptGeneratorInput, { output: PromptGeneratorOutput }>(
    "/generate/prompt",
    input
  );
  return data.output;
}


