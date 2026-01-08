---
id: 0002
title: Vercel production deployment workflow
stage: general
date: 2026-01-09
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: feature/backend-rag-improvements
user: user
command: manual
labels: ["deployment", "vercel", "build", "production", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: https://github.com/Huzafi/AI-Native-Physical-Book/pull/4
files:
  - website/build/ (generated)
  - website/build/ur/ (generated)
tests:
  - Docusaurus build for English locale (en)
  - Docusaurus build for Urdu locale (ur)
  - Vercel production deployment
---

## Prompt

Now First Run Command cd website then run npm run build and then Finally Run Command vercel --prod for deployment

## Response snapshot

Executed sequential build and deployment workflow:

1. **Build Phase** (`npm run build`):
   - Built Docusaurus website for 2 locales (en, ur)
   - English build: Compiled successfully in ~4.18s (Client), 3.93s (Server)
   - Urdu build: Compiled successfully in ~3.53s (Client), 3.40s (Server)
   - Generated static files in `build/` and `build/ur/`
   - Received deprecation warnings for `siteConfig.onBrokenMarkdownLinks` (migrate to `siteConfig.markdown.hooks.onBrokenMarkdownLinks`)

2. **Deployment Phase** (`vercel --prod`):
   - Uploaded 1.6MB of deployment files to Vercel
   - Build executed in Washington, D.C. (iad1) with 2 cores, 8GB RAM
   - Restored build cache from previous deployment
   - Completed full build in 15s, total deployment in 35s
   - Successfully deployed to production

**Deployment URLs:**
- Production: https://ai-native-book-74qu2i04k-huzafis-projects.vercel.app
- Aliased: https://ai-native-book-green.vercel.app

## Outcome

- ✅ Impact: Hero section UI improvements with clean black theme and blue accents successfully deployed to Vercel production. Site is now live with modernized visual design.
- 🧪 Tests: Build completed successfully for both locales (en, ur) with no errors. Webpack compilation passed for client and server bundles.
- 📁 Files: Generated optimized static files in website/build/ directory. Uploaded 238 deployment files (1.6MB) to Vercel.
- 🔁 Next prompts: Monitor production site performance, address Docusaurus v4 deprecation warnings, consider additional UI improvements, or merge remaining backend changes.
- 🧠 Reflection: Sequential build-then-deploy workflow executed smoothly. Vercel's build cache optimization reduced deployment time. The hero section improvements are now visible to production users.

## Evaluation notes (flywheel)

- Failure modes observed: None. Both build and deployment completed without errors.
- Graders run and results (PASS/FAIL): PASS - Build succeeded for both locales, deployment completed successfully, production URLs accessible
- Prompt variant (if applicable): Standard sequential command execution (build → deploy)
- Next experiment (smallest change to try): Address Docusaurus v4 deprecation warning by migrating `onBrokenMarkdownLinks` config to new location
