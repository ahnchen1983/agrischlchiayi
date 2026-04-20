/**
 * Agricultural Resources Database (Cleaned Version - 2026-04-20)
 * 農業資源盤點 - Traditional Chinese (繁體中文) Only
 * Official channels and government agricultural resources for Chiayi County farmers
 */

export interface ResourceSite {
  nameKey: string; // i18n key, e.g. 'resources.site.moa.main'
  url: string;
  domain: string;
  descKey?: string; // optional description i18n key (featured sites only)
  featured?: boolean; // Top 3 featured per chapter
}

export interface HeroCategory {
  id: string;
  labelKey: string;
  color: string;
  sites: ResourceSite[];
}

// ─── Hero Mindmap Data (5 Agricultural Categories) ───
export const heroCategories: HeroCategory[] = [
  {
    id: 'agri-governance',
    labelKey: 'resources.category.agri.governance.label',
    color: '#15803d', // Deeper green for agriculture
    sites: [
      {
        nameKey: 'resources.site.moa.main',
        url: 'https://www.moa.gov.tw/',
        domain: 'moa.gov.tw',
        featured: true,
      },
      {
        nameKey: 'resources.site.cyhg.agri',
        url: 'https://agriculture.cyhg.gov.tw/',
        domain: 'cyhg.gov.tw',
        featured: true,
      },
      {
        nameKey: 'resources.site.fa',
        url: 'https://www.fa.gov.tw/',
        domain: 'fa.gov.tw',
        featured: true,
      },
    ],
  },
  {
    id: 'agri-technology',
    labelKey: 'resources.category.agri.technology.label',
    color: '#059669', // Standard green
    sites: [
      {
        nameKey: 'resources.site.tari',
        url: 'https://www.tari.gov.tw/',
        domain: 'tari.gov.tw',
        featured: true,
      },
      {
        nameKey: 'resources.site.tfri',
        url: 'https://www.tfri.gov.tw/',
        domain: 'tfri.gov.tw',
        featured: true,
      },
      {
        nameKey: 'resources.site.tndais.chiayi',
        url: 'https://www.tndais.gov.tw/index_chiayi_branch.php',
        domain: 'tndais.gov.tw',
        featured: true,
      },
    ],
  },
  {
    id: 'agri-marketing',
    labelKey: 'resources.category.agri.marketing.label',
    color: '#10b981', // Light green
    sites: [
      {
        nameKey: 'resources.site.moa.trade',
        url: 'https://trade.moa.gov.tw/',
        domain: 'moa.gov.tw',
        featured: true,
      },
    ],
  },
  {
    id: 'agri-finance',
    labelKey: 'resources.category.agri.finance.label',
    color: '#047857', // Dark green
    sites: [
      {
        nameKey: 'resources.site.moa.subsidy',
        url: 'https://www.moa.gov.tw/theme_list.php?theme=subsidy',
        domain: 'moa.gov.tw',
        featured: true,
      },
    ],
  },
  {
    id: 'agri-sustainability',
    labelKey: 'resources.category.agri.sustainability.label',
    color: '#065f46', // Forest green
    sites: [
      {
        nameKey: 'resources.site.ardswc',
        url: 'https://www.ardswc.gov.tw/',
        domain: 'ardswc.gov.tw',
        featured: true,
      },
    ],
  },
];

// ─── Chapter 1: 農業行政與管理 (Agricultural Administration & Management) ───

// Subcategory 1.1: 中央主管機關 (Central Ministries)
export const agriGovernanceCentral: ResourceSite[] = [
  {
    nameKey: 'resources.site.moa.main',
    url: 'https://www.moa.gov.tw/',
    domain: 'moa.gov.tw',
    featured: true,
  },
  {
    nameKey: 'resources.site.fa',
    url: 'https://www.fa.gov.tw/',
    domain: 'fa.gov.tw',
  },
  {
    nameKey: 'resources.site.afa',
    url: 'https://www.afa.gov.tw/cht/index.php',
    domain: 'afa.gov.tw',
  },
  {
    nameKey: 'resources.site.ardswc',
    url: 'https://www.ardswc.gov.tw/',
    domain: 'ardswc.gov.tw',
  },
  {
    nameKey: 'resources.site.forest',
    url: 'https://www.forest.gov.tw/',
    domain: 'forest.gov.tw',
  },
];

