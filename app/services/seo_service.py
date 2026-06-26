import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SEOService:
    def evaluate_seo(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs audit rules against website crawl signals to yield SEO scores and recommendations."""
        score = 0
        strengths = []
        weaknesses = []
        opportunities = []

        title = crawl_data.get("title", "")
        meta_desc = crawl_data.get("meta_description", "")
        headings = crawl_data.get("headings", {})
        h1s = headings.get("h1", [])
        images = crawl_data.get("images", {})
        total_images = images.get("total", 0)
        images_alt = images.get("with_alt", 0)
        ssl_enabled = crawl_data.get("ssl_enabled", False)

        # 1. Title Audit
        if title:
            score += 20
            strengths.append("Title tag exists on the page.")
            if 40 <= len(title) <= 60:
                score += 10
                strengths.append("Page title is perfectly optimized (40-60 characters).")
            else:
                weaknesses.append(f"Page title is non-optimal ({len(title)} chars). Aim for 40-60.")
                opportunities.append("Modify homepage title length to fit standard Google SERP limits.")
        else:
            weaknesses.append("Homepage is missing a page Title tag entirely.")
            opportunities.append("Create a unique, descriptive page title containing focus keywords.")

        # 2. Meta Description Audit
        if meta_desc:
            score += 20
            strengths.append("Meta description tags exist.")
            if 120 <= len(meta_desc) <= 160:
                score += 10
                strengths.append("Meta description length matches recommendations (120-160 characters).")
            else:
                weaknesses.append(f"Meta description tag has suboptimal length ({len(meta_desc)} chars). Aim for 120-160.")
                opportunities.append("Shorten or expand meta descriptions to remain within 120-160 character limits.")
        else:
            weaknesses.append("Page is missing a meta description tag.")
            opportunities.append("Draft a compelling meta description highlighting your core value offers.")

        # 3. Headings Structure Audit
        if h1s:
            score += 15
            strengths.append("H1 headings are structured.")
            if len(h1s) > 1:
                weaknesses.append(f"Multiple H1 tags ({len(h1s)}) detected on page. Only use a single H1.")
                opportunities.append("Consolidate H1 tags; wrap sub-headings inside H2/H3 tags.")
        else:
            weaknesses.append("Missing H1 heading tag on home page.")
            opportunities.append("Insert one central H1 tag containing target brand positioning keywords.")

        # 4. Alt Tags Audit
        if total_images > 0:
            ratio = images_alt / total_images
            if ratio >= 0.8:
                score += 10
                strengths.append("Alt tags are defined on almost all website images.")
            else:
                score += int(ratio * 10)
                weaknesses.append(f"Only {images_alt} of {total_images} images contain alternative ALT tags.")
                opportunities.append("Audit all image blocks to ensure alt attributes are populated for screen-readers and image SEO.")
        else:
            score += 10
            strengths.append("No layout images found (ALT tag audit skipped).")

        # 5. SSL SSL
        if ssl_enabled:
            score += 15
            strengths.append("SSL encryption is active (HTTPS).")
        else:
            weaknesses.append("Website is running on unsecure connection (HTTP).")
            opportunities.append("Obtain and configure a SSL certificate (HTTPS) immediately to safeguard sessions.")

        return {
            "seo_score": f"{score}/100",
            "crawl_metrics": crawl_data,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "opportunities": opportunities
        }

seo_service = SEOService()
