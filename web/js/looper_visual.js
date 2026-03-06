import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Logic.LooperVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_Looper") return;

        const barEl = document.createElement("div");
        barEl.style.cssText = "width:100%; padding:4px 6px;";
        barEl.innerHTML = `
            <div style="display:flex; justify-content:space-between; font-size:12px; color:#aaa; margin-bottom:3px;">
                <span class="loop-label">等待执行</span>
                <span class="loop-count"></span>
            </div>
            <div style="width:100%; height:6px; background:#333; border-radius:3px; overflow:hidden;">
                <div class="loop-bar" style="width:0%; height:100%; background:#4a9; border-radius:3px; transition:width .3s;"></div>
            </div>`;

        const barWidget = node.addDOMWidget("循环进度", "customprogress", barEl, {
            serialize: false,
            hideOnZoom: false,
        });
        barWidget.computeSize = () => [node.size[0], 36];

        const label = barEl.querySelector(".loop-label");
        const count = barEl.querySelector(".loop-count");
        const bar = barEl.querySelector(".loop-bar");

        const origExec = node.onExecuted;
        node.onExecuted = function (data) {
            if (origExec) origExec.call(this, data);

            const current = data?.current?.[0];
            const total = data?.total?.[0];
            const remaining = data?.remaining?.[0];

            if (current == null || total == null) return;

            const pct = Math.round(((current + 1) / total) * 100);
            bar.style.width = pct + "%";
            count.textContent = `${current + 1} / ${total}`;

            if (remaining > 0) {
                label.textContent = "处理中...";
                bar.style.background = "#4a9";
                node.title = `⚙️ 批处理器 ${current + 1}/${total}`;
                setTimeout(() => app.queuePrompt(0, 1), 200);
            } else {
                label.textContent = "完成 ✓";
                bar.style.background = "#6a6";
                node.title = `⚙️ 批处理器 ✓ ${total}/${total}`;
            }

            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        };
    },
});