// Subcategory 1.2: 地方農業單位 (Local Agricultural Units & Regional Stations)
export const agriGovernanceLocal: ResourceSite[] = [
  {
    nameKey: 'resources.site.cyhg.agri',
    url: 'https://agriculture.cyhg.gov.tw/',
    domain: 'cyhg.gov.tw',
    featured: true,
  },
  {
    nameKey: 'resources.site.chiayicity.agri',
    url: 'https://economic.chiayi.gov.tw/',
    domain: 'chiayi.gov.tw',
  },
  {
    nameKey: 'resources.site.tndais',
    url: 'https://www.tndais.gov.tw/',
    domain: 'tndais.gov.tw',
    featured: true,
  },
  {
    nameKey: 'resources.site.tndais.chiayi',
    url: 'https://www.tndais.gov.tw/index_chiayi_branch.php',
    domain: 'tndais.gov.tw',
  },
  {
    nameKey: 'resources.site.afrec.taichung',
    url: 'https://taichung.afrec.gov.tw/',
    domain: 'afrec.gov.tw',
  },
  {
    nameKey: 'resources.site.afrec.kaohsiung',
    url: 'https://kaohsiung.afrec.gov.tw/',
    domain: 'afrec.gov.tw',
  },
  {
    nameKey: 'resources.site.tainan.agri',
    url: 'https://agron.tainan.gov.tw/',
    domain: 'tainan.gov.tw',
  },
  {
    nameKey: 'resources.site.yunlin.agri',
    url: 'https://agriculture.yunlin.gov.tw/',
    domain: 'yunlin.gov.tw',
  },
  {
    nameKey: 'resources.site.kaohsiung.agri',
    url: 'https://agri.kcg.gov.tw/',
    domain: 'kcg.gov.tw',
  },
  {
    nameKey: 'resources.site.taichung.agri',
    url: 'https://www.agriculture.taichung.gov.tw/',
    domain: 'taichung.gov.tw',
  },
  {
    nameKey: 'resources.site.pingtung.agri',
    url: 'https://www.pthg.gov.tw/plantou/',
    domain: 'pthg.gov.tw',
  },
  {
    nameKey: 'resources.site.nantou.main',
    url: 'https://www.nantou.gov.tw/',
    domain: 'nantou.gov.tw',
  },
];

// Subcategory 1.3: 法規與土地資訊 (Regulations & Land Information)
export const agriGovernancePolicy: ResourceSite[] = [
  {
    nameKey: 'resources.site.moa.main',
    url: 'https://www.moa.gov.tw/',
    domain: 'moa.gov.tw',
  },
  {
    nameKey: 'resources.site.nladb',
    url: 'https://nladb.nla.gov.tw/',
    domain: 'nladb.nla.gov.tw',
  },
  {
    nameKey: 'resources.site.nlsc',
    url: 'https://www.nlsc.gov.tw/',
    domain: 'nlsc.gov.tw',
  },
];

// ─── Chapter 2: 技術研發與推廣 (Technical R&D & Promotion) ───

// Subcategory 2.1: 農業試驗研究機構 (Agricultural Research Institutions)
export const agriTechResearch: ResourceSite[] = [
  {
    nameKey: 'resources.site.tari',
    url: 'https://www.tari.gov.tw/',
    domain: 'tari.gov.tw',
    featured: true,
  },
  {
    nameKey: 'resources.site.tfri',
    url: 'https://www.tfri.gov.tw/',
    domain: 'tfri.gov.tw',
  },
  {
    nameKey: 'resources.site.tfrin',
    url: 'https://www.tfrin.gov.tw/',
    domain: 'tfrin.gov.tw',
  },
  {
    nameKey: 'resources.site.acri',
    url: 'https://www.acri.gov.tw/',
    domain: 'acri.gov.tw',
  },
];

