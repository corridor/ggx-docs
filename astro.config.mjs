// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import starlightImageZoom from "starlight-image-zoom";
import starlightSidebarTopics from "starlight-sidebar-topics";
import { llmsIntegration } from "./src/integrations/llms.mjs";

// Base path defaults to '/' for local dev, published docs, and the Python/Flask offline package.
const base = process.env.DOCS_BASE ?? "/";

const GA_ID = "G-SMFMDV1JW7";

export default defineConfig({
  site: "https://ggx-docs.corridorplatforms.com",
  base,
  outDir: "./dist",
  // Astro 6.4.x was causing issues with the table rendering.
  // REF: https://github.com/withastro/starlight/issues/3934
  // REF: https://github.com/withastro/astro/issues/16971
  markdown: {
    gfm: true,
  },
  integrations: [
    llmsIntegration({ site: "https://ggx-docs.corridorplatforms.com", base }),
    starlight({
      title: "Corridor GGX Documentation",
      logo: {
        light: "./src/assets/ggx-blue.png",
        dark: "./src/assets/ggx-white.png",
        alt: "Corridor GenGuardX",
      },
      favicon: "/favicon.ico",
      customCss: [
        "@fontsource/dm-sans/400.css",
        "@fontsource/dm-sans/500.css",
        "@fontsource/dm-sans/600.css",
        "@fontsource/dm-sans/700.css",
        "@fontsource/dm-mono/400.css",
        "@fontsource/dm-mono/500.css",
        "./src/styles/custom.css",
      ],
      lastUpdated: true,
      editLink: {
        baseUrl: "https://github.com/corridor/ggx-docs/edit/main/",
      },
      components: {
        PageTitle: "./src/components/PageTitle.astro",
      },
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/corridor",
        },
        {
          icon: "linkedin",
          label: "LinkedIn",
          href: "https://www.linkedin.com/company/corridor-platforms/",
        },
        {
          icon: "youtube",
          label: "YouTube",
          href: "https://www.youtube.com/@corridorplatforms",
        },
      ],
      plugins: [
        starlightImageZoom(),
        starlightSidebarTopics([
          {
            id: "register-and-refine",
            label: "Register and Refine",
            link: "/register-and-refine/",
            icon: "add-document",
            items: [
              { label: "Overview", slug: "register-and-refine" },
              {
                label: "Inventory Management",
                items: [
                  {
                    label: "Overview",
                    slug: "register-and-refine/inventory-management",
                  },
                  {
                    label: "Table Registry",
                    slug: "register-and-refine/inventory-management/table-registry",
                  },
                  {
                    label: "Model Catalog",
                    slug: "register-and-refine/inventory-management/model-catalog",
                  },
                  {
                    label: "Prompts",
                    slug: "register-and-refine/inventory-management/prompts",
                  },
                  {
                    label: "RAGs",
                    slug: "register-and-refine/inventory-management/rags",
                  },
                  {
                    label: "Pipelines",
                    slug: "register-and-refine/inventory-management/pipelines",
                  },
                  {
                    label: "Global Functions",
                    slug: "register-and-refine/inventory-management/global-functions",
                  },
                ],
              },
              {
                label: "Collaboration",
                slug: "register-and-refine/collaboration",
              },
              {
                label: "Version Management",
                slug: "register-and-refine/version-management",
              },
              {
                label: "Lineage Tracking",
                slug: "register-and-refine/lineage-tracking",
              },
              {
                label: "Prompt Optimization",
                slug: "register-and-refine/prompt-optimization",
              },
              {
                label: "Corridor Sync",
                slug: "register-and-refine/corridor_sync",
              },
              {
                label: "Asset Registration Examples",
                collapsed: true,
                items: [
                  {
                    label: "Gemini 2.0 Flash Model Registration",
                    slug: "register-and-refine/examples/model",
                  },
                  {
                    label: "Intent Classification Pipeline Example",
                    items: [
                      {
                        label: "Prompt Registration",
                        slug: "register-and-refine/examples/intent-classification-pipeline-registration/prompt",
                      },
                      {
                        label: "Pipeline Registration",
                        slug: "register-and-refine/examples/intent-classification-pipeline-registration/pipeline",
                      },
                    ],
                  },
                  {
                    label: "Language Translation Pipeline Example",
                    items: [
                      {
                        label: "Pipeline Registration",
                        slug: "register-and-refine/examples/language-translation-pipeline-registration/pipeline",
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            label: "Evaluate and Approve",
            link: "/evaluate-and-approve/",
            icon: "approve-check-circle",
            items: [
              { label: "Overview", slug: "evaluate-and-approve" },
              { label: "Simulation", slug: "evaluate-and-approve/simulation" },
              { label: "Comparison", slug: "evaluate-and-approve/comparison" },
              { label: "Reporting", slug: "evaluate-and-approve/reporting" },
              {
                label: "Approval Workflows",
                slug: "evaluate-and-approve/approval-workflows",
              },
              {
                label: "Human Testing",
                slug: "evaluate-and-approve/human-testing",
              },
              {
                label: "Feedback Portals",
                slug: "evaluate-and-approve/feedback-portals",
              },
              {
                label: "Document Generation",
                slug: "evaluate-and-approve/document-generation",
              },
            ],
          },
          {
            label: "Deploy and Monitor",
            link: "/deploy-and-monitor/",
            icon: "rocket",
            items: [
              { label: "Overview", slug: "deploy-and-monitor" },
              {
                label: "Direct to Production",
                slug: "deploy-and-monitor/direct-to-production",
              },
              { label: "Oversight", slug: "deploy-and-monitor/oversight" },
              { label: "Performance", slug: "deploy-and-monitor/performance" },
              {
                label: "Annotation Queues",
                slug: "deploy-and-monitor/annotation-queues",
              },
            ],
          },
          {
            label: "Integrations",
            link: "/integrations/",
            icon: "puzzle",
            items: [
              { label: "Overview", slug: "integrations" },
              {
                label: "LLM Providers",
                items: [
                  {
                    label: "Setting up Integrations",
                    slug: "integrations/llm-providers",
                  },
                  {
                    label: "GCP VertexAI",
                    slug: "integrations/llm-providers/gcp-vertexai",
                  },
                  {
                    label: "AWS Bedrock",
                    slug: "integrations/llm-providers/aws-bedrock",
                  },
                  {
                    label: "AzureAI",
                    slug: "integrations/llm-providers/azureai",
                  },
                  {
                    label: "OpenAI",
                    slug: "integrations/llm-providers/openai",
                  },
                  {
                    label: "HuggingFace",
                    slug: "integrations/llm-providers/huggingface",
                  },
                  {
                    label: "Anthropic",
                    slug: "integrations/llm-providers/anthropic",
                  },
                ],
              },
              {
                label: "LLM Gateways",
                items: [
                  {
                    label: "Overview",
                    slug: "integrations/llm-gateways",
                  },
                  {
                    label: "LiteLLM",
                    slug: "integrations/llm-gateways/litellm",
                  },
                  {
                    label: "Portkey",
                    slug: "integrations/llm-gateways/portkey",
                  },
                  {
                    label: "OpenRouter",
                    slug: "integrations/llm-gateways/openrouter",
                  },
                  {
                    label: "Cloudflare AI Gateway",
                    slug: "integrations/llm-gateways/cloudflare-ai-gateway",
                  },
                ],
              },
              {
                label: "Evaluation Providers",
                items: [
                  {
                    label: "Cleanlab",
                    slug: "integrations/evaluation-providers/cleanlab",
                  },
                ],
              },
              {
                label: "AI Governance",
                items: [
                  {
                    label: "Databricks AI Gateway",
                    slug: "integrations/ai-governance/databricks-ai-gateway",
                  },
                ],
              },
            ],
          },
          {
            label: "Technology",
            link: "/technology/self-hosting/",
            icon: "server",
            items: [
              {
                label: "Self Hosted Installation",
                items: [
                  { label: "Overview", slug: "technology/self-hosting" },
                  {
                    label: "Minimum Requirements",
                    slug: "technology/self-hosting/installation/minimum-requirements",
                  },
                  {
                    label: "Installation",
                    items: [
                      {
                        label: "AWS",
                        slug: "technology/self-hosting/installation/aws",
                      },
                      {
                        label: "Azure",
                        slug: "technology/self-hosting/installation/azure",
                      },
                      {
                        label: "GCP",
                        slug: "technology/self-hosting/installation/gcp",
                      },
                      {
                        label: "Kubernetes",
                        slug: "technology/self-hosting/installation/kubernetes",
                      },
                      {
                        label: "Terraform",
                        slug: "technology/self-hosting/installation/terraform",
                      },
                      {
                        label: "Docker-based",
                        slug: "technology/self-hosting/installation/docker-based",
                      },
                      {
                        label: "Manual",
                        slug: "technology/self-hosting/installation/manual",
                      },
                    ],
                  },
                  {
                    label: "Configurations",
                    collapsed: true,
                    items: [
                      {
                        autogenerate: {
                          directory: "technology/self-hosting/configurations",
                        },
                      },
                    ],
                  },
                  {
                    label: "Hardening - Security",
                    slug: "technology/self-hosting/hardening",
                  },
                  {
                    label: "Scaling",
                    collapsed: true,
                    items: [
                      {
                        autogenerate: {
                          directory: "technology/self-hosting/scaling",
                        },
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            label: "FAQ",
            link: "/faq/",
            icon: "question-circle",
            items: [{ label: "FAQ", slug: "faq" }],
          },
        ]),
      ],
      head: [
        {
          tag: "script",
          attrs: {
            async: true,
            src: `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`,
          },
        },
        {
          tag: "script",
          content: `window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${GA_ID}');`,
        },
      ],
    }),
  ],
});
