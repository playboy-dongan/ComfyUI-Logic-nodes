import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "Logic.UniversalPreviewVisual",
    nodeCreated(node) {
        if (node.comfyClass !== "Logic_UniversalPreview") return;

        // --- text widget ---
        const textEl = document.createElement("textarea");
        textEl.readOnly = true;
        textEl.style.cssText = [
            "background: transparent",
            "color: #ddd",
            "border: none",
            "outline: none",
            "resize: none",
            "padding: 6px",
            "font-size: 13px",
            "font-family: monospace",
            "line-height: 1.4",
            "width: 100%",
            "overflow-y: auto",
        ].join(";");

        const textWidget = node.addDOMWidget("预览文本", "customtext", textEl, {
            serialize: false,
            hideOnZoom: false,
        });
        textWidget.computeSize = () => [node.size[0], 0];

        // --- audio widget ---
        const audioContainer = document.createElement("div");
        audioContainer.style.cssText = "width:100%; padding:4px 6px; display:flex; flex-direction:column; gap:6px;";

        const audioWidget = node.addDOMWidget("预览音频", "customaudio", audioContainer, {
            serialize: false,
            hideOnZoom: false,
        });
        audioWidget.computeSize = () => [node.size[0], 0];

        const origOnExecuted = node.onExecuted;
        node.onExecuted = function (output) {
            if (origOnExecuted) origOnExecuted.call(this, output);

            const hasImages = output?.images?.length > 0;
            const hasText = output?.text?.length > 0 && output.text[0] !== "";
            const hasAudio = output?.audio?.length > 0;

            // text
            if (hasText && !hasImages) {
                textEl.value = output.text[0];
                const lines = output.text[0].split("\n").length;
                textWidget.computeSize = () => [node.size[0], Math.min(lines * 20 + 16, 300)];
            } else {
                textEl.value = "";
                textWidget.computeSize = () => [node.size[0], 0];
            }

            // audio
            if (hasAudio) {
                audioContainer.innerHTML = "";
                for (const a of output.audio) {
                    const audioEl = document.createElement("audio");
                    audioEl.controls = true;
                    audioEl.style.cssText = "width:100%;";
                    const params = new URLSearchParams({
                        filename: a.filename,
                        subfolder: a.subfolder || "",
                        type: a.type,
                    });
                    audioEl.src = api.apiURL(`/view?${params.toString()}`);
                    audioContainer.appendChild(audioEl);
                }
                const count = output.audio.length;
                audioWidget.computeSize = () => [node.size[0], count * 54 + 8];
            } else {
                audioContainer.innerHTML = "";
                audioWidget.computeSize = () => [node.size[0], 0];
            }

            node.setSize(node.computeSize());
            node.setDirtyCanvas(true, true);
        };
    },
});
