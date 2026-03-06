import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Logic.JudgeVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Judge") return;

        let lastResult = null;

        node.addCustomWidget({
            type: "custom", name: "判断结果", serialize: false,
            computeSize: () => [node.size[0], 28],
            draw(ctx, _node, width, y) {
                if (lastResult === null) return;
                ctx.save();
                ctx.textAlign = "center";
                ctx.font = "bold 16px Arial";
                ctx.fillStyle = lastResult ? "#8f8" : "#f88";
                ctx.fillText(lastResult ? "✅ TRUE" : "❌ FALSE", width / 2, y + 20);
                ctx.restore();
            },
        });

        const orig = node.onExecuted;
        node.onExecuted = function (o) {
            orig?.call(this, o);
            if (o?.result?.[0] != null) {
                lastResult = o.result[0];
                node.color = node.bgcolor = lastResult ? "#335533" : "#553333";
                node.title = lastResult
                    ? "✅ ⚖️ 判断器 - 真"
                    : "❌ ⚖️ 判断器 - 假";
            }
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        };
    },
});
