import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Logic.BlockerVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Blocker") return;
        const w = node.widgets?.find(w => w.name === "启用");
        if (!w) return;

        function update(v) {
            node.color = node.bgcolor = v ? "#335533" : "#553333";
            node.title = v ? "✅ 🚧 阻断器 - 通过" : "🚫 🚧 阻断器 - 阻断中";
            node.setDirtyCanvas(true, true);
        }

        update(w.value);
        const orig = w.callback;
        w.callback = function (v) { update(v); orig?.call(this, v); };
    },
});