// Subcategory 2.2: 區域改良場 (Regional Improvement Stations)
export const agriTechInnovation: ResourceSite[] = [
  {
    nameKey: 'resources.site.tndais',
    url: 'https://www.tndais.gov.tw/',
    domain: 'tndais.gov.tw',
    featured: true,
  },
  {
    nameKey: 'resources.site.tndais.chiayi',
    url: 'https://www.tndais.gov.tw/index_chiayi_branch.php',
    domain: 'tndais.gov.tw',
    featured: true,
  },
  {
    nameKey: 'resources.site.afrec.taichung',
    url: 'https://taichung.afrec.gov.tw/',
    domain: 'afrec.gov.tw',
  },
  {
    nameKey: 'resources.site.afrec.kaohsiung',
    url: 'https://kaohsiung.afrec.gov.tw/',
    domain: 'afrec.gov.tw',
  },
];

// Subcategory 2.3: 農業推廣與教育 (Agricultural Extension & Education)
export const agriTechExtension: ResourceSite[] = [
  {
    nameKey: 'resources.site.tndais',
    url: 'https://www.tndais.gov.tw/',
    domain: 'tndais.gov.tw',
  },
  {
    nameKey: 'resources.site.tndais.chiayi',
    url: 'https://www.tndais.gov.tw/index_chiayi_branch.php',
    domain: 'tndais.gov.tw',
  },
];

// ─── Chapter 3: 農產品行銷與銷售 (Agricultural Marketing & Sales) ───

// Subcategory 3.1: 線上銷售平台 (Online Sales Platforms)
export const agriMarketingOnline: ResourceSite[] = [
  {
    nameKey: 'resources.site.moa.trade',
    url: 'https://trade.moa.gov.tw/',
    domain: 'moa.gov.tw',
    featured: true,
  },
];

// Subcategory 3.2: 直銷與市集 (Direct Sales & Markets)
export const agriMarketingDirect: ResourceSite[] = [];

// Subcategory 3.3: 認證與品牌建立 (Certification & Branding)
export const agriMarketingCertification: ResourceSite[] = [];

// ─── Chapter 4: 融資與補助資源 (Financing & Subsidy Resources) ───

// Subcategory 4.1: 農業融資管道 (Agricultural Financing Channels)
export const agriFinanceChannels: ResourceSite[] = [];

// Subcategory 4.2: 政府補助計畫 (Government Subsidy Programs)
export const agriFinanceSubsidy: ResourceSite[] = [
  {
    nameKey: 'resources.site.moa.subsidy',
    url: 'https://www.moa.gov.tw/theme_list.php?theme=subsidy',
    domain: 'moa.gov.tw',
    featured: true,
  },
];

// Subcategory 4.3: 農業保險 (Agricultural Insurance)
export const agriFinanceInsurance: ResourceSite[] = [];

// ─── Chapter 5: 水資源與環境永續 (Water Resources & Environmental Sustainability) ───

// Subcategory 5.1: 水資源管理 (Water Resource Management)
export const agriSustainabilityWater: ResourceSite[] = [
  {
    nameKey: 'resources.site.ardswc',
    url: 'https://www.ardswc.gov.tw/',
    domain: 'ardswc.gov.tw',
    featured: true,
  },
];

// Subcategory 5.2: 友善農業與認證 (Sustainable Farming & Certification)
export const agriSustainabilityOrganic: ResourceSite[] = [];

// Subcategory 5.3: 氣候調適資源 (Climate Adaptation Resources)
export const agriSustainabilityClimate: ResourceSite[] = [];
