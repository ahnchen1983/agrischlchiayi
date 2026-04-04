import { ui, defaultLang, showDefaultLang } from './ui';
import type { Lang } from '../types';

const normalizedBase = import.meta.env.BASE_URL.replace(/\/$/, '');

function prefixInternalPaths(value: string) {
  if (!normalizedBase) return value;

  return value
    .replace(/(href|src)=(['"])\/(?!\/)/g, `$1=$2${normalizedBase}/`)
    .replace(/url\((['"]?)\/(?!\/)/g, `url($1${normalizedBase}/`);
}

export function getLangFromUrl(url: URL): Lang {
  const [, lang] = url.pathname.split('/');
  if (lang in ui) return lang as Lang;
  return defaultLang;
}

export function useTranslations(lang: Lang) {
  return function t(key: keyof (typeof ui)[typeof defaultLang]) {
    const value = ui[lang][key] || ui[defaultLang][key];
    return typeof value === 'string' ? prefixInternalPaths(value) : value;
  };
}

export function useTranslatedPath(lang: Lang) {
  return function translatePath(path: string, l: string = lang) {
    return !showDefaultLang && l === defaultLang ? path : `/${l}${path}`;
  };
}
