// see https://www.pdfreactor.com/product/doc_html/index.html#MathML;
// you'll probably want to configure the roMj{Path,File,SvgBlacker} vars before:
document.documentElement.firstElementChild.insertAdjacentHTML('beforeend',
    '\u003Cscript type="text/x-mathjax-config">MathJax.Hub.Config(' +
    JSON.stringify({
               jax: ["input/MathML", "output/SVG"],
        extensions: ["mml2jax.js"],
            MathML: { extensions: ["content-mathml.js"] },
               SVG: { blacker: (typeof window.roMjSvgBlacker == "number" &&
                               window.roMjSvgBlacker > 0 ? window.roMjSvgBlacker : 0) }
    }) +
    ');\u003C/script>\n' +
    '\u003Cscript type="text/javascript" src="' +
    (window.roMjPath ? window.roMjPath : "MathJax/") +
    (window.roMjPath && !(window.roMjPath + "").endsWith("/") ? "/" : "") +
    (window.roMjFile ? window.roMjFile : "MathJax.js") +
    '">\u003C/script>'
);
