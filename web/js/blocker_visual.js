import { app } from "../../scripts/app.js";
import { tr, trNode } from "./tr.js";

/**
 * ComfyUI 布尔控件的 label_on/label_off 可能不被前端读取，
 * 通过替换 draw 方法用翻译后的标签自行绘制。
 */
function patchBoolWidget(w, labelOnKey, labelOffKey) {
    const labelOn = tr(labelOnKey);
    const labelOff = tr(labelOffKey);
    const origDraw = w.draw;
    if (typeof origDraw !== "function") return;

    w.draw = function (ctx, node, width, y) {
        this.options = this.options || {};
        this.options.label_on = this.options.on = labelOn;
        this.options.label_off = this.options.off = labelOff;
        return origDraw.call(this, ctx, node, width, y);
    };
}

app.registerExtension({
    name: "Logic.BlockerVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Blocker") return;
        const w = node.widgets?.find(w => w.name === "enable");
        if (!w) return;

        patchBoolWidget(w, "Logic.Blocker.Pass", "Logic.Blocker.Blocked");
        w.options = w.options || {};
        const lo = tr("Logic.Blocker.Pass"), lf = tr("Logic.Blocker.Blocked");
        w.options.label_on = w.options.on = lo;
        w.options.label_off = w.options.off = lf;

        const baseTitle = trNode("Logic_Blocker");
        function update(v) {
            node.color = node.bgcolor = v ? "#335533" : "#553333";
            const status = v ? tr("Logic.Blocker.Pass") : tr("Logic.Blocker.Blocked");
            node.title = v ? `✅ ${baseTitle} - ${status}` : `🚫 ${baseTitle} - ${status}`;
            node.setDirtyCanvas(true, true);
        }

        update(w.value);
        const orig = w.callback;
        w.callback = function (v) { update(v); orig?.call(this, v); };
    },
});
