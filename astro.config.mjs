// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightImageZoom from 'starlight-image-zoom';

// Base path defaults to '/' for local dev, published docs, and the Python/Flask offline package.
const base = process.env.DOCS_BASE ?? '/';

const GA_ID = 'G-SMFMDV1JW7';

export default defineConfig({
  site: 'https://corridor.github.io',
  base,
  outDir: './corridor_docs/site',
  integrations: [
    starlight({
      title: 'Corridor GGX Documentation',
      logo: {
        light: './src/assets/ggx-blue.png',
        dark: './src/assets/ggx-white.png',
        alt: 'Corridor GenGuardX',
      },
      favicon: '/favicon.ico',
      customCss: [
        '@fontsource/dm-sans/400.css',
        '@fontsource/dm-sans/500.css',
        '@fontsource/dm-sans/600.css',
        '@fontsource/dm-sans/700.css',
        '@fontsource/dm-mono/400.css',
        '@fontsource/dm-mono/500.css',
        './src/styles/custom.css',
      ],
      lastUpdated: true,
      editLink: {
        baseUrl: 'https://github.com/corridor/ggx-docs/edit/main/',
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/corridor' },
        { icon: 'linkedin', label: 'LinkedIn', href: 'https://www.linkedin.com/company/corridor-platforms/' },
        { icon: 'youtube', label: 'YouTube', href: 'https://www.youtube.com/@corridorplatforms' },
      ],
      plugins: [starlightImageZoom()],
      head: [
        {
          tag: 'script',
          attrs: { async: true, src: `https://www.googletagmanager.com/gtag/js?id=${GA_ID}` },
        },
        {
          tag: 'script',
          content: `window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${GA_ID}');`,
        },
      ],
      sidebar: [
        {
          label: 'Register and Refine',
          items: [
            { label: 'Overview', slug: 'register-and-refine' },
            {
              label: 'Inventory Management',
              items: [
                { label: 'Overview', slug: 'register-and-refine/inventory-management' },
                { label: 'Table Registry', slug: 'register-and-refine/inventory-management/table-registry' },
                { label: 'Model Catalog', slug: 'register-and-refine/inventory-management/model-catalog' },
                { label: 'Prompts', slug: 'register-and-refine/inventory-management/prompts' },
                { label: 'RAGs', slug: 'register-and-refine/inventory-management/rags' },
                { label: 'Pipelines', slug: 'register-and-refine/inventory-management/pipelines' },
                { label: 'Global Functions', slug: 'register-and-refine/inventory-management/global-functions' },
              ],
            },
            { label: 'Collaboration', slug: 'register-and-refine/collaboration' },
            { label: 'Version Management', slug: 'register-and-refine/version-management' },
            { label: 'Lineage Tracking', slug: 'register-and-refine/lineage-tracking' },
            { label: 'Prompt Optimization', slug: 'register-and-refine/prompt-optimization' },
            { label: 'Corridor Sync', slug: 'register-and-refine/corridor_sync' },
            {
              label: 'Asset Registration Examples',
              items: [
                { label: 'Gemini 2.0 Flash Model Registration', slug: 'register-and-refine/examples/model' },
                {
                  label: 'Intent Classification Pipeline Example',
                  items: [
                    { label: 'Prompt Registration', slug: 'register-and-refine/examples/intent-classification-pipeline-registration/prompt' },
                    { label: 'Pipeline Registration', slug: 'register-and-refine/examples/intent-classification-pipeline-registration/pipeline' },
                  ],
                },
                {
                  label: 'Language Translation Pipeline Example',
                  items: [
                    { label: 'Pipeline Registration', slug: 'register-and-refine/examples/language-translation-pipeline-registration/pipeline' },
                  ],
                },
              ],
            },
          ],
        },
        {
          label: 'Evaluate and Approve',
          items: [
            { label: 'Overview', slug: 'evaluate-and-approve' },
            { label: 'Simulation', slug: 'evaluate-and-approve/simulation' },
            { label: 'Comparison', slug: 'evaluate-and-approve/comparison' },
            { label: 'Reporting', slug: 'evaluate-and-approve/reporting' },
            { label: 'Approval Workflows', slug: 'evaluate-and-approve/approval-workflows' },
            { label: 'Human Testing', slug: 'evaluate-and-approve/human-testing' },
            { label: 'Feedback Portals', slug: 'evaluate-and-approve/feedback-portals' },
            { label: 'Document Generation', slug: 'evaluate-and-approve/document-generation' },
          ],
        },
        {
          label: 'Deploy and Monitor',
          items: [
            { label: 'Overview', slug: 'deploy-and-monitor' },
            { label: 'Direct to Production', slug: 'deploy-and-monitor/direct-to-production' },
            { label: 'Oversight', slug: 'deploy-and-monitor/oversight' },
            { label: 'Performance', slug: 'deploy-and-monitor/performance' },
            { label: 'Annotation Queues', slug: 'deploy-and-monitor/annotation-queues' },
          ],
        },
        { label: 'FAQ', slug: 'faq' },
        {
          label: 'Integrations',
          items: [
            { label: 'Overview', slug: 'integrations' },
            {
              label: 'LLM Providers',
              items: [
                { label: 'Setting up Integrations', slug: 'integrations/llm-providers' },
                { label: 'GCP VertexAI', slug: 'integrations/llm-providers/gcp-vertexai' },
                { label: 'AWS Bedrock', slug: 'integrations/llm-providers/aws-bedrock' },
                { label: 'AzureAI', slug: 'integrations/llm-providers/azureai' },
                { label: 'OpenAI', slug: 'integrations/llm-providers/openai' },
                { label: 'HuggingFace', slug: 'integrations/llm-providers/huggingface' },
                { label: 'Anthropic', slug: 'integrations/llm-providers/anthropic' },
              ],
            },
            {
              label: 'Evaluation Providers',
              items: [
                { label: 'Cleanlab', slug: 'integrations/evaluation-providers/cleanlab' },
              ],
            },
          ],
        },
        {
          label: 'Technology',
          items: [
            {
              label: 'Self Hosted Installation',
              items: [
                { label: 'Overview', slug: 'technology/self-hosting' },
                { label: 'Minimum Requirements', slug: 'technology/self-hosting/installation/minimum-requirements' },
                {
                  label: 'Installation',
                  items: [
                    {
                      label: 'GCP',
                      items: [
                        { label: 'Installation on GCP', slug: 'technology/self-hosting/installation/gcp' },
                        { label: 'Google Kubernetes Engine (GKE)', slug: 'technology/self-hosting/installation/gcp/gcp-gke' },
                        { label: 'Google Compute Engine VMs (GCE)', slug: 'technology/self-hosting/installation/gcp/gcp-vms' },
                      ],
                    },
                    {
                      label: 'AWS',
                      items: [
                        { label: 'Installation on AWS', slug: 'technology/self-hosting/installation/aws' },
                        { label: 'Amazon Fargate', slug: 'technology/self-hosting/installation/aws/aws-fargate' },
                        { label: 'Amazon Elastic Kubernetes Service (EKS)', slug: 'technology/self-hosting/installation/aws/aws-eks' },
                        { label: 'Amazon Elastic Compute Cloud (EC2)', slug: 'technology/self-hosting/installation/aws/aws-ec2' },
                      ],
                    },
                    {
                      label: 'Azure',
                      items: [
                        { label: 'Installation on Azure', slug: 'technology/self-hosting/installation/azure' },
                        { label: 'Azure Kubernetes Service (AKS)', slug: 'technology/self-hosting/installation/azure/azure-aks' },
                        { label: 'Azure Virtual Machines', slug: 'technology/self-hosting/installation/azure/azure-vms' },
                      ],
                    },
                    {
                      label: 'On Prem',
                      items: [
                        { label: 'Installation On Prem', slug: 'technology/self-hosting/installation/on-prem' },
                        { label: 'Bundle Install', slug: 'technology/self-hosting/installation/on-prem/bundle-install' },
                        { label: 'Docker Containers', slug: 'technology/self-hosting/installation/on-prem/docker' },
                      ],
                    },
                  ],
                },
                {
                  label: 'Configurations',
                  items: [{ autogenerate: { directory: 'technology/self-hosting/configurations' } }],
                },
                { label: 'Hardening - Security', slug: 'technology/self-hosting/hardening' },
                {
                  label: 'Scaling',
                  items: [{ autogenerate: { directory: 'technology/self-hosting/scaling' } }],
                },
              ],
            },
          ],
        },
      ],
    }),
  ],
});
