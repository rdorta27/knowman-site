/* A click on a language link is saved and wins over everything: the browser
   language and the page the visitor landed on. Without a saved choice, an English
   page sends the visitor to the browser language (English when it is none of the three). */
(function () {
  var KEY = "knowman-lang";
  function read() {
    try {
      var v = localStorage.getItem(KEY);
      return v === "en" || v === "es" || v === "pt-BR" ? v : null;
    } catch (e) { return null; }
  }
  function write(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function fromBrowser() {
    var list = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || "en"];
    for (var i = 0; i < list.length; i++) {
      var l = String(list[i]).toLowerCase();
      if (l === "en" || l.indexOf("en-") === 0) return "en";
      if (l === "es" || l.indexOf("es-") === 0) return "es";
      if (l === "pt" || l.indexOf("pt-") === 0) return "pt-BR";
    }
    return "en";
  }
  var here = document.documentElement.lang;
  var saved = read();
  var want = saved || (here === "en" ? fromBrowser() : here);
  var redirect = want !== here;
  if (redirect) document.write("<style id=\"lang-hide\">html{visibility:hidden}</style>");
  document.addEventListener("DOMContentLoaded", function () {
    var links = document.querySelectorAll("a[hreflang]");
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener("click", function () { write(this.getAttribute("hreflang")); });
    }
    var target = redirect && document.querySelector("a[hreflang=\"" + want + "\"]");
    if (target) { location.replace(target.href + location.search + location.hash); return; }
    var hide = document.getElementById("lang-hide");
    if (hide) hide.remove();
  });
})();
