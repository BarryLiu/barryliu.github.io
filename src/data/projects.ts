export type Project = {
  id: string;
  title: string;
  titleEn?: string;
  status: string;
  statusEn?: string;
  summary: string;
  summaryEn?: string;
  stack: string[];
  github: string;
  preview: string;
  relatedTags: string[];
  featured: boolean;
  proofs?: { label: string; labelEn?: string; value: string }[];
  signals?: number[];
  metrics?: [string, string];
};

export const projects: Project[] = [
  {
    id: 'ai-knowledge-navigator',
    title: 'AI 知识导航器',
    titleEn: 'AI Knowledge Navigator',
    status: '实验中',
    statusEn: 'In lab',
    summary: '面向个人知识库的 RAG / AI Search 项目，把博客文章、工作笔记、代码片段组织成可检索、可追问、可复用的技术地图。',
    summaryEn: 'A RAG and AI Search project for personal knowledge bases, turning posts, work notes, and code snippets into searchable, reusable technical maps.',
    stack: ['RAG', 'Vector DB', 'Agent Tools', 'Markdown Pipeline'],
    github: 'https://github.com/BarryLiu',
    preview: '',
    relatedTags: ['AI', 'RAG', '知识库'],
    featured: true,
    proofs: [
      { label: 'GitHub', value: 'Open' },
      { label: '预览', labelEn: 'Preview', value: 'Soon' },
      { label: '文章', labelEn: 'Articles', value: 'AI/RAG' },
    ],
    signals: [42, 78, 36, 96, 66, 112, 54],
    metrics: ['Markdown', 'Vector Map'],
  },
  {
    id: 'code-assistant',
    title: '代码助手实验',
    titleEn: 'Code Assistant Lab',
    status: '整理中',
    statusEn: 'Organizing',
    summary: '围绕智能体工具调用、代码生成、评审和自动化执行沉淀工程实践。',
    summaryEn: 'Engineering notes around agent tool use, code generation, reviews, and automated execution.',
    stack: ['Agent', 'Code Tools', 'Review'],
    github: 'https://github.com/BarryLiu',
    preview: '',
    relatedTags: ['Agent', 'AI编程', '工具调用'],
    featured: false,
    metrics: ['Agent', 'Tooling'],
  },
  {
    id: 'model-deploy',
    title: '模型部署 Dock',
    titleEn: 'Model Deploy Dock',
    status: '持续更新',
    statusEn: 'Updating',
    summary: '整理模型服务、容器化、证书、Cloudflare Pages 与静态站发布路径。',
    summaryEn: 'Model serving, containers, certificates, Cloudflare Pages, and static publishing paths.',
    stack: ['MLOps', 'Docker', 'Cloudflare'],
    github: 'https://github.com/BarryLiu',
    preview: '',
    relatedTags: ['MLOps', 'Docker', '部署'],
    featured: false,
    metrics: ['Static', 'Deploy'],
  },
  {
    id: 'sign-tool',
    title: '签名工具链',
    titleEn: 'Signing Toolchain',
    status: '工作记录',
    statusEn: 'Work log',
    summary: '沉淀证书、双向认证、签名脚本和 Maven 打包中的真实排障记录。',
    summaryEn: 'Real troubleshooting notes for certificates, mutual TLS, signing scripts, and Maven packaging.',
    stack: ['OpenSSL', 'Maven', 'Shell'],
    github: 'https://github.com/BarryLiu',
    preview: '',
    relatedTags: ['签名', '证书', '工具'],
    featured: false,
    metrics: ['Work', 'Ops'],
  },
  {
    id: 'ai-roadmap',
    title: 'AI 学习路线',
    titleEn: 'AI Learning Roadmap',
    status: '主线更新',
    statusEn: 'Main track',
    summary: '从数学基础、机器学习到 RAG 和 Agent，把学习路线拆成可跟进文章。',
    summaryEn: 'A followable route from math and machine learning to RAG and agents.',
    stack: ['AI', 'RAG', 'Roadmap'],
    github: 'https://github.com/BarryLiu',
    preview: '',
    relatedTags: ['AI', '学习路线', 'RAG'],
    featured: false,
    metrics: ['Guide', 'Notes'],
  },
];
