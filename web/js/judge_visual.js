import { app } from "../../scripts/app.js";
import { tr, trNode, replaceComboWithTranslated } from "./tr.js";

const JUDGE_CONDITIONS = [
    "A == B", "A != B", "A > B", "A < B", "A >= B", "A <= B",
    "A contains B", "A is empty", "A is not empty", "A is true", "A is false",
    "length == B", "length > B", "length < B",
];

app.registerExtension({
    name: "Logic.JudgeVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Judge") return;

        replaceComboWithTranslated(node, "condition", JUDGE_CONDITIONS, "Logic.Judge.");

        let lastResult = null;

        node.addCustomWidget({
            type: "custom", name: tr("Logic.Judge.ResultLabel"), serialize: false,
            computeSize: () => [node.size[0], 28],
            draw(ctx, _node, width, y) {
                if (lastResult === null) return;
                ctx.save();
                ctx.textAlign = "center";
                ctx.font = "bold 16px Arial";
                ctx.fillStyle = lastResult ? "#8f8" : "#f88";
                ctx.fillText(lastResult ? "✅ " + tr("Logic.Judge.True") : "❌ " + tr("Logic.Judge.False"), width / 2, y + 20);
                ctx.restore();
            },
        });

        const orig = node.onExecuted;
        node.onExecuted = function (o) {
            orig?.call(this, o);
            if (o?.result?.[0] != null) {
                lastResult = o.result[0];
                node.color = node.bgcolor = lastResult ? "#335533" : "#553333";
                const status = lastResult ? tr("Logic.Judge.True") : tr("Logic.Judge.False");
                const base = trNode("Logic_Judge");
                node.title = lastResult ? `✅ ${base} - ${status}` : `❌ ${base} - ${status}`;
            }
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        };
    },
});
