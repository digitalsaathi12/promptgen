"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/dashboard");
  }, [router]);

  return (
    <div className="flex h-screen w-screen items-center justify-center bg-gray-50/50">
      <div className="flex flex-col items-center gap-3">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary-100 border-t-primary-700" />
        <p className="text-xs text-gray-400 font-bold tracking-wide animate-pulse">
          Connecting to The Digital Saathi...
        </p>
      </div>
    </div>
  );
}

