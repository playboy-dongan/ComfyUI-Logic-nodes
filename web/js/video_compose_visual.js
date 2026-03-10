import { app } from "../../scripts/app.js";
import { tr, trNode } from "./tr.js";

app.registerExtension({
    name: "Logic.VideoComposeVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_VideoCompose") return;

        let data = null;

        node.addCustomWidget({
            type: "custom", name: tr("Logic.VideoCompose.infoLabel"), serialize: false,
            computeSize: () => [node.size[0], data ? 84 : 0],
            draw(ctx, _node, width, y) {
                if (!data) return;
                ctx.save();

                ctx.strokeStyle = "#555";
                ctx.beginPath();
                ctx.moveTo(10, y + 4);
                ctx.lineTo(width - 10, y + 4);
                ctx.stroke();

                const x0 = 10, x1 = width - 10;
                const lines = [
                    { icon: "📐", label: tr("Logic.common.Resolution"), value: data.resolution, color: "#6af" },
                    { icon: "⏱️", label: tr("Logic.common.Duration"),   value: data.duration + "s", color: "#8f8" },
                    { icon: "🎞️", label: tr("Logic.common.FPS"),   value: data.fps + " fps", color: "#fda" },
                    { icon: "🖼️", label: tr("Logic.common.Frames"), value: data.frames, color: "#fda" },
                    { icon: "🔊", label: tr("Logic.common.Audio"),   value: data.hasAudio ? "✅ " + tr("Logic.common.Yes") : "❌ " + tr("Logic.common.No"), color: data.hasAudio ? "#8f8" : "#888" },
                ];
                let cy = y + 18;
                for (const l of lines) {
                    ctx.font = "12px Arial";
                    ctx.textAlign = "left";
                    ctx.fillStyle = l.color;
                    ctx.fillText(`${l.icon} ${l.label}`, x0, cy);
                    ctx.textAlign = "right";
                    ctx.fillStyle = "#ddd";
                    ctx.fillText(l.value, x1, cy);
                    cy += 15;
                }
                ctx.restore();
            },
        });

        const orig = node.onExecuted;
        node.onExecuted = function (o) {
            orig?.call(this, o);
            data = {
                resolution: o?.resolution?.[0] ?? "?",
                duration:   o?.duration?.[0]   ?? "0",
                fps:        o?.fps?.[0]        ?? "0",
                frames:     o?.frames?.[0]     ?? "0",
                hasAudio:   o?.has_audio?.[0] === "True",
            };
            node.title = `${trNode("Logic_VideoCompose")} ${data.resolution} ${data.duration}s`;
            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        };
    },
});
