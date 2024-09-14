import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

// Add new colors to LGraphCanvas.node_colors
function addNewColors() {
  // Completely replacing the node_colors object
  LGraphCanvas.node_colors = {
    red: { color: "#C62828", bgcolor: "#E53935", groupcolor: "#B71C1C" },     // Red: 800, 600, 900
    pink: { color: "#AD1457", bgcolor: "#D81B60", groupcolor: "#880E4F" },    // Pink: 800, 600, 900
    purple: { color: "#6A1B9A", bgcolor: "#8E24AA", groupcolor: "#4A148C" },  // Purple: 800, 600, 900
    indigo: { color: "#283593", bgcolor: "#3949AB", groupcolor: "#1A237E" },  // Indigo: 800, 600, 900
    blue: { color: "#1565C0", bgcolor: "#1E88E5", groupcolor: "#0D47A1" },    // Blue: 800, 600, 900
    cyan: { color: "#00838F", bgcolor: "#00ACC1", groupcolor: "#006064" },    // Cyan: 800, 600, 900
    teal: { color: "#00695C", bgcolor: "#00897B", groupcolor: "#004D40" },    // Teal: 800, 600, 900
    green: { color: "#2E7D32", bgcolor: "#43A047", groupcolor: "#1B5E20" },   // Green: 800, 600, 900
    "light green": { color: "#558B2F", bgcolor: "#7CB342", groupcolor: "#33691E" },  // Light Green: 800, 600, 900
    "deep orange": { color: "#D84315", bgcolor: "#F4511E", groupcolor: "#BF360C" },  // Deep Orange: 800, 600, 900
    grey: { color: "#424242", bgcolor: "#757575", groupcolor: "#212121" },    // Grey: 800, 600, 900

    // Adding the 6 extra colors
    "blue grey": { color: "#455A64", bgcolor: "#607D8B", groupcolor: "#263238" },  // Blue Grey
    lime: { color: "#9E9D24", bgcolor: "#C0CA33", groupcolor: "#827717" },         // Lime
    "light blue": { color: "#0277BD", bgcolor: "#039BE5", groupcolor: "#01579B" }, // Light Blue
    "steel blue": { color: "#4682B4", bgcolor: "#5A9BD3", groupcolor: "#2B5A8A" }, // Steel Blue
    "turquoise": { color: "#00796B", bgcolor: "#009688", groupcolor: "#004D40" },  // Turquoise
    navy: { color: "#003366", bgcolor: "#004080", groupcolor: "#001f3f" },  // Navy Blue
  };
}


// Function to enhance nodes with text display
function addTextDisplay(nodeType) {
  const onNodeCreated = nodeType.prototype.onNodeCreated;
  nodeType.prototype.onNodeCreated = function () {
    const r = onNodeCreated?.apply(this, arguments);
    const w = ComfyWidgets["STRING"](this, "display", ["STRING", { multiline: true, placeholder: " " }], app).widget;
    w.inputEl.readOnly = true;
    w.inputEl.style.opacity = 0.7;
    w.inputEl.style.cursor = "auto";
    return r;
  };

  const onExecuted = nodeType.prototype.onExecuted;
  nodeType.prototype.onExecuted = function (message) {
    onExecuted?.apply(this, arguments);

    for (const widget of this.widgets) {
      if (widget.type === "customtext" && widget.name === "display" && widget.inputEl.readOnly === true) {
        widget.value = message.text.join('');
      }
    }

    this.onResize?.(this.size);
  };
}

app.registerExtension({
  name: "rka.GetRandomDimensions",
  setup() {
    // Call the function to add new colors
    addNewColors();
  },
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (["GetRandomDimensions"].includes(nodeData.name)) {
      addTextDisplay(nodeType);
    }
  },
});
