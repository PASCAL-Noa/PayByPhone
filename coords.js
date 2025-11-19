(function() {
    if (window.__coordTrackerLoaded) return;
    window.__coordTrackerLoaded = true;

    const box = document.createElement("div");
    box.style.position = "fixed";
    box.style.bottom = "10px";
    box.style.right = "10px";
    box.style.background = "rgba(0,0,0,0.7)";
    box.style.color = "lime";
    box.style.padding = "8px 12px";
    box.style.borderRadius = "6px";
    box.style.zIndex = "999999";
    box.style.fontFamily = "monospace";
    box.style.fontSize = "14px";
    box.style.pointerEvents = "none";
    box.innerText = "X: 0  Y: 0";
    document.body.appendChild(box);

    document.addEventListener("mousemove", function(e) {
        box.innerText = "X: " + e.clientX + "   Y: " + e.clientY;
    });

    console.log("CoordTracker loaded (coords.js)");
})();
