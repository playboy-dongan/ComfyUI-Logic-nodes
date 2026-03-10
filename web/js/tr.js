import { app } from "../../scripts/app.js";
import { EN, ZH } from "./translations.js";

/** 从 ComfyUI 同步 locale 到 document.documentElement.lang */
function syncLang() {
    if (typeof document === "undefined") return;
    try {
        let loc =
            app?.extensionManager?.setting?.get?.("Comfy.Locale.Language") ??
            app?.extensionManager?.setting?.get?.("Comfy.Locale") ??
            app?.ui?.settings?.getSettingValue?.("Comfy.Locale.Language") ??
            app?.ui?.settings?.getSettingValue?.("Comfy.Locale") ??
            app?.i18n?.global?.locale?.value ??
            app?.i18n?.global?.locale;
        if (loc == null && typeof localStorage !== "undefined") {
            loc = localStorage.getItem("Comfy.Locale.Language") ?? localStorage.getItem("Comfy.Locale") ?? localStorage.getItem("comfy-locale") ?? localStorage.getItem("locale");
        }
        if (loc != null && loc !== "") {
            document.documentElement.lang = String(loc);
        }
    } catch (_) {}
}

/** 判断是否为中文环境 */
export function isZhLocale() {
    syncLang();
    try {
        const s = String(document.documentElement?.lang ?? document.documentElement?.getAttribute?.("lang") ?? "");
        return s === "zh" || s === "zh-CN" || s === "zh-Hans" || s.startsWith("zh");
    } catch (_) {
        return false;
    }
}

/** 获取当前语言字典 */
function getDict() {
    return isZhLocale() ? ZH : EN;
}

/** 主翻译函数：tr(key) 或 tr(key, fallback)。fallback 仅当 key 在 EN/ZH 中都不存在时使用 */
export function tr(key, fallback) {
    try {
        const dict = getDict();
        if (dict[key]) return dict[key];
        const other = dict === ZH ? EN : ZH;
        if (other[key]) return other[key];
        if (typeof app?.st === "function") {
            const v = app.st(key, fallback);
            if (v && v !== key) return v;
        }
        const i18n = app?.i18n ?? app?.$i18n;
        if (i18n?.global?.t) {
            const v = i18n.global.t(key);
            if (v && v !== key) return v;
        }
    } catch (_) {}
    return fallback ?? key;
}

/** 翻译节点显示名：trNode("Logic_Blocker") */
export function trNode(nodeId) {
    return tr(nodeId, nodeId);
}

/** 翻译类型名：trTypeName("IMAGE") → 图像 / IMAGE */
export function trTypeName(typeName) {
    if (!typeName || typeof typeName !== "string") return typeName;
    const key = "Logic.type." + typeName;
    return tr(key, typeName);
}

/** 翻译 Python 返回的 detail 字符串（如 "batch: 2  size: 1244×1664  ch: 3"）*/
const DETAIL_REPLACES = [
    ["no input", "Logic.detail.noInput"],
    ["batch:", "Logic.detail.batch"],
    [" size:", "Logic.detail.size"],
    [" ch:", "Logic.detail.ch"],
    ["count:", "Logic.detail.count"],
    ["empty", "Logic.detail.empty"],
    ["null", "Logic.detail.empty"],
    ["keys:", "Logic.detail.keys"],
    ["value:", "Logic.detail.value"],
    ["length:", "Logic.detail.length"],
    ["shape:", "Logic.detail.shape"],
];

export function trDetail(detail) {
    if (!detail || typeof detail !== "string") return detail;
    try {
        if (!isZhLocale()) return detail;
        let s = detail;
        for (const [en, key] of DETAIL_REPLACES) {
            const zh = ZH[key];
            if (zh) s = s.replace(new RegExp(en.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g"), zh + (en.endsWith(":") ? ":" : ""));
        }
        return s;
    } catch (_) {
        return detail;
    }
}

/** 仅修改原 combo 的 options 显示翻译，不添加额外控件，避免重叠。
 *  在 draw 前注入 options（与 blocker 相同方式），确保框架读取到。
 *  @param onChange 可选，值变更时调用 (newValue) => void */
export function replaceComboWithTranslated(node, widgetName, keys, keyPrefix, onChange) {
    const orig = node.widgets?.find((w) => w.name === widgetName);
    if (!orig) return;
    let value = orig.value;
    if (!value || !keys.includes(value)) {
        value = keys[0];
        orig.value = value;
    }

    const combined = keys.map((k) => [tr(keyPrefix + k, k), k]);
    const origDraw = orig.draw;
    if (typeof origDraw === "function") {
        orig.draw = function (ctx, n, width, y) {
            this.options = this.options || {};
            this.options.combined = combined;
            this.options.values = keys;
            return origDraw.call(this, ctx, n, width, y);
        };
    } else {
        orig.options = orig.options || {};
        orig.options.combined = combined;
        orig.options.values = keys;
    }

    const origCallback = orig.callback;
    orig.callback = function (v) {
        origCallback?.call(this, v);
        onChange?.(v);
    };
}

/** 翻译 Python 返回的 "True"/"False" 字符串 */
export function trBool(value) {
    if (value === "True" || value === true) return tr("Literal.True", "True");
    if (value === "False" || value === false) return tr("Literal.False", "False");
    return String(value);
}

if (typeof document !== "undefined") {
    syncLang();
    setTimeout(syncLang, 100);
    setTimeout(syncLang, 500);
    window.addEventListener?.("storage", (e) => {
        if (e?.key?.includes?.("Locale") || e?.key === "locale") syncLang();
    });
}
