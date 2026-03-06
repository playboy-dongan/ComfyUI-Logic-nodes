import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Logic.SwitchVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Switch") return;
        const w = node.widgets?.find(w => w.name === "条件");
        if (!w) return;

        function update(v) {
            node.color = node.bgcolor = v ? "#335533" : "#553333";
            node.title = v ? "✅ 🔀 条件切换 - 真" : "❌ 🔀 条件切换 - 假";
            node.setDirtyCanvas(true, true);
        }

        update(w.value);
        const orig = w.callback;
        w.callback = function (v) { update(v); orig?.call(this, v); };
    },
});
