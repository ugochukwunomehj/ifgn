// "use strict"
// function _(e){return document.getElementById(e); }
// var div = _("side_bar_box"), sp2 = _("sbar_ico2"), sp3 = _("sbar_ico3"), sp1 = _("sbar_ico1"), onodu = false, btn = _("btn"), cover = _("cover");
// function show_sbar(){
// if(onodu === false){
//     cover.style.display = "block";
//     div.style.transition = "0.5s";
//     div.style.width = "86%";
//     // sb_inner.style.transition = "1.9s";
//     // sb_inner.style.height = "100%";
//     div.style.maxWidth = "350px";
//     sp1.style.transform = "rotate(45deg) translateX(7px) translateY(7px)";
//     sp3.style.transform = "rotate(-45deg) translateX(8px) translateY(-8px)";
//     sp2.style.transform = "scale(0)";
//     sp1.style.backgroundColor = "#872a2a";
//     sp3.style.backgroundColor = "#872a2a";
//     onodu = true
// } else {
//         div.style.transition = "0.3s";
//         // sb_inner.style.transition = "0.03s";
//         div.style.width = "0px";
//         // sb_inner.style.height = "0%";
//         cover.style.display = "none";
//         sp1.style.transform = "rotate(0deg) translateX(0px) translateY(0px)";
//         sp3.style.transform = "rotate(0deg) translateX(0px) translateY(0px)";
//         sp2.style.transform = "scale(1)";
//         sp1.style.backgroundColor = "#555";
//         sp3.style.backgroundColor = "#555";
//         onodu = false
//     }
// }
// btn.addEventListener("click", function(){ show_sbar(); });
// cover.addEventListener("click", function(){ show_sbar(); });
// cover.addEventListener("touchstart", function(){ show_sbar(); });
// window.addEventListener("resize", function () {
//     if(onodu === true){
//         div.style.transition = "0.3s";
//         sb_inner.style.transition = "0.03s";
//         div.style.width = "0px";
//         sb_inner.style.height = "0%";
//         cover.style.display = "none";
//         sp1.style.transform = "rotate(0deg) translateX(0px) translateY(0px)";
//         sp3.style.transform = "rotate(0deg) translateX(0px) translateY(0px)";
//         sp2.style.transform = "scale(1)";
//         sp1.style.backgroundColor = "#555";
//         sp3.style.backgroundColor = "#555";
//         onodu = false
//     }
// });


// var ok_c = _("ok"), notify_box = _("notif_box"); var ct = _("c_t"); var ud = _("hd"); var md ="hfsdr32ewdwrthsffhsgfeqywgw8";
// var m_s = localStorage.getItem("U_da");
// if(m_s === null || m_s === ""){setTimeout(function() {notify_box.style.display = "block"; ct.innerHTML = 'This website uses cookies to analyze traffic and better user experience. If you continue browsing, we consider that you have accepted our <a style="color:black;" href="/terms/">cookies policy.</a>'
//  }, 10000); }else{ notify_box.style.display = "none";} ok_c.addEventListener("click", function() {localStorage.setItem("U_da", md); notify_box.style.display = "none"; });
